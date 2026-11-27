# Reading Statistics

One **dual-mode Reading Statistics plugin**: Dessen firmware runs the bundled statistics application, stock CrossPoint receives optional Techy-Notes reading-session sync, and compatible native-dashboard firmware retains the SD offline dashboard with a Server Sync page.

Explore global and individual-book reading time, counted sessions, qualified page turns, time-of-day patterns, a seven-day chart, and a numbered monthly Reading Calendar with Best Day, Daily Average, and Reading Consistency insights.

The sixth page can preview and import existing CrossInk and vCodex reading history into the firmware's native binary records. Import requires a second confirmation, preserves source files, and uses durable receipts to prevent duplicate imports.

**Basic mode:** supported by stock CrossPoint's device-code, catalog and `reader.session` plugin APIs. No KOSync configuration or Techy-Notes account is required. **Full mode:** requires `stats.native.v1`, `ui.dashboard.v2`, and firmware with the seventh Server Sync page implemented. Local statistics remain offline. A durable pairing credential outside the installed plugin folder survives uninstall/reinstall. Server sync is opt-in and targets the production Techy-Notes server. Dessen mode on updated Razor-Crest supports batched cumulative history upload and refresh, with declarative event synchronization reserved for fallback mode.
