# Engineering Router v2

Current version: **2.2.0** (2026-10-06)

Engineering Router is a Codex-native Team Mode Skill. The root thread owns the
task; a small set of non-recursive custom agents handles bounded exploration,
implementation, expert consultation, and independent review when delegation
adds value.

It adapts ideas and diagnostics from
[oil-oil/codex-team-mode](https://github.com/oil-oil/codex-team-mode) while
preserving stricter handoff precedence, exact-model verification, protected
boundaries, explicit-only external providers, read-only consultation, and
independent review.

## Activation

On first activation in a turn, the Skill emits exactly one commentary line in
the user's language:

- Chinese: `🐈 已开启小队模式。`
- English: `🐈 Team Mode activated.`

The line is not repeated during routing, reference loading, or route changes
in the same turn.

## Architecture

The root thread owns decomposition, unresolved decisions, permissions, scope,
integration, and acceptance. Simple tasks may use no children. One bounded
question defaults to one child. Discretionary concurrent fan-out is capped at
two; required design or independent-review coverage is never dropped to meet
that cap.

Fresh children start without inherited turns. Children cannot spawn
descendants, communicate directly, or share overlapping write ownership. A
child is reused only for a direct continuation of its assignment, while every
independent review starts with a fresh reviewer.

External CLI routes are not part of default routing. They require a current
explicit user request or a valid handoff that selects the provider.

## Native role matrix

| Role | Model | Effort | Sandbox | Purpose |
| --- | --- | --- | --- | --- |
| `code_explorer` | `gpt-5.6-luna` | medium | read-only | Targeted code investigation. |
| `code_writer` | `gpt-5.6-luna` | medium | workspace-write | Local, low-risk implementation. |
| `luna_worker` | `gpt-5.6-luna` | max | workspace-write | Bounded deeper implementation. |
| `hard_code_writer` | `gpt-6.1-sol` | high | workspace-write | High-risk or contract-sensitive implementation. |
| `independent_reviewer` | `gpt-6.1-sol` | high | read-only | Fresh independent review. |
| `expert_advisor` | selected per consultation | selected per consultation | read-only | Demanding or high-cost-to-rework consultation. |

`expert_advisor` deliberately has no model or effort in its TOML. Normal
demanding consultation requests `gpt-6.1-sol`/high. High-cost-to-rework
consultation may request `gpt-6.1-sol`/max when the extra usage is explicitly
authorized. The exact runtime model and effort must be verified.

The recommended root default is `gpt-6.1-sol`/medium. The three Luna child
profiles retain GPT-5.6 and their original efforts. The two fixed Sol profiles
use GPT-6.1 Sol/high; advisor selection uses GPT-6.1 Sol/high or explicitly
authorized max.
`gpt-6-sol` and `gpt-6-luna` are excluded from default routing and automatic
fallbacks. Quota pressure never authorizes a silent model change.

For critical architecture decisions or a separate key review, the current
user or a valid handoff may explicitly select `gpt-6-astra`, normally with
medium reasoning. A task being critical alone does not select Astra. Use the
read-only `expert_advisor` for consultation; a key review must use a fresh
read-only reviewer. Verify exact model, effort, and sandbox support before
execution; report and stop if the requested combination cannot be applied.

No profile requests the Fast service tier. The package does not ship or create
a `default.toml` sentinel.

## Install

Do not replace the live files in `~/.codex` while an existing Codex task
or delegated child is still active. Existing processes may retain
old instructions while newly created children discover new profiles, producing
a mixed-version run. Finish or stop active work first, make the backups below,
install the complete release as one change, and then restart Codex or open a
new task.

Back up any existing files with the same names, then copy from a trusted
checkout:

```bash
mkdir -p ~/.codex/skills ~/.codex/agents
mkdir -p ~/.codex/skills/engineering-router
cp -R skills/engineering-router/. ~/.codex/skills/engineering-router/
cp agents/*.toml ~/.codex/agents/
```

Open a new Codex task or restart the app so profile discovery reloads. The
root model remains user-configured; this package does not edit `config.toml`.

Optional `local-overlay/` files are machine-specific and are not distributed
in the public repository. Local overlay tests skip when that directory is
absent. The public Skill does not require an AI Control Plane service.
Review any personal overlays manually; never overwrite a local agreement
blindly or publish machine-specific policy as a generic requirement.

## Upgrade

1. Save copies of the installed `engineering-router` Skill and the six named
   agent profiles.
2. Replace only those files from the new release.
3. Confirm no obsolete design profile remains from an earlier release.
4. Restart or open a new task.
5. Run the full test suite from the release checkout and verify one real child
   trace before relying on routing.

Version 2 replaces the old Sol design-architect profile with the model-free,
read-only `expert_advisor` profile.

## Rollback

Restore the saved Skill directory and named profile files, remove only profile
files that were introduced by the failed upgrade, then restart or open a new
task. Do not restore or delete unrelated agents. A rollback changes files on
disk; verify the effective role, model, effort, and sandbox in a new runtime
trace.

## Diagnostics

From the installed Skill directory:

```bash
python3 scripts/current_model.py
python3 scripts/usage_by_model.py --task-id current --by-agent --by-session --json
```

`current_model.py` is best-effort and returns an explicit unknown status when
local evidence is absent. `usage_by_model.py` reports locally retained token
observations and dated Standard-credit estimates. It can miss unavailable or
ephemeral sessions and cannot prove mixed-tier billing. The product's account
usage view is authoritative for quotas, resets, and remaining credits.

Run validation with Python 3.10 or newer:

```bash
python3 -m unittest discover -s tests -v
```

## Known runtime limitation

The 2026-10-04 desktop smoke test observed parent permission overrides giving
configured read-only children workspace-write permissions, including in a fresh
chat. This model-only update does not resolve that issue. Keep the intended
read-only contract and stop a mismatched route; do not treat instructions alone
as enforced sandbox isolation.

## Privacy and safety

The diagnostics read local Codex JSONL traces. They do not upload data, but
their output can contain task identifiers, paths, role labels, and usage
metadata. Share only the minimum necessary output. Never publish raw traces,
prompts, credentials, private source, or personal data.

A profile file or spawn request is not runtime proof. Confirm the effective
role, exact model, effort, sandbox, parentage, and child depth in the trace.
Unavailable or mismatched routes stop with a report; they do not trigger a
silent model or provider fallback.

## Attribution and license

This package is licensed under the MIT License. It includes adapted material
from `oil-oil/codex-team-mode`; see [NOTICE.md](NOTICE.md) and
[LICENSE](LICENSE).
