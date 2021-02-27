#!/bin/sh
if [ $1 = "dev" ]; then
docker run --rm --name GH \
 -p 80:8080 \
 -d \
 -v DB:/usr/src/app/DB \
 -v /home/pi/Server/src:/usr/src/app/src \
 -v /home/pi/Server/static:/usr/src/app/static \
   greenhouse-control
echo "Dev is Running"
else
docker run --rm -d --name GH -p 80:8080 -v DB:/usr/src/app/DB greenhouse-control
echo "Prod Running" 
fi
