#!/bin/bash

set -e

docker-compose down --rmi all

docker-compose up -d

sleep 5;

docker-compose run --rm backend python3.11 initial_data.py