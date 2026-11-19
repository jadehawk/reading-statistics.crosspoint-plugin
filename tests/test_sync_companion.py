"""Compatibility checks for the separate stock CrossPoint stats collector."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "companion" / "reading-stats-sync"


class CompanionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PLUGIN / "manifest.json").read_text(encoding="utf-8"))
        cls.device = json.loads((PLUGIN / "device.json").read_text(encoding="utf-8"))

    def test_is_a_distinct_plugin_and_does_not_require_native_dashboard(self):
        self.assertEqual(self.manifest["name"], "reading-stats-sync")
        self.assertNotIn("stats.native.v1", json.dumps(self.manifest))
        self.assertNotIn("ui.dashboard.v2", json.dumps(self.manifest))
        self.assertLessEqual((PLUGIN / "device.json").stat().st_size, 8192)
        self.assertLessEqual(len(self.manifest["name"]), 23)

    def test_device_code_and_persisted_token(self):
        self.assertEqual(self.device["token"], {"file": "token.json", "path": "token", "persist": True})
        self.assertEqual(self.device["auth"]["type"], "device_code")
        self.assertIn("/api/device/code", self.device["auth"]["request"]["url"])
        self.assertIn("/api/device/token", self.device["auth"]["poll"]["url"])
        self.assertIn("{device_code}", self.device["auth"]["poll"]["body"])
        self.assertIn("/api/device/catalog", self.device["browse"]["url"])
        self.assertIn("XXXX-XXXX", self.device["auth"]["manual_hint"])
        self.assertIn("sync-beta.techy-notes.com/link", self.device["auth"]["display_url"])

    def test_event_uses_auth_and_transmits_book_path_only_to_private_endpoint(self):
        event = self.device["events"]["reader.session"]
        self.assertTrue(event["connect"])
        req = event["request"]
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["headers"]["Authorization"], "Bearer {token}")
        self.assertIn("{event.id}", req["body"])
        self.assertIn("{event.document}", req["body"])
        self.assertIn("{event.book}", req["body"])
        self.assertEqual(json.loads(req["body"])["book"], "{event.book}")
        self.assertIn("/api/device/sessions", req["url"])
        hosts = {part["url"].split("/")[2] for part in (
            self.device["auth"]["request"], self.device["auth"]["poll"],
            self.device["browse"], req)}
        self.assertEqual(hosts, {"sync-beta.techy-notes.com"})

    def test_package_has_exactly_declared_files(self):
        from tools.package_sync_companion import make_package
        zip_path = make_package()
        from zipfile import ZipFile
        with ZipFile(zip_path) as z:
            self.assertEqual(set(z.namelist()), {
                "plugins/reading-stats-sync/" + p for p in self.manifest["files"]
            })


if __name__ == "__main__":
    unittest.main()
