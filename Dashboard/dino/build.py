"""Build Dashboard/site/index.html: Chrome's offline page with the real dino game.

Bundles the Chromium game sources in chromium/ (see fetch_chromium.py) with esbuild,
then inlines the bundle, Chrome's error-page CSS, the original sprite sheets and the
original sound clips into one self-contained page. Needs Node (npx fetches esbuild).

    python build.py
"""
import base64
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "chromium/components/neterror/resources"
INTERSTITIAL = HERE / "chromium/components/security_interstitials/core/common/resources"
OUT = HERE.parent / "site/index.html"
ESBUILD = "esbuild@0.24.0"

# Chrome's two internal modules the game imports, mapped to our stand-ins.
SHIMS = {
    "chrome://resources/js/assert.js": "assert.js",
    "chrome://resources/js/load_time_data.js": "load_time_data.js",
}

# Grit <if expr> flags for desktop Chrome.
GRIT_FLAGS = {"is_ios": False, "is_android": False}


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def grit_ifs(css):
    """Keep or drop <if expr="..."> blocks the way grit does for desktop builds."""
    def keep(m):
        return m.group(2) if eval(m.group(1), {}, dict(GRIT_FLAGS)) else ""
    return re.sub(r'<if expr="([^"]+)">\n?(.*?)</if>\n?', keep, css, flags=re.S)


def bundle():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        game = tmp / "dino_game"
        shutil.copytree(RES / "dino_game", game)
        shutil.copy(RES / "constants.ts", tmp / "constants.ts")
        for src in game.glob("*.ts"):
            text = src.read_text(encoding="utf-8")
            for spec, shim in SHIMS.items():
                text = text.replace(f"'{spec}'", f"'../shims/{shim}'")
            src.write_text(text, encoding="utf-8")
        shutil.copytree(HERE / "shims", tmp / "shims")
        entry = (HERE / "main.js").read_text(encoding="utf-8")
        (tmp / "main.js").write_text(
            entry.replace("./chromium/components/neterror/resources/", "./"), encoding="utf-8")
        leftover = [s for s in game.glob("*.ts") if "from 'chrome://" in s.read_text(encoding="utf-8")]
        assert not leftover, f"unmapped chrome:// imports in {leftover}"
        out = subprocess.run(
            f"npx --yes {ESBUILD} main.js --bundle --minify --format=iife --target=es2020 --legal-comments=none",
            cwd=tmp, shell=True, check=True, capture_output=True, text=True, encoding="utf-8")
        return out.stdout.strip()


def css():
    parts = [
        (INTERSTITIAL / "interstitial_core.css").read_text(encoding="utf-8"),
        (INTERSTITIAL / "interstitial_common.css").read_text(encoding="utf-8"),
        (RES / "neterror.css").read_text(encoding="utf-8"),
    ]
    text = grit_ifs("\n".join(parts))
    for p in (100, 200):
        rel = f"images/default_{p}_percent/offline/{p}-error-offline.png"
        text = text.replace(f"url({rel})", f"url({data_uri(RES / rel, 'image/png')})")
    return text


def main():
    sprite = "images/default_{0}_percent/offline/{0}-offline-sprite.png"
    sound = "sounds/{}.mp3"  # Chrome names them .mp3; they are Ogg Vorbis
    fills = {
        "/*CSS*/": css(),
        "/*JS*/": bundle(),
        "/*SPRITE_1X*/": data_uri(RES / sprite.format(100), "image/png"),
        "/*SPRITE_2X*/": data_uri(RES / sprite.format(200), "image/png"),
        "/*SOUND_PRESS*/": data_uri(RES / sound.format("button-press"), "audio/ogg"),
        "/*SOUND_HIT*/": data_uri(RES / sound.format("hit"), "audio/ogg"),
        "/*SOUND_REACHED*/": data_uri(RES / sound.format("score-reached"), "audio/ogg"),
    }
    page = (HERE / "page.html").read_text(encoding="utf-8")
    for key, value in fills.items():
        assert key in page, key
        page = page.replace(key, value)
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({len(page) // 1024} KB), Chromium {(HERE / 'chromium/REVISION').read_text().strip()[:12]}")


if __name__ == "__main__":
    main()
