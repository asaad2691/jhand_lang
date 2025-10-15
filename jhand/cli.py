import sys
import argparse
from .lexer import Lexer
# Agar parser aur transpiler abhi tak banay nahi to unko skip ya placeholder rakh sakte ho
from .parser import Parser
from .transpiler import Transpiler
from .runtime import run_jhand as run_code  # 👈 yeh naam runtime.py mein hona chahiye

def run_file(path: str, show_translated: bool = False):
    """Run a .jhand source file"""
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    # 🧠 Tokenize
    lexer = Lexer(src)
    tokens = lexer.tokenize()

    # 🧠 Parse
    parser = Parser(tokens)
    ast = parser.parse()

    # 🧠 Transpile to Python
    transp = Transpiler(ast)
    py_code = transp.transpile()

    if show_translated:
        print("\n=== 📜 Translated Python Code ===")
        print(py_code)
        print("=================================\n")

    # 🧠 Run the transpiled Python code
    run_code(py_code, filename=path)


def repl():
    """Interactive REPL shell for Jhand language"""
    print("🤡 Jhand REPL — Type ':q' to quit | ';' to execute buffer | ':t' to toggle translation")
    buffer = []
    show_translation = False

    while True:
        try:
            line = input("jhand> ")
        except (KeyboardInterrupt, EOFError):
            print("\n🚪 Exiting REPL.")
            break

        if line.strip() == ":q":
            break

        elif line.strip() == ":t":
            show_translation = not show_translation
            print("🔄 Translation view:", "ON" if show_translation else "OFF")
            continue

        elif line.strip() == ";":
            src = "\n".join(buffer)
            buffer.clear()

            lexer = Lexer(src)
            tokens = lexer.tokenize()
            ast = Parser(tokens).parse()
            py_code = Transpiler(ast).transpile()

            if show_translation:
                print("\n--- Python ---")
                print(py_code)
                print("-------------\n")

            run_code(py_code)
            continue

        buffer.append(line)


def main():
    ap = argparse.ArgumentParser(prog="jhand", description="🧠 Jhand Language CLI Runner")
    ap.add_argument("file", nargs="?", help="Jhand source file")
    ap.add_argument("-t", "--translate", action="store_true", help="Show translated Python code before execution")
    ap.add_argument("-i", "--repl", action="store_true", help="Start interactive REPL shell")

    args = ap.parse_args()

    if args.repl:
        repl()
        return

    if args.file:
        run_file(args.file, show_translated=args.translate)
        return

    ap.print_help()


if __name__ == "__main__":
    main()
