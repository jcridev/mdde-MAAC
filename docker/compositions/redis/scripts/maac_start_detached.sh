#!/bin/sh

# Project name as defined when compose was launched
PROJ=${1:-mdde_maac}
# MDDE-MAAC repo root
REPO_ROOT=${2:-../../../..}
# MDDE core location
MDDE_DIR=${3:-${REPO_ROOT}/mdde}

# Bring up full setup with default MAAC
(cd .. && docker-compose -f ${MDDE_DIR}/docker/compositions/redis/docker-compose.yml -f docker-compose.maac.yml -p $PROJ up -d)
