#bin/bash

docker-compose -f users/docker-compose-local.yaml up -d &&
docker-compose -f videos/docker-compose-local.yaml up -d && 
docker-compose -f s3/docker-compose-local.yaml up -d