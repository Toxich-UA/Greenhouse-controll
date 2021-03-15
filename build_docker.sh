docker build -t greenhouse-control .
docker rmi $(docker images -f "dangling=true" -q)
mkdir sensors
mkdir logs
mkdir DB