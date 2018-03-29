#!/bin/bash

folder=$1
URL='http://13.74.249.42/BACKUP/'

if [ -z "$folder" ];then
    folder=$(ls -ltr $nfs | tail -n1|awk '{print $9}')
fi

echo "Extracting from extracting from $URL/$folder"

cd /tmp
wget ${URL}/${folder}.gz
tar -zxvf ${folder}.gz
cd -
cp /tmp/${folder}/etc/jobs/* jenkins/jobs/
cp /tmp/${folder}/etc/zuul/layout/layout.yaml zuul/
sudo rm -rf /tmp/${folder}*

