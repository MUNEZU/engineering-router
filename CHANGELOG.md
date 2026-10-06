# Changelog

All notable changes to Engineering Router are documented here.

## 2.2.0 - 2026-10-06

- Migrated hard_code_writer and independent_reviewer to GPT-6.1 Sol/high.
- Migrated normal and explicitly authorized Max advisor selections to GPT-6.1 Sol;
  the advisor still omits fixed model/effort and remains configured read-only.
- Left all three GPT-5.6 Luna profiles, the root config, Astra authorization,
  external providers, and sandbox contracts unchanged.
- Added dated GPT-6.1 Sol Standard-credit estimates while retaining historical
  GPT-5.6 rates; estimates are not included Plus allowance accounting.
- Documented the existing desktop read-only sandbox override limitation.

## 2.1.0 - 2026-10-04

- Recommended GPT-6.1 Sol Medium for the root while retaining the five fixed
  GPT-5.6 child profiles and the model-free read-only expert advisor.
- Added explicitly selected GPT-6 Astra Medium for critical consultation or
  separate key review; requires exact-model and sandbox verification.
- Excluded GPT-6 Sol and GPT-6 Luna from default routing and automatic fallback.
- Fixed usage diagnostics to scan active sessions by default and include
  archives only through an explicit `--archived-sessions-root` argument.
- Retained the dated GPT-5.6 credit estimates; other models still report tokens
  without inventing a credit rate.

## 2.0.0 - 2026-09-27

- Consolidated engineering delegation into one Codex-native Team Mode Skill
  named `engineering-router`.
- Standardized every native profile and consultation default on the GPT-5.6
  Luna and Sol family after instruction-following review; GPT-6 is not a
  default route in this release.
- Replaced `sol_design_architect` with model-free, effort-free, read-only
  `expert_advisor` consultation.
- Added exact one-time cat activation, root ownership, two-child discretionary
  fan-out, fresh-context, no-descendant, disjoint-write, and fresh-review rules.
- Preserved valid-handoff precedence, exact-model verification, and
  no-silent-fallback behavior without private paths in the public Skill.
- Adapted Explore, Simplify, Interactive Testing, Evaluation, model detection,
  usage diagnostics, and optional sentinel documentation from Team Mode.
- Disabled automatic external-provider routing and implicit invocation in the
  local external Skill overlays while retaining their CLI workflows.
- Added Plus-plan safeguards, no-Fast defaults, dated Standard-credit estimate
  labeling, authoritative-account-usage guidance, packaging documentation, and
  invariant-focused tests.
