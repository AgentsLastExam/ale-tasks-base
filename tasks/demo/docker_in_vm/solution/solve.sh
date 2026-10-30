#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/user/output
docker import /usr/local/share/docker-in-vm/busybox-rootfs.tar ale-busybox:offline >/dev/null
docker run --rm --network none ale-busybox:offline \
    sh -c 'printf "nested-container-ok\n"' \
    > /home/user/output/nested-container.txt
