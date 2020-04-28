#!/bin/sh

# Remove the project containers and volumes

# Project name as defined when compose was launched
PROJ=${1:-mdde_maac}

docker-compose -f ../../../mdde/docker/compositions/redis/docker-compose.yml -f ./docker-compose.maac.yml -p $PROJ down -v
