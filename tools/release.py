"""Check and package the portable skill using only the Python standard library."""
from __future__ import annotations

import argparse
import io
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NAME = "hd2d-scene-builder"
TOP_FILES = ("SKILL.md", "README.md", "README.en.md", "LICENSE", "THIRD_PARTY_NOTICES.md", ".gitignore", ".gitattributes")
FOLDERS = ("agents", "references", "assets", "tools")
DEMO_FILES = ("assets/demos/雨港.html", "assets/demos/千里江山.html")
PREVIEW_FILES = ("assets/previews/rain-harbor.gif", "assets/previews/mountains-and-rivers.gif")


def package_files() -> list[Path]:
    files = [ROOT / name for name in TOP_FILES]
    for folder in FOLDERS:
        files.extend(p for p in (ROOT / folder).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    return sorted(files)


class Resources(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.external: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in ("src", "href", "poster", "srcset") and value:
                if not value.startswith(("data:", "#")):
                    self.external.append(f"{tag}.{key}")


def check() -> list[Path]:
    files = package_files()
    required = (*TOP_FILES, "agents/openai.yaml", "references/pixel-art.md",
                "references/lighting-stability.md", "references/water.md",
                "assets/demos/README.md", "assets/demos/licenses/CC0-1.0.txt", *DEMO_FILES,
                *PREVIEW_FILES)
    for relative in required:
        if not (ROOT / relative).is_file():
            raise ValueError(f"Missing required file: {relative}")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or not re.search(r"^name: hd2d-scene-builder$", skill, re.M):
        raise ValueError("Unexpected skill frontmatter or name")
    if "\ndescription:" not in skill.split("\n---", 1)[0]:
        raise ValueError("Missing skill description")
    links = 0
    secret = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
                        r"sk-[A-Za-z0-9]{24,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
    machine = re.compile(r"(?<![A-Za-z])(?:[A-Za-z]:[\\/]|file:/{3}|/(?:Users|home)/)")
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.name.startswith(".env") or path.suffix.lower() in (".pem", ".key"):
            raise ValueError(f"Unexpected private configuration: {relative}")
        if relative in PREVIEW_FILES:
            data = path.read_bytes()
            if (len(data) < 14 or data[:6] not in (b"GIF87a", b"GIF89a")
                    or data[-1:] != b";"):
                raise ValueError(f"Invalid GIF header or trailer: {relative}")
            width = int.from_bytes(data[6:8], "little")
            height = int.from_bytes(data[8:10], "little")
            if not (0 < width <= 4096 and 0 < height <= 4096) or len(data) > 5_000_000:
                raise ValueError(f"Preview dimensions or file size exceed budget: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        if secret.search(text) or machine.search(text):
            raise ValueError(f"Review possible credential or machine path in {relative}")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                parsed = urlsplit(target.strip("<>"))
                if parsed.scheme or not parsed.path:
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                    raise ValueError(f"Broken or external local link in {relative}: {target}")
                links += 1
        if relative in DEMO_FILES:
            scan = Resources()
            scan.feed(text)
            if scan.external or re.search(r"@import\b", text):
                raise ValueError(f"External HTML/CSS resource in {relative}")
            for url in re.findall(r"url\(\s*[\"']?([^\s)\"']+)", text):
                if not url.startswith(("data:", "#")):
                    raise ValueError(f"External CSS resource in {relative}")
            if "Permission is hereby granted" not in text or "three.js authors" not in text:
                raise ValueError(f"Missing embedded third-party license in {relative}")
    print(f"Checked {len(files)} files, {links} local links, 2 GIF previews, and 2 self-contained HTML demos.")
    print("Static checks only; browser rendering and device behavior require runtime testing.")
    return files


def pack(output: Path | None) -> None:
    files = check()
    output = output or ROOT / "dist" / f"{NAME}.zip"
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            entry = zipfile.ZipInfo(f"{NAME}/{path.relative_to(ROOT).as_posix()}",
                                    date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(data) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
        for path in files:
            name = f"{NAME}/{path.relative_to(ROOT).as_posix()}"
            if archive.read(name) != path.read_bytes():
                raise ValueError(f"ZIP content mismatch: {name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data.getvalue())
    print(f"Created {output.name}: {output.stat().st_size:,} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "pack"))
    parser.add_argument("--output", type=Path, help="ZIP output path for pack")
    args = parser.parse_args()
    if args.command == "check":
        check()
    else:
        pack(args.output)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
