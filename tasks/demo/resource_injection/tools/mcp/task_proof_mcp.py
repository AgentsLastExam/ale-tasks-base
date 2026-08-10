#!/usr/bin/env python3
"""Task-local MCP server used by the resource-injection demo."""

import json
import secrets
import sys
from pathlib import Path

NONCE_PATH = Path("/home/user/input/nonce.txt")
RECEIPT_PATH = Path("/home/user/output/mcp-call.json")


def result(request_id, payload):
    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def main():
    for line in sys.stdin:
        message = json.loads(line)
        request_id = message.get("id")
        if request_id is None:
            continue
        method = message.get("method")
        if method == "initialize":
            reply = result(
                request_id,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "task-proof", "version": "1.0.0"},
                },
            )
        elif method == "tools/list":
            reply = result(
                request_id,
                {
                    "tools": [
                        {
                            "name": "derive_fragment",
                            "description": "Derive the task fragment for an exact nonce.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"nonce": {"type": "string"}},
                                "required": ["nonce"],
                                "additionalProperties": False,
                            },
                        }
                    ]
                },
            )
        elif method == "tools/call":
            params = message.get("params") or {}
            nonce = str((params.get("arguments") or {}).get("nonce") or "")
            expected_nonce = NONCE_PATH.read_text(encoding="utf-8").strip()
            if params.get("name") != "derive_fragment" or nonce != expected_nonce:
                payload = {
                    "content": [{"type": "text", "text": "nonce mismatch"}],
                    "isError": True,
                }
            else:
                fragment = secrets.token_hex(12).upper()
                RECEIPT_PATH.write_text(
                    json.dumps({"nonce": nonce, "fragment": fragment}, sort_keys=True),
                    encoding="utf-8",
                )
                payload = {
                    "content": [{"type": "text", "text": json.dumps({"fragment": fragment})}],
                    "structuredContent": {"fragment": fragment},
                }
            reply = result(request_id, payload)
        else:
            reply = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"unsupported method: {method}"},
            }
        sys.stdout.write(json.dumps(reply) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
