#!/bin/bash

scp root@cloudx-16-01:/home/mlnx-project-config/jenkins/jobs/* jenkins/jobs/
scp root@cloudx-16-01:/etc/zuul/layout/layout.yaml zuul/
