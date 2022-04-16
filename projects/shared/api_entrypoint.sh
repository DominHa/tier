#!/bin/bash
#https://aws.amazon.com/blogs/containers/graceful-shutdowns-with-ecs/
uvicorn vc_api.main:app --limit-concurrency 1000 --loop 'uvloop' --workers 2 --host 0.0.0.0 --port 80 --no-access-log &
UVICORN_PID=$!

function gracefulShutdown {
  for mypid in $UVICORN_PID $CELERY_PID; do
    echo "container graceful shutdown. pid=$mypid"
    kill -15 $mypid
    wait $mypid
  done
}
trap gracefulShutdown SIGTERM TERM INT
# wait for pid 1 to exit
wait "${!}"
