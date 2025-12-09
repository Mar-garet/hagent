#!/usr/bin/env python3
"""
Batch runner for SGAgent to process unresolved instances from resp.json
"""
import json
import os
import subprocess
from pathlib import Path


def load_unresolved_ids() -> list:
    """Load unresolved IDs from the missing_ids_from_patches.txt file."""
    try:
        with open('missing_ids_from_patches.txt', 'r', encoding='utf-8') as f:
            ids = [line.strip() for line in f if line.strip()]
        return ids
    except FileNotFoundError:
        # If the file doesn't exist, return empty list
        return []


# def _get_project_name_by_instance_id(id: str) -> str:
#     """Extract project name from instance id."""
#     return id.split("__")[0]


# def extract_base_package(name: str) -> str:
#     """Extract base package name from project name."""
#     mapping = {
#         "astropy": "astropy",
#         "matplotlib": "matplotlib",
#         "mwaskom": "seaborn",
#         "pallets": "flask",
#         "psf": "requests",
#         "pydata": "xarray",
#         "sphinx-doc": "sphinx",
#         "scikit-learn": "scikit-learn",
#         "pytest-dev": "pytest",
#         "pylint-dev": "pylint",
#         "django": "django",
#         "sympy": "sympy",
#     }
#     return mapping.get(name, name)


def run_single_instance(instance_id: str) -> dict:
    """Run the main.py script for a single instance ID."""
    print(f"\n{'='*60}")
    print(f"Running for instance: {instance_id}")
    print(f"{'='*60}")

    # Set the environment variables for this specific run
    env = os.environ.copy()
    env['INSTANCE_ID'] = instance_id

    
    env['PROJECT_NAME'] = instance_id

    # Run the main.py script with the specific instance ID using uv run
    try:
        result = subprocess.run([
            'uv', 'run', 'main.py'
        ], env=env, capture_output=False, text=True, timeout=3600)  # 1 hour timeout

        success = result.returncode == 0

        instance_result = {
            'instance_id': instance_id,
            'success': success,
            'return_code': result.returncode,
        }

        print(f"Completed instance: {instance_id}, Success: {success}")
        return instance_result
    except subprocess.TimeoutExpired:
        print(f"Timeout running instance {instance_id}")
        return {
            'instance_id': instance_id,
            'success': False,
            'error': 'Timeout after 1 hour',
            'result': 'Timeout during execution'
        }
    except Exception as e:
        print(f"Error running instance {instance_id}: {str(e)}")
        return {
            'instance_id': instance_id,
            'success': False,
            'error': str(e),
            'result': 'Error during execution'
        }


def run_batch_instances(instance_ids: list):
    """
    Run the main.py script for multiple instance IDs one by one.

    Args:
        instance_ids: List of instance IDs to process
    """
    print(f"Starting batch run for {len(instance_ids)} unresolved instances")
    print("Processing one instance at a time...")

    results = []

    for i, instance_id in enumerate(instance_ids):
        print(f"\nProcessing {i+1}/{len(instance_ids)}: {instance_id}")

        # Run each instance individually by executing main.py
        result = run_single_instance(instance_id)
        results.append(result)

    # Summarize results
    successful = sum(1 for r in results if r.get('success', False))
    failed = len(results) - successful

    print(f"\n{'='*60}")
    print("BATCH RUN SUMMARY")
    print(f"{'='*60}")
    print(f"Total instances: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    return results


def main():
    # Load unresolved IDs
    unresolved_ids = load_unresolved_ids()

    if not unresolved_ids:
        print("No unresolved IDs found in resp.json")
        return

    print(f"Found {len(unresolved_ids)} unresolved instances to process")

    # Ask user for confirmation
    print("\nThis will run 'uv run main.py' for each unresolved instance using INSTANCE_ID and PROJECT_NAME environment variables.")
    print("Do you want to continue? (y/n): ", end="", flush=True)
    response = input().lower().strip()

    if response not in ['y', 'yes']:
        print("Batch run cancelled.")
        return

    # Run batch processing
    results = run_batch_instances(unresolved_ids)

    # Save results
    results_file = "batch_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {results_file}")


if __name__ == "__main__":
    main()