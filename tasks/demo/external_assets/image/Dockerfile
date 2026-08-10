FROM ghcr.io/agentslastexam/sandbox-base-cli:latest

COPY assets/public.txt /home/user/input/public.txt

RUN mkdir -p /home/user/output \
    && chown -R user:user /home/user/input /home/user/output
