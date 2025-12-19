#!/usr/bin/env python3
"""
Script to find instance IDs that appear in logs_qwen3-coder-plus but not in patch_diff
"""
import os
from pathlib import Path


def find_missing_ids():
    # Get all log files from logs_qwen3-coder-plus directory
    log_dir = Path("results/logs")
    if not log_dir.exists():
        print(f"Directory {log_dir} does not exist")
        return

    log_files = list(log_dir.glob("*.log"))
    print(f"Found {len(log_files)} log files in logs_qwen3-coder-plus")

    # Extract instance IDs from log filenames (remove .log extension)
    log_instance_ids = set()
    for log_file in log_files:
        instance_id = log_file.name.replace('.log', '')
        log_instance_ids.add(instance_id)

    print(f"Extracted {len(log_instance_ids)} unique instance IDs from logs")

    # Get all patch files from patch_diff directory
    patch_dir = Path("results/patch_diff")
    if not patch_dir.exists():
        print(f"Directory {patch_dir} does not exist")
        return

    patch_files = list(patch_dir.glob("*.patch"))
    print(f"Found {len(patch_files)} patch files in patch_diff")

    # Extract instance IDs from patch filenames (remove .patch extension)
    patch_instance_ids = set()
    for patch_file in patch_files:
        instance_id = patch_file.name.replace('.patch', '')
        patch_instance_ids.add(instance_id)

    print(f"Extracted {len(patch_instance_ids)} unique instance IDs from patches")

    # Find IDs that are in logs but not in patches
    missing_ids = log_instance_ids - patch_instance_ids

    print(f"\nFound {len(missing_ids)} instance IDs that are in logs but not in patches:")
    for missing_id in sorted(missing_ids):
        print(f"  - {missing_id}")

    # Also find IDs that are in patches but not in logs (for completeness)
    extra_ids = patch_instance_ids - log_instance_ids
    print(f"\nFound {len(extra_ids)} instance IDs that are in patches but not in logs:")
    for extra_id in sorted(extra_ids):
        print(f"  - {extra_id}")

    # Save missing IDs to a file
    if missing_ids:
        with open("missing_ids_from_patches.txt", "w") as f:
            for missing_id in sorted(missing_ids):
                f.write(f"{missing_id}\n")
        print(f"\nMissing IDs saved to missing_ids_from_patches.txt")

    return missing_ids


if __name__ == "__main__":
    find_missing_ids()