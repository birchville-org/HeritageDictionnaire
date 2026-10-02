#!/usr/bin/env python3
"""
Updates portal index.html to Birchville Scholarly Synthesis standard.
Updates local copy /Volumes/SanDisk1TB/proj/myhomarr/portal/index.html
and remote /volume1/docker/traefik/homarr/portal/index.html on synology.local.
"""

import sys
import os
import subprocess
from pathlib import Path

LOCAL_PATH = Path("/Volumes/SanDisk1TB/proj/myhomarr/portal/index.html")

def transform_html(content: str) -> str:
    # 1. Update :root variables
    old_root_block = """        /* Farbpalette übernommen aus payer.birchville.cc (VitePress-Theme) */
        :root {
            --bg: #fcf9f2;
            --bg-alt: #f1eee7;
            --text-1: #03192e;
            --text-2: #1e2d37;
            --text-3: #6b6257;
            --brand-1: #03192e;
            --brand-2: #1e2d37;
            --on-brand: #fcf9f2;
            --border: #d8d2c6;
            --divider: #a1a1a1;
            --header-bg: rgba(252,249,242,.85);
            --up: #15803d;
            --down: #b91c1c;
            --checking: #b45309;
        }"""

    new_root_block = """        /* Farbpalette: Birchville Scholarly Synthesis Standard */
        :root {
            --bg: #fcf9f2;
            --bg-alt: #f1eee7;
            --text-1: #03192e;
            --text-2: #1e2d37;
            --text-3: #6b6257;
            --brand-1: #b45309;
            --brand-2: #92400e;
            --on-brand: #ffffff;
            --border: #d8d2c6;
            --divider: #d8d2c6;
            --header-bg: rgba(252, 249, 242, 0.88);
            --up: #15803d;
            --down: #b91c1c;
            --checking: #b45309;
        }"""

    if old_root_block in content:
        content = content.replace(old_root_block, new_root_block)
    else:
        # Fallback replacement if formatting differs
        content = content.replace("--brand-1: #03192e;", "--brand-1: #b45309;")
        content = content.replace("--brand-2: #1e2d37;", "--brand-2: #92400e;")
        content = content.replace("--on-brand: #fcf9f2;", "--on-brand: #ffffff;")
        content = content.replace("--divider: #a1a1a1;", "--divider: #d8d2c6;")
        content = content.replace("rgba(252,249,242,.85)", "rgba(252, 249, 242, 0.88)")

    # 2. Update .dark block header-bg and divider
    old_dark_block = """        .dark {
            --bg: #0a1628;
            --bg-alt: #0f1e35;
            --text-1: #e8e0d3;
            --text-2: #c4bba5;
            --text-3: #a09080;
            --brand-1: #eab308;
            --brand-2: #ca8a04;
            --on-brand: #0a1628;
            --border: #334155;
            --divider: #334155;
            --header-bg: rgba(10,22,40,.85);
            --up: #4ade80;
            --down: #f87171;
            --checking: #facc15;
        }"""

    new_dark_block = """        .dark {
            --bg: #0a1628;
            --bg-alt: #0f1e35;
            --text-1: #e8e0d3;
            --text-2: #c4bba5;
            --text-3: #a09080;
            --brand-1: #eab308;
            --brand-2: #ca8a04;
            --on-brand: #0a1628;
            --border: #334155;
            --divider: #334155;
            --header-bg: rgba(10, 22, 40, 0.88);
            --up: #4ade80;
            --down: #f87171;
            --checking: #facc15;
        }"""

    if old_dark_block in content:
        content = content.replace(old_dark_block, new_dark_block)
    else:
        content = content.replace("rgba(10,22,40,.85)", "rgba(10, 22, 40, 0.88)")

    # 3. Header backdrop blur: 12px -> 14px
    content = content.replace("backdrop-filter: blur(12px);", "backdrop-filter: blur(14px);")

    # 4. Logo styling
    content = content.replace(
        "header .logo img { height: 36px; width: auto; display: block; }",
        "header .logo img { height: 2.1rem; width: auto; display: block; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18)); }"
    )

    # 5. Button transitions
    content = content.replace(
        "transition: background .2s;",
        "transition: background .2s, color .2s;"
    )

    # 6. Contact button hover
    content = content.replace(
        ".contact-form button:hover { background: var(--brand-2); }",
        ".contact-form button:hover { background: var(--brand-2); color: var(--on-brand); }"
    )

    # 7. Hero subtitle
    content = content.replace(
        "<p>Selbstgehostete Dienste auf eigener Infrastruktur.</p>",
        "<p>Marco's reputable playground for philological texts and services</p>"
    )
    content = content.replace(
        "<p>Selbstgehostete Dienste auf eigener Infrastruktur</p>",
        "<p>Marco's reputable playground for philological texts and services</p>"
    )

    return content

def main():
    print(f"Reading local file: {LOCAL_PATH}")
    if LOCAL_PATH.exists():
        raw = LOCAL_PATH.read_text(encoding="utf-8")
        updated = transform_html(raw)
        LOCAL_PATH.write_text(updated, encoding="utf-8")
        print("Updated local file successfully.")
    else:
        print("Local file not found, will fetch from synology first...")
        fetch_cmd = ["ssh", "marco@synology.local", "cat /volume1/docker/traefik/homarr/portal/index.html"]
        raw = subprocess.check_output(fetch_cmd, text=True)
        updated = transform_html(raw)

    final_content = LOCAL_PATH.read_text(encoding="utf-8") if LOCAL_PATH.exists() else updated

    # 1. Create remote backup on synology
    print("Creating remote backup on synology...")
    subprocess.run([
        "ssh", "marco@synology.local",
        "cp /volume1/docker/traefik/homarr/portal/index.html /volume1/docker/traefik/homarr/portal/index.html.bak-2026-10-02-palette"
    ], check=True)

    # 2. Write new content to remote file via ssh cat
    print("Uploading updated index.html to synology.local...")
    proc = subprocess.run(
        ["ssh", "marco@synology.local", "cat > /volume1/docker/traefik/homarr/portal/index.html"],
        input=final_content,
        text=True,
        capture_output=True
    )
    if proc.returncode != 0:
        print("Error writing to synology:", proc.stderr)
        sys.exit(proc.returncode)

    print("Successfully wrote updated index.html to Synology NAS.")

if __name__ == "__main__":
    main()
