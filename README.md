# Reading Statistics — CrossPoint Plugin

One **dual-mode Reading Statistics plugin** for CrossPoint and Razor-Crest. Baseline CrossPoint gets optional Techy-Notes reader pairing and measured-session sync (without KOSync or an account); firmware advertising `stats.native.v1` and `ui.dashboard.v2` also gets the full offline native statistics dashboard. Local BIN records, rendering and import are firmware-owned.

## Dashboard preview

[![Five photographed Reading Statistics screens, each showing the entire device](assets/screenshots/reading-statistics-contact-sheet.jpg)](assets/screenshots/reading-statistics-contact-sheet.jpg)

Five real device photos in capture order (oldest first), cropped with the **entire reader and a small black border** intact, and scaled to the same height. Select the contact sheet to enlarge it, or view each photo: [Overall Statistics](assets/screenshots/01-overall-statistics.jpg) · [Current Book](assets/screenshots/02-current-book.jpg) · [Reading Calendar](assets/screenshots/03-reading-calendar.jpg) · [All Books](assets/screenshots/04-all-books.jpg) · [Import Statistics](assets/screenshots/05-import-statistics.jpg). The sixth dashboard page, **Your Week**, is not included in this photo set.

## Installable payload

```text
reading-statistics.crosspoint-plugin/
  manifest.json
  device.json
  README.md
  DETAILS.md
  icons/
    book.pbm
    clock.pbm
    sessions.pbm
    turns.pbm
    calendar.pbm
    bars.pbm
    speed.pbm
```

The installed directory is **`/.crosspoint/plugins/reading-statistics/`** (not the source repository folder name). Put all declared manifest files, including the `icons/` folder, in that directory. The alternative `/plugins/reading-statistics/` location is also supported by compatible firmware.

The plugin is **device-only** (no `plugin.js`). **Baseline CrossPoint:** the standard catalog/device-code UI offers a private server account or anonymous guest pairing, statistics and uploads of `reader.session` events, with no KOSync configuration required. **Razor-Crest with native dashboard support:** the existing six offline pages remain unchanged and a seventh **Server Sync** page opens the same standard catalog/pairing flow. The offline dashboard works without Wi-Fi or a server; sync is optional. Updating the native dashboard to support the seventh page is required before installing this package on Razor-Crest builds with the older six-page renderer.

The dashboard's six original pages use concise labels and a compact grayscale layout. Metric cards can display their own icons, divider lines and rounded or chamfered borders; a featured hero card spans the page width. Overall Statistics removes duplicated Reading Time and Active Days cards, shows compact Sessions/Page Turns cards, and adds a time-of-day chart. Current Book has its own time-of-day breakdown; Your Week uses the latest seven recorded reading days. The firmware records local session-start time buckets in separate small files, so older/imported history remains intact without invented times. Morning is 06:00-11:59, Afternoon 12:00-16:59, Evening 17:00-20:59, and Night 21:00-05:59. The firmware renders the current pre-release V1 dashboard contract. Current Book metadata wraps across lines rather than being forced into a single truncated row. "Page Turns" means qualified forward turns, not unique pages. The seven-day chart ends on the latest recorded reading day. Reading Calendar uses the current device-local month, with numbered, shaded dates and Best Day, Daily Average, and Reading Consistency insights. It uses existing daily readings and does not repeat the old lifetime Active Days metric.

The optional import page accepts CrossInk and vCodex history and uses a two-step confirmation. Originals are preserved, and each legacy source/book is imported at most once. Stock CrossPoint `develop` has no native historical reading-statistics database to migrate; saved book progress cannot reproduce reading duration or session counts. For test fixtures or advanced storage details, see the firmware's `docs/reading-stats-plugin-architecture.md`.

## Server Sync and persistent pairing

The same plugin can upload measured `reader.session` events to Techy-Notes **without KOSync**. Server pairing is optional; the offline dashboard never depends on the server. The production endpoint is `https://sync.techy-notes.com`. Existing beta-only pairing tokens may require re-pairing with production; keep the persistent token file intact.

The pairing credential is now stored at **`/.crosspoint/reading-statistics-token.json`**, outside every plugin-install directory. Uninstalling/reinstalling Reading Statistics does **not** delete this token. The native offline BIN statistics remain under `/.crosspoint/reading-stats/`; that directory is protected and unavailable to ordinary plugins, including stock CrossPoint, so a separate persistent token file is required for dual-mode compatibility. Treat this token as a secret; never upload or publish it.

**Upgrading a previously paired reader:** On Razor-Crest with the updated seven-page renderer, open Reading Statistics once before uninstalling the previous collector. Firmware copies an existing pairing credential to the persistent location only if no new credential exists; it also preserves pending events when their destination is empty. Original files are left untouched. On stock CrossPoint, first copy the older `token.json` (including its JSON `token` field) to the persistent path above, without replacing an existing token. Let queued uploads finish before uninstalling the old collector. Verify the unified plugin shows the same server identity before removing any older installation. Avoid keeping two event collectors installed simultaneously.

## Optional Home shortcut

On firmware exposing `home.shortcuts.v1`, the plugin can register a **Reading Statistics** Home button that opens the native dashboard. Manage visible buttons and free space through **Settings > Display > Home Menu Buttons**. Firmware without this optional shortcut primitive still supports launching from **Home > Plugins** when it exposes the required statistics/dashboard capabilities. Uninstalling the plugin removes its shortcut without deleting reading records.

## Publishing

This repository follows the Plugin Hub standalone-plugin contract. The public GitHub repository, `crosspoint-plugin` topic, and a stable GitHub Release tag matching the version in `manifest.json` make the plugin eligible for automatic catalog discovery. The manifest deliberately does not require native dashboard capabilities, allowing the same package to offer pairing and session sync on baseline CrossPoint. No GitHub access is required for local sideloading.

## Validate locally

```powershell
python tests/test_package.py
```

To build the optional SD-card-root ZIP locally:

```powershell
python tools/package.py
```

The generated archive contains `plugins/reading-statistics/` and is deliberately not committed.
