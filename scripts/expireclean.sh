#!/bin/env bash

# supervisord and calender logs are auto cleaned.
# see the configure files for them.

# remove out of date calender logs and compress log
clover_log_path=/home1/irteam/logs/calender/
find $calender_log_path -mtime +50 -name 'calender.log.*.xz' -delete
find $calender_log_path -name 'calender.log.*-*' -not -name 'calender.log.*.xz' -execdir xz -z -T4 {} \;
