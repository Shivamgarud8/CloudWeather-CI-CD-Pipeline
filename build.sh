#!/bin/bash

set -e

IMAGE_NAME="tagid-ui"

echo "========================================="
echo "        Docker Image Builder"
echo "========================================="

# Check if we're inside a Git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "❌ Not a Git repository."
    exit 1
fi

# Try to get the latest Git tag
VERSION=$(git describe --tags --abbrev=0 2>/dev/null)

if [ -n "$VERSION" ]; then
    VERSION_SOURCE="Git Release Tag"
else
    VERSION=$(git rev-parse --short HEAD)
    VERSION_SOURCE="Latest Commit ID"
fi

echo
echo "Image Name    : $IMAGE_NAME"
echo "Version       : $VERSION"
echo "Version From  : $VERSION_SOURCE"
echo "Docker Image  : ${IMAGE_NAME}:${VERSION}"
echo

read -p "Do you want to build this image? (y/N): " CONFIRM

case "$CONFIRM" in
    y|Y|yes|YES)
        ;;
    *)
        echo "Build cancelled."
        exit 0
        ;;
esac

echo
echo "Building Docker image..."
echo

docker build -t ${IMAGE_NAME}:${VERSION} .

echo
echo "========================================="
echo "Build completed successfully!"
echo "========================================="
echo "Image Created : ${IMAGE_NAME}:${VERSION}"
echo

echo "Available Images:"
docker images | grep "$IMAGE_NAME"
