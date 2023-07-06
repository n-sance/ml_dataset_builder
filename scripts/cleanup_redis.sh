#!/bin/bash

REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0
SET_NAME="urls_set"


redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -n "$REDIS_DB" <<EOF

while [[ \$(redis-cli SPOP $SET_NAME) ]]; do :; done
EOF