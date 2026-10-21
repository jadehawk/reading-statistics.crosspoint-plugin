"""Build an SD-root ZIP with exactly the declared installable files."""
import json
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "reading-statistics.crosspoint-plugin"


def make_package() -> Path:
    manifest = json.loads((PAYLOAD / "manifest.json").read_text(encoding="utf-8"))
    plugin_id, version = manifest["name"], manifest["version"]
    if plugin_id != "reading-statistics" or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Unexpected plugin name or version")
    files = manifest["files"]
    if len(files) != len(set(files)) or "manifest.json" not in files or "device.json" not in files:
        raise ValueError("Invalid installable payload")
    output = ROOT / "dist" / f"{plugin_id}-{version}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name in files:
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts or "\\" in name:
                raise ValueError(f"Unsafe runtime file: {name}")
            full = PAYLOAD / relative
            if not full.is_file():
                raise FileNotFoundError(full)
            archive.write(full, f"plugins/{plugin_id}/{name}")
    with ZipFile(output) as archive:
        expected = {f"plugins/{plugin_id}/{name}" for name in files}
        if set(archive.namelist()) != expected:
            raise AssertionError("Unexpected ZIP contents")
    return output


if __name__ == "__main__":
    print(make_package())
