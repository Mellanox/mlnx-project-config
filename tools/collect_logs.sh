#!/bin/bash -x
CI_ARTIFACTS=${LOGDIR:-/opt/stack/logs}
echo "Saving SYSLOG files to $CI_ARTIFACTS"
mkdir -p $CI_ARTIFACTS
sudo systemctl status devstack\* > $CI_ARTIFACTS/devstack_services_status.log
for s in $(systemctl list-unit-files| grep devstack | awk '{print $1}'|sort)
do
    log_name=$CI_ARTIFACTS/$(echo $s|cut -d'@' -f2).log
    echo $log_name
    sudo journalctl -o short-precise --unit $s > $log_name
done
sudo journalctl -o short-precise --unit tgtd.service > $CI_ARTIFACTS/tgtd.log

