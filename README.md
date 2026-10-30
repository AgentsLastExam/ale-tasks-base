# ALE Tasks base

Reference collection of independent container and VM Tasks in ALE's `task.toml` format:
Harbor's task layout and schema 1.4 plus an `[ale]` table. This repository contains no shared
Task code; each folder below `tasks/` is complete on its own.

## Folder layout

```text
tasks/<path>/
├── task.toml
├── instruction.md
├── environment/
│   ├── Dockerfile              # container or Linux VM image ([ale].sandbox); context
│   │                           # environment/ without setup/
│   └── setup/setup.sh          # optional per-episode initialization
├── tests/
│   ├── test.sh
│   ├── verify.py
│   └── Dockerfile              # optional separate verifier image
├── solution/
│   └── solve.sh
└── tools/
    ├── skills/<name>/SKILL.md
    └── mcp/<server>.toml
```

Stable packages, services, permissions, and solver-visible state belong in the image.
`environment/setup/` performs only irreducibly episode-dynamic initialization. The format
contract is the engine's `docs/specs/task-authoring.md`.

## Assets

Large files live in `assets/` directories beside the files that read them:
`environment/assets/` (the image build, container or VM), `tests/assets/` and
`solution/assets/`. They are ignored by Git and synchronized with the
private Hugging Face dataset `agents-last-exam/ale-tasks-base`, which mirrors their paths.
Asset commands authenticate with `ALE_HF_TOKEN` from the engine checkout's `.env`:

```bash
cd /absolute/path/to/ale
uv run ale assets status /absolute/path/to/ale-tasks-base
uv run ale assets pull /absolute/path/to/ale-tasks-base
uv run ale assets push /absolute/path/to/ale-tasks-base/tasks/demo/external_assets
```

Running a Task never downloads assets, and `task.toml` declares none. Stage code reads them
through ordinary relative paths, for example in `environment/Dockerfile`:

```dockerfile
COPY assets/public.txt /home/user/input/public.txt
```

A Task without an assets directory requires no Hugging Face configuration. The specification
is the engine's `docs/specs/task-assets.md`.

## Authoring commands

Run the engine CLI from the ALE checkout; this repository does not install `ale-run`:

```bash
cd /absolute/path/to/ale
uv run ale new-task /absolute/path/to/ale-tasks-base/tasks/my_task
uv run ale lint /absolute/path/to/ale-tasks-base
uv run ale prepare /absolute/path/to/ale-tasks-base/tasks/my_task
uv run ale validate /absolute/path/to/ale-tasks-base/tasks/my_task
uv run ale run /absolute/path/to/ale-tasks-base/tasks/my_task --agent oracle
```

The deterministic examples can be validated without model credentials:

```bash
just lint
just validate
```

Judge demos require their corresponding run-level model/endpoint/credential and exact
Agent Judge CLI version configuration. The `verification_separate` demo shows a separate
verifier built from `tests/Dockerfile` with its own `[verifier.environment]` resources, and
exact restoration of one file plus one directory artifact. A separate verifier without
`tests/Dockerfile` or `[verifier.environment].docker_image` reuses the prepared solver image.
