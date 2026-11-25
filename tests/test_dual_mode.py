"""Regression contract for the unified Reading Statistics plugin."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "reading-statistics.crosspoint-plugin"
TOKEN = "/.crosspoint/reading-statistics-token.json"

class UnifiedReadingStatsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PAYLOAD / "manifest.json").read_text(encoding="utf-8"))
        cls.device = json.loads((PAYLOAD / "device.json").read_text(encoding="utf-8"))

    def test_one_installable_plugin_for_both_modes(self):
        self.assertEqual(self.manifest["name"], "reading-statistics")
        self.assertEqual(self.manifest["version"], "0.6.35")
        self.assertEqual(self.manifest["id"], self.manifest["name"])
        self.assertEqual(self.device["version"], self.manifest["version"])
        self.assertEqual(self.device["dessen"], {"entry": "app.bin"})
        self.assertIn(self.device["dessen"]["entry"], self.manifest["files"])
        self.assertEqual(self.manifest["permissions"]["credentials"]["shared"], [TOKEN])
        self.assertNotIn("compatibility", self.manifest)
        self.assertEqual(self.device["dashboard"]["source"], "reading-stats.v1")
        pages = self.device["dashboard"]["pages"]
        self.assertEqual(len(pages), 7)
        self.assertEqual([p["title"] for p in pages], [
            "Overall Statistics", "Current Book", "Your Week",
            "Reading Calendar", "All Books", "Import Statistics", "Server Sync",
        ])
        self.assertEqual([w["type"] for w in pages[-1]["widgets"]], ["server_sync"])
        self.assertLessEqual((PAYLOAD / "device.json").stat().st_size, 8192)

    def test_persistent_authentication_is_not_inside_plugin_folder(self):
        self.assertEqual(self.device["token"], {
            "file": TOKEN, "path": "token", "persist": True,
        })
        self.assertTrue(TOKEN.startswith("/.crosspoint/"))
        self.assertNotIn("/plugins/", TOKEN)
        self.assertFalse(TOKEN.startswith("/.crosspoint/reading-stats/"))

    def test_server_sync_contract(self):
        self.assertEqual(self.device["auth"]["type"], "device_code")
        self.assertIn("/api/device/code", self.device["auth"]["request"]["url"])
        self.assertIn("/api/device/token", self.device["auth"]["poll"]["url"])
        self.assertIn("{device_code}", self.device["auth"]["poll"]["body"])
        self.assertEqual(self.device["browse"]["page_size"], 8)
        self.assertNotIn("{page}", self.device["browse"]["url"])
        self.assertNotIn("{limit}", self.device["browse"]["url"])
        self.assertTrue(self.device["events"]["reader.session"]["connect"])
        self.assertEqual(
            self.device["events"]["reader.session"]["request"]["headers"]["Authorization"],
            "Bearer {token}",
        )
        sleep = self.device["events"]["sleep.enter"]["download"]
        self.assertEqual(sleep["url"], "https://sync.techy-notes.com/api/device/overview")
        self.assertEqual(sleep["headers"]["Authorization"], "Bearer {token}")
        self.assertEqual(sleep["dest"], "server-overview.json")
        self.assertNotIn("request", self.device["events"]["sleep.enter"])

    def test_published_server_sync_uses_production_endpoints(self):
        production = "https://sync.techy-notes.com"
        self.assertEqual(self.device["auth"]["request"]["url"], production + "/api/device/code")
        self.assertEqual(self.device["auth"]["poll"]["url"], production + "/api/device/token")
        self.assertEqual(self.device["auth"]["display_url"], "sync.techy-notes.com/link")
        self.assertEqual(self.device["browse"]["url"], production + "/api/device/catalog")
        self.assertEqual(self.device["events"]["reader.session"]["request"]["url"], production + "/api/device/sessions")
        self.assertNotIn("sync-beta.techy-notes.com", json.dumps(self.device))

    def test_only_unified_distribution_is_present(self):
        self.assertFalse((ROOT / "companion").exists())
        self.assertFalse((ROOT / "tests" / "test_sync_companion.py").exists())
        self.assertNotIn("companion/", " ".join(self.manifest["files"]))
        self.assertIn(TOKEN, (PAYLOAD / "README.md").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
