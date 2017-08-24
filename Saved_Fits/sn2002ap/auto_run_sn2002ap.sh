#!/bin/sh
nohup ./run_synapps_sn2002ap.sh > nohup_sn2002ap.out 2>&1&
sleep 10
while true
do
    if pgrep -x "synapps" > /dev/null
    then
        echo "Running"
    else
        echo "Stopped"
        python rerun_synapps_if_stopped.py sn2002ap.yaml nohup_sn2002ap.out
        nohup ./run_synapps_sn2002ap.sh > nohup_sn2002ap.out 2>&1&
    fi
    date
    sleep 600
done

