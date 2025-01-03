#!/usr/bin/env bash

set -e

# shellcheck disable=SC2068
python -m uvicorn \
    --loop uvloop \
    --workers 1 \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    --access-log \
    --factory \
    food_review_api:build_service_app \
    $@
