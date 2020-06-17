#!/bin/sh

# Prfix for container names
PFX=${1:-""}

WORK_DIR=$PWD
COMPOSE_DIR=../docker/compositions/redis

# With do-nothing
mkdir -p ${WORK_DIR}/res_maac/maac_dn
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_dn ${WORK_DIR}/res_maac/maac_dn)

# Without do-nothing
mkdir -p ${WORK_DIR}/res_maac/maac_wdn
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_wdn ${WORK_DIR}/res_maac/maac_wdn)

# With do-nothing, disregard storage, bench at every step
mkdir -p ${WORK_DIR}/res_maac/maac_dn_sm0_b1
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_dn_sm0_b1 ${WORK_DIR}/res_maac/maac_dn_sm0_b1)

# Without do-nothing, disregard storage, bench at every step
mkdir -p ${WORK_DIR}/res_maac/maac_wdn_sm0_b1
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_wdn_sm0_b1 ${WORK_DIR}/res_maac/maac_wdn_sm0_b1)


# With do-nothing, disregard storage, bench at every step, 1e7 replay buffer
mkdir -p ${WORK_DIR}/res_maac/maac_dn_sm0_b1_10mrb
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_dn_sm0_b1_10mrb ${WORK_DIR}/res_maac/maac_dn_sm0_b1_10mrb)

# Without do-nothing, disregard storage, bench at every step, 1e7 replay buffer
mkdir -p ${WORK_DIR}/res_maac/maac_wdn_sm0_b1_10mrb
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_wdn_sm0_b1_10mrb ${WORK_DIR}/res_maac/maac_wdn_sm0_b1_10mrb)

# With do-nothing, consider storage, 80 fragments, bench at every step
mkdir -p ${WORK_DIR}/res_maac/maac_dn_b1_f80
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_dn_b1_f80 ${WORK_DIR}/res_maac/maac_dn_b1_f80)

# Without do-nothing, consider storage, 80 fragments, bench at every step
mkdir -p ${WORK_DIR}/res_maac/maac_wdn_b1_f80
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_wdn_b1_f80 ${WORK_DIR}/res_maac/maac_wdn_b1_f80)

# With do-nothing
#mkdir -p ${WORK_DIR}/res_maac/maac_dn_g05
#(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_dn_g05 ${WORK_DIR}/res_maac/maac_dn_g05)

# Without do-nothing
#mkdir -p ${WORK_DIR}/res_maac/maac_wdn_g05
#(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results_stopped.sh ${PFX}maac_wdn_g05 ${WORK_DIR}/res_maac/maac_wdn_g05)