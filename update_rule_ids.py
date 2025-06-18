import os
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_rule_ids_from_dir(directory: Path):
    ids = set()
    for file in directory.glob("*.xml"):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            for rule in root.findall(".//rule"):
                rule_id = rule.get("id")
                if rule_id and rule_id.isdigit():
                    ids.add(int(rule_id))
        except ET.ParseError as e:
            print(f"⚠️ Skipping {file.name} (XML parse error: {e})")
    return ids

def main():
    pr_rules_dir = Path("rules")
    main_rules_dir = Path("main_branch_rules")

    pr_ids = extract_rule_ids_from_dir(pr_rules_dir)
    main_ids = extract_rule_ids_from_dir(main_rules_dir)

    conflicting_ids = pr_ids.intersection(main_ids)

    if conflicting_ids:
        print(f"❌ Conflict! These rule IDs already exist in main: {sorted(conflicting_ids)}")
        exit(1)
    else:
        print("✅ No rule ID conflicts with main branch.")

if __name__ == "__main__":
    main()
