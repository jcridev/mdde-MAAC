#/bin/sh

# Retrieve results and logs witout running containers

# Project name as defined when compose was launched
PROJ=${1:-mdde_maac}
# Destination folder
DEST=${2:-.}


# Create a folder with a unique name
UUID=$(dbus-uuidgen)
DEST_U_FOLDER=${DEST}/${UUID}
mkdir -p ${DEST_U_FOLDER}

docker run -d --rm --name ${PROJ}_dummy_1 -v ${PROJ}_mdde_reg_logs:/mdde/registry-logs -v ${PROJ}_mdde_results:/mdde/results alpine tail -f /dev/null
docker cp ${PROJ}_dummy_1:/mdde/registry-logs ${DEST_U_FOLDER}
docker cp ${PROJ}_dummy_1:/mdde/results ${DEST_U_FOLDER}
docker stop ${PROJ}_dummy_1

echo ${UUID}
