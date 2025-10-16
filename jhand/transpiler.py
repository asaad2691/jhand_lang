from .parser import ASTNode, Parser
from .lexer import Lexer  # ✅ sahi import

class Transpiler:
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.lines = []
        self.indent = 0

    # High-level: start transpiling
    def transpile(self) -> str:
        self.visit(self.ast)
        return "\n".join(self.lines)

    # Helper to emit code lines with proper indentation
    def emit(self, line: str):
        if line.strip():
            self.lines.append("    " * self.indent + line.strip())
        else:
            self.lines.append("")

    # Dispatcher: visit node by nodetype
    def visit(self, node: ASTNode):
        if node is None:
            return
        method = getattr(self, f"visit_{node.nodetype.lower()}", None)
        if method:
            return method(node)
        for c in node.children:
            self.visit(c)

    # ---------------- Program ----------------
    def visit_program(self, node: ASTNode):
        for c in node.children:
            self.visit(c)

    # ---------------- Print ----------------
    def visit_print(self, node: ASTNode):
        self.emit(f"print({node.value})")

    # ---------------- Expression ----------------
    def visit_expr(self, node: ASTNode):
        if node.value:
            self.emit(node.value)

    # ---------------- Function ----------------
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

    # ---------------- Class ----------------
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

    # ---------------- Block ----------------
    def visit_block(self, node: ASTNode):
        header = node.value.get("header", "").strip()

        if header.startswith("koshish"):
            self.emit("try:")
            self.indent += 1
        elif header.startswith("phaansi"):
            rest = header[len("phaansi"):].strip()
            self.indent -= 1  # exit previous try
            self.emit(f"except {rest}:" if rest else "except:")
            self.indent += 1
        elif header.startswith("aakhir"):
            self.indent -= 1  # exit previous except
            self.emit("finally:")
            self.indent += 1
        elif header.startswith("jabtak"):
            self.emit("while True:")
            self.indent += 1
        elif header.startswith("with"):
            if not header.endswith(":"):
                header += ":"
            self.emit(header)
            self.indent += 1
        elif header.startswith("haramkhor") or header.startswith("lagateraha"):
            rest = header.split(" ", 1)[1] if " " in header else ""
            if " in " in rest:
                self.emit(f"for {rest}:")
                self.indent += 1
            else:
                self.emit("continue")
                return
        elif header == "nikalja":
            self.emit("break")
            return
        else:
            # sabse pehle elif -> warna -> if, warna agar ke replace se "ele agar" tootega
            header = header.replace("ele agar", "elif")
            header = header.replace("warna", "else")
            header = header.replace("agar", "if")
            if not header.endswith(":"):
                header += ":"
            self.emit(header)
            self.indent += 1

        # visit children
        for c in node.children:
            self.visit(c)
        self.indent -= 1


# ✅ Module-level transpile function
def transpile(source_code: str) -> str:
    """
    Raw .jhand code → Tokenize → Parse → Transpile → Python code string
    """
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()   # Tokenizer returns token list or lines
    parser = Parser(tokens)
    ast = parser.parse()
    t = Transpiler(ast)
    return t.transpile()
