import json
import sys
import os
from pathlib import Path

REPO_ROOT = Path(os.environ.get("SCAN_ROOT", "."))
reports = REPO_ROOT / "validation" / "reports"
ast = []
secret = []

# -------------------------------
# Load AST Report
# -------------------------------
ast_file = reports / "ast_report.json"
if ast_file.exists():
    ast = json.load(open(ast_file))

# -------------------------------
# Load Gitleaks Report
# -------------------------------
secret_file = reports / "gitleaks_report.json"
if secret_file.exists():
    secret = json.load(open(secret_file))

total = len(ast) + len(secret)

print("=" * 69)
print("            FEATURE STORE GOVERNANCE REPORT")
print("=" * 69)

# ============================================================
# Feature Store Validation
# ============================================================

print("\nRule_check Validation will be done for : ")
print("=" * 69)

Rule_check = [
    "No Pandas Usage",
    "No collect()",
    "No toPandas()",
    "No display()",
    "No toLocalIterator()",
    "Python Syntax Validation",
]

print("----------------------------")
for rule in Rule_check:
    print(f"{rule}")

if ast:
    print("Rule Checks Violations Found :")
    print("-" * 69)
    for v in ast:
        message = v["message"].lower()
        # ---------------- Pandas ----------------
        if "pandas" in message:
            rule = "No Pandas Usage"
            recommendation = (
                "Pandas libraries are not permitted in Feature Store production code.\n"
                "Use PySpark DataFrame APIs instead."
            )
        # ---------------- collect() ----------------
        elif "collect()" in message:
            rule = "No collect()"
            recommendation = (
                "collect() retrieves all records from the Spark cluster to the driver node.\n"
                "Use distributed Spark transformations instead."
            )
        # ---------------- toPandas() ----------------
        elif "topandas()" in message:
            rule = "No toPandas()"
            recommendation = (
                "toPandas() converts a distributed Spark DataFrame into a local Pandas DataFrame.\n"
                "Keep processing in Spark instead."
            )
        # --------------- display() ----------------
        elif "display()" in message:
            rule = "No display()"
            recommendation = (
                "display() is a Databricks notebook visualization function intended for "
                "interactive exploration.\n"
                "Remove display() before committing production code."
            )
        # ---------------- toLocalIterator() ----------------
        elif "tolocaliterator()" in message:
            rule = "No toLocalIterator()"
            recommendation = (
                "toLocalIterator() moves Spark data to the driver.\n"
                "Use distributed Spark transformations instead."
            )
        # ---------------- Syntax ----------------
        elif "syntax error" in message:
            rule = "Python Syntax Validation"
            recommendation = (
                "Fix the Python syntax before creating the Pull Request."
            )
        # ---------------- Unknown ----------------
        else:
            rule = "Validation Rule"
            recommendation = (
                "Please review the validation message and update the code."
            )
        print(f"Rule Name : {rule}")
        print(f"Validation Message : {v['message']}")
        print("Recommendation :")
        print(recommendation)
        print(f"File : {v['file']}")
        print(f"Line : {v['line']}")
        print("-" * 69)
else:
    print("Result :")
    print("No Violations of Rules detected.")
# ============================================================
# Security Validation
# ============================================================
print("\nSecurity Validation")
print("=" * 69)

if secret:
    for s in secret:
        print("\nHardcoded Secret Detected\n")
        print("Recommendation :")
        print("Store secrets in Azure Key Vault or Azure DevOps Variable Groups.")
        print()
        print("File :")
        print(s["file"])
        print()
        print("Line :")
        print(s["line"])
        print()
        print("-" * 69)
else:
    print("\nRepository scanned using Gitleaks.\n")
    print("Security Checks Performed")
    print("-------------------------")
    security_check=[
        "API Keys","Hardcoded Passwords","Access Tokens","Azure Storage Keys",
        "Connection Strings","Client Secrets","Private Keys"
    ]
    print("----------------------------")
    print("Security Checks Performed")
    for check in security_check:
        print(f"{check}")

    print("Result :")
    print("No hardcoded secrets detected.")

# ============================================================
# Validation Summary
# ============================================================
print("\n" + "=" * 69)
print("Validation Summary")
print("=" * 69)

files_scanned = len(list((REPO_ROOT / "deployment").rglob("*.py")))
files_scanned += len(list((REPO_ROOT / "training").rglob("*.py")))
files_scanned += len(list((REPO_ROOT / "inference").rglob("*.py")))
files_scanned += len(list((REPO_ROOT / "monitoring").rglob("*.py")))

print()
print(f"Files Scanned       : {files_scanned}")
print("Feature Rules       : 6")
print("Security Rules      : 1")
print(f"Violations Found    : {total}")
print()

if total:
    print("Overall Status      : MERGE FAILED")
else:
    print("Overall Status      : PASSED")

print("\n" + "=" * 69)

if total:
    sys.exit(1)
sys.exit(0)