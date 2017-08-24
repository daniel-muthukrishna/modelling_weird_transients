#!/bin/sh
nohup ./run_synapps_sn2006jo.sh > nohup_sn2006jo.out 2>&1&
sleep 10
while true
do
    if pgrep -x "synapps" > /dev/null
    then
        echo "Running"
    else
        echo "Stopped"
        python rerun_synapps_if_stopped.py sn2006jo.yaml nohup_sn2006jo.out
        nohup ./run_synapps_sn2006jo.sh > nohup_sn2006jo.out 2>&1&
    fi
    date
    sleep 600
done

