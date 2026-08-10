FROM ghcr.io/agentslastexam/sandbox-base-cli:latest

RUN mkdir -p /home/user/output /var/lib/ale-report \
    && printf '{}\n' > /home/user/output/result.json \
    && chown -R user:user /home/user/output /var/lib/ale-report
