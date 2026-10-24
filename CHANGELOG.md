# Changelog

## 0.1.6 (release)

- Publish the completed V1 Reading Statistics dashboard with current-book covers, progress bars, All Books, optional history removal and CrossInk/vCodex import.
- Support the capability-gated Reading Statistics sleep-screen source in compatible firmware, including scheduled deep-sleep refresh.
- Preserve existing native reading records; no external service required.

## 0.1.5 (X3/X4Pro test)

- Restored centered page titles beneath the persistent Reading Statistics header, without page counters.
- Renamed the global/lifetime totals page to "Overall Statistics"; retained "Current Book" for per-book totals.
- Removed redundant "Currently Reading" and "Book Summary" labels inside the hero cards.
- Both book heroes use an identical 195-pixel target height with a larger cover and aligned metadata; metric/chart rows share the remaining space.
- Firmware registers the installed plugin as "Reading Statistics" in Custom Wallpaper Collection, rendering a fresh Overall Statistics page at normal sleep entry and at each configured Custom timed wake before returning to deep sleep. This is firmware functionality, requiring no additional plugin payload or network service. The noninteractive
  sleep frame omits its navigation header and button hints, using the extra
  display space for the statistics page.

## 0.1.4 (X3 test)

- Book hero uses an actual cover on the left, with title, author, and series aligned in one right column.
- Raised the percentage label to visually align it with the progress bar.
- Media lookup can use a uniquely matched Home/Recent Books record when older imported history has a different path, recovering cover, author, and completion percentage.
- All Books: hold Select (or long-press a row on touch) to confirm removal of that book's statistics BIN/index entry; original EPUB and lifetime totals are untouched.
- Preserved 0.1.3's in-page All Books list and single experimental V1 dashboard contract.

## 0.1.3 (pre-release test)

- New hero-card and icon-backed statistics layout, with rounded and chamfered borders.
- Seven sharp 80x80 binary PBM icons shipped as runtime assets (809 bytes each).
- Current-book hero reserves full-width lines for the series name and index.
- Uses one pre-release `ui.dashboard.v1` contract; no V2 capability or compatibility shim.
- Fixed hero-card footer crowding, with optional value hiding on the overview.
- Centered card headings and dramatically enlarged icon rendering; icon sources
  remain compact and reusable across devices.
- Moved Current Book to page 2, directly after Your Reading.
- Activity Calendar now starts weeks on Monday and aligns the four-week grid
  with actual weekdays; metric icons keep a consistent size across pages.
- All Books is now a direct cover-thumbnail list with reading time and real completion percentages.
- Both book hero cards show a progress bar and percentage. Removed the redundant page titles.
- Firmware retains covers and last-known percentages even after book deletion; generic cover fallback.
- Import workflow and native statistics snapshots remain unchanged.

## 0.1.1

- Shorter, consistent metric labels, including truthful `Page Turns` and `Avg. / Turn` terminology.
- Current Book metric labels no longer repeat `Book`.
- Works with the updated native dashboard host's centered cards, wrapped metadata, compact charts and book navigation.
- No changes to statistics storage or CrossInk/vCodex import format.

## 0.1.0

- Six-page, capability-gated, offline Reading Statistics dashboard.
- Global and per-book reading metrics, weekly graph and activity calendar.
- Book list, per-book details and touch navigation.
- CrossInk and vCodex import preview and two-step confirmation through Razor-Crest's native BIN import engine.
- Separate repository layout for Plugin Hub-compatible packaging and future release.
