#!/bin/sh
if [ $1 = "dev" ]; then
docker run --rm --name GH \
 -p 80:8080 \
 -v DB:/usr/src/app/DB \
 -v configs:/usr/src/app/configs \
   greenhouse-control
echo "Dev is Running"
else
docker run --rm -d --name GH -p 80:8080 -v DB:/usr/src/app/DB greenhouse-control
echo "Prod Running" 
fi
