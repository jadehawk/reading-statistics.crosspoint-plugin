# Reading Statistics — Server Synchronization TODO

> Findings and ideas recorded **2026-11-12**. This is a future-planning document, **not a claim that synchronization has shipped**.

## Current implementation (verified against repositories)

- **Reading Statistics plugin v0.1.8** is a declarative, offline, six-page dashboard (`reading-statistics.crosspoint-plugin/device.json`). It has no networking code. Razor-Crest firmware owns the statistics collector, SD BIN store, import engine, and renderer. It advertises `stats.native.v1` and `ui.dashboard.v1`; stock CrossPoint does not provide this same native historical store.
- Razor-Crest firmware stores `/.crosspoint/reading-stats/global_v2.bin`, per-book `book_<path_hash>_v2.bin`, transaction/recovery markers, a book index, and one-time import receipts. See `src/util/ReadingStatsData.h` and `docs/reading-stats-plugin-architecture.md` in the Razor-Crest repository.
- Each snapshot contains cumulative reading seconds (64-bit), session count, qualified forward page turns, and **366 days** of per-day reading seconds, with a latest-day anchor. There is both a global and a per-book snapshot.
- A qualified forward turn after **2–1800 seconds** of page dwell contributes measured time and a turn; reverse turns/skips are excluded. An active session of at least **10 seconds** is saved; only sessions of **60+ seconds** increment the session count. Untrusted clock time can add to lifetime totals but not to dated buckets.
- Per-book native identity is an **SD path hash**, not a KOSync document hash. Moving a file may create a distinct native record. Book index metadata includes path, title, and author. Progress/cover display is maintained separately from the statistics store.
- Legacy **CrossInk** and **vCodex** import is additive with one-time receipts and confirmation, preserving original files. CrossInk can lack exact dated daily history; vCodex has dated history but not qualified-turn counts. Do not fabricate missing data.

## What matches CrossPoint Sync and Techy-Notes today

| Local field or concept | CrossPoint Sync | Techy-Notes | Conversion or caution |
| --- | --- | --- | --- |
| Cumulative reading seconds | Global/per-book `seconds` | Per-device/book reading seconds | Same unit; use source/lifetime IDs to avoid adding the same data twice |
| Session count | Global/per-book `sessions` | Reading-summary sessions | Compatible *quantity*, not necessarily identical definition across devices |
| Dated reading seconds | Daily stats/snapshots, activity | Dated summary/event analytics | Convert ordinal to calendar date carefully; keep trusted-clock flag |
| Active days / streak | 730-day activity bitmap and streaks | Dated calendar/streaks and Android adapter | Derive from actual dated days; local BIN stores 366 rolling days |
| Per-book total time | Per-book snapshots | Per-book summary/events | Requires reliable book identity mapping |
| Qualified forward turns | `pages` counter has a *different* meaning in some clients | Page events and `pages` totals also have a *different* meaning | **Do not equate** turns with unique EPUB pages or printed-book pages |
| Seconds per turn | Can be derived | Can be derived | Keep as qualified-turn pace, not generic reading speed |
| Day-of-week / time-of-day distributions | Supports day-of-week and time-of-day arrays | Has daily and hourly aggregations | Day-of-week partly derivable from dated totals; **hourly buckets not present** in native BIN |
| Completion/date metadata | Per-book state and timestamps | Document/linked-book status and dates | Native stats alone do not establish all these fields |
| Detailed per-page events | Separate CrossPoint-style session data | Detailed KOReader statistics events | Native BIN aggregates cannot reconstruct individual historical events |

Important: **The Techy-Notes Android compatibility worktree now exposes CrossPoint-compatible global/book counters, dated activity, streaks, and idempotent session checkpoints.** These are existing server primitives, *not* a claim that the current plugin uploads or downloads data. The app's Android streak adaptation also uses meaningful forward progress journal dates (1% floor), separate from measured reading time.

Current source references:
- Plugin: `reading-statistics.crosspoint-plugin/device.json`, `README.md`, `CHANGELOG.md`.
- Razor-Crest firmware: `src/util/ReadingStatsData.h`, `src/util/ReadingStatsBookIndex.h`, `docs/reading-stats-plugin-architecture.md`.
- CrossPoint Sync: `src/models/stats.ts`, `src/models/activity.ts`, `src/routes/v1/stats.ts`.
- Techy-Notes: `src/readingStats.ts`, `src/crosspointCounterStats.ts`, `src/crosspointStatsOverlay.ts`, `src/crosspointMobileCompatibility.ts` (Android compatibility work introduced for server v0.2.0.15).

