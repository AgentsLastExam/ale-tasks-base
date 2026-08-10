# ALE Tasks base

Reference collection of independent `core/v1` container and VM Tasks. This repository contains no
runtime manifest or shared Task code; each folder below `tasks/` is complete on its own.

## Folder layout

```text
tasks/<path>/
├── task.yaml
├── instruction.md
├── image/
│   ├── Dockerfile
│   └── assets/                 # optional large input, ignored by Git
├── setup/
│   ├── run.sh
│   └── assets/                 # optional dynamic-stage data, ignored
├── verify/
│   ├── run.sh
│   ├── verify.py
│   ├── Dockerfile              # optional separate verifier image
│   └── assets/                 # optional references, ignored
├── oracle/
│   ├── run.sh
│   └── assets/                 # optional oracle-only data, ignored
└── tools/
    ├── skills/<name>/SKILL.md
    └── mcp/<server>.toml
```

Every Task explicitly declares `image.kind: container|vm`. A fixed `image/Dockerfile`
selects a local build and wins over an authored ref; without it, `image.ref` is required.
Stable packages, services, permissions, and solver-visible state belong in the image.
`setup/` performs only irreducibly episode-dynamic initialization.

There is no `domain.yaml`, repository Kit, shared image, implicit `files/`, or top-level
Skills/MCP. Top-level manifest fields define `base`; variants may override only params,
resources, and timeouts.

## Assets

Large files remain directly below their owning stage. Each Task repository maps to a
same-named Hugging Face dataset in the configured assets collection. Pull restores the
exact local folder structure and push uploads only stage asset roots.

```bash
cd /absolute/path/to/ale
export ALE_ASSETS_COLLECTION='Chennzi/assets-6a72bdee6d6b38dc9036c15c'

uv run ale assets status /absolute/path/to/ale-tasks-base
uv run ale assets pull /absolute/path/to/ale-tasks-base
uv run ale assets pull --force /absolute/path/to/ale-tasks-base/tasks/demo/external_assets
uv run ale assets push /absolute/path/to/ale-tasks-base/tasks/demo/external_assets
```

The public `Chennzi/ale-tasks-base` dataset was last synchronized for this contract at
commit `863a27f00880dff03001b524f371af025aca548e`.

There is no runtime pull and no asset declaration in `task.yaml`. Dockerfiles use normal
paths such as:

```dockerfile
COPY assets/public.txt /home/user/input/public.txt
```

Setup, verifier, and oracle code use ordinary relative `assets/...` paths. A Task without
an assets directory requires no Hugging Face configuration.

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

Unqualified selection means base. Use `@hard` or an ordered selector such as
`@{base,hard}` for additional variants.

The deterministic examples can be validated without model credentials:

```bash
just lint
just validate
```

Judge demos require their corresponding run-level model/endpoint/credential and exact
Agent Judge CLI version configuration. The `verification_separate` demo shows a local
verifier image selected by `verify/Dockerfile` plus explicit `verify.image.kind`, and exact
restoration of one file plus one directory artifact. External verifier images use the
same structured `{kind, ref}` shape. Omission reuses the prepared solver image.

See the engine's `docs/task-authoring.md`, `docs/task-design-principles.md`, and
`docs/specs/task-folder.md` for the complete contract.
