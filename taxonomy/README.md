# Taxonomy and Task placements

An example of the `taxonomy/` folder every Task repository keeps; the rules are in
[CONVENTIONS.md](../CONVENTIONS.md#4-taxonomy-and-placements).

`tree.json` is a small taxonomy of the capabilities this repository's demo Tasks show
(environment, agent behaviour, verification). A domain repository uses its domain's real
taxonomy instead, with `source` naming the page or document it was taken from.

`mapping.json` places each Task, by its path under `tasks/`, on tree nodes. It is kept outside
the Task folders, so changing a placement never changes a Task's code or version. Every Task
has one `primary` row; `demo/external_assets` and `example_task` also show a `secondary` row.
All rows are `proposed`: they are example placements, not confirmed by a domain owner.

```bash
python3 taxonomy/check.py            # Task paths, node ids, one primary per Task, field values
python3 taxonomy/check.py --counts   # Tasks per node, ancestors included
```

A row whose Task is not on the current branch (still in its own pull request) is listed and
left out of the counts instead of failing the check. When the taxonomy itself changes, replace
`tree.json`; `check.py` lists every row whose node no longer exists.
