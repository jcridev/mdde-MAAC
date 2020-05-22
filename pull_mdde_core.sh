#!/bin/sh

MDDE_CORE_DIR=./mdde

# Delete the old version
if [ -d "${MDDE_CORE_DIR}" ]; then rm -Rf ${MDDE_CORE_DIR}; fi

# Pull mdde core in the default folder for docker builds
git clone https://github.com/akharitonov/mdde ${MDDE_CORE_DIR}
