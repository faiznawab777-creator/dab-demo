import sys
import pkgutil
import importlib
from utils import get_python_files
from utils import parse_ast
import rules
import os
import json
from pathlib import Path

violations = []
files = get_python_files()

# Automatically discover every rule
REPO_ROOT = Path(os.environ.get("SCAN_ROOT", "."))
REPORT_DIR = REPO_ROOT / "validations" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

loaded_rules = []
#instead of hardcoding the rules, we can dynamically load them from the rules package
for module in pkgutil.iter_modules(rules.__path__):
    loaded_rules.append(importlib.import_module(f"rules.{module.name}"))

print("\nLoaded Rules")
for rule in loaded_rules:
    print(rule.__name__)
print()

for file in files:
    print(f"Scanning {file}")
    try:
        tree = parse_ast(file)
    except Exception as ex:
        violations.append((file,"-",str(ex)))
        continue
    for rule in loaded_rules:
        violations.extend(rule.validate(file, tree))

print()
print("=" * 70)
print(f"Files Scanned : {len(files)}")
print(f"Rules Loaded  : {len(loaded_rules)}")
print(f"Violations    : {len(violations)}")
print("=" * 70)

report = []
for file, line, msg in violations:
    report.append({"file": str(file),"line": line,"message": msg,"type": "AST"} )

with open(REPORT_DIR / "ast_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"\nAST validations Completed ({len(report)} violations)")
sys.exit(0)
