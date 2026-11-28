# Reading Statistics

This is a **Reading Statistics Dessen app** for current Razor-Crest firmware, with a native SD dashboard fallback. Server sync is optional. Version 0.1.14 requires `stats.native.v1` and `ui.dashboard.v2` for Plugin Hub discovery; stock CrossPoint is not yet supported by this release.

Install by copying the complete payload, including its `icons/` folder, from the standalone
`reading-statistics.crosspoint-plugin/` payload folder into
`/.crosspoint/plugins/reading-statistics/` on the SD card. In firmware,
enable **Settings > Connectivity > Plugins**, then open
**Home > Plugins > Reading Statistics**. On firmware with Home Menu Buttons support, this plugin also registers an optional **Reading Statistics** Home shortcut. Razor-Crest opens the Dessen app when the engine is enabled and the app is installed. Firmware with Home shortcuts can otherwise open the native SD dashboard. If all Home slots are occupied, use **Settings > Display > Home Menu Buttons** to disable another button to make room, then enable Reading Statistics; buttons can also be reordered. Removing the plugin automatically removes the shortcut; no reading history is altered.

The **offline dashboard** needs `stats.native.v1` and `ui.dashboard.v2`; the seventh **Server Sync** page requires the updated Razor-Crest native dashboard renderer. The manifest requires both native dashboard capabilities for catalog discovery. Existing stock CrossPoint v0.1.13 installations are unaffected. Existing Razor-Crest firmware limited to six pages must be upgraded before installing this dual-mode release.

The Dessen entry in `device.json` describes the bundled `app.bin`, and `manifest.json` declares its permissions and lists it for installation. v0.1.14 bundles the compact Rust application (83 KiB guest allocation). The SD dashboard and Dessen app share the persistent pairing file. On the updated Razor-Crest firmware, **Upload & refresh** uploads this reader's own JSONL history in resumable batches and refreshes server totals from the receipt. The optional identity grants enable this operation only on capable hosts. The top-level `events_fallback_only` flag prevents the updated firmware from running declarative session and sleep events alongside the Dessen app. Stock CrossPoint ignores the flag and retains SD pairing and measured-session upload. Do not use cumulative upload on older firmware lacking this fallback guard.

On Razor-Crest firmware with Dessen capture support, set the firmware sleep screen to Custom, then turn on **Stats on Sleep** in the Reading Statistics settings. The setting defaults to Off. The app updates its own sleep image after server stats refresh and on unpaired launches. Turning it off restores the firmware's regular wallpaper selection. The app uses generic capture and rename to publish the selected page to `/sleep.bmp`, preserving the original custom image as `/sleep-backup.bmp` and restoring it when disabled.

`device.json` controls page titles, metric order, labels, and which
generic widgets are displayed. Firmware supplies only the local records
and widget renderer. This host supports `metric`, `reading_snapshot`,
`week_bars`, `time_of_day`, `month_calendar`, `month_insights`, `book_list`,
`legacy_import` and a full-width `hero`. `metric` and `hero` widgets can use
custom 80x80 monochrome binary PBM icons in `icons/`, plus `square`, `rounded` or
`chamfered` borders and a 0..16-pixel corner radius. Metric-card titles are centered;
80x80 high-resolution icon sources fill most of the card's available body area
without requiring larger asset files. Optional `icon_size` (1Ã¢â‚¬â€œ128) can request
smaller icons; the renderer always clamps icons to card bounds. See the firmware's
`docs/dashboard-cards-v1.md` for the complete reusable card contract.
The first page is titled **Overall Statistics** and shows a Reading Snapshot:
current calendar-month reading time, consecutive-day streak, active days this
month and count of books with recorded history. The compact Sessions and Page
Turns cards have icon dividers; the Reading Time and Active Days duplicate cards
were removed. A rounded Time of Day panel shows recorded session-start reading
time by morning, afternoon, evening and night, followed by the seven-day chart.
The snapshot is independent of an open book.
If the device date is invalid, calendar-dependent values show -- (the count
of tracked books remains visible). The second page is **Current Book** and
shows per-book totals, using the most recently opened book when no reader
session is active. Current Book also shows its own Time of Day profile, and
Your Week uses the same latest seven recorded reading days as the seven-day bar chart. The buckets are
Morning 06:00-11:59, Afternoon 12:00-16:59, Evening 17:00-20:59, and Night
21:00-05:59; all qualifying seconds belong to the session-start bucket.
Time-of-day collection begins with this firmware update: older reading records
and imported statistics remain intact but cannot be assigned invented hours.
If the local device clock is unreliable, no new time bucket is attributed.
Each interactive page uses its own title in the existing firmware header,
rendered with built-in Noto Sans independently of the active SD theme.
The header's emblem/Back target and clock/battery remain unchanged.
No duplicate title row or `(n/6)` counter is shown; the optional headerless
sleep overview retains its centered page title. The Current Book hero
shows the enlarged cover at left, with title, author and series/index on the
right, and the progress bar and percentage below.
All Books directly shows cover thumbnails, title, author, reading time, and
completion percentage; selecting a row opens the Current Book detail dashboard.
For imported history with a moved EPUB, only an unambiguous title/author
match recovers the Home cover, author, and progress; statistics stay separate.
Dashboard order on updated Razor-Crest: **Overall Statistics Ã¢â€ â€™ Current Book Ã¢â€ â€™ Your Week Ã¢â€ â€™ Reading Calendar Ã¢â€ â€™ All Books Ã¢â€ â€™ Import Statistics Ã¢â€ â€™ Server Sync**.
Reading Calendar displays the current device-local month with numbered Monday-first
dates, four grayscale reading-time levels (none, under 15 minutes, 15Ã¢â‚¬â€œ44 minutes,
45+ minutes), and an outline for today. Future days are never attributed activity.
The monthly insights show the most-read day (duration/date), average reading time
per active day, and the share of elapsed calendar days with reading. If the device
clock is invalid, monthly figures are unavailable rather than inferred from the
last session. The seven-day bar chart remains a rolling seven-day view.

