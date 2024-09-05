#!/bin/bash

declare -A IMAGES
IMAGES["ereceiver-image"]="docker/Dockerfile-eReceiver"
IMAGES["eprocessor-image"]="docker/Dockerfile-eProcessor"
IMAGES["evalidator-image"]="docker/Dockerfile-eValidator"
IMAGES["databroker-image"]="docker/Dockerfile-DataBroker"

for IMAGE in "${!IMAGES[@]}"; do
  if docker images -q "$IMAGE" > /dev/null 2>&1; then
    echo "Removing existing image: $IMAGE"
    docker rmi "$IMAGE" || { echo "Failed to remove image: $IMAGE"; exit 1; }
  fi
done

for IMAGE in "${!IMAGES[@]}"; do
  DOCKERFILE_PATH="${IMAGES[$IMAGE]}"
  echo "Building image: $IMAGE using Dockerfile: $DOCKERFILE_PATH"
  docker build -t "$IMAGE" -f "$DOCKERFILE_PATH" . || { echo "Failed to build image: $IMAGE"; exit 1; }
done

echo "Docker images built successfully."

