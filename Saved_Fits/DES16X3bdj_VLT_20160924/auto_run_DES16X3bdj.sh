#!/bin/sh
nohup ./run_synapps_DES16X3bdj.sh > nohup_DES16X3bdj.out 2>&1&
sleep 10
while true
do
    if pgrep -x "synapps" > /dev/null
    then
        echo "Running"
    else
        echo "Stopped"
        python rerun_synapps_if_stopped.py DES16X3bdj_VLT_20160924.yaml nohup_DES16X3bdj.out
        nohup ./run_synapps_DES16X3bdj.sh > nohup_DES16X3bdj.out 2>&1&
    fi
    date
    sleep 600
done

