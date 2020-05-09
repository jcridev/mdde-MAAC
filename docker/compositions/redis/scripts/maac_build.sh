#!/bin/sh

# MDDE-MAAC repo root
REPO_ROOT=${1:-../../../..}
# MDDE core location
MDDE_DIR=${2:-${REPO_ROOT}/mdde}

# Build (re-build) default MAAC and all supporting images

# 1. Build the MAAC container based on the sample code
(cd ../../../images/environment/scripts/ && sh build_maac_local.sh ${REPO_ROOT})
# 2. Build the MDDE Registry base image
(cd ${MDDE_DIR}/docker/images/registry/scripts/ && sh build_redis_images.sh)
# 3. Build the final composition, including MDDE Registry image (From MDDE Registry base image) relying on Redis DB for own storgate and data nodes
docker-compose -f ${MDDE_DIR}/docker/compositions/redis/docker-compose.yml -f ../docker-compose.maac.yml build --no-cache
