#!/usr/bin/env python3
"""Check taxonomy/mapping.json against taxonomy/tree.json and tasks/, and print node counts.

usage: python3 taxonomy/check.py [--counts]

The mapping is soft: it lives outside the Task folders, so editing it never changes a Task's
source digest, and it names Tasks by folder and nodes by tree id. This check fails on entries
that point at a missing node, malformed rows, or a Task with more than one primary. It reports,
without failing, Tasks that have no primary yet and entries for Tasks not on this branch (a Task
still in its own pull request keeps its placement here, so the pull requests never conflict).
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tree = json.loads((ROOT / "taxonomy/tree.json").read_text())
mapping = json.loads((ROOT / "taxonomy/mapping.json").read_text())

nodes, parent = {}, {}


def walk(node, up=None):
    nodes[node["id"]] = node
    parent[node["id"]] = up
    for child in node.get("children", []):
        walk(child, node["id"])


walk(tree["root"])
# A Task is named by its path under tasks/ ("demo/external_assets", or a single folder name).
tasks = {str(p.parent.relative_to(ROOT / "tasks")) for p in (ROOT / "tasks").rglob("task.toml")
         if "assets" not in p.relative_to(ROOT / "tasks").parts}
errors, primaries, pending = [], Counter(), set()
ROLES, STATUSES, CONFIDENCE = {"primary", "secondary"}, {"proposed", "confirmed", "rejected"}, {"high", "medium", "low"}
if mapping.get("schema") != "ale-taxonomy-mapping@1":
    errors.append("mapping.json: schema must be ale-taxonomy-mapping@1")
for i, row in enumerate(mapping.get("entries", [])):
    where = f"entries[{i}] ({row.get('task')})"
    if row.get("task") not in tasks:
        pending.add(row.get("task"))
    if row.get("node") is not None and row.get("node") not in nodes:
        errors.append(f"{where}: node {row.get('node')!r} is not in tree.json")
    if row.get("role") not in ROLES or row.get("status") not in STATUSES or row.get("confidence") not in CONFIDENCE:
        errors.append(f"{where}: role/status/confidence must be one of {sorted(ROLES)}/{sorted(STATUSES)}/{sorted(CONFIDENCE)}")
    if row.get("role") == "primary" and row.get("status") != "rejected":
        primaries[row.get("task")] += 1
errors += [f"tasks/{t}: {n} primary entries (at most one)" for t, n in primaries.items() if n > 1]
unmapped = sorted(tasks - set(primaries))

if "--counts" in sys.argv:
    members = {}
    for row in mapping["entries"]:
        if row.get("status") == "rejected" or row.get("node") not in nodes or row["task"] not in tasks:
            continue
        node = row["node"]
        while node is not None:  # a Task counts once at its node and every ancestor
            members.setdefault(node, set()).add(row["task"])
            node = parent[node]
    counts = {k: len(v) for k, v in members.items()}
    for node_id, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n:4d}  {node_id}  {nodes[node_id].get('name_en', '')}")

print(f"{len(tasks)} tasks, {len(mapping.get('entries', []))} entries, {len(nodes) - 1} tree nodes; "
      f"{len(unmapped)} tasks without a primary" + (": " + ", ".join(unmapped) if unmapped else ""))
if pending:
    print(f"{len(pending)} mapped tasks are not on this branch (open pull request or removed): " + ", ".join(sorted(pending)))
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
