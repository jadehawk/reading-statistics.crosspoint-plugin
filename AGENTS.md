# Reading Statistics plugin agent rules

## Pre-release development policy

The Reading Statistics plugin and its Razor-Crest firmware dashboard integration are experimental, **not official released interfaces**. Do not spend development effort on backwards compatibility with earlier local builds, test plugin packages, or superseded dashboard schemas unless the human explicitly requests it.

- Keep evolving the existing **V1** plugin/dashboard contract in place. Do not invent V2 capability gates or parallel versions simply because an experimental design changes.
- Remove or replace obsolete experimental behavior instead of adding legacy fallbacks, compatibility shims, schema aliases, or migrations for old tests.
- When the current contract changes, update the plugin manifest, `device.json`, relevant documentation, and tests together. Compatibility concerns for previous experimental versions are **not** a reason to retain dead code.
- Keep changes within the Reading Statistics plugin and its requested firmware primitives. Do not modify unrelated upstream or released interfaces.
- Preserve existing user reading-statistics data unless the human explicitly authorizes destructive changes. Protecting stored user data is not an excuse to maintain obsolete UI or API versions.

The human owns firmware flashing, device testing, commits, and publication decisions. Do not commit, push, or create a firmware release without explicit authorization.
