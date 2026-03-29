"""
Adapter for Copilot/VS Code integration with PRP framework.
Mirrors the adapter pattern from prp_runner.py (Claude-centric).
Supports fallback if Copilot CLI is not available.
"""
import subprocess
import sys
import shutil

COPILOT_CLI = shutil.which("copilot")


def run_copilot_command(args):
    if not COPILOT_CLI:
        print("[WARN] Copilot CLI not found. Falling back to manual mode.")
        return manual_fallback(args)
    try:
        result = subprocess.run([COPILOT_CLI] + args, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"[ERROR] Copilot CLI failed: {result.stderr}")
            sys.exit(result.returncode)
    except Exception as e:
        print(f"[ERROR] Exception running Copilot CLI: {e}")
        sys.exit(1)

def manual_fallback(args):
    print("Manual fallback: Please run the following command in your terminal:")
    print("copilot", " ".join(args))
    return 1

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Invoke Copilot for PRP workflows.")
    parser.add_argument("--chat", nargs=argparse.REMAINDER, help="Pass arguments to Copilot Chat")
    args = parser.parse_args()

    if args.chat:
        run_copilot_command(["chat"] + args.chat)
    else:
        print("No Copilot command specified. Use --chat <args>.")
        sys.exit(1)

if __name__ == "__main__":
    main()
