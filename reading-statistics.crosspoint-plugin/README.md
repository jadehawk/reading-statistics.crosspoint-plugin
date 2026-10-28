# Reading Statistics

This is an optional **on-device** statistics dashboard. It is declarative;
no code runs from the SD card and no server or Wi-Fi connection is needed.

Install by copying the complete payload, including its `icons/` folder, from the standalone
`reading-statistics.crosspoint-plugin/` payload folder into
`/.crosspoint/plugins/reading-statistics/` on the SD card. In firmware,
enable **Settings > Connectivity > Plugins**, then open
**Home > Plugins > Reading Statistics**. On firmware with Home Menu Buttons support, this plugin also registers an optional **Reading Statistics** Home shortcut. The firmware launches the same native dashboard; if all Home slots are occupied, use **Settings > Display > Home Menu Buttons** to disable another button to make room, then enable Reading Statistics; buttons can also be reordered. Removing the plugin automatically removes the shortcut; no reading history is altered.

Requirements: firmware advertising both `stats.native.v1` and `ui.dashboard.v1`.
Compatibility depends on these capabilities, not the firmware name or version.
Razor-Crest is a known compatible firmware when both are exposed. Firmware without either capability cannot render the dashboard; it may display the README instead.
The `manifest.json` declares both required capabilities so Plugin Hub can filter out unsupported firmware.

`device.json` controls page titles, metric order, labels, and which
generic widgets are displayed. Firmware supplies only the local records
and widget renderer. This host supports `metric`, `week_bars`, `heatmap_28`, `book_list`,
`legacy_import` and a full-width `hero`. `metric` and `hero` widgets can use
custom 80x80 monochrome binary PBM icons in `icons/`, plus `square`, `rounded` or
`chamfered` borders and a 0..16-pixel corner radius. Metric-card titles are centered;
80x80 high-resolution icon sources fill most of the card's available body area
without requiring larger asset files. Optional `icon_size` (1–128) can request
smaller icons; the renderer always clamps icons to card bounds. See the firmware's
`docs/dashboard-cards-v1.md` for the complete reusable card contract.
The first page is titled **Overall Statistics** and shows lifetime/global
reading totals with a featured current-book hero; page two is **Current Book**
and shows per-book totals. All six pages have centered page titles beneath the
Reading Statistics header, without `(n/6)` counters. The hero cards themselves
have no repeated headings and both use the same size. Their enlarged book cover
stays on the left, with title, author, and series/index in one right-hand column;
the progress bar spans the bottom with its percentage vertically aligned.
All Books directly shows cover thumbnails, title, author, reading time, and
completion percentage; selecting a row opens the Current Book detail dashboard.
For imported history with a moved EPUB, only an unambiguous title/author
match recovers the Home cover, author, and progress; statistics stay separate.
Dashboard order: **Overall Statistics → Current Book → Your Week → Activity Calendar → All Books → Import Statistics**.
The Activity Calendar is Monday-first and displays four aligned Monday–Sunday
calendar weeks (with future cells left empty). The seven-day bar chart remains
a rolling seven-day view.

### Custom sleep-screen choice (V1 firmware)

With this plugin installed and the Plugin System enabled, set **Sleep Screen**
to **Custom** and select **Reading Statistics** under **Wallpaper
Collection**. Firmware renders a fresh copy of the first page,
**Overall Statistics**, from current native data as the e-ink sleep image on
each normal sleep entry. No image file, Wi-Fi or external service is involved.
The same V1 page renderer omits the navigation header, Back control and bottom
button hints while retaining the centered Overall Statistics title. **Cover +
Custom** also honors the live source; **Quick Resume** intentionally keeps its
normal behavior. With **Custom** Sleep Screen and **Timed Sleep-Screen
Refresh** enabled, the device wakes on the configured interval, reloads
the current statistics and redraws page one before entering deep sleep
again. No network is needed. This works when the reader is on a charging
stand or on battery (with the battery cost of scheduled wakes). Timed
refresh does not run for Cover + Custom. If the plugin is unavailable,
firmware returns to the normal Custom wallpaper collection.

The sixth **Import Statistics** page previews CrossInk `global_stats.bin`
and vCodex v6 `reading_stats.json`. Select opens the import review screen;
choose CrossInk or vCodex, then **select that same source again** to confirm
the conversion. Back cancels before the second selection. The two source rows
show their complete names and summaries, and the status/confirmation message
wraps below them instead of occupying a truncated third list row. The operation
writes native statistics BIN snapshots only, never legacy source files.

CrossInk imports global counts and per-book EPUB cache counts for books whose
original paths are discoverable through recent books or the native index.
vCodex imports per-book sessions, totals and dated reading days; it has no
qualified page-turn counts, so none are invented. Import is **additive** to
existing native data, with one-time receipts to prevent re-importing the same
source/book even if its file changes later. To prevent possible overlap, only
one legacy firmware source can be imported into a native statistics database.
Use a spare SD card for synthetic fixtures or risky migration tests.

Back exits. Side Up/Down buttons change dashboard pages, including 5→6 and 6→1.
Front Previous/Next change pages except on All Books, where they select book rows.
Confirm refreshes metric pages. On **All Books**, front Previous/Next select
book rows and Confirm opens per-book details. On touch devices, horizontal
swipes change pages, while tapping a row or swiping vertically navigates
books within All Books. Holding Select, or
long-pressing a row on a touch device, displays a cancellation-first confirmation
before removing that book's native reading-statistics BIN record and history
index entry. The EPUB and cumulative global reading totals are not deleted.
Back returns to the same All Books row. Firmware caches a 142px hero
cover and separate 68px list preview under `/.crosspoint/reading-stats/covers/`,
preserving them after the source EPUB is deleted. Native-sized JPEG/PNG covers
use a single Atkinson 1-bit dithering pass, with no second screen-space Bayer
pass. The sleep Cover mode still uses its native grayscale waveform.
Unavailable covers use a generic placeholder; unknown progress is shown as --,
not zero. On Import Statistics, Confirm opens the review/confirmation screen.
Books appear as soon as they successfully open and render, even if previously
removed from All Books. Reopening an erased README.TXT thus recreates the book
list entry with 0m read and no fabricated session counts; qualifying reading
sessions add real time and turns when the reader exits or sleeps. The current
selection uses a light-gray dither, a bold outline, and a dark left marker.
New reading time becomes visible when a qualifying session is saved on
reader exit or sleep.

Notes: Daily charts need a trusted date; otherwise all-time totals
continue accumulating but chart buckets remain blank. Stats tracking
counts qualifying forward turns, not browser/catalog navigation.
