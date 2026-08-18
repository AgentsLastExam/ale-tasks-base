FROM busybox:1.36.1@sha256:73aaf090f3d85aa34ee199857f03fa3a95c8ede2ffd4cc2cdb5b94e566b11662 AS busybox

FROM ghcr.io/agentslastexam/vm-ubuntu24-base:0.1.0

RUN apt-get update \
    && apt-get install -y docker.io \
    && rm -rf /var/lib/apt/lists/* \
    && systemctl enable docker.service containerd.service \
    && usermod -aG docker user

COPY --from=busybox / /usr/local/share/docker-in-vm/busybox-rootfs/
RUN tar -C /usr/local/share/docker-in-vm/busybox-rootfs \
        -cf /usr/local/share/docker-in-vm/busybox-rootfs.tar . \
    && rm -rf /usr/local/share/docker-in-vm/busybox-rootfs
