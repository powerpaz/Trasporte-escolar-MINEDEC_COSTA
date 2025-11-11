#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge seguro de dependencias para asegurar Flask y pandas en requirements.txt
Uso:
  python3 merge_requirements.py
Resultado:
  - Crea/actualiza requirements.txt con Flask==3.1.2 y pandas==2.3.3 si faltan.
  - Mantiene el contenido existente sin duplicar líneas.
"""
import io
import os
import re

PINNED = {
    "Flask": "3.1.2",
    "pandas": "2.3.3",
}

REQ = "requirements.txt"

def normalize(line: str) -> str:
    return re.sub(r"\s+", "", line)

def ensure_pinned(lines):
    pkgs = {k.lower() for k in PINNED.keys()}
    present = set()
    out = []
    for line in lines:
        n = normalize(line)
        if not n or n.startswith("#"):
            out.append(line)
            continue
        m = re.match(r"([A-Za-z0-9_\-]+)", n)
        if m:
            name = m.group(1).lower()
            if name in pkgs:
                present.add(name)
        out.append(line)
    for name, ver in PINNED.items():
        if name.lower() not in present:
            out.append(f"{name}=={ver}\n")
    return out

def main():
    if os.path.exists(REQ):
        with io.open(REQ, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []
    new_lines = ensure_pinned(lines)
    with io.open(REQ, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("[OK] requirements.txt verificado/actualizado con dependencias mínimas.")

if __name__ == "__main__":
    main()
