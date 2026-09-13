#!/usr/bin/env python3
import subprocess
import sys
import argparse

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ Error running command: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def deploy(commit_msg):
    print("📦 Staging updated match files...")
    run_cmd("git add content/brackets/ content/stations/ data/")

    print(f"📝 Creating commit: '{commit_msg}'...")
    run_cmd(f'git commit -m "{commit_msg}"')

    print("🚀 Pushing to main branch (Triggering Netlify deployment)...")
    output = run_cmd("git push origin main")
    print(output)
    print("✅ Successfully pushed! Netlify build initiated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Commit and push match updates to trigger Netlify.")
    parser.add_argument("--message", default="Update tournament match results", help="Git commit message")
    args = parser.parse_args()
    
    deploy(args.message)
