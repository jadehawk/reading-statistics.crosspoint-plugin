# Reading Statistics Sync (beta)

This optional companion is for **stock CrossPoint** firmware with the `reader.session` plugin event API. It does not replace the richer offline Reading Statistics dashboard on Razor-Crest.

1. Install and open **Reading Statistics Sync** on the reader.
2. Select **Sign in**, scan the QR code to open the mobile-friendly Techy-Notes pairing page with the uppercase XXXX-XXXX code prefilled. You can also type it manually.
3. Select **Continue without account** to start reading as a guest, or sign in to your existing Techy-Notes account and choose **Pair with existing account**. Both require confirmation.
4. The reader saves the issued token under its own plugin folder as `token.json` and uploads finished reading sessions at Wi-Fi connections (including sleep, when battery/network permit).

The beta package deliberately targets `https://sync-beta.techy-notes.com`. It will not work against the old production server until these endpoints have been deployed. It never needs the reader's KOSync password. New users can collect reading history anonymously with a server-side guest identity. Existing KOSync users can pair to their own account.

The stock event queue is small and can discard old unsent events; it is not a substitute for the Razor-Crest native BIN history. Only measured sessions with a trustworthy clock are sent. If the reader is offline, events remain queued until a later connection (subject to firmware limits).

**Returning to the web portal:** Open the paired plugin to see a fresh **Web Sign-in Code**. Enter that code in the Techy-Notes **Sign in with Reader PIN** form. The one-time code grants a browser session without revealing the device token, and expires after 10 minutes. A guest can later link an existing KOSync account under **Settings → Link existing account**, preserving the guest reading sessions. If the reader and all signed-in browsers are lost before linking, guest-only history may not be recoverable.

**Privacy:** The plugin uploads the hashed document identifier, session ID, active duration, progress and timestamps. It does not transmit full book paths. Disconnect the reader at the server's `/link` page. Removing the plugin also removes its local token when deleting the folder.
