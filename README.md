# ALE Tasks base

Reference collection of independent container and VM Tasks in Orbit's `task.toml` format:
Harbor's Task layout and fields, with Orbit's additions in the Harbor tables they configure. This
repository contains no shared Task code; each folder below `tasks/` is complete on its own.

## Folder layout

```text
tasks/<path>/
├── task.toml
├── instruction.md
├── environment/
│   ├── Dockerfile              # container image; context environment/ without setup/
│   ├── build.sh                # or a VM image built on [environment].image, same context
│   └── setup/setup.sh          # optional per-episode initialization
├── tests/
│   ├── test.sh
│   ├── verify.py
│   └── Dockerfile              # optional separate verifier image
└── solution/
    └── solve.sh
```

Stable packages, services, permissions, and solver-visible state belong in the image.
`environment/setup/` performs only irreducibly episode-dynamic initialization. The format
contract is the engine's
[task-authoring.md](https://github.com/AgentsLastExam/orbit/blob/main/docs/specs/task-authoring.md),
and what makes a Task acceptable is its
[task-quality-standard.md](https://github.com/AgentsLastExam/orbit/blob/main/docs/specs/task-quality-standard.md).

## Code in Git, material on the Hub

Task code and configuration live in Git. **All** Task material, whatever its size, lives in the
stage `assets/` directories, which Git ignores, and is synchronized with the gated Hugging Face
dataset [`agents-last-exam/ale-tasks-base`](https://huggingface.co/datasets/agents-last-exam/ale-tasks-base), which mirrors their paths exactly:
`tasks/<path>/tests/assets/x` here is `tasks/<path>/tests/assets/x` there. The dataset name is the repository name; its namespace is `agents-last-exam` unless `ORBIT_ASSETS_NAMESPACE` names a team's own organization (`AgentsLastExam/ale-tasks-<domain>` → `<team organization>/ale-tasks-<domain>`). This repository uses the default.

| Material | Asset root | How stage code reaches it |
|---|---|---|
| Inputs the agent works from | `environment/assets/` | the image build copies it, e.g. `COPY assets/input/ /home/user/input/` |
| Reference deliverables of the oracle | `solution/assets/` | `solve.sh` copies it, e.g. `cp -a assets/reference/. /home/user/output/` |
| Rubrics, expected values, reference and source documents of the verifier | `tests/assets/` | the verifier reads `assets/…` by relative path |

Material is data an author supplies rather than writes as program logic: documents, spreadsheets,
images, data files, rubric workbooks, expected outputs. `task.toml`, `instruction.md`, the
Dockerfile and build scripts, `setup/`, `test.sh`, `verify.py` and other verifier code, and
`solve.sh` stay in Git. When a verifier was written to read material at another path, its entry
links `tests/assets/` back to those paths before it runs instead of editing the scorer.

`demo/external_assets` shows all three: `environment/assets/public.txt` and `service-response.txt`
(copied by its Dockerfile, e.g. `COPY assets/public.txt /home/user/input/public.txt`),
`tests/assets/expected.json` (read by `verify.py`) and `solution/assets/result.json` (copied by
`solve.sh`), all four on the dataset under `tasks/demo/external_assets/`.

Running a Task never downloads assets, and `task.toml` declares none. Request access on the
dataset's page; once an administrator approves it, asset commands authenticate with
`ORBIT_HF_TOKEN` from the engine checkout's `.env`:

```bash
cd /absolute/path/to/orbit
uv run orbit assets status /absolute/path/to/ale-tasks-base
uv run orbit assets pull   /absolute/path/to/ale-tasks-base                 # after every fresh clone
uv run orbit assets push   /absolute/path/to/ale-tasks-base/tasks/<path>    # one or more Task paths
```

Push Task paths, not the whole collection, when other Tasks live only on unmerged branches. Each
push makes one dataset commit per Task, titled `Update tasks/<path> assets`; merge a change's code
and push its material together. Two recoveries:

- A push of a Task whose assets were pushed before is rejected as `non-fast-forward`, and Tasks
  later in the batch are skipped: its cached checkpoint branch is stale. Remove
  `.orbit-cache/asset-worktrees/tasks/<path>` (`git worktree remove` in `.git/orbit-assets/repository`),
  the branch `manual/tasks/<path>` there and `.orbit-cache/asset-worktrees/tasks/<path>.publication.json`,
  then push again and check `orbit assets status`.
- After the dataset moves to another organization, a checkout that pushed before refuses with
  `asset workspace belongs to a different Task repository`: remove its `.orbit-cache/` and
  `.git/orbit-assets/` once and run the command with the new namespace.

The specification is the engine's [task-assets.md](https://github.com/AgentsLastExam/orbit/blob/main/docs/specs/task-assets.md).

## Versions

There are no hand-written version numbers or tags; every identity is a content hash that Git or
the Hub computes.

| Identity | Form | Changes when |
|---|---|---|
| Task code | git tree id of `tasks/<path>` on `main` | a file of this Task's code or configuration changes |
| Task material | git tree id of `tasks/<path>` on the dataset (LFS pointers carry each file's sha256) | a material file of this Task is added, removed or changed |
| Dataset revision | the dataset's commit id | any Task's material is pushed |
| Task version | sha256 over the two trees (below) | the Task's code or material changes |

Both trees cover only the Task's own folder, so each Task is versioned independently: pushing
another Task's material moves the dataset revision but no other Task's tree. The dataset revision
is recorded beside a version, never inside it.

```
version = "sha256:" + sha256(canonical JSON of
  {"schema": "ale-atlas/task-version@2", "repo": "AgentsLastExam/ale-tasks-base", "path": "tasks/<path>",
   "code":   {"git_object_format": "sha1", "tree": <code tree>},
   "assets": {"kind": "hf-dataset", "dataset": <dataset id>, "path": "tasks/<path>", "tree": <material tree>}})
canonical JSON: keys sorted, separators "," and ":", UTF-8, no ASCII escaping
```

`assets` is `null` for a Task with no material. `<dataset id>` is the dataset's name when its
first versions were recorded; moving the dataset to another organization does not change existing
versions.

Worked example, `demo/external_assets` at repository commit `e122715` and dataset revision
`e8d8dac`: code tree `c767700875d3d398f005993354e3e1c21a7f6091`, material tree
`34e189ad6cfad36ebf00fca08ff8eaa17ca218b5`, version
`sha256:97632300cc4ae07596f9a5bb654e32c69230ca55c652eaa73858948883b19801`.

```bash
git rev-parse HEAD:tasks/<path>                                                     # code tree
curl -s https://huggingface.co/api/datasets/agents-last-exam/ale-tasks-base/revision/main                     # dataset revision
curl -s https://huggingface.co/api/datasets/agents-last-exam/ale-tasks-base/tree/<revision>/tasks             # material trees
```

Every run's RunLock records the asset commit it used and whether local assets were dirty; a run
with dirty or unsynchronized assets is not reportable. Results bind to a full Task version and
are never mixed across versions.

## Run records

The episodes that `orbit run` produces for a repository's Tasks are kept in a run-record dataset beside its asset dataset, in the same organization: `<organization>/ale-tasks-<domain>-runs` next to `<organization>/ale-tasks-<domain>`. [`agents-last-exam/ale-tasks-demo-runs`](https://huggingface.co/datasets/agents-last-exam/ale-tasks-demo-runs) shows the layout; it holds no runs.

```
tasks/<path>/
└── <task version>/                 sha256-<64 hex>, the Task version above
    ├── version.json                repository, commit, code_tree, dataset, dataset_revision, material_tree, version
    └── <run id>/                   the run directory name orbit run created under runs/
        └── <episode id>/           the episode directory exactly as orbit run wrote it: result.json, lock.json,
                                    trajectory.json, verification.json, Judge records, traces, blobs/, attempts/
```

- Only real `orbit run` episodes are uploaded, and only under the Task version their RunLock names:
  its Task source and its asset commit must match `version.json`, and its assets must be clean.
  Runs of different versions are never mixed; results are compared within a version.
- `version.json` records which repository commit and which asset revision a version's runs used,
  the pairing the repository itself does not keep.
- What each record holds is the engine's [trace specification](https://github.com/AgentsLastExam/orbit/blob/main/docs/specs/trace.md); consumers read
  each run's immediate episode folders (`*/result.json`), not the archived attempts.
- Every file under `tasks/` is stored with Git LFS. The dataset is gated like the asset dataset:
  run records hold what the agent saw and produced, the verifier's details and Judge reasoning.
  Orbit redacts the credentials it knows; review a run before uploading it all the same.

```bash
hf upload <organization>/ale-tasks-<domain>-runs runs/<run id> tasks/<path>/<task version>/<run id> --repo-type dataset
```

## Taxonomy and placements

`taxonomy/` places Tasks on the domain's task taxonomy. It is kept outside the Task folders on
purpose: placements change often, and editing them must never change a Task's code tree or version.
This repository's `taxonomy/` is a complete example: a small tree of the capabilities its demo Tasks show, with every Task placed; see [`taxonomy/README.md`](taxonomy/README.md).

| File | Content |
|---|---|
| `taxonomy/tree.json` | the taxonomy, `ale-taxonomy-tree@1`: `source` (where it came from, when, sha256) and `root`, a tree of `{id, name_en, children}` |
| `taxonomy/mapping.json` | placements, `ale-taxonomy-mapping@1`: `entries[]` (below) |
| `taxonomy/check.py` | validation and per-node counts; standard library only |

| Entry field | Meaning |
|---|---|
| `task` | path under `tasks/`, e.g. `my_task` or `demo/my_task` |
| `node` | a node `id` of `tree.json`, or `null` when no node fits (a taxonomy gap worth recording) |
| `role` | `primary` (exactly one per Task) or `secondary` (at most two) |
| `status` | `proposed`, `confirmed` or `rejected`; a rejected row stays as history and is not counted |
| `confidence` | `high`, `medium` or `low` |
| `basis` | one sentence on why |
| `same_as` | optional: a tree leaf that is this same case under another id |
| `by`, `at` | who set the row and when |

A Task counts once at its node and every ancestor. To move a Task, edit its row or mark it
`rejected` and add a new one; update `status`, `by` and `at`. When the taxonomy changes, replace
`tree.json`; `check.py` then lists every entry whose node no longer exists.

```bash
python3 taxonomy/check.py            # Task paths, node ids, one primary per Task, field values
python3 taxonomy/check.py --counts   # Tasks per node, ancestors included
```

## Merging Tasks

The step-by-step guide for contributors, with a pull request template, is the
[`ale-contribute` skill](https://github.com/AgentsLastExam/ale-skills/blob/main/skills/ale-contribute/SKILL.md).

- One Task per pull request: it adds or changes exactly one Task and touches only `tasks/<path>/`.
  Repository-wide files (README, `taxonomy/`, CI) change in their own pull requests.
- A Task that builds and verifies goes to `main`.
- A Task blocked on something outside the repository (missing source material, a service, a
  licence) goes in its own pull request, one Task per pull request. Its `task.toml` records
  `[metadata] blocked = true` and `blocked_reason`; the pull request says what would unblock it.
- A Task's pull request does not edit `taxonomy/mapping.json`: its placement (primary node,
  optional secondary nodes, confidence, basis) is proposed in the pull request description, and a
  maintainer records it on `main` as `proposed`. A Task still in its pull request keeps that row on
  `main`; `check.py` reports such rows as not on the branch instead of failing, so concurrent Task
  pull requests never edit the same file.
- A Task's material is pushed to the dataset when its code is pushed, including for a Task in a
  pull request; the dataset only ever holds material, never code.

## Imported Tasks

A batch converted from another source records, per Task, in `[metadata]`: `source_platform`,
`source_id` (the source's own identifier), a link to the source item, `source_snapshot` (date) and
`conversion_notes`, one line per change made in conversion. The repository root's `IMPORT.md`
lists the batch: each Task, its source id, and whether it is on `main` or in its pull request with
the reason.

## Authoring commands

Run the engine CLI from the Orbit checkout; this repository does not install `orbit-run`:

```bash
cd /absolute/path/to/orbit
uv run orbit new-task /absolute/path/to/ale-tasks-base/tasks/my_task
uv run orbit lint /absolute/path/to/ale-tasks-base
uv run orbit prepare /absolute/path/to/ale-tasks-base/tasks/my_task
uv run orbit calibrate /absolute/path/to/ale-tasks-base/tasks/my_task
uv run orbit run /absolute/path/to/ale-tasks-base/tasks/my_task --agent oracle
```

The deterministic examples can be calibrated without model credentials:

```bash
just lint
just calibrate
```

Judge demos require their corresponding run-level model/endpoint/credential and exact
Agent Judge CLI version configuration. The `verification_separate` demo shows a separate
verifier built from `tests/Dockerfile` with its own `[verifier.environment]` resources, and
exact restoration of one file plus one directory artifact. A separate verifier without
`tests/Dockerfile` or `[verifier.environment].image` reuses the prepared solver image.
