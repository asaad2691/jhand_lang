# jhand/lexer.py
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"<{self.type}('{self.value}') @{self.line}:{self.col}>"

# ==============================
# Token specifications
# ==============================
_TOKEN_SPEC = [
    ("NUMBER",   r"\d+(\.\d+)?"),  # integers and floats
    ("STRING",   r"(?:[fF]?|[rR]?|[bB]?|[frFR]?|[rbRB]?)(\"([^\"\\]|\\.)*\"|'([^'\\]|\\.)*')"),  # f-strings + normal strings
    ("NAME",     r"[A-Za-z_][A-Za-z0-9_]*"),  # identifiers
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
    ("COMMENT",  r"#.*"),
    ("OP", r"\*\*|\+=|-=|\*=|/=|==|!=|<=|>=|=|\+|-|\*|/|%|<|>|\(|\)|:|,|\.|\[|\]|\{|\}"),
    ("MISMATCH", r"."),  # catch-all
]

_TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in _TOKEN_SPEC), re.MULTILINE)

# ==============================
# JHAND → Python keyword mapping
# ==============================
KEYWORD_MAP = {
    "bhenchod": "def",
    "madarchod": "class",
    "naya_kutta": "def",
    "agar": "if",
    "ele": "elif",
    "warna": "else",
    "jabtak": "while",
    "haramkhor": "for",
    "nikalja": "break",
    "lagateraha": "continue",
    "koshish": "try",
    "phaansi": "except",
    "aakhir": "finally",
    "utha": "raise",
    "leja": "return",
    "beghairat": "pass",
    "saath": "with",
    "haaan": "True",
    "naaa": "False",
    "kuchbhi": "None",
    "laao": "import",
    "se_laao": "from",
    "bol": "print",
    "bhenkelode": "print",
    "gand_faad": "exec",
    "dimag_laga": "input",
    "aur": "and",
    "ya": "or",
    "nahi": "not",
    "tez_bhenchod": "async",
}

# ==============================
# Lexer
# ==============================
class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.line = 1

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        for mo in _TOKEN_RE.finditer(self.text):
            kind = mo.lastgroup
            value = mo.group()
            start = mo.start()
            prev_newline = self.text.rfind("\n", 0, start)
            col = start - (prev_newline + 1) if prev_newline >= 0 else start

            if kind == "NUMBER":
                tokens.append(Token("NUMBER", value, self.line, col))
            elif kind == "STRING":
                tokens.append(Token("STRING", value, self.line, col))
            elif kind == "NAME":
                mapped = KEYWORD_MAP.get(value, value)
                tokens.append(Token("NAME", mapped, self.line, col))
            elif kind == "NEWLINE":
                tokens.append(Token("NEWLINE", "\\n", self.line, col))
                self.line += 1
            elif kind == "SKIP":
                continue
            elif kind == "COMMENT":
                continue
            elif kind == "OP":
                tokens.append(Token("OP", value, self.line, col))
            elif kind == "MISMATCH":
                raise SyntaxError(f"Unexpected character {value!r} at {self.line}:{col}")

        tokens.append(Token("EOF", "", self.line, 0))
        return tokens

# ==============================
# Quick test
# ==============================
if __name__ == "__main__":
    sample = '''
# JHAND Full Test
laao random
laao datetime

madarchod Player:
    naya_kutta __init__(self, name):
        self.name = name
        self.hp = 100
        self.items = []
        self.alive = haaan

    bhenchod add_item(self, item):
        self.items.append(item)
        bol(f"{self.name} ne item liya: {item}")

    bhenchod show_stats(self):
        bol(f"--- {self.name} Stats ---")
        bol(f"HP: {self.hp}, Alive: {self.alive}, Items: {self.items}")

# Collections
x = [1, 2, 3, 4]
y = {"name": "JHAND", "level": 9000}
bol(f"Player: {x[0]} {y['name']}")
'''
    lexer = Lexer(sample)
    for token in lexer.tokenize():
        print(token)
