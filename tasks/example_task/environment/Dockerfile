FROM ghcr.io/agentslastexam/container-ubuntu22-base:latest

RUN mkdir -p /home/user/input /home/user/output \
    && printf world > /home/user/input/word.txt \
    && chown -R user:user /home/user/input /home/user/output
