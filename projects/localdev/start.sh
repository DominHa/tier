set -e
./build.sh
# See https://aws.amazon.com/blogs/containers/graceful-shutdowns-with-ecs/
DOCKER_BUILDKIT=1 docker-compose -f docker-stack.yml up  "$@"