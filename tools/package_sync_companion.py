"""Package the stock CrossPoint Reading Statistics Sync beta companion for SD sideloading."""
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "companion" / "reading-stats-sync"


def make_package() -> Path:
    manifest = json.loads((PAYLOAD / "manifest.json").read_text(encoding="utf-8"))
    plugin_id, version = manifest["name"], manifest["version"]
    if plugin_id != "reading-stats-sync" or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Unexpected companion name/version")
    files = manifest["files"]
    if len(files) != len(set(files)) or not {"manifest.json", "device.json"} <= set(files):
        raise ValueError("Invalid companion payload")
    target = ROOT / "dist" / f"{plugin_id}-{version}-beta.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        for name in files:
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts or "\\" in name:
                raise ValueError(f"Unsafe companion file: {name}")
            full = PAYLOAD / relative
            if not full.is_file():
                raise FileNotFoundError(full)
            archive.write(full, f"plugins/{plugin_id}/{name}")
    with ZipFile(target) as archive:
        if set(archive.namelist()) != {f"plugins/{plugin_id}/{name}" for name in files}:
            raise AssertionError("Unexpected companion ZIP contents")
    return target


if __name__ == "__main__":
    print(make_package())
