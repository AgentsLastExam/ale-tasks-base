FROM ghcr.io/agentslastexam/sandbox-base-cli:latest

RUN mkdir -p /home/user/input /home/user/output \
    && printf world > /home/user/input/word.txt \
    && chown -R user:user /home/user/input /home/user/output
