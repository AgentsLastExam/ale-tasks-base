#!/usr/bin/env bash
set -euo pipefail

apt-get update
apt-get install -y docker.io
rm -rf /var/lib/apt/lists/*
systemctl enable docker.service containerd.service
usermod -aG docker user

# The agent's network is closed, so the image it runs is kept as a root filesystem to import.
busybox=busybox:1.36.1@sha256:73aaf090f3d85aa34ee199857f03fa3a95c8ede2ffd4cc2cdb5b94e566b11662
systemctl start docker
docker pull --quiet "$busybox" >/dev/null
container=$(docker create "$busybox")
install -d /usr/local/share/docker-in-vm
docker export "$container" -o /usr/local/share/docker-in-vm/busybox-rootfs.tar
chmod 0644 /usr/local/share/docker-in-vm/busybox-rootfs.tar
docker rm "$container" >/dev/null
docker image prune --all --force >/dev/null
