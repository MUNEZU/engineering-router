# Simplify

Wait until a coherent change is stable. Review changed code and its related
documentation, not the whole repository. If there is no substantive change and
no explicit request to simplify documentation, report that there is nothing to
simplify instead of widening scope.

Use a fresh `independent_reviewer` with a read-only sandbox. One reviewer is
the default. A second concurrent reviewer is justified only for a genuinely
independent lens on broader or riskier work. Keep required acceptance review
distinct when the simplification brief does not include correctness and
omission checks.

Look for unnecessary gates, duplicated rules, fallback chains that hide
failures, stale documentation, oversized responsibilities, needless
abstraction, and avoidable runtime or resource cost. Preserve observable
outputs, errors, ordering, side effects, security checks, trust-boundary
validation, data-loss protection, and accessibility behavior.

The reviewer reports concrete, behavior-preserving opportunities with
locations, reasons, and proposed changes, but edits nothing. The root selects
findings and either applies them or gives one writer exclusive ownership. If
reviewed evidence changes materially, run required checks and obtain a fresh
independent review before acceptance.
