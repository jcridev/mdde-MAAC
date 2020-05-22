#!/bin/sh

# Prfix for container names
PFX=${1:-""}

WORK_DIR=$PWD
COMPOSE_DIR=../docker/compositions/redis

# With do-nothing
mkdir -p ${WORK_DIR}/res_maac/maac_dn
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results.sh ${PFX}maac_dn ${WORK_DIR}/res_maac/maac_dn)

# Without do-nothing
mkdir -p ${WORK_DIR}/res_maac/maac_wdn
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results.sh ${PFX}maac_wdn ${WORK_DIR}/res_maac/maac_wdn)

# With do-nothing
mkdir -p ${WORK_DIR}/res_maac/maac_dn_g05
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results.sh ${PFX}maac_dn_g05 ${WORK_DIR}/res_maac/maac_dn_g05)

# Without do-nothing
mkdir -p ${WORK_DIR}/res_maac/maac_wdn_g05
(cd ${COMPOSE_DIR}/scripts/ && sh maac_retrieve_results.sh ${PFX}maac_wdn_g05 ${WORK_DIR}/res_maac/maac_wdn_g05)
