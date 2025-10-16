import argparse
import sys
import os
from . import transpiler
from . import runtime  # ✅ Required for run_jhand

# Ensure current working directory is on sys.path so relative imports work
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())


def main():
    parser = argparse.ArgumentParser(
        prog="jhand",
        description="🔥 JHAND Language CLI — transpile & run .jhand code like a boss"
    )
    parser.add_argument("file", help="Path to the .jhand file to run")
    parser.add_argument(
        "-t", "--transpile",
        action="store_true",
        help="Sirf transpile karo, run mat karo (Python code print karega)"
    )
    args = parser.parse_args()

    # ✅ Validate file path
    if not os.path.isfile(args.file):
        print(f"❌ File nahi mili: {args.file}")
        sys.exit(1)

    # ✅ Read file with UTF-8 encoding
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as e:
        print(f"❌ File read karte waqt error: {e}")
        sys.exit(1)

    # ✅ Transpile JHAND code into Python code
    py_code = transpiler.transpile(source, source_path=os.path.abspath(args.file))

    if args.transpile:
        print("\n=== 📜 Transpiled Python Code ===")
        print(py_code)
        print("=================================\n")
    else:
        # ✅ Run transpiled code through runtime (with roasting 🥵)
        runtime.run_jhand(py_code, filename=args.file)


if __name__ == "__main__":
    main()
