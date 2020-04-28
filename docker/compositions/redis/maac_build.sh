#!/bin/sh

# Build (re-build) default MADDPG and all supporting images

# 1. Build the MADDPG container based on the sample code
docker build -t mdde/env:maac-latest -f ../../images/maac.Dockerfile --build-arg MDDE_CORE_LOCATION=./mdde ../../../ --no-cache
# 2. Build the MDDE Registry base image
docker build -t mdde/registry:base-latest -f ../../../mdde/docker/images/registry/registry-base.Dockerfile ../../../mdde/registry --no-cache
# 3. Build the final composition, including MDDE Registry image (From MDDE Registry base image) relying on Redis DB for own storgate and data nodes
docker-compose -f ../../../mdde/docker/compositions/redis/docker-compose.yml -f ./docker-compose.maac.yml build --no-cache
