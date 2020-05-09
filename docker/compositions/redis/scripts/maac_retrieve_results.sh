#/bin/sh

# Retrieve results and logs from the currently running containers

# Project name as defined when compose was launched
PROJ=${1:-mdde_maac}
# Destination folder
DEST=${2:-.}


REGISTRY_CONTAINER=${PROJ}_registry_1
MAAC_CONTAINER=${PROJ}_maac_1

if [ ! "$(docker ps -q -f name=${REGISTRY_CONTAINER})" ]; then
    echo "Registy container is not running: '${REGISTRY_CONTAINER}'."
    exit 1 
fi

if [ ! "$(docker ps -q -f name=${MAAC_CONTAINER})" ]; then
    echo "MAAC container is not running:'${MAAC_CONTAINER}'."
    exit 1 
fi

# Create a folder with a unique name
UUID=$(dbus-uuidgen)
DEST_U_FOLDER=${DEST}/${UUID}
mkdir -p ${DEST_U_FOLDER}

docker cp ${REGISTRY_CONTAINER}:/mdde/registry-logs ${DEST_U_FOLDER}
docker cp ${MAAC_CONTAINER}:/mdde/results ${DEST_U_FOLDER}

echo ${UUID}
