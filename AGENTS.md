# Reading Statistics plugin agent rules

## Pre-release development policy

The Reading Statistics plugin and its Razor-Crest firmware dashboard integration are experimental, **not official released interfaces**. Do not spend development effort on backwards compatibility with earlier local builds, test plugin packages, or superseded dashboard schemas unless the human explicitly requests it.

- Keep evolving the existing **V1** plugin/dashboard contract in place. Do not invent V2 capability gates or parallel versions simply because an experimental design changes.
- Remove or replace obsolete experimental behavior instead of adding legacy fallbacks, compatibility shims, schema aliases, or migrations for old tests.
- When the current contract changes, update the plugin manifest, `device.json`, relevant documentation, and tests together. Compatibility concerns for previous experimental versions are **not** a reason to retain dead code.
- Keep changes within the Reading Statistics plugin and its requested firmware primitives. Do not modify unrelated upstream or released interfaces.
- Preserve existing user reading-statistics data unless the human explicitly authorizes destructive changes. Protecting stored user data is not an excuse to maintain obsolete UI or API versions.

The human owns firmware flashing, device testing, commits, and publication decisions. Do not commit, push, or create a firmware release without explicit authorization.

## Independent pre-push review gate

Apply this gate to agent-authored code changes before proposing a merge, pushing a branch or PR, publishing, or declaring the work verified. It adds to, and does not override, this project's own rules or the human's approval requirements.

1. **Implementation pass:** Establish the requested behavior and the current code paths. Make focused changes with tests. Identify the real production entry points, callers and downstream consumers; check the pinned versions of cross-repository dependencies and actual runtime/firmware/server contracts rather than relying on documentation alone.
2. **Skeptical second pass:** After implementation, review the complete diff again as a defect-hunting reviewer, not as its author. Challenge every changed behavior, its assumptions, error handling, compatibility, data integrity, security, resource costs, and effects on callers/consumers. Do not rubber-stamp your own implementation.
3. **Adversarial coverage:** Test the relevant malformed inputs, wrong JSON types, Unicode/numeric conversion, boundary/oversized values, missing files or fields, duplicate identifiers, failure and timeout paths, and state transitions. For embedded systems, check memory/PSRAM constraints and firmware-exposed capabilities when relevant. Test both acceptance and rejection. Use the real consumer's requirements to determine expected results; a passing test that encodes a false assumption is not evidence of correctness.
4. **Verification before delivery:** Run applicable unit and integration suites, linters/static checks and builds (where feasible), then inspect final Git status, full diff and whitespace checks. Confirm any generated assets and documentation match runtime behavior. Record what actually passed, what could not be exercised, and remaining uncertainty. Never claim an integration is tested if only isolated mocks were tested.
5. **Independent external review:** Treat CodeRabbit and other bot/human findings as untrusted hypotheses to verify against current source and real consumers. Correct valid defects and add regressions before requesting another review. Bot approval supplements, but never substitutes for, this pre-push gate. Do not merge or release solely because tests are green; follow the project's explicit authorization and review workflow.
