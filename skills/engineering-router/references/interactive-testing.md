# Interactive testing

Read this only when acceptance depends on real UI, browser, device, account,
or external state and code inspection plus automated tests cannot provide a
credible answer.

## Choose the operator

- Give a repeatable, bounded, objectively observable scenario to one writer
  role whose risk boundary matches the task.
- Keep product trade-offs, subjective visual judgment, and final experience
  acceptance in the root.
- Allow only one active operator per browser session, device, account, or
  external environment. Parallelize only across genuinely isolated contexts.
- External-provider automation remains explicit-user-or-valid-handoff only.

## Task packet

Include the user goal and starting state, environment and identity boundary,
minimum necessary actions, observable success and failure criteria, acceptable
tolerance, minimum evidence, and cleanup. Do not disguise exploration as a
fixed script or grant broader permissions than the scenario requires.

## Acceptance

Reuse facts already proved by code and automated checks. If the environment is
unavailable, state is uncertain, or criteria are incomplete, return a clear
blocker instead of guessing. The root inspects the key evidence, confirms
cleanup, and makes final acceptance.
