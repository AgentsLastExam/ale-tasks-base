---
name: resource-proof
description: Complete the ALE Skill and Task MCP resource-injection proof.
---

When asked to complete the resource-injection proof:

1. Read the nonce from `/home/user/input/nonce.txt`.
2. Call the `derive_fragment` tool from the injected `task-proof` MCP server, passing
   that exact nonce.
3. Read the `fragment` value returned by the tool.
4. Write exactly `SKILL-R7::<nonce>::<fragment>` to
   `/home/user/output/result.txt`, with no trailing newline.

Do not derive or invent the fragment yourself. The MCP call is part of the task.
