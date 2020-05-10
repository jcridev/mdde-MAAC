#!/bin/sh

# MDDE-MAAC repo root
REPO_ROOT=../../../..
# MDDE core location
MDDE_DIR=${REPO_ROOT}/mdde  # TODO: Copy over into the repo root if outside of it (repo root is the Docker build tontext)

SKIPREGISTRY=0
for i in "$@"
do
case $i in
    -g=*|--gitreporoot=*)
    REPO_ROOT="${i#*=}"
    shift
    ;;
    -m=*|--mddecore=*)
    MDDE_DIR="${i#*=}"
    shift
    ;;
    -r|--regskip) # Skip registry image rebuild
    SKIPREGISTRY=1
    shift 
    ;;
    *)
    echo "Unknown argument ${i}"
    exit 1
    ;;
esac
done

# Build (re-build) default MAAC and all supporting images

# 1. Build the MAAC container based on the sample code
(cd ../../../images/environment/scripts/ && sh build_maac_local.sh -g=${REPO_ROOT})
# 2. Build the MDDE Registry image
if [ $SKIPREGISTRY -eq 0 ];then
  (cd ${MDDE_DIR}/docker/images/registry/scripts/ && sh build_redis_images.sh)
fi
# 3. Build the final composition, including MDDE Registry image (From MDDE Registry base image) relying on Redis DB for own storgate and data nodes
docker-compose -f ${MDDE_DIR}/docker/compositions/redis/docker-compose.yml -f ../docker-compose.maac.yml build --no-cache
