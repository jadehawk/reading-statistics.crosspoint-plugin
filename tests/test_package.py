"""Validate the standalone device-only plugin payload and firmware contract."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "reading-statistics.crosspoint-plugin"
REQUIRED_CAPS = {"stats.native.v1", "ui.dashboard.v1"}
REQUIRED_FILES = {"manifest.json", "device.json", "README.md", "DETAILS.md"} | {
    f"icons/{name}.pbm" for name in ("book", "clock", "sessions", "turns", "calendar", "bars", "speed")
}


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
        self.assertEqual(set(meta["compatibility"]), {"requires"})
        self.assertNotIn("firmware", meta["compatibility"])
        self.assertEqual(set(meta["compatibility"]["requires"]), REQUIRED_CAPS)
        self.assertEqual(set(meta["files"]), REQUIRED_FILES)
        for name in meta["files"]:
            self.assertRegex(name, r"^[A-Za-z0-9._/-]+$")
            self.assertNotIn("..", Path(name).parts)
            self.assertTrue((PLUGIN / name).is_file(), name)

    def test_home_shortcut_contract(self):
        shortcut = self.manifest["home_shortcut"]
        self.assertEqual(shortcut, {"label": "Reading Statistics", "target": "dashboard", "icon": "stats"})
        self.assertEqual(self.device["dashboard"]["source"], "reading-stats.v1")

    def test_dashboard_layout(self):
        doc = self.device
        self.assertEqual(doc["dashboard"]["source"], "reading-stats.v1")
        self.assertEqual(doc["title"], self.manifest["title"])
        pages = doc["dashboard"]["pages"]
        self.assertEqual([p["title"] for p in pages], [
            "Overall Statistics", "Current Book", "Your Week",
            "Activity Calendar", "All Books", "Import Statistics"
        ])
        self.assertTrue(all(0 < len(p["widgets"]) <= 6 for p in pages))
        self.assertEqual([w["type"] for w in pages[4]["widgets"]], ["book_list"])
        self.assertEqual([w["type"] for w in pages[5]["widgets"]], ["legacy_import"])
        self.assertEqual(pages[3]["widgets"][0]["type"], "heatmap_28")
        self.assertEqual(pages[3]["widgets"][0]["label"], "Last 4 Weeks")
        self.assertLessEqual((PLUGIN / "device.json").stat().st_size, 8192)
        known = {"metric", "hero", "reading_snapshot", "week_bars", "heatmap_28", "book_list", "legacy_import"}
        self.assertTrue(all(w["type"] in known for p in pages for w in p["widgets"]))
        self.assertEqual(
            [w.get("label", "") for w in pages[0]["widgets"]],
            ["", "Reading Time", "Sessions", "Page Turns", "Active Days", "Latest 7 Days"]
        )
        self.assertEqual(
            [w.get("label", "") for w in pages[1]["widgets"]],
            ["", "Sessions", "Page Turns", "Active Days", "Avg. / Turn"]
        )
        self.assertTrue(all(w.get("scope") == "current-book" for w in pages[1]["widgets"]))
        self.assertEqual(pages[0]["title"], "Overall Statistics")
        self.assertEqual(pages[1]["title"], "Current Book")
        self.assertNotIn("label", pages[0]["widgets"][0])
        self.assertNotIn("label", pages[1]["widgets"][0])
        self.assertEqual(pages[4]["widgets"][0]["label"], "All Books")
        for page in pages:
            for widget in page["widgets"]:
                if widget.get("field") == "qualified_turns":
                    self.assertEqual(widget["label"], "Page Turns")

    def test_bounded_icon_assets(self):
        icons = {w["icon"] for page in self.device["dashboard"]["pages"]
                 for w in page["widgets"] if "icon" in w}
        self.assertLessEqual(len(icons), 8)
        for name in icons:
            self.assertRegex(name, r"^[a-z0-9_-]{1,32}$")
            self.assertIn(f"icons/{name}.pbm", self.manifest["files"])
        for path in sorted((PLUGIN / "icons").glob("*.pbm")):
            raw = path.read_bytes()
            self.assertEqual(len(raw), 809)
            self.assertTrue(raw.startswith(b"P4\n80 80\n"), path.name)
            self.assertTrue(any(byte != 0 for byte in raw[9:]), path.name)
            self.assertTrue(any(byte != 0xFF for byte in raw[9:]), path.name)

    def test_dashboard_card_contract(self):
        pages = self.device["dashboard"]["pages"]
        self.assertEqual(pages[0]["widgets"][0], {
            "type": "reading_snapshot", "border": "rounded", "corner_radius": 12
        })
        self.assertTrue(all(w.get("scope", "global") == "global" for w in pages[0]["widgets"]))
        self.assertEqual(pages[1]["widgets"][0]["type"], "hero")
        self.assertTrue(pages[1]["widgets"][0].get("show_value", True))
        self.assertEqual([w["type"] for w in pages[0]["widgets"][1:5]], ["metric"] * 4)
        self.assertEqual(set(pages[4]["widgets"][0]), {"type", "label"})
        self.assertTrue(all(w.get("border") in ("rounded", "chamfered")
                            for page in (pages[0], pages[1])
                            for w in page["widgets"] if w["type"] in ("metric", "hero", "reading_snapshot")))

    def test_no_browser_component_or_embedded_data(self):
        self.assertFalse((PLUGIN / "plugin.js").exists())
        self.assertEqual(
            set(f.name for f in PLUGIN.iterdir()),
            {"manifest.json", "device.json", "README.md", "DETAILS.md", "icons"}
        )
        text = (PLUGIN / "README.md").read_text(encoding="utf-8")
        self.assertIn("/.crosspoint/plugins/reading-statistics/", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
