import argparse
import sys
from . import transpiler  # ya jahan tu ne transpiler rakha hai

def main():
    parser = argparse.ArgumentParser(prog="jhand", description="🔥 JHAND Language CLI")
    parser.add_argument("file", help="Path to .jhand file")
    parser.add_argument("-t", "--transpile", action="store_true", help="Sirf transpile karke Python code dikhao")

    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"❌ File nahi mili: {args.file}")
        sys.exit(1)

    # Transpile karo
    py_code = transpiler.transpile(source)

    if args.transpile:
        print("=== 📜 Transpiled Python Code ===")
        print(py_code)
        print("=================================")
    else:
        # Direct execute
        exec(py_code, {})

if __name__ == "__main__":
    main()
