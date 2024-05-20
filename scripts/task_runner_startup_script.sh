#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

export GCP_LOGGING_ENABLED = "TRUE"

INSTANCE_GROUP_NAME=$(curl --silent --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/instance_group_name -H "Metadata-Flavor: Google")
DOCKER_IMAGE=$(curl --silent --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/docker_image -H "Metadata-Flavor: Google")
ZONE=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/zone -H "Metadata-Flavor: Google")
PYTHON_HASH_SEED=$(curl --silent --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/python_hash_seed -H "Metadata-Flavor: Google" || echo "42")
MLFLOW_TRACKING_URI=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/mlflow_tracking_uri -H "Metadata-Flavor: Google")
NODE_COUNT=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/node_count -H "Metadata-Flavor: Google")
DISKS=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/disks -H "Metadata-Flavor: Google")

echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
echo "hello world!"
echo "everything went well"
echo "INSTANCE_GROUP_NAME=${INSTANCE_GROUP_NAME}"
echo "DOCKER_IMAGE=${DOCKER_IMAGE}"
echo "ZONE=${ZONE}"
echo "PYTHON_HASH_SEED=${PYTHON_HASH_SEED}"
echo "MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}"
echo "NODE_COUNT=${NODE_COUNT}"
echo "DISKS=${DISKS}"

echo "Deleting instance group ${INSTANCE_GROUP_NAME}"
gcloud compute instance-groups managed delete --quiet "${INSTANCE_GROUP_NAME}" --zone "${ZONE}"