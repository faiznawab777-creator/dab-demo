import json
import os
import sys
from pathlib import Path

REPORT = "gitleaks-report.json"

if not os.path.exists(REPORT):
    print("No Gitleaks report found.")
    sys.exit(0)

with open(REPORT, encoding="utf-8") as f:
    findings = json.load(f)

if not findings:
    print("✔ No secrets detected.")
    sys.exit(0)

print("\n======================================")
print("   FEATURE STORE SECRET VALIDATION")
print("======================================\n")

for finding in findings:

    rule = finding.get("RuleID", "")
    file = finding.get("File", "")
    line = finding.get("StartLine", "")

    #
    # Friendly messages
    #

    if "password" in rule.lower():
        message = "Hardcoded Password detected."

    elif "api" in rule.lower():
        message = "Hardcoded API Key detected."

    elif "azure" in rule.lower():
        message = "Azure Secret detected."

    elif "token" in rule.lower():
        message = "Hardcoded Token detected."

    else:
        message = "Hardcoded Secret detected."

    #
    # Azure DevOps logging command
    #

    print(
        f"##vso[task.logissue "
        f"type=error;"
        f"sourcepath={file};"
        f"linenumber={line}]"
        f"{message}"
    )

print()

print("Please store secrets in Azure Key Vault or Azure DevOps Variable Groups.")

import json

formatted = []

for finding in findings:

    ...

    formatted.append(
        {
            "file": file,
            "line": line,
            "message": message,
            "type": "SECRET"
        }
    )

report_dir = Path(os.environ.get("SCAN_ROOT", ".")) / "validation" / "reports"
os.makedirs(report_dir, exist_ok=True)
with open(report_dir / "gitleaks_report.json", "w") as f:
    json.dump(formatted,f,indent=2)

print(f"Secrets Found : {len(formatted)}")

sys.exit(0)