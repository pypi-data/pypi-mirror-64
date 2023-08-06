#!/usr/bin/env bash
set -e
TAG=$1
VERSION=${2:$CI_PIPELINE_IID}
DOCKER_TAG=$TAG-$VERSION
REPO=probator/probator

semver "$TAG" &> /dev/null
RC=$?

if [[ -z "$TAG" || $RC -ne 0 || -z "$VERSION" ]]; then
    echo "Usage: $0 [TAG] <VERSION>"
    echo "Version if not set, will try and use CI_PIPELINE_IID environment variable"
    exit 1
fi

TOKEN=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username": "'"${DOCKER_USERNAME}"'", "password": "'"${DOCKER_PASSWORD}"'"}' https://hub.docker.com/v2/users/login/ | jq -r .token)
IDX=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/${REPO}/tags?page_size=10000 | jq ".tags | index (\"$DOCKER_TAG\")")
if [[ "$IDX" != "null" ]]; then
    echo "Docker image ${REPO}:$DOCKER_TAG already exists"
    exit 1
fi

docker build \
    --no-cache \
    --build-arg VERSION="$TAG" \
    -t ${REPO}:"$DOCKER_TAG" \
    -t ${REPO}:latest .
# docker push ${REPO}:"$DOCKER_TAG"
# docker push ${REPO}:latest
