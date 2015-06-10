#!/bin/bash

END=100
mkdir -p /tmp/job_progress

for i in $(seq 1 $END); 
do 
    echo $i;
    echo $i > /tmp/job_progress/${PAS_TASK_ID}.progress
    sleep 1
done
