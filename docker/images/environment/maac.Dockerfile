FROM ubuntu:18.04

LABEL org.label-schema.name="mdde/env/maac"
LABEL org.label-schema.description="MDDE MAAC based agents"
LABEL org.label-schema.vcs-url="https://github.com/akharitonov/mdde-MAAC/"
LABEL org.label-schema.version="0.5"
LABEL org.label-schema.schema-version="1.0"
LABEL maintainer="https://github.com/akharitonov/"

# Where MDDE core source should be obtained from. './mdde-git' means it will be retrieved from the GitHub repository at build time.
# You can't also provide a directory within the build context if you have MDDE core sources locally.
ARG MDDE_CORE_LOCATION=./mdde-git
# "cpu" or "gpu"
ARG PLATFORM=cpu

SHELL ["/bin/bash", "-c"]

RUN apt-get update

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    cmake \
    git \
    sudo \
    rsync \
    wget \
    software-properties-common \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libopenmpi-dev


RUN update-ca-certificates

ENV HOME /home
WORKDIR ${HOME}/

# Download Miniconda
# https://docs.anaconda.com/anaconda/install/silent-mode/
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p $HOME/miniconda
RUN rm miniconda.sh

ENV PATH ${HOME}/miniconda/bin:$PATH
ENV CONDA_PATH ${HOME}/miniconda
# https://docs.conda.io/projects/conda-build/en/latest/resources/use-shared-libraries.html
# Relying on LD_LIBRARY_PATH is not recommended but in case issues with any shred libraries, uncomment the next line
#ENV LD_LIBRARY_PATH ${CONDA_PATH}/lib:${LD_LIBRARY_PATH}

RUN eval "$(conda shell.bash hook)"


ENV MDDE_SRC /usr/src/mdde
RUN mkdir p $MDDE_SRC
# Location where the root of the MDDE repo should be copied
ENV MDDE_CORE_SRC $MDDE_SRC/mdde-core

WORKDIR $MDDE_SRC
# MAAC Extension for MDDE
ENV MDDE_MAAC_SRC $MDDE_SRC/integration-maac
RUN mkdir p $MDDE_MAAC_SRC
COPY ./src $MDDE_MAAC_SRC
# Entrypoint code
COPY ./samples/sample_maac_default.py ./run.py

# Script creating the conda environment suitable for the used version of MAAC
COPY ./support/scripts/create_conda_env.sh ./create_conda_env.sh
# Entrypoint script
COPY ./support/scripts/execute_in_conda_env.sh ./execute_in_conda_env.sh
RUN chmod +x ./create_conda_env.sh
RUN chmod +x ./execute_in_conda_env.sh

# Create environment
COPY $MDDE_CORE_LOCATION $MDDE_CORE_SRC
RUN bash ./create_conda_env.sh $MDDE_CORE_LOCATION $MDDE_CORE_SRC $MDDE_MAAC_SRC $PLATFORM

# Make sure conda has execution permissions
RUN find ${CONDA_PATH} -type d -exec chmod +x {} \;

# A volume for shared files, such as MDDE config.yml
ENV MDDE_RESULTS /mdde/results
RUN mkdir -p $MDDE_RESULTS
VOLUME $MDDE_RESULTS

# A volume for shared files, such as MDDE config.yml
ENV MDDE_SHARED /mdde/shared
RUN mkdir -p $MDDE_SHARED

# Run experiments
ENTRYPOINT $MDDE_SRC/execute_in_conda_env.sh $MDDE_SRC/run.py $MDDE_RESULTS $REG_HOST $REG_PORT $MDDE_SHARED/config.yml