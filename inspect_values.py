import json
import re

INPUT_FILE = r'c:\Users\Will Mecoy\.gemini\antigravity\playground\electric-singularity\data\items_weapon_cleaned.json'

def parse_value(val_str):
    if not isinstance(val_str, str):
        return 0.0
    # Remove units and other non-numeric chars except dot and minus
    # Example: "-1.5m/s" -> "-1.5", "35%" -> "35"
    match = re.search(r'-?\d+(\.\d+)?', val_str)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            return 0.0
    return 0.0

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}")
        return

    found_count = 0
    print("Scanning for properties with value > 0...")
    
    for item in data:
        item_name = item.get('class_name', 'Unknown')
        properties = item.get('properties', {})
        
        for prop_key, prop_obj in properties.items():
            val_raw = prop_obj.get('value')
            if val_raw:
                val_num = parse_value(str(val_raw))
                if val_num > 0:
                    found_count += 1
                    print(f"Item: {item_name} | Prop: {prop_key} | Value: {val_raw}")

    print(f"\nTotal matches found: {found_count}")

if __name__ == "__main__":
    main()
