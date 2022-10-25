FROM python:3.9-slim-buster

ARG ENV_FILE

ENV ENV_FILE=${ENV_FILE} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install python/pip
RUN pip install --upgrade pip

WORKDIR /backend

COPY requirements.txt /backend
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Creating folders, and files for a project:
COPY . /backend

