
# Cron runs the moment an event occurs
#   So its not great for "at least once a X"
Minute Hour Day-of-month Month Day-of-week



# ------------------------------------------------------
# CronTab times

*       # all values
1,4     # 1 and 4
3,9/2   # from 3 to 9 with a step of 2 (aka 3,5,7,9)
*/3     # all values with a step of 3

# Special values are also allowed
@reboot
@yearly/@annually
@monthly
@weekly
@daily/@midnight
@hourly

