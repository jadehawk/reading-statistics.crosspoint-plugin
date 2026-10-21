"""Validate the standalone device-only plugin payload and firmware contract."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "reading-statistics.crosspoint-plugin"
REQUIRED_CAPS = {"stats.native.v1", "ui.dashboard.v1"}
REQUIRED_FILES = {"manifest.json", "device.json", "README.md", "DETAILS.md"}


class PluginPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PLUGIN / "manifest.json").read_text(encoding="utf-8"))
        cls.device = json.loads((PLUGIN / "device.json").read_text(encoding="utf-8"))

    def test_manifest_and_discovery(self):
        meta = self.manifest
        self.assertEqual(meta["name"], "reading-statistics")
        self.assertEqual(PLUGIN.name, meta["name"] + ".crosspoint-plugin")
        self.assertRegex(meta["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(meta["compatibility"]["firmware_family"], ["crosspoint"])
        self.assertGreaterEqual(meta["compatibility"]["plugin_api_min"], 1)
        self.assertEqual(set(meta["compatibility"]["requires"]), REQUIRED_CAPS)
        self.assertEqual(set(meta["files"]), REQUIRED_FILES)
        for name in meta["files"]:
            self.assertRegex(name, r"^[A-Za-z0-9._/-]+$")
            self.assertNotIn("..", Path(name).parts)
            self.assertTrue((PLUGIN / name).is_file(), name)

    def test_dashboard_layout(self):
        doc = self.device
        self.assertEqual(doc["dashboard"]["source"], "reading-stats.v1")
        self.assertEqual(doc["title"], self.manifest["title"])
        pages = doc["dashboard"]["pages"]
        self.assertEqual([p["title"] for p in pages], [
            "Your Reading", "Your Week", "Activity Calendar",
            "All Books", "Current Book", "Import Statistics"
        ])
        self.assertTrue(all(0 < len(p["widgets"]) <= 6 for p in pages))
        self.assertEqual([w["type"] for w in pages[3]["widgets"]], ["book_list"])
        self.assertEqual([w["type"] for w in pages[5]["widgets"]], ["legacy_import"])
        self.assertLessEqual((PLUGIN / "device.json").stat().st_size, 8192)
        known = {"metric", "week_bars", "heatmap_28", "book_list", "legacy_import"}
        self.assertTrue(all(w["type"] in known for p in pages for w in p["widgets"]))

    def test_no_browser_component_or_embedded_data(self):
        self.assertFalse((PLUGIN / "plugin.js").exists())
        self.assertEqual(
            set(f.name for f in PLUGIN.iterdir()),
            REQUIRED_FILES
        )
        text = (PLUGIN / "README.md").read_text(encoding="utf-8")
        self.assertIn("/.crosspoint/plugins/reading-statistics/", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
