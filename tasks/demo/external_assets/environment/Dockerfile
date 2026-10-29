FROM ghcr.io/agentslastexam/container-ubuntu22-base:latest

COPY assets/public.txt /home/user/input/public.txt
# Served by setup: root-only, so the agent reaches it only through the service.
COPY assets/service-response.txt /opt/external-assets/service-response.txt

RUN chmod 0700 /opt/external-assets \
    && mkdir -p /home/user/output \
    && chown -R user:user /home/user/input /home/user/output
