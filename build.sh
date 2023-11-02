#!/bin/bash

set -e

docker-compose down --rmi all

docker-compose up

sleep 5;

docker-compose run --rm backend python3 initial_data.py