#!/usr/bin/env python3
"""
Script to convert all patch files in patch_diff directory to JSON format
with model_name_or_path set to '111'.
"""
import json
import os
from pathlib import Path


def convert_patch_files_to_json():
    """
    Convert all patch files in the patch_diff directory to JSON format
    similar to pred.json format with fixed model_name_or_path.
    """
    patch_dir = Path("results/patch_diff")

    if not patch_dir.exists():
        print(f"Patch directory {patch_dir} does not exist")
        return

    # Find all .patch files
    patch_files = list(patch_dir.glob("*.patch"))

    if not patch_files:
        print(f"No patch files found in {patch_dir}")
        return

    print(f"Found {len(patch_files)} patch files to convert")

    # Create the output dictionary
    output_data = {}

    for patch_file in patch_files:
        # Extract instance_id from filename (remove .patch extension and 'verified_' prefix if present)
        instance_id = patch_file.name.replace('.patch', '')
        if instance_id.startswith('verified_'):
            instance_id = instance_id[len('verified_'):]

        print(f"Processing {patch_file.name} -> {instance_id}")

        # Read the patch content
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_content = f.read()

        # Add to output data with the required format
        output_data[instance_id] = {
            "model_patch": patch_content,
            "model_name_or_path": "111"
        }

    # Write to output file
    output_file = "converted_pred.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Conversion complete! Output saved to {output_file}")
    print(f"Converted {len(output_data)} patch files.")


if __name__ == "__main__":
    convert_patch_files_to_json()