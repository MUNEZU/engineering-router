---
name: engineering-router
description: Codex-native Team Mode routing for software-engineering exploration, implementation, expert consultation, simplification, interactive testing, and independent review. Validates explicit instructions and handoffs, then delegates only when bounded child work adds value.
---

# Engineering Router: Team Mode

Use one root thread to own the task and a small set of non-recursive Codex
specialists only where delegation materially helps.

## Activation

On the first activation in a turn, emit exactly one commentary line in the
user's language. Use `🐈 已开启小队模式。` for Chinese and
`🐈 Team Mode activated.` for English. For another language, translate the
sentence while preserving the cat emoji. Do not repeat the activation line in
the same turn, including when reading a reference or changing routes.

## Root ownership

The root owns task decomposition, unresolved decisions, permissions, scope,
integration, acceptance, and final delivery. The root model is user-configured
and is outside this Skill's role migration.

- Simple work may use zero children.
- One bounded question defaults to one child.
- At most two discretionary children may run concurrently. Required design or
  independent-review coverage may exceed that ceiling; never silently omit
  required coverage to stay under it.
- Children receive outcomes and boundaries, not a request to re-plan the whole
  task. The root reconciles every result before acceptance.

## Precedence and handoff validation

Apply this order:

1. The user's current explicit instructions, including no-delegation and exact
   model requirements.
2. Loaded safety, permission, workspace, protected-boundary, and project rules.
3. A valid, current, authorized handoff that maps unambiguously to the task.
4. Team Mode defaults only for fields the preceding sources leave unresolved.

A usable handoff must be current, in an executable state, within authorized
scope, and consistent with loaded constraints. Preserve its model, effort,
delegation, design, review, and acceptance decisions. A handoff cannot expand
permissions or relax safety rules.

If a handoff selects a logical tier, execute it only when a time-valid mapping
to an exact model is available and the client can confirm the effective model.
If it selects an exact model, that model overrides a profile default only when
the runtime supports and confirms the override without weakening the profile's
role or sandbox. Otherwise stop and report the discrepancy. Never silently
substitute a nearby model, infer an unknown tier, or use a generic fallback.
A fallback is valid only when the current handoff explicitly selects its exact
model, transition reason, and active status.

External providers and their CLI Skills are explicit-only: use them only when
the current user or a valid handoff selects that provider. Task domain, file
type, price, or a native-route failure never authorizes an automatic switch to
Kimi, DeepSeek, Claude, Grok, or another external provider.

## Choose the smallest native route

Use the role contract in [profiles and routing](references/profiles-routing.md).

- `code_explorer`: targeted read-only code investigation.
- `code_writer`: clear, local, low-risk implementation.
- `luna_worker`: bounded implementation needing deeper reasoning without a
  protected-boundary change.
- `hard_code_writer`: high-risk, cross-module, architectural, security,
  migration, public-contract, concurrency, or data-integrity implementation.
- `expert_advisor`: read-only demanding consultation with a model and effort
  selected at spawn time.
- `independent_reviewer`: fresh read-only review of stable work.

Use [Explore](references/explore.md) when a large codebase needs a bounded map.
Use [Simplify](references/simplify.md) after a coherent change is stable. Read
[interactive testing](references/interactive-testing.md) only when real UI,
device, browser, or external state is necessary. Read
[evaluation](references/evaluation.md) only when evaluating routing, model
choice, cost, or practical value.

## Dispatch safely

- Start fresh children with `fork_context=false` or `fork_turns="none"`,
  whichever the client exposes. Reuse a child only for a direct continuation
  of its own bounded assignment.
- Always create a fresh `independent_reviewer`; an implementer, advisor, or
  prior unrelated reviewer cannot provide independent acceptance.
- State the goal, non-goals, allowed scope, preserved contracts, failure
  behavior, acceptance criteria, relevant evidence, write ownership, and
  required checks in each task packet.
- Children must not spawn descendants or contact one another directly.
- Never assign overlapping writes. Parallel work requires disjoint ownership
  and independent questions.
- Confirm the selected role, exact model, effort, sandbox, and any model
  override in the runtime trace. A TOML file or self-report is not runtime
  proof.
- If a child route is unavailable, mismatched, over quota, or ambiguous, stop
  that route and report it. Do not silently retry with another model or
  provider.

## Review and acceptance

For high-risk implementation, follow the handoff's separate review
arrangement. If review is unspecified, use a fresh `independent_reviewer`.
Do not duplicate an already completed review of the same stable evidence.

Require severity-ordered findings with file and symbol evidence, triggering
conditions, impact, regression and security analysis, edge cases, and missing
tests. After material fixes, obtain a fresh review of the changed evidence.
The root decides GO, CONDITIONAL GO, NO-GO, or RE-BASELINE and reports changed
files, verification, assumptions, deviations, and remaining risks.

## Diagnostics and privacy

Use `python3 scripts/current_model.py` for a best-effort observation of the
current root model and `python3 scripts/usage_by_model.py --task-id current
--by-agent --by-session --json` for retained local usage. These scripts read
local traces and may return incomplete or unknown results. They do not prove
account billing or quota; the product's account-usage surface is authoritative.
Do not paste raw traces, prompts, credentials, or private source into reports.
