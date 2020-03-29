# MAAC extenstion for MDDE
[Multi-agent Data Distribution Environment](https://github.com/akharitonov/mdde) wrapper for [Actor-Attention-Critic for Multi-Agent Reinforcement Learning (Iqbal and Sha, ICML 2019)](https://github.com/shariqiqbal2810/MAAC)


We're relying on the original implementation of MAAC provided by Iqbal and Sha, we reuse as much of its code as possible. We do not introduce a lot of changes into the original code with only two exceptions:

   1. MDDE does not support concurrent environments, so the option of creating multiple copies of the environment was removed (*n_rollout_threads*).
   2. Fixed critic attention heads logging for tensorboard in the scenarios where there is a group of agents consisting of only a single agent.

## Installation

Steps to roll out a development version of MAAC for MDDE

### MDDE dependencies

Create a new Conda environment and activate it

1. `conda create -y --name mdde-maac python=3.7`
2. `conda activate maac`

Then checkout [MDDE](https://github.com/akharitonov/mdde), go to the folder where you checked it out and follow the installation instructions in `./mdde`.
You will need to install **MDDE Core** and **TCP extension**.

1. `git clone https://github.com/akharitonov/mdde.git "mdde"`

### MAAC dependencies

1. `pip install gym==0.9.4 tensorboardx==1.9 tensorboard==2.0.0 seaborn==0.9.0`

2. Then you need to install one of the specific PyTorch builds, either for GPU **or** CPU

   * CPU: `pip install --progress-bar off torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html`

   * GPU: `pip install --progress-bar off torch==1.4.0+cu92 torchvision==0.5.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html`


3. OpenAI baselines, specific checkout [as specified in the original MAAC codebase](https://github.com/shariqiqbal2810/MAAC)

    1. `git clone -n --single-branch https://github.com/openai/baselines.git "baselines"`
    2. `cd baselines`
    3. `git checkout 98257ef8c9bd23a24a330731ae54ed086d9ce4a7`
    4. `pip install --progress-bar off -e .`
    5. `cd ..`

After you're done with the installation, take a look at the example code in the `./samples` directory.