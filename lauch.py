#!/usr/bin/env python3
"""
Script to launch 5 tmux sessions with different API keys and input files.
Each session will run the batch runner with a different p{i}.txt file.

Before running this script:
1. Replace the placeholder API keys below with your actual API keys
2. Create the input files (p1.txt, p2.txt, etc.) with the instance IDs you want to process
"""

import subprocess
import os
import sys
from pathlib import Path

def create_tmux_session(session_name: str, api_key: str, input_file: str):
    """Create a tmux session with the specified API key and input file."""
    print(f"Creating tmux session: {session_name}")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Warning: Input file {input_file} does not exist!")
        return False

    # Set environment variables and run the batch runner in a new tmux session
    shell_cmd = (
        f"export API_KEY={api_key} && "  # 显式 export 环境变量（更易读）
        f"export INPUT_FILE={input_file} && "
        f"python batch_runner.py; "  # 执行脚本
        f"exec bash"  # 保留会话
    )
    
    # 3. 构建 tmux 命令（避免直接拼接，用列表传参）
    cmd = [
        "tmux", "new-session", "-d",
        "-s", session_name,
        "bash", "-c",
        shell_cmd
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Successfully created session: {session_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create session {session_name}: {e}")
        return False

def main():
    # Define the API keys for each session - REPLACE THESE WITH YOUR ACTUAL API KEYS
    api_keys = [
        "sk-153316bbc86262542e784ba7fb4a3a11",  
        "sk-efddd7f104ad2d0d6077dd0124d08502",               
        "sk-1fa3241c020da6b76848ce11823705d0",               
        "sk-c81fd0b7b668a5702bb6395c871eb3da",              
        "sk-2a8c985919317e16de949e2d77c5dbaa"                 
    ]

    # Define the input files for each session
    input_files = [
        "p1.txt",
        "p2.txt",
        "p3.txt",
        "p4.txt",
        "p5.txt"
    ]

    # Check if the input files exist
    missing_files = []
    for file in input_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"The following input files are missing: {missing_files}")
        print("Please create these files before running the script.")
        print("Each file should contain instance IDs you want to process, one per line.")
        return 1

    # Check if tmux is installed
    if not subprocess.run(["which", "tmux"], capture_output=True).returncode == 0:
        print("Error: tmux is not installed or not in PATH")
        return 1

    print("Starting 5 tmux sessions with different API keys and input files...")
    print("Make sure to replace the placeholder API keys in this script with your actual API keys!")
    print()

    successful = 0
    for i in range(5):
        session_name = f"fr_{i+1}"
        if create_tmux_session(session_name, api_keys[i], input_files[i]):
            successful += 1

    print(f"\nCreated {successful}/5 tmux sessions successfully")
    print("\nTo attach to a session: tmux attach -t fr_X")
    print("To list all sessions: tmux ls")
    print("To kill a session: tmux kill-session -t fr_X")
    print("\nNote: Each session is running in the current directory and will use the API_KEY")
    print("      environment variable and the INPUT_FILE environment variable to determine")
    print("      which instances to process.")

    return 0 if successful == 5 else 1

if __name__ == "__main__":
    sys.exit(main())