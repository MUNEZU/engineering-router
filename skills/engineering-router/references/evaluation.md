# Evaluate Team Mode

Read this only when the user asks to evaluate routing, model choice, usage,
cost, or practical value.

## Collect evidence

1. Record the task goal, baseline, acceptance checks, and installed role map.
2. Check every child's actual role, exact model, effort, sandbox, parent, and
   depth in runtime traces. TOML files and self-reports are not runtime proof.
3. Judge the returned artifact and root rework against acceptance, not the
   child's confidence.
4. Compare comparable work only. Do not create duplicate work solely to fill a
   benchmark.

Run `python3 scripts/usage_by_model.py --task-id current --by-agent
--by-session --json` for retained local observations. It scans active local
sessions by default; add `--archived-sessions-root <path>` only when the
comparison explicitly needs archived sessions. Separate uncached input,
cached input, output, reasoning output, and estimated Standard credits. Local
traces may be missing, archived, duplicated, or incomplete. The script's rate
card is dated and its credit output is an estimate, not an invoice. Account
limits, reset times, and remaining credits shown by the product are
authoritative.

## Interpret roles

- `code_explorer` is useful when it finds the right primary path and reduces
  root investigation.
- `code_writer` and `luna_worker` are useful when bounded output is accepted
  with low rework and without crossing their protected boundaries.
- `hard_code_writer` is judged on contract preservation, failure paths, tests,
  and the result of separate review.
- `independent_reviewer` should find material issues or document that a
  meaningful risk was checked; no findings is not automatically wasted work.
- `expert_advisor` should contribute an independently grounded decision or
  model. Verify which exact model actually ran before attributing its value.

Compare coordination overhead, local usage, wall-clock effect, missed context,
rework, and final acceptance. Improve routing or task packets before upgrading
every role. Change a lasting profile only when repeated task-scoped evidence
supports it, then update the profile, docs, and tests together.
