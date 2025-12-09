#!/usr/bin/env python3
"""
Calculate the union of @300.txt and @500.txt files, then subtract IDs that appear in @swebench_names.txt.

The script:
1. Reads @300.txt and @500.txt files
2. Finds the union of their IDs
3. Reads @swebench_names.txt
4. Extracts the relevant IDs from @swebench_names.txt by extracting strings between "sweb.eval.x86_64." and ":latest"
5. Subtracts the swebench_names IDs from the union
6. Outputs the final result
"""

def read_file_lines(filepath):
    """Read all lines from file and return a set of IDs without line numbers."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    ids = set()
    for line in lines:
        # Remove any leading/trailing whitespaces and extract just the ID portion
        clean_line = line.strip()
        # Skip lines that are just numbers (line numbers)
        if clean_line and not clean_line.startswith(' '):
            # Extract just the ID part (without line numbers like "1→")
            parts = clean_line.split('→')
            if len(parts) > 1:
                actual_id = parts[1].strip()
                ids.add(actual_id)
            else:
                actual_id = clean_line.strip()
                ids.add(actual_id)
    return ids

def extract_id_from_swebench_line(line):
    """Extract the ID portion from a swebench_names line like 'sweb.eval.x86_64.ID:latest'."""
    line = line.strip()
    if line.startswith('sweb.eval.x86_64.') and line.endswith(':latest'):
        # Find the start position after 'sweb.eval.x86_64.'
        start_pos = len('sweb.eval.x86_64.')
        # Find the end position before ':latest'
        end_pos = len(line) - len(':latest')
        return line[start_pos:end_pos]
    return None

def main():
    print("Reading 300.txt...")
    set_300 = read_file_lines('/root/hy2/sg/300.txt')
    print(f"Found {len(set_300)} IDs in 300.txt")

    print("Reading 500.txt...")
    set_500 = read_file_lines('/root/hy2/sg/500.txt')
    print(f"Found {len(set_500)} IDs in 500.txt")

    # Union of 300.txt and 500.txt
    union_300_500 = set_300.union(set_500)
    print(f"Union of 300.txt and 500.txt has {len(union_300_500)} unique IDs")

    print("Reading swebench_names.txt...")
    swebench_ids = set()
    with open('/root/hy2/sg/swebench_names.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                extracted_id = extract_id_from_swebench_line(line)
                if extracted_id:
                    swebench_ids.add(extracted_id)
    print(f"Found {len(swebench_ids)} IDs in swebench_names.txt")

    # Subtract swebench_names IDs from the union
    result = union_300_500 - swebench_ids
    print(f"Result (union minus swebench_names) has {len(result)} IDs")

    # Write the result to a file
    output_file = '/root/hy2/sg/result.txt'
    with open(output_file, 'w') as f:
        for id_val in sorted(result):
            f.write(id_val + '\n')

    print(f"Result written to {output_file}")

    # Print the first few and last few results as a sample
    result_list = sorted(list(result))
    if len(result_list) > 10:
        print("Sample of results (first 5):")
        for id_val in result_list[:5]:
            print(f"  {id_val}")
        print("Sample of results (last 5):")
        for id_val in result_list[-5:]:
            print(f"  {id_val}")
    else:
        print("All results:")
        for id_val in result_list:
            print(f"  {id_val}")

if __name__ == "__main__":
    main()