## Server Sync and persistent pairing

The same plugin can upload measured `reader.session` events to Techy-Notes **without KOSync**. Server pairing is optional; the offline dashboard never depends on the server. The production endpoint is `https://sync.techy-notes.com`. Existing beta-only pairing tokens may require re-pairing with production; keep the persistent token file intact.

In SD fallback mode, when a reader is paired, `sleep.enter` also requests one bounded,
read-only account-wide statistics snapshot from Techy-Notes using the same
persistent token. This runs in the firmware's existing background sleep
event-drain path **after the sleep screen is drawn**. The result is atomically
stored as `server-overview.json` inside the installed standard plugin folder,
including if that folder is under `/.crosspoint/plugins`, `/plugins`, or
`/.plugins`. A failed request preserves the last valid copy, and unpaired
readers do not bring up Wi-Fi for this operation. The Dessen app now performs its own pairing and refresh, including on X3/X4 using the firmware's network handoff. It can reuse the cached overview. Automatic refresh is optional and checks a 24-hour freshness window.

The pairing credential is now stored at **`/.crosspoint/reading-statistics-token.json`**, outside every plugin-install directory. Uninstalling/reinstalling Reading Statistics does **not** delete this token. Current Razor-Crest migrates native statistics to `/.crosspoint/reading_sessions.jsonl`; older native SD dashboard hosts own their BIN records under `/.crosspoint/reading-stats/`. The Dessen app reads JSONL history, not legacy BIN records. Treat this token as a secret; never upload or publish it.

**Upgrading a previously paired reader:** On Razor-Crest with the updated seven-page renderer, open Reading Statistics once before uninstalling the previous collector. Firmware copies an existing pairing credential to the persistent location only if no new credential exists; it also preserves pending events when their destination is empty. Original files are left untouched. On stock CrossPoint, first copy the older `token.json` (including its JSON `token` field) to the persistent path above, without replacing an existing token. Let queued uploads finish before uninstalling the old collector. Verify the unified plugin shows the same server identity before removing any older installation. Avoid keeping two event collectors installed simultaneously.

### Legacy native SD dashboard sleep-screen choice (not Dessen)

With this plugin installed and the Plugin System enabled, set **Sleep Screen**
to **Custom** and select **Reading Statistics** under **Wallpaper
Collection**. Firmware renders a fresh copy of the first page,
**Overall Statistics**, from current native data as the e-ink sleep image on
each normal sleep entry. That **image generation** is local and does not
depend on any external service; the optional separate paired-server snapshot
download described above can reuse sleep Wi-Fi independently.
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

Back exits. Side Up/Down buttons change dashboard pages, including 5Ã¢â€ â€™6 and 6Ã¢â€ â€™1.
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
