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
import sys


def resolve_base():
    """Electron partition cache root, per platform.

    Windows: %APPDATA%/hermes/Partitions/<partition>
    macOS:   ~/Library/Application Support/hermes/Partitions/<partition>
    Linux:   $XDG_CONFIG_HOME/hermes/Partitions/<partition> (default ~/.config)
    """
    if sys.platform == "win32":
        return os.path.join(os.environ.get("APPDATA", ""), "hermes", "Partitions", "hermes-browser")
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/hermes/Partitions/hermes-browser")
    return os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        "hermes", "Partitions", "hermes-browser",
    )


BASE = resolve_base()

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


def main():
    results = {}
    for name in TARGETS:
        results[name] = clear_dir_contents(os.path.join(BASE, name))

    # 找不到缓存目录（平台路径解析错误 / 分区未创建）时明确报失败，
    # 避免"已清理"的假成功——插件侧据此显示失败 toast。
    if not os.path.isdir(BASE) or not any(v == "cleared" for v in results.values()):
        print(json.dumps({"ok": False, "error": "no cache directory found", "base": BASE, "results": results}, ensure_ascii=False))
        raise SystemExit(1)

    print(json.dumps({"ok": True, "base": BASE, "results": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
