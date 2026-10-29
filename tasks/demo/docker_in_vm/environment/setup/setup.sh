#!/usr/bin/env bash
set -euo pipefail

mkdir -p /home/user/output
: > /home/user/output/nested-container.txt
chown -R user:user /home/user/output

for _ in $(seq 1 60); do
    docker info >/dev/null 2>&1 && exit 0
    sleep 1
done

echo "Docker did not become ready" >&2
exit 1
