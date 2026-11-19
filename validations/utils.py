import os
from pathlib import Path
import ast

REPO_ROOT = Path(os.environ.get("SCAN_ROOT", Path(__file__).resolve().parent.parent))
SCAN_FOLDERS = ["src","sql","tests"]

def get_python_files():
    files = []
    for folder in SCAN_FOLDERS:
        path = REPO_ROOT / folder
        if path.exists():
            files.extend(path.rglob("*.py"))
    return files

def clean_source(source):
    cleaned = []
    for line in source.splitlines():
        if line.strip().startswith("%"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def parse_ast(file):
    source = file.read_text(encoding="utf-8")
    source = clean_source(source)
    return ast.parse(source)