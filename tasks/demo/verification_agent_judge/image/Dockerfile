FROM ghcr.io/agentslastexam/container-ubuntu22-base:latest

RUN npm install -g \
        @openai/codex@0.146.0 \
        @anthropic-ai/claude-code@2.1.220 \
    && codex --version \
    && claude --version \
    && mkdir -p /home/user/output \
    && chown -R user:user /home/user/output
