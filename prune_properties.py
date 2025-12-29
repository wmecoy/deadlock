import json
import os

# Configuration
INPUT_FILE = r'c:\Users\Will Mecoy\.gemini\antigravity\playground\electric-singularity\data\items_weapon.json'
OUTPUT_FILE = r'c:\Users\Will Mecoy\.gemini\antigravity\playground\electric-singularity\data\items_weapon_cleaned.json'

# Whitelist keys (The "Stay" List)
WHITELIST = {
    "value",
    "scale_function",
    "provided_property_type",
    "usage_flags",
    "conditional",
    "disable_value",
    "scaling_stats"
}

def prune_property_object(obj):
    """
    Prunes a property object, keeping only whitelisted keys.
    Returns a new dictionary with preserved keys.
    """
    if not isinstance(obj, dict):
        return obj # Should not happen based on schema, but safety first
    
    new_obj = {}
    for key, value in obj.items():
        if key in WHITELIST:
            # Special handling for 'scale_function': Keep the entire nested object value
            # The prompt says: "scale_function": The entire nested object containing scaling logic.
            # This implies deep preservation for this key's value.
            new_obj[key] = value
        
        # Note regarding Type Inference and Labels:
        # The prompt says: "If a property contains a 'label' ... preserve the property key itself but discard the 'label' field"
        # Since we iterate over keys and only keep WHITELIST, 'label' is automatically discarded.
        # The property key (in the parent dict) is preserved by the caller logic.
            
    return new_obj

def process_items(data):
    """
    Iterates through the list of items and prunes their 'properties' field.
    """
    if not isinstance(data, list):
        print("Error: Root data is not a list.")
        return data

    processed_data = []
    for item in data:
        # Create a shallow copy of the item to modify 'properties'
        new_item = item.copy()
        
        if 'properties' in new_item and isinstance(new_item['properties'], dict):
            original_props = new_item['properties']
            new_props = {}
            for prop_key, prop_val in original_props.items():
                # Prune the property object
                pruned_val = prune_property_object(prop_val)
                # Always preserve the property key, even if the value is empty (per "preserve the property key itself")
                new_props[prop_key] = pruned_val
            
            new_item['properties'] = new_props
        
        processed_data.append(new_item)
    return processed_data

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}")
        return

    print(f"Reading {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    print("Processing items...")
    cleaned_data = process_items(data)
    
    print(f"Writing to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2)
        print("Done.")
    except Exception as e:
        print(f"Error writing JSON: {e}")

if __name__ == "__main__":
    main()
