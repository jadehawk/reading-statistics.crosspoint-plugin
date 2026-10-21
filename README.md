# Reading Statistics — CrossPoint Plugin

An optional **offline, on-reader** Reading Statistics dashboard for Razor-Crest. This repository holds the separately installable plugin payload. The firmware owns the native BIN statistics store and import engine; the plugin defines the dashboard's six pages, metric labels and widgets.

## Installable payload

```text
reading-statistics.crosspoint-plugin/
  manifest.json
  device.json
  README.md
  DETAILS.md
```

The installed directory is **`/.crosspoint/plugins/reading-statistics/`** (not the source repository folder name). Put all four files directly in that directory. The alternative `/plugins/reading-statistics/` location is also supported by compatible firmware.

The plugin is **device-only**. It has no `plugin.js`, does not require Wi-Fi or an account, and does not expose local reading records through a browser. The six-page native dashboard is available only when firmware advertises **`stats.native.v1`** and **`ui.dashboard.v1`**.

The optional import page accepts CrossInk and vCodex history and uses a two-step confirmation. Originals are preserved, and each legacy source/book is imported at most once. For test fixtures or advanced storage details, see the firmware's `docs/reading-stats-plugin-architecture.md`.

## Publishing (not yet released)

This repository uses the Plugin Hub standalone-plugin contract. Once hosted publicly and released with a stable `v0.1.0` GitHub Release matching `manifest.json`, it can be discovered by Plugin Hub (prefer the GitHub `crosspoint-plugin` topic). The capability requirements in the manifest prevent installation on unsupported firmware. No release or remote push is required for local sideloading.

## Validate locally

```powershell
python tests/test_package.py
```

To build the optional SD-card-root ZIP locally:

```powershell
python tools/package.py
```

The generated archive contains `plugins/reading-statistics/` and is deliberately not committed.
