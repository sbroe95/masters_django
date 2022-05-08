#!/bin/bash

echo 'Starting to Analysis UAT environment...'
# 1st arg is server  , 2nd and 3rd argument are for server key if needed "-i", "path_to_secret.pem"
ssh $2 $3 ubuntu@$1 "
	sudo docker system prune -f
	cd Finacc_Analysis/fastapi
	git fetch --all
	git checkout --force master
	cp .prod.env .env
	sudo docker-compose build --no-cache
	if [ $? -eq 0 ]; then
		sudo docker-compose down
		sudo docker-compose up -d
		echo 'Deploying Analysis UAT environment completed successfully'
	else
		echo 'Deploying Analysis UAT environment. Could not build docker image.'
	fi
	"