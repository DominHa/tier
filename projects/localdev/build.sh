set -e
export SOURCE_HASH=localdev
printf "%s+${SOURCE_HASH}" $(cat ../__VERSION__) > __VERSION_SOURCE__

docker-compose -f docker-compose.build.yml \
               -f docker-compose.command.yml \
               -f docker-compose.env.yml \
               -f docker-compose.ports.yml \
               -f docker-compose.deploy.yml \
               config > docker-stack.yml
DOCKER_BUILDKIT=1  docker-compose -f docker-stack.yml build