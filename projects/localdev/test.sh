set -e
./build.sh
docker run --entrypoint pytest -t localdev_api --pyargs vc_api