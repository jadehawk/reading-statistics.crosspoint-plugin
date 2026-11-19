# Reading Statistics Sync (beta)

This optional companion is for **stock CrossPoint** firmware with the `reader.session` plugin event API. It does not replace the richer offline Reading Statistics dashboard on Razor-Crest.

1. Install and open **Reading Statistics Sync** on the reader.
2. Select **Sign in**, scan the QR code to open the mobile-friendly Techy-Notes pairing page with the uppercase XXXX-XXXX code prefilled. You can also type it manually.
3. Select **Continue without account** for an internal guest identity (no username, password or KOSync account), or sign in to your existing KOSync-linked Techy-Notes account and choose **Pair with existing account**. Both require confirmation. The guest's private mobile statistics dashboard is at `/stats`.
4. The reader saves the issued token under its own plugin folder as `token.json` and uploads finished reading sessions at Wi-Fi connections (including sleep, when battery/network permit).

The beta package deliberately targets `https://sync-beta.techy-notes.com`. After pairing, the private `/stats` dashboard shows Today, All-Time, streaks, daily averages, the last 30 days, a calendar heatmap, time-of-day/weekday charts and per-book progress when available. It will not work against the old production server until these endpoints have been deployed. It never needs the reader's KOSync password. New users can collect reading history anonymously with a server-side guest identity. Existing KOSync users can pair to their own account.

The stock event queue is small and can discard old unsent events; it is not a substitute for the Razor-Crest native BIN history. Only measured sessions with a trustworthy clock are sent. If the reader is offline, events remain queued until a later connection (subject to firmware limits).

**Returning to the web portal:** Open the paired plugin to see a fresh **Web Sign-in Code**. Enter that code in the Techy-Notes **Sign in with Reader PIN** form. The one-time code grants a browser session without revealing the device token, and expires after 10 minutes. A guest can later link an existing KOSync account under **Settings → Link existing account**, preserving the guest reading sessions. If the reader and all signed-in browsers are lost before linking, guest-only history may not be recoverable.

**Privacy:** The plugin uploads the hashed document identifier, session ID, active duration, progress and timestamps. To show recognizable book labels like Almanac, it also transmits the book's SD path over HTTPS; the server immediately reduces it to a sanitized filename and never stores the complete path. Uploaded session information stays private behind a one-time reader/browser sign-in; pairing does not automatically publish it. Revoke a paired reader from the server's device list. Removing the plugin folder removes its local token.
