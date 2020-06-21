#!/bin/sh

# Prfix for container names
PFX=${1:-""}

# Simulation (benchmark estimation flag)
SIM=" --sim"

SLEEP_BETWEEN=1
SLEEP_TIME=4m

# *.env file used by docker-compose
ARGS_FILE=args.env
COMPOSE_DIR=../docker/compositions/redis
COMPOSE_DIR_CORE=../mdde/docker/compositions/redis

# Build required images 
(cd ${COMPOSE_DIR}/scripts && sh maac_build.sh)

# With do-nothing
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
if [ "$SIM" = " --sim" ]
then
  echo "LAUNCH_ARGS=--sim" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
else
  echo "" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
fi
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_dn)

if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# Without do-nothing
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--no-do-nothing${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_wdn)

if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 


# With do-nothing, disregard storage, bench at every step
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--store-m 0.0 --bench-psteps 1${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_dn_sm0_b1)

if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# Without do-nothing, disregard storage, bench at every step
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--no-do-nothing --store-m 0.0 --bench-psteps 1${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_wdn_sm0_b1)

if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 


# With do-nothing, disregard storage, bench at every step, 1e7 replay buffer
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--store-m 0.0 --bench-psteps 1 --buffer-length 10000000${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_dn_sm0_b1_10mrb)

if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# Without do-nothing, disregard storage, bench at every step, 1e7 replay buffer
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--no-do-nothing --store-m 0.0 --bench-psteps 1 --buffer-length 10000000${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_wdn_sm0_b1_10mrb)

if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# With do-nothing, consider storage, 80 fragments, bench at every step
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--bench-psteps 1 --n-frags 80${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_dn_b1_f80)

# Without do-nothing, consider storage, 80 fragments, bench at every step
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "LAUNCH_ARGS=--no-do-nothing --bench-psteps 1 --n-frags 80${SIM}" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_wdn_b1_f80)

#if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# With do-nothing
#rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
#echo "LAUNCH_ARGS=--gamma 0.5" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
#(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_dn_g05)

#if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# Without do-nothing
#rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
#echo "LAUNCH_ARGS=--no-do-nothing --gamma 0.5" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}
#(cd ${COMPOSE_DIR}/scripts && sh maac_start_detached.sh ${PFX}maac_wdn_g05)

#if [ $SLEEP_BETWEEN -eq 1 ]; then sleep $SLEEP_TIME; fi 

# Cleanup the args file
rm ${COMPOSE_DIR_CORE}/${ARGS_FILE}
echo "" > ${COMPOSE_DIR_CORE}/${ARGS_FILE}