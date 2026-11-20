"""Regression contract for one basic/full Reading Statistics plugin and persistent pairing."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "reading-statistics.crosspoint-plugin"
LEGACY = ROOT / "companion" / "reading-stats-sync"
TOKEN = "/.crosspoint/reading-statistics-token.json"


class UnifiedReadingStatsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PAYLOAD / "manifest.json").read_text(encoding="utf-8"))
        cls.device = json.loads((PAYLOAD / "device.json").read_text(encoding="utf-8"))
        cls.legacy = json.loads((LEGACY / "device.json").read_text(encoding="utf-8"))

    def test_one_installable_plugin_for_both_modes(self):
        self.assertEqual(self.manifest["name"], "reading-statistics")
        self.assertEqual(self.manifest["version"], "0.1.11")
        self.assertNotIn("compatibility", self.manifest)
        self.assertEqual(self.device["dashboard"]["source"], "reading-stats.v1")
        pages = self.device["dashboard"]["pages"]
        self.assertEqual(len(pages), 7)
        self.assertEqual([w["type"] for w in pages[-1]["widgets"]], ["server_sync"])
        self.assertEqual(pages[-1]["title"], "Server Sync")
        self.assertLessEqual((PAYLOAD / "device.json").stat().st_size, 8192)

    def test_persisted_token_survives_uninstall_and_matches_all_paths(self):
        self.assertEqual(self.device["token"], {"file": TOKEN, "path": "token", "persist": True})
        self.assertTrue(TOKEN.startswith("/.crosspoint/"))
        self.assertNotIn("/plugins/", TOKEN)
        self.assertFalse(TOKEN.startswith("/.crosspoint/reading-stats/"))
        self.assertEqual(self.legacy["token"]["file"], "token.json")
        self.assertIn("reader.session", self.device["events"])

    def test_network_contract_reuses_stock_companion(self):
        for key in ("auth", "browse", "events"):
            self.assertEqual(self.device[key], self.legacy[key])
        self.assertEqual(self.device["browse"]["page_size"], 8)
        self.assertNotIn("{page}", self.device["browse"]["url"])
        self.assertTrue(self.device["events"]["reader.session"]["connect"])
        self.assertEqual(
            self.device["events"]["reader.session"]["request"]["headers"]["Authorization"],
            "Bearer {token}",
        )

    def test_old_native_dashboard_pages_are_preserved_exactly(self):
        old = json.loads(subprocess.check_output(
            ["git", "show", "HEAD:reading-statistics.crosspoint-plugin/device.json"],
            cwd=ROOT, text=True, encoding="utf-8",
        ))
        self.assertEqual(self.device["dashboard"]["pages"][:6], old["dashboard"]["pages"])

    def test_legacy_companion_remains_available_for_safe_migration(self):
        self.assertTrue((LEGACY / "manifest.json").is_file())
        self.assertNotIn("companion/", " ".join(self.manifest["files"]))
        text = (PAYLOAD / "README.md").read_text(encoding="utf-8")
        self.assertIn(TOKEN, text)
        self.assertIn("reading-stats-sync/token.json", text)


if __name__ == "__main__":
    unittest.main()
