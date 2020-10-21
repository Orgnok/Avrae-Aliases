tembed
"""Storing the first argument in a var so we can use it from the gvar."""
{{args = &ARGS& if len(&ARGS&) > 0 else [""]}}
{{A="&1&" if "&*&" else ""}}

"""Getting the current time"""
{{current_time = int(time())}}

"""Creating all the necessary cvars"""
{{character().set_cvar_nx("LastPing", str(current_time))}}
{{character().set_cvar_nx("Downtime", "0")}}

{{character().set_cvar_nx("is_exalted","False")}}
{{character().set_cvar_nx("is_retired","False")}}
{{character().set_cvar_nx("is_dead","False")}}


"""The old dt alias kept track of retiring by setting LastPing to -1, this updates it to the new cvars"""
{{character().set_cvar("is_retired","True") if LastPing=="-1" else 0}}
{{character().set_cvar("LastPing", str(current_time)) if LastPing=="-1" else 0}}


"""Checking to see if the character is active and is eligible to earn DT since the last time the alias was used"""
{{is_active = is_retired=="False" and is_dead == "False"}}

"""Setting the upper limit for the ammount of downtime you can have."""

{{seconds_per_day = 24*60*60}}
{{max_exalted_days = 60}}
{{max_exalted_seconds = max_exalted_days*seconds_per_day}}


"""Handling inputs"""
"""Command aliases, so we can handle more than one variant"""
{{toggle_rteired_aliases = ["retire","retirement","active"]}}
{{toggle_dead_aliases = ["dead","death","f"]}}
{{toggle_exalted_aliases = ["exalt","ascend","exalted"]}}


"""Checking if any of the subcommands were used"""
{{toggle_exalted = (A and (A in toggle_exalted_aliases))}}
{{toggle_retired = A and (A in toggle_rteired_aliases)}}
{{toggle_dead = A and (A in toggle_dead_aliases)}}

"""Toggling statuses: If the toggle is set above, the cvar is swapped. Technically set to True if it isn't already "True"."""

"""toggling exalted status"""
{{(character().set_cvar("is_exalted", (not is_exalted == "True")) if toggle_exalted else 0)}}

"""toggling retirement"""
{{(character().set_cvar("is_retired", (not is_retired == "True")) if toggle_retired else 0)}}

"""toggling death"""
{{(character().set_cvar("is_dead", (not is_dead == "True")) if toggle_dead else 0)}}

"""Checks if any of the toggles were used ADD NEW TOGGLES HERE if you add any. Or put em all in a dictionary or something, that'd probably be cleaner anyways"""
{{status_changed = toggle_dead or toggle_retired or toggle_exalted}}

"""Checks if the character is still active after potential toggles"""
{{still_active = is_retired=="False" and is_dead == "False"}}

"""Checks if any of the subcommands were used, for now it's the same as toggle sicne the only subcommands are toggles"""
{{subcommand_used = status_changed}}


"""calculating how much time passed since the last time the command was used and converting to hours/minutes/days for output to the player"""
{{delta_seconds = (current_time - int(LastPing)) if is_active else 0}}
{{delta_minutes = delta_seconds / 60}}
{{delta_hours = delta_minutes / 60}}
{{delta_days = delta_hours / 24}}


"""converting the manual input into seconds"""
{{adjustment_in_seconds = int((float(A) if A and not subcommand_used and is_active else 0) * seconds_per_day)}}


"""Saving the previous downtime"""
{{previous_downtime = Downtime}}


"""not technically unlimited DT but having an actual number makes things easier down the road."""
{{unlimited_dt = 10**100}}
"""Logic to detemine the actual number of max seconds, could be handled better than with just an arbitrarily high max if no limit exists."""
{{personal_max_seconds = max_exalted_seconds if is_exalted=="True" else unlimited_dt}}


"""actually adjusting dowtntime"""
{{character().set_cvar("Downtime", str(min(int(Downtime) + delta_seconds, personal_max_seconds)))}}


"""Need to do the time adjustment seperate so we set the maximum and *then* subtract DT days if the maximum is exceeded"""
{{character().set_cvar("Downtime", str(min(int(Downtime) + adjustment_in_seconds,personal_max_seconds)))}}
{{downtime_days = int(Downtime) / (seconds_per_day)}}


"""Generate output text"""

"""Displays the time added in days/hours/minutes/seconds depending on how much was added"""
{{time_added= f'{delta_days:.0f} days' if delta_days>1 else f'{delta_hours:.0f} hours' if delta_hours>1 else f'{delta_minutes:.0f} minute' if delta_minutes>1 else f'{delta_seconds} seconds' if delta_seconds>1 else 0}}

{{status_change = (f'has become exalted' if is_exalted =="True" else f'is no longer exalted') if toggle_exalted else (f'has retired' if is_retired=="True" else f'has come out of retirement') if toggle_retired else (f'has died' if is_dead == "True" else f'is no longer dead') if toggle_dead else 0}}
{{current_status = (f'' if not still_active else 'active ') + (f'retired ' if is_retired == "True" else "") + (f'exalted ' if is_exalted == "True" else "") + (f'dead ' if is_dead == "True" else "")}}
{{max_dt_message = (f'Maximum DT: ' + str(max(int(personal_max_seconds/seconds_per_day),0))) + ' days.' if personal_max_seconds<unlimited_dt else ''}}
{{current_downtime_message = f'Current Downtime {max_dt_message} | '+ str(int(downtime_days))+' days'}}

-title "Downtime Tracker: {{name}}"
{{f'-f "Status Change | {name} {status_change}"' if status_changed else 0}}
{{f'-f "Manual Adjustment | {str(int(adjustment_in_seconds/(seconds_per_day)))} days"' if adjustment_in_seconds else ''}}
{{f'-f "Time added | {time_added}"' if delta_seconds > 1 else 0}}
{{f'-f "{current_downtime_message}"'}}
{{f'-f "Current Status | {current_status}"'}}
{{character().set_cvar("LastPing", str(current_time))}}
-footer "Current: {{Downtime}} Previous: {{previous_downtime}}"
-color <color> -thumb <image>