## Proposed integration stages (not yet approved for implementation)

- [ ] **1. Agree on wire contract and field semantics.** Reuse supported `/api/v1/stats/counters/global`, `/api/v1/stats/counters/books`, and read APIs only if their payloads accurately represent Razor-Crest data; otherwise introduce a versioned `reading-stats.native.v2` capability and an additive adapter. Never silently map qualified turns to print pages or make up `tod`, `dow`, `avg_fwd`, or completion dates.
- [ ] **2. Define stable device identity + reset generation.** Preserve counters across reconnects, reboots, restores, and SD swaps. Use reset-safe counter IDs or equivalent lifetimes, monotonic sequence/high-water marks, and idempotent upserts; prevent an old snapshot from overwriting new counters.
- [ ] **3. Map books safely.** Resolve SD path hashes to the existing KOSync document IDs when known; fall back to user-confirmed title/author/edition matching when ambiguous. Keep unlinked statistics in an account-scoped holding area. Do not merge two editions or two physical books on title alone.
- [ ] **4. Implement opt-in firmware sync, not plugin JavaScript.** Keep the plugin declarative and fully functional offline. A small firmware-side adapter should export local stats and optionally pull remote data when networking is already available, with strict bounded buffers, retry/backoff, and no user-blocking Wi-Fi dialog or battery-draining wakeups. Never require a server to view locally saved statistics.
- [ ] **5. Preserve provenance and avoid duplicate history.** Store each source/device/counter lifetime separately. KOReader events, CrossInk/vCodex imports, CrossPoint counters, and Razor-Crest BIN aggregates may describe **the same physical reading session**. Do not naïvely add everything together without verified overlap rules or shared event IDs. Keep uploaded session checkpoints from being counted twice.
- [ ] **6. Decide on download/restore semantics.** Clarify whether remote history should render as an overlay on the device, import into local BIN, or remain server-only. For destructive replacement/merging, require explicit user action and a rollback/backup plan; do not replay server aggregates as newly measured on-device sessions.
- [ ] **7. Handle retention and dates correctly.** BIN retains 366 daily buckets; CrossPoint's wire format carries a 730-day bitmap; Techy-Notes normalized storage can preserve longer dated histories. Transfer reliable daily seconds when available, preserve historical streak information where legitimate, and do not invent missing days or timestamps. Test timezone/DST and unknown-RTC behavior.
- [ ] **8. Implement privacy and capability controls.** Authenticated per-user/per-device endpoints, server feature gating, bounded batches/pagination, account deletion cleanup, opt-in visibility, and predictable behavior when server support is absent or disabled.
- [ ] **9. Add regression + live testing.** Verify same-snapshot replay, power loss mid-sync, counter reset/restore, moved or renamed EPUB, multiple devices sharing a book, legacy import overlap, >366-day truncation, timezone changes, offline sessions, very large libraries, and corrupt/partial BIN files. Test on X3/X4/X4Pro where available without broad firmware changes.
- [ ] **10. Document UI choices.** Decide what shows “Device Only” vs “Synced”, local vs remote reading time, source provenance, last successful stats upload/download, and how manual removal of statistics affects the server.

## Design principles

1. **Local-first:** offline reading tracking and dashboard must continue regardless of server reachability.
2. **No fabricated metrics:** time, sessions, qualified turns, print pages, reading days, and page positions are distinct concepts.
3. **Minimal firmware impact:** reuse existing collector and BIN store; prefer a narrow, capability-gated transport.
4. **Nondestructive by default:** protect native history, one-time import receipts, and statistics from unrelated devices.
5. **Stage changes separately:** this TODO creates no firmware changes and does not authorize building firmware.

## Android streak issue fixed separately

On 2026-11-12, the Techy-Notes Android compatibility update added a conservative reading-day fallback from existing KOSync `change_journal` uploads: only forward progress reaching at least 1% counts; unchanged/reversed/below-1% syncs do not. Dated activity and the 730-day bitmap/streak share those dates without fabricating reading time or page totals. That fix is **not** a substitute for future upload of the plugin's local measured statistics.
