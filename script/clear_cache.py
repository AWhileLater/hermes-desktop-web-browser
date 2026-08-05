# -*- coding: utf-8 -*-
"""Clear the disk caches of the hermes-desktop-web-browser plugin partition.

Only touches %APPDATA%/hermes/Partitions/hermes-browser/ — the browser
plugin's own Electron session partition. It never touches the Hermes main
app data, other plugins' partitions, bookmarks, or login state (cookies /
IndexedDB / Local Storage are kept).

Locked files (Chromium still holding them) are skipped silently; the
remaining files are deleted. Prints one short JSON line for the plugin.
"""

import json
import os
import shutil

BASE = os.path.join(os.environ.get("APPDATA", ""), "hermes", "Partitions", "hermes-browser")
if not os.path.isdir(BASE):
    # Fallback: derive Roaming from the home dir when APPDATA is missing.
    BASE = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "hermes", "Partitions", "hermes-browser")

# Pure cache directories only — cookies / IndexedDB / Local Storage stay.
TARGETS = ["Cache", "Code Cache", "GPUCache", "DawnGraphiteCache", "DawnWebGPUCache"]


def clear_dir_contents(path):
    """Delete everything inside `path`, keeping the directory itself."""
    if not os.path.isdir(path):
        return "missing"
    for entry in os.listdir(path):
        fp = os.path.join(path, entry)
        try:
            if os.path.isdir(fp) and not os.path.islink(fp):
                shutil.rmtree(fp, ignore_errors=True)
            else:
                try:
                    os.remove(fp)
                except OSError:
                    pass  # locked by the running Chromium — skip
        except OSError:
            pass
    return "cleared"


results = {}
for name in TARGETS:
    results[name] = clear_dir_contents(os.path.join(BASE, name))

print(json.dumps({"ok": True, "base": BASE, "results": results}, ensure_ascii=False))
