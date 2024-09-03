#!/bin/bash

COMPOSE_FILE="evertest.yml"

deploy() {
  echo "Starting Docker services using $COMPOSE_FILE..."
  docker-compose -f $COMPOSE_FILE up -d
  echo "Docker services started."
}

teardown() {
  echo "Stopping and removing Docker services from $COMPOSE_FILE..."
  docker-compose -f $COMPOSE_FILE down
  echo "Docker services stopped and removed."
}

usage() {
  echo "Usage: $0 {deploy|teardown}"
  exit 1
}

if [ $# -ne 1 ]; then
  usage
fi

case "$1" in
  deploy)
    deploy
    ;;
  teardown)
    teardown
    ;;
  *)
    usage
    ;;
esac

