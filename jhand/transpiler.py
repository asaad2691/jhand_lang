import os
import sys
from .parser import Parser, ASTNode
from .lexer import Lexer


class Transpiler:
    def __init__(self, ast: ASTNode, source_path=None):
        self.ast = ast
        self.lines = []
        self.indent = 0
        self.source_path = source_path

    def transpile(self) -> str:
        self.visit(self.ast)
        return "\n".join(self.lines)

    def emit(self, line: str):
        if line.strip():
            self.lines.append("    " * self.indent + line.strip())
        else:
            self.lines.append("")

    def visit(self, node: ASTNode):
        if node is None:
            return
        method = getattr(self, f"visit_{node.nodetype.lower()}", None)
        if method:
            return method(node)
        for c in node.children:
            self.visit(c)

    # ---------------- IMPORT ----------------
    def visit_import(self, node: ASTNode):
        module = node.value.get("module")
        symbols = node.value.get("symbols", [])
        alias = node.value.get("alias", None)

        def transpile_and_add(py_module_name, jhand_path):
            build_dir = "__jhand_build__"
            os.makedirs(build_dir, exist_ok=True)
            py_out = os.path.join(build_dir, py_module_name + ".py")

            jhand_mtime = os.path.getmtime(jhand_path)
            if not os.path.exists(py_out) or os.path.getmtime(py_out) < jhand_mtime:
                with open(jhand_path, "r", encoding="utf-8") as f:
                    s = f.read()
                py_code = transpile(s, source_path=jhand_path)
                with open(py_out, "w", encoding="utf-8") as f:
                    f.write(py_code)
            if build_dir not in sys.path:
                sys.path.insert(0, build_dir)

        maybe_path = module.replace(".", os.sep) + ".jhand"
        if self.source_path:
            base_dir = os.path.dirname(self.source_path)
            candidate = os.path.join(base_dir, maybe_path)
            if os.path.isfile(candidate):
                py_module_name = (module.replace(".", "_")).lstrip(".")
                transpile_and_add(py_module_name, candidate)

        if symbols:
            parts = []
            for entry in symbols:
                if isinstance(entry, tuple):
                    name, al = entry
                    parts.append(f"{name} as {al}" if al else name)
                else:
                    parts.append(entry)
            self.emit(f"from {module} import {', '.join(parts)}")
        else:
            if alias:
                self.emit(f"import {module} as {alias}")
            else:
                self.emit(f"import {module}")

    def visit_program(self, node: ASTNode):
        for c in node.children:
            self.visit(c)

    def visit_print(self, node: ASTNode):
        self.emit(f"print({node.value})")

    def visit_expr(self, node: ASTNode):
        if node.value:
            self.emit(node.value)

    def visit_function(self, node: ASTNode):
        name = node.value.get("name", "")
        params = node.value.get("params", "")
        is_async = node.value.get("async", False)
        prefix = "async " if is_async else ""
        self.emit(f"{prefix}def {name}({params}):")
        self.indent += 1
        if node.children:
            for c in node.children:
                self.visit(c)
        else:
            self.emit("pass")
        self.indent -= 1

    def visit_class(self, node: ASTNode):
        name = node.value.get("name", "")
        self.emit(f"class {name}:")
        self.indent += 1
        if node.children:
            for c in node.children:
                self.visit(c)
        else:
            self.emit("pass")
        self.indent -= 1

    def visit_block(self, node: ASTNode):
        header = node.value.get("header", "").strip()
        if not header.endswith(":"):
            header += ":"
        self.emit(header)
        self.indent += 1
        for c in node.children:
            self.visit(c)
        self.indent -= 1


# ✅ Module-level transpile function
def transpile(source_code: str, source_path=None) -> str:
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    t = Transpiler(ast, source_path=source_path)
    return t.transpile()
