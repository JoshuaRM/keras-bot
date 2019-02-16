#!/usr/bin/env bash

set -e

docker build -t keras-bot ./
docker run -e GITHUB_TOKEN=$GITHUB_TOKEN keras-bot python ./enforce_codeowners/keras_bot/pull_requests.py