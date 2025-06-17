import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path

RULES_DIR = Path("rules")
RULE_IDS_FILE = Path("rule_ids.json")

def extract_ids_from_xml():
    ids = set()
    for file in RULES_DIR.glob("*.xml"):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            for rule in root.findall(".//rule"):
                rule_id = rule.get("id")
                if rule_id and rule_id.isdigit():
                    ids.add(int(rule_id))
        except ET.ParseError as e:
            print(f"Warning: Skipping {file.name} (XML parse error: {e})")
    return ids

def load_existing_ids():
    if RULE_IDS_FILE.exists():
        with open(RULE_IDS_FILE) as f:
            return set(json.load(f))
    return set()

def save_ids_to_file(all_ids):
    with open(RULE_IDS_FILE, "w") as f:
        json.dump(sorted(all_ids), f, indent=2)

def main():
    new_ids = extract_ids_from_xml()
    existing_ids = load_existing_ids()
    all_ids = new_ids.union(existing_ids)
    save_ids_to_file(all_ids)
    print(f"✅ Updated {RULE_IDS_FILE} with {len(all_ids)} unique rule IDs.")

if __name__ == "__main__":
    main()
