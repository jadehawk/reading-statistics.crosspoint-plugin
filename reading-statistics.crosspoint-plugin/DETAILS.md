# Reading Statistics

An **on-device**, offline statistics dashboard for firmware supporting the required native statistics and dashboard capabilities.

Explore global and individual-book reading time, counted sessions, qualified page turns, a seven-day chart, and a 28-day activity calendar.

The sixth page can preview and import existing CrossInk and vCodex reading history into the firmware's native binary records. Import requires a second confirmation, preserves source files, and uses durable receipts to prevent duplicate imports.

**Requires:** firmware advertising both `stats.native.v1` and `ui.dashboard.v1`. Compatibility depends on capabilities, not firmware branding. **Known compatible firmware:** Razor-Crest builds exposing both capabilities; other firmware providing them may also run this plugin. This plugin does not include a browser interface, network access, or a Web Stats access code.
