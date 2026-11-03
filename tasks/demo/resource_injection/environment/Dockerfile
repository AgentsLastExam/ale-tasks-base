FROM ghcr.io/agentslastexam/container-ubuntu22-base:0.1.1

COPY skills/ /skills/
COPY mcp/ /opt/task-proof/
RUN mkdir -p /home/user/input /home/user/output \
    && chown -R user:user /home/user/input /home/user/output
