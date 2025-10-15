from typing import List, Optional
from .lexer import Token
from .astnode import ASTNode

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def lookahead(self, n=1) -> Optional[Token]:
        idx = self.pos + n
        return self.tokens[idx] if idx < len(self.tokens) else None

    def eat(self, ttype=None, tval=None) -> Token:
        tok = self.current()
        if ttype and tok.type != ttype:
            raise SyntaxError(f"Expected {ttype}, got {tok.type} ({tok.value}) at {tok.line}:{tok.col}")
        if tval and tok.value != tval:
            raise SyntaxError(f"Expected {tval}, got {tok.value} at {tok.line}:{tok.col}")
        self.pos += 1
        return tok

    def parse(self) -> ASTNode:
        program = ASTNode("Program", children=[])
        while self.current().type != "EOF":
            if self.current().type == "NEWLINE":
                self.eat("NEWLINE")
                continue
            program.children.append(self.parse_statement(0))
        return program

    # ------------------------ PARSE STATEMENT ------------------------
    def parse_statement(self, parent_indent: int) -> ASTNode:
        tok = self.current()
        if tok.type == "NAME":
            if tok.value == "def":
                return self.parse_function(parent_indent, is_async=False)
            if tok.value == "async":
                # next token should be def
                self.eat("NAME")  # async
                if self.current().value != "def":
                    raise SyntaxError(f"Expected 'def' after 'async', got {self.current().value}")
                return self.parse_function(parent_indent, is_async=True)
            if tok.value == "class":
                return self.parse_class(parent_indent)
            if tok.value == "print":
                return self.parse_print()
            # Blocks: normal + try/catch/finally
            if tok.value in ("if", "elif", "else", "while", "for", "try", "except", "finally", "with"):
                return self.parse_block(parent_indent)
        # Default: treat as expression
        return self.parse_expr()

    # ------------------------ PARSE PRINT ------------------------
    def parse_print(self) -> ASTNode:
        self.eat("NAME")  # print
        content = self._collect_paren_or_string()
        if self.current().type == "NEWLINE":
            self.eat("NEWLINE")
        return ASTNode("Print", value=content)

    def _collect_paren_or_string(self) -> str:
        if self.current().type == "OP" and self.current().value == "(":
            self.eat("OP", "(")
            parts = []
            while not (self.current().type == "OP" and self.current().value == ")"):
                parts.append(self.eat().value)
            self.eat("OP", ")")
            return " ".join(parts).strip()
        if self.current().type == "STRING":
            return self.eat("STRING").value
        raise SyntaxError("Invalid print content")

    # ------------------------ PARSE EXPRESSION ------------------------
    def parse_expr(self) -> ASTNode:
        parts = []
        while self.current().type not in ("NEWLINE", "EOF"):
            parts.append(self.eat().value)
        if self.current().type == "NEWLINE":
            self.eat("NEWLINE")
        return ASTNode("Expr", value=" ".join(parts).strip())

    # ------------------------ FUNCTION ------------------------
    def parse_function(self, parent_indent: int, is_async: bool = False) -> ASTNode:
        self.eat("NAME")  # def
        name = self.eat("NAME").value
        params = ""
        if self.current().type == "OP" and self.current().value == "(":
            self.eat("OP", "(")
            pparts = []
            while not (self.current().type == "OP" and self.current().value == ")"):
                pparts.append(self.eat().value)
            self.eat("OP", ")")
            params = " ".join(pparts).strip()
        if self.current().type == "OP" and self.current().value == ":":
            self.eat("OP", ":")
        if self.current().type == "NEWLINE":
            self.eat("NEWLINE")
        children = self._parse_body(self.current().col)
        return ASTNode("Function", value={"name": name, "params": params, "async": is_async}, children=children)


    # ------------------------ CLASS ------------------------
    def parse_class(self, parent_indent: int) -> ASTNode:
        self.eat("NAME")  # class
        name = self.eat("NAME").value
        if self.current().type == "OP" and self.current().value == ":":
            self.eat("OP", ":")
        if self.current().type == "NEWLINE":
            self.eat("NEWLINE")
        children = self._parse_body(self.current().col)
        return ASTNode("Class", value={"name": name}, children=children)

    # ------------------------ BLOCK ------------------------
    def parse_block(self, parent_indent: int) -> ASTNode:
        header_parts = []
        while self.current().type not in ("NEWLINE", "EOF"):
            header_parts.append(self.eat().value)
        if self.current().type == "NEWLINE":
            self.eat("NEWLINE")
        header = " ".join(header_parts).strip()

        # Decide body_indent specially for try/except/finally
        if header.startswith("koshish"):  # try
            children = self._parse_body(self.current().col + 4)
        elif header.startswith("phaansi") or header.startswith("aakhir"):  # except/finally
            children = self._parse_body(parent_indent + 4)
        else:
            children = self._parse_body(self.current().col)

        return ASTNode("Block", value={"header": header}, children=children)

    # ------------------------ PARSE BODY ------------------------
    def _parse_body(self, body_indent: int) -> List[ASTNode]:
        children = []
        while self.current().type != "EOF":
            tok = self.current()

            if tok.type == "NEWLINE":
                self.eat("NEWLINE")
                continue

            # Agar token ka col < body_indent matlab block khatam
            if tok.col < body_indent:
                break

            # Agar next token except/finally hai, current block ka part nahi
            # lookahead_val = tok.value if tok.type == "NAME" else ""
            # if lookahead_val in ("except", "finally"):
            #     break

            # Normal statement parse karo
            stmt_node = self.parse_statement(body_indent)
            children.append(stmt_node)
            # print(stmt_node)  # Debug: show AST

        return children
