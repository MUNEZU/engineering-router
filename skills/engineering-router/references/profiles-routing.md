# Profiles and routing

The root chooses the smallest Codex-native role that satisfies the accepted
contract. A valid handoff or current explicit user instruction takes
precedence over these defaults.

| Role | Model | Effort | Sandbox | Use |
| --- | --- | --- | --- | --- |
| `code_explorer` | `gpt-5.6-luna` | `medium` | `read-only` | Targeted entry-point, call-chain, root-cause, or impact investigation. |
| `code_writer` | `gpt-5.6-luna` | `medium` | `workspace-write` | Clear, local, low-risk implementation with a direct check. |
| `luna_worker` | `gpt-5.6-luna` | `max` | `workspace-write` | Bounded work that needs deeper reasoning but does not cross a protected boundary. |
| `hard_code_writer` | `gpt-6.1-sol` | `high` | `workspace-write` | High-risk, cross-module, architectural, security, migration, concurrency, data-integrity, or public-contract work. |
| `independent_reviewer` | `gpt-6.1-sol` | `high` | `read-only` | Fresh independent review of stable evidence. |
| `expert_advisor` | selected per consultation | selected per consultation | `read-only` | Demanding consultation, modeling, or a high-cost-to-rework decision. |

`expert_advisor.toml` intentionally omits model and effort. For normal
demanding consultation, request `gpt-6.1-sol` with `high` reasoning. For a
decision whose error would be materially expensive to rework, request the
same `gpt-6.1-sol` model with `max` reasoning only when the user or a valid
handoff authorizes the extra usage. Verify the effective runtime model and
effort. Do not continue when the client cannot apply and confirm the request.

For critical consultation or a separate key review, the current user or a
valid handoff may explicitly select `gpt-6-astra`, normally with `medium`
reasoning. Criticality alone does not authorize Astra. Consultation uses the
read-only `expert_advisor`; key review requires a fresh read-only reviewer.
Preserve the role and sandbox when applying an exact-model override. If the
client cannot confirm that combination, report and stop. Astra is never an
automatic fallback.

## Classification

Keep work in the root when it is trivial, mechanical, or safer without a
handoff. Use one child for one bounded question. Add a second concurrent child
only for an independent question with disjoint ownership. Required design or
review coverage is not optional and may exceed the discretionary concurrency
ceiling.

Use `code_writer` only when scope, behavior, and checks are clear and the work
does not affect architecture, authorization, security, migrations, persistent
formats, public contracts, complex concurrency, irreversible actions, or data
integrity. Use `luna_worker` when the same boundaries hold but deeper reasoning
is useful. Route any protected-boundary implementation to `hard_code_writer`.

Use `expert_advisor` to advise, not to implement. It stays read-only even when
the consultation covers architecture or security. Use `independent_reviewer`
for explicit review requests and after high-risk work when the accepted
contract does not already provide a separate review arrangement.

## Plus and service-tier safeguards

No profile requests the Fast service tier. Standard is the default unless the
user or a valid handoff explicitly selects another supported tier and the
runtime confirms it. Keep discretionary concurrency at two to avoid surprising
Plus-plan usage and quota pressure. A child that fails for quota or tier
availability is a reported stop, not authority to switch models or providers.

Local trace token totals are observations of retained files. The dated rate
card in `scripts/usage_by_model.py` produces Standard-credit estimates only;
it cannot detect every mixed-tier event and is not a bill. The account usage
surface in the product is authoritative for limits, resets, and remaining
credits.

Prefer `gpt-6.1-sol`/medium for the root. Retain the three GPT-5.6 Luna profiles unchanged; the two fixed Sol
child profiles use GPT-6.1 Sol/high as shown above. Exclude `gpt-6-sol` and `gpt-6-luna`
from default routes and automatic fallbacks. Quota pressure requires a report,
not a silent root or child model change.

## Optional default sentinel

Codex has a built-in general-purpose `default` agent. Some users install a
personal `default.toml` that refuses omitted or generic dispatches so routing
mistakes are visible. This package neither ships nor installs that sentinel.
A sentinel still creates a child, consumes usage, overrides the built-in
default for its scope, and is not a security boundary. Use it only as an
explicit local customization, keep it outside this package, and restart or
open a new task after changing installed profiles.

## Runtime verification

Parse the installed TOML files, then verify actual child traces. Check role,
exact model, effort, sandbox, parentage, and child depth. A profile on disk,
the requested spawn arguments, or a child's self-report does not prove the
runtime honored the route.
