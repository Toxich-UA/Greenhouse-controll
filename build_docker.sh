docker build -t greenhouse-control .
docker rmi $(docker images -f "dangling=true" -q)
mkdir configs
mkdir logs
mkdir DB
