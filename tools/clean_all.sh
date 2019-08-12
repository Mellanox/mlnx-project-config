#!/bin/bash

sudo systemctl stop devstack@*
sudo systemctl stop openvswitch
sudo yum remove -y $(rpm -qa|grep openvswitch)

for i in radvd neutron-server dnsmasq haproxy; do
    sudo kill -9 $(pgrep $i);
done

for i in $(ps -ef |grep neutron|awk '{print $2}'); do
    sudo kill -9 $i
done
