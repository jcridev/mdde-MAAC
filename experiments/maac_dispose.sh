#!/bin/sh

# Prfix for container names
PFX=${1:-""}

COMPOSE_DIR=../docker/compositions/redis

# With do-nothing
(cd ${COMPOSE_DIR}/scripts/ && sh maac_dispose.sh ${PFX}maac_dn)

# Without do-nothing
(cd ${COMPOSE_DIR}/scripts/ && sh maac_dispose.sh ${PFX}maac_wdn)

# With do-nothing, disregard storage, bench at every step
(cd ${COMPOSE_DIR}/scripts/ && sh maac_dispose.sh ${PFX}maac_dn_sm0_b1)

# Without do-nothing, disregard storage, bench at every step
(cd ${COMPOSE_DIR}/scripts/ && sh maac_dispose.sh ${PFX}maac_wdn_sm0_b1)

# With do-nothing
#(cd ${COMPOSE_DIR}/scripts/ && sh maac_dispose.sh ${PFX}maac_dn_g05)

# Without do-nothing
#(cd ${COMPOSE_DIR}/scripts/ && sh maac_dispose.sh ${PFX}maac_wdn_g05)
