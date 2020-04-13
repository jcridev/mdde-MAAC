#!/bin/bash

# './mdde-git' or path to where the MDDE core is located (should point to the root of the repo checkout)
MDDE_CORE_SOURCE={$1:-"./mdde-git"}
# Destination folder where the MDDE core source files should be placed
MDDE_CHECKOUT_LOCATION=${2:-"/usr/src/mdde/mdde-core"}    
# Root of the mdde-MAAC src
MDDE_MAAC_LOCATION=${3:-"/usr/src/mdde/integration-maac"} 
# PyTourch build version (CPU or GPU)
TORCH_CFG=${4:-"cpu"}

source ~/miniconda/etc/profile.d/conda.sh
conda create -y --name mdde python=3.7
conda activate mdde

base_dir=/code

# Install PyTorch with dependencies
pip install --progress-bar off gym==0.9.4
pip install --progress-bar off tensorboardx==1.9
pip install --progress-bar off tensorboard==2.0.0
pip install --progress-bar off seaborn==0.9.0

if [ "$TORCH_CFG" = "gpu" ];then
    pip install --progress-bar off torch==1.4.0+cu92 torchvision==0.5.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html
elif [ "$TORCH_CFG" = "cpu" ];then
    pip install --progress-bar off torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
else
    echo "Incorrect configuration argument TORCH_CFG: '$TORCH_CFG'" >&2
    exit 1
fi

#conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=9.0 -c pytorch
#https://pytorch.org/get-started/previous-versions/

# Install baselines
git clone -n --single-branch https://github.com/openai/baselines.git "$base_dir/baselines"
cd "$base_dir/baselines"
git checkout 98257ef8c9bd23a24a330731ae54ed086d9ce4a7
pip install --progress-bar off -e .
cd "$base_dir"

# Install MDDE
if [ "$MDDE_CORE_SOURCE" == "./mdde-git" ]; then
    # From git
    git clone https://github.com/akharitonov/mdde.git --no-checkout $MDDE_CHECKOUT_LOCATION
    cd $MDDE_CHECKOUT_LOCATION
    git sparse-checkout init --cone
    git sparse-checkout set mdde    
else
    # Locally
    cd $MDDE_CHECKOUT_LOCATION
fi
# Core MDDE and registry connection protocol
pip install --progress-bar off -e ./mdde/core
pip install --progress-bar off -e ./mdde/extensions/mdde-registry-client-tcp
# Install MDDE-MAAC extension
cd $MDDE_MAAC_LOCATION
pip install --progress-bar off -e .

conda deactivate