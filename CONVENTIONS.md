# Task repository conventions

How an `AgentsLastExam/ale-tasks-<domain>` repository keeps its Tasks, their material on Hugging
Face, their versions and their place in a domain taxonomy. These conventions sit on top of the
engine's specifications and never override them: the Task format is
[task-authoring.md](https://github.com/AgentsLastExam/ale/blob/main/docs/specs/task-authoring.md),
asset synchronisation is
[task-assets.md](https://github.com/AgentsLastExam/ale/blob/main/docs/specs/task-assets.md).
This repository follows them and carries the worked examples referenced below.

## 1. One repository, one dataset

```
AgentsLastExam/ale-tasks-<domain>            GitHub: code and configuration
├── tasks/<path>/                            one Task per folder, complete on its own
│   ├── environment/assets/  tests/assets/  solution/assets/      ignored by Git
└── taxonomy/                                domain taxonomy and Task placements (section 4)

<namespace>/ale-tasks-<domain>                Hugging Face dataset: all Task material
└── tasks/<path>/{environment,tests,solution}/assets/…             same paths as the repository
```

The dataset name is the repository name. Its namespace is `agents-last-exam` unless
`ALE_ASSETS_NAMESPACE` names the team's own organization, set in the engine checkout's `.env` or
per command:

| Task repository | `ALE_ASSETS_NAMESPACE` | Dataset |
|---|---|---|
| `AgentsLastExam/ale-tasks-base` | unset | `agents-last-exam/ale-tasks-base` |
| `AgentsLastExam/ale-tasks-legal` | `ale-legal` | `ale-legal/ale-tasks-legal` |
| `AgentsLastExam/ale-tasks-finance` | `ale-finance` | `ale-finance/ale-tasks-finance` |
| `AgentsLastExam/ale-tasks-or` | `ale-or` | `ale-or/ale-tasks-or` |

Datasets are public and gated: anyone sees the file list, only approved users download. Paths
mirror the repository exactly, so `tasks/demo/external_assets/tests/assets/expected.json` is the
same file in both. [`ale-or/ale-tasks-or`](https://huggingface.co/datasets/ale-or/ale-tasks-or)
starts from a copy of that one Task's material and a card describing the layout.

When a dataset moves to another organization, Hugging Face redirects its old name, but a checkout
that pushed before keeps an asset cache bound to the old name and refuses with `asset workspace
belongs to a different Task repository`: remove that checkout's `.ale-cache/` and
`.git/ale-assets/` once and run the command with the new namespace.

## 2. Code in Git, material on the Hub

All Task material lives in the stage asset roots, **whatever its size**. Git holds only code and
configuration, so the two are reviewed, versioned and moved independently.

| Material | Asset root | How stage code reaches it |
|---|---|---|
| Inputs the agent works from | `environment/assets/` | the image build copies it, e.g. `COPY assets/input/ /home/user/input/` |
| Reference deliverables of the oracle | `solution/assets/` | `solve.sh` copies it, e.g. `cp -a assets/reference/. /home/user/output/` |
| Rubrics, expected values, reference and source documents of the verifier | `tests/assets/` | the verifier reads `assets/…` by relative path |

Material is data an author supplies rather than writes as program logic: documents, spreadsheets,
images, data files, rubric workbooks, expected outputs. Code and configuration stay in Git:
`task.toml`, `instruction.md`, `Dockerfile` and build scripts, `setup/`, `test.sh`, `verify.py` and
other verifier code, `solve.sh`. When a verifier was written to read material at another path,
its entry links `tests/assets/` back to those paths before it runs rather than editing the scorer.

`.gitignore` already excludes the three roots. `demo/external_assets` shows all three:
`environment/assets/public.txt` and `service-response.txt` (copied by its Dockerfile),
`tests/assets/expected.json` (read by `verify.py`) and `solution/assets/result.json` (copied by
`solve.sh`), all four files on the dataset under `tasks/demo/external_assets/`.

```bash
cd /absolute/path/to/ale                                   # engine checkout; ALE_HF_TOKEN in its .env
uv run ale assets status /absolute/path/to/ale-tasks-<domain>
uv run ale assets push   /absolute/path/to/ale-tasks-<domain>/tasks/<path>   # one or more Task paths
uv run ale assets pull   /absolute/path/to/ale-tasks-<domain>                # after every fresh clone
```

Push Task paths, not the whole collection, when other Tasks live only on unmerged branches.
Each push creates one dataset commit per Task, titled `Update tasks/<path> assets`. A Task's
code and its material change in separate commits on separate remotes; merge the code and push
the material for the same change together.

If a push of a Task whose assets were pushed before is rejected as `non-fast-forward`, its
cached checkpoint branch is stale: remove `.ale-cache/asset-worktrees/tasks/<path>` (with
`git worktree remove` in `.git/ale-assets/repository`), the branch `manual/tasks/<path>` there and
`.ale-cache/asset-worktrees/tasks/<path>.publication.json`, then push again. Tasks later in the
same batch are skipped after such a rejection; check `ale assets status` afterwards.

## 3. Versions

There are no hand-written version numbers or tags. Every identity is a content hash that Git or
the Hub computes:

| Identity | Form | Changes when |
|---|---|---|
| Task code | git tree id of `tasks/<path>` on `main` | a file of this Task's code or configuration changes |
| Task material | git tree id of `tasks/<path>` on the dataset (LFS pointers carry each file's sha256) | a material file of this Task is added, removed or changed |
| Dataset revision | the dataset's commit id | any Task's material is pushed |
| Task version | sha256 over the two trees (below) | the Task's code or material changes |

Both trees cover only the Task's own folder, so a Task's version is independent of every other
Task: pushing another Task's material moves the dataset revision but no other Task's tree. The
dataset revision is therefore recorded beside a version, never inside it.

```
version = "sha256:" + sha256(canonical JSON of
  {"schema": "ale-atlas/task-version@2", "repo": "AgentsLastExam/ale-tasks-<domain>", "path": "tasks/<path>",
   "code":   {"git_object_format": "sha1", "tree": <code tree>},
   "assets": {"kind": "hf-dataset", "dataset": "agents-last-exam/ale-tasks-<domain>",
              "path": "tasks/<path>", "tree": <material tree>}})
canonical JSON: keys sorted, separators "," and ":", UTF-8, no ASCII escaping
```

`assets` is `null` for a Task with no material. Worked example, `demo/external_assets` at
repository commit `e122715` and dataset revision `e8d8dac`: code tree `c767700875d3d398f005993354e3e1c21a7f6091`,
material tree `34e189ad6cfad36ebf00fca08ff8eaa17ca218b5`, version
`sha256:97632300cc4ae07596f9a5bb654e32c69230ca55c652eaa73858948883b19801`.

```bash
git rev-parse HEAD:tasks/<path>                                                      # code tree
curl -s https://huggingface.co/api/datasets/agents-last-exam/ale-tasks-<domain>/revision/main   # dataset revision
curl -s https://huggingface.co/api/datasets/agents-last-exam/ale-tasks-<domain>/tree/<revision>/tasks/<parent>   # material trees
```

Every run's RunLock records the asset commit it used and whether local assets were dirty; a run
with dirty or unsynchronised assets is not reportable. Results bind to a full Task version and
are never mixed across versions.

## 4. Taxonomy and placements

`taxonomy/` places Tasks on the domain's task taxonomy. It is kept **outside** the Task folders on
purpose: placements change often, and editing them must never change a Task's code tree or version.

| File | Content |
|---|---|
| `taxonomy/tree.json` | the taxonomy, `ale-taxonomy-tree@1`: `source` (where it came from, when, sha256) and `root`, a tree of `{id, name_en, children}` |
| `taxonomy/mapping.json` | placements, `ale-taxonomy-mapping@1`: `entries[]` (below) |
| `taxonomy/check.py` | validation and per-node counts; standard library only |
| `taxonomy/README.md` | the same rules for people editing the files |

Each entry places one Task (by its path under `tasks/`) on one node:

| Field | Meaning |
|---|---|
| `task` | path under `tasks/`, e.g. `demo/external_assets` |
| `node` | a node `id` of `tree.json`, or `null` when no node fits (a taxonomy gap worth recording) |
| `role` | `primary` (exactly one per Task) or `secondary` (at most two) |
| `status` | `proposed`, `confirmed` or `rejected`; a rejected row stays as history and is not counted |
| `confidence` | `high`, `medium` or `low` |
| `basis` | one sentence on why |
| `same_as` | optional: a tree leaf that is this same case under another id |
| `by`, `at` | who set the row and when |

A Task counts once at its node and every ancestor. To move a Task, edit its row or mark it
`rejected` and add a new one; update `status`, `by` and `at`. When the source taxonomy changes,
replace `tree.json`; `check.py` then lists every entry whose node no longer exists.

```bash
python3 taxonomy/check.py            # Task paths, node ids, one primary per Task, field values
python3 taxonomy/check.py --counts   # Tasks per node, ancestors included
```

This repository's `taxonomy/` is a complete example: a small tree of the capabilities its demo
Tasks show, with every Task placed.

## 5. Merging Tasks

- A Task that builds and verifies goes to `main`.
- A Task blocked on something outside the repository (missing source material, a service, a
  licence) goes in **its own pull request**, one Task per pull request. Its `task.toml` records
  `[metadata] blocked = true` and `blocked_reason`; the pull request says what would unblock it.
- A Task still in its pull request keeps its `taxonomy/mapping.json` row on `main`. `check.py`
  reports such rows as not on the branch instead of failing, so concurrent Task pull requests
  never edit the same file.
- A Task's material is pushed to the dataset when its code is pushed, including for a Task in a
  pull request; the dataset only ever holds material, never code.

## 6. Imported Tasks

A batch converted from another source records, per Task, in `[metadata]`: `source_platform`,
`source_id` (the source's own identifier), a link to the source item, `source_snapshot` (date),
and `conversion_notes`, one line per change made in conversion. The repository root's
`IMPORT.md` lists the batch: each Task, its source id, and whether it is on `main` or in its pull
request with the reason.
