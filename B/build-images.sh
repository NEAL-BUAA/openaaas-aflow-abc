#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
docker build --build-arg AFLOW_ROLE=query -t abc-aflow-query:latest ./executor
docker build --build-arg AFLOW_ROLE=stats -t abc-aflow-stats:latest ./executor
