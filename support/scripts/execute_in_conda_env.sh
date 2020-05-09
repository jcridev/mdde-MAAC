#!/bin/bash

source ~/miniconda/etc/profile.d/conda.sh

# For debug
echo "Expected location of MDDE registry: $3:$4"
echo "Expected location of the registry config: $5"

# Wait for registry to be up and ready before running the script
# Reference: https://docs.docker.com/compose/startup-order/
for i in {0..15}; 
do
    timeout 2 bash -c "</dev/tcp/$3/$4"

    result=$?
    if [ $result -eq 0 ] ; then
        # Registry is reachable
        echo "MDDE Registry is up at: $3:$4"
        conda activate mdde
        python $1 --model-dir $2 --reg-host "$3" --reg-port $4 --env-temp-dir /agents_temp --config "$5" --result-dir $6
        exit 0
    fi
    sleep 3
done
echo "Registry connection timed out" >&2
exit 1