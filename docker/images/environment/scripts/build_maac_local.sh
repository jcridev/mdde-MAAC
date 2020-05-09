#bin/sh

# MDDE-MAAC repo root
REPO_ROOT=${1:-../../../..}
# MDDE core subfolder
MDDE_CORE_FOLDER=${2:-./mdde}

# The following command assumes that the MDDE repo (https://github.com/akharitonov/mdde) was checkout in the ./mdde folder of mdde-MAAC repo or copied there.
# (specifically https://github.com/akharitonov/mdde/mdde subfolder) 
docker build -t mdde/env/maac:latest -f ../maac.Dockerfile --build-arg MDDE_CORE_LOCATION=${MDDE_CORE_FOLDER} ${REPO_ROOT}/ --no-cache
