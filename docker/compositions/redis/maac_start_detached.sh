#!/bin/sh

# Project name as defined when compose was launched
PROJ=${1:-mdde_maac}

# Bring up full setup with default MAAC
docker-compose -f ../../../mdde/docker/compositions/redis/docker-compose.yml -f ./docker-compose.maac.yml -p $PROJ up -d
