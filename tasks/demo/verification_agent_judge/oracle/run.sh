#!/usr/bin/env bash
set -euo pipefail
cat > /home/user/output/hello.sh <<'EOF'
#!/usr/bin/env bash
printf 'hello\n'
EOF
chmod +x /home/user/output/hello.sh
