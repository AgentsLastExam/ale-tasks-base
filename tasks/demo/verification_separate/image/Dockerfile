FROM ghcr.io/agentslastexam/container-ubuntu22-base:latest

RUN mkdir -p /home/user/output /var/lib/ale-report \
    && printf '{}\n' > /home/user/output/result.json \
    && chown -R user:user /home/user/output /var/lib/ale-report
