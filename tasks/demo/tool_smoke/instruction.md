Goal: test every tool available to you and produce a structured report.

Context: an ephemeral sandbox with no human in the loop. Evaluation begins the moment
this invocation returns. Default to testing a tool. If one needs prior session state
(plan mode, a worktree, a running background task), bootstrap that state yourself and
then test it. Side effects and destructive operations do not matter — the sandbox is
discarded.

**What counts as a real test.** A tool counts as `passed` only if you actually invoked it
and observed a return that proves it worked. For each tool:

- (a) Construct the simplest concrete scenario that produces an observable, verifiable
  result. Not an empty or no-op call made to "touch" the tool — the input must be real
  enough that a working tool returns something checkable and a broken one would not.
  - a file-write tool: write a known string to a temporary path, read it back, confirm
    the bytes match;
  - a file-read tool: read a file you just created and confirm its contents;
  - a shell tool: run `echo <marker>` and confirm the exact marker in stdout;
  - a list or search tool: list a directory you just populated and confirm the entry;
  - a screenshot or desktop tool: capture, and confirm you received non-empty image data.
- (b) Invoke the tool with that input.
- (c) Read the tool's actual return content.
- (d) Confirm it matches the expected effect. Only then mark it `passed`.

If a call errors, returns nothing observable, or you cannot verify the result, mark it
`failed` with the error. Never mark a tool `passed` on a call whose result you did not
observe. A response such as `omitted`, `unavailable`, `pending`, `pending_init`, `queued`,
or `accepted` is not proof of completion. Follow it to a terminal, verified result or mark
the tool `failed`/`untested`.

**Instructions**

1. Identify the tools you can actually see and call here — native tools, external tools,
   and any provided by a connected MCP server. Do not invent tools and do not list tools
   that are not available to you. If an MCP server is connected (desktop control, for
   instance, with names like `mcp__desktop__*`) those *are* available tools: exercise
   them and count them in your total. Do not skip them because they came from a server.
   Count callable endpoints, not parameter modes: a callable such as `web.run` is one
   tool even if it accepts `search_query`, `open`, `finance`, or other operations. Test a
   concrete mode and report `web.run` once; do not invent separate `web.*` tool names.
2. For each available tool, follow (a)–(d) with the simplest safe scenario. Prefer
   read-only, list, status, metadata, validation, dry-run or tiny local inputs — but the
   call must still produce an observable result you verify.
3. Keep each individual test under three minutes. This task only checks that tools work.
4. If a tool's purpose is interactive, persistent, long-running, irreversible,
   payment-related or account-changing, do not run the real operation. Use a harmless
   dry-run, status or listing mode if it has one, and still observe the return.
5. Do not invoke a tool whose successful operation ends, yields, or replaces this current
   invocation. You cannot observe its return and then finish the report, so record it under
   `tools_untested` with that reason. A tool such as `sessions_yield` belongs here.
6. If a tool has no safe bounded way to produce an observable result, needs credentials
   or configuration you do not have, or requires user interaction, record it under
   `tools_untested` with a short reason instead of calling it.
7. Create `/home/user/output/tool_report.json` before testing and update it after every
   tool result. Do not defer the entire report until the end: a later tool may fail or end
   the invocation.
8. Record for each tool you called whether it passed or failed, based on what you
   observed.
9. When every available tool has been handled, leave the JSON report at
   `/home/user/output/tool_report.json` with exactly this structure:

   ```json
   {
     "tools_tested": ["tool_a", "tool_b"],
     "tools_passed": ["tool_a"],
     "tools_failed": {"tool_b": "error message"},
     "tools_untested": {"tool_c": "reason not tested"},
     "total": 3,
     "tested": 2,
     "passed": 1,
     "failed": 1,
     "untested": 1
   }
   ```

   `total`, `tested`, `passed`, `failed` and `untested` are required integers, and
   `total` must equal `tested` + `untested`.
10. Exit normally when done.
