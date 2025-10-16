# 🧠 JHAND Language 💥

> “Galiyon mein likho, duniya ko hilao.” – Sadran

**JHAND** is a full-stack abusive programming language that transpiles your rage into runnable Python code.  
Built with love, sarcasm, and solid compiler design.

---

## ✨ Features

- **Full OOP Support** — Functions, Classes, Loops, Try–Catch, Async... sab kuch.
- **Gali-to-Logic Transpilation** — likho `bhenchod` aur ban jaaye `def`.
- **Roasting Runtime** — errors sirf crash nahi karte... rooh tak hila dete hain.
- **Seamless Python Interop** — import karo aur Python libraries use karo jaise asli bhasha ho.
- **GUI Ready** — Tkinter ke zariye real-world apps bhi likho JHAND mein.
- **JSON Storage** — SQLite ya file-based handling out-of-the-box.

---

## 🚀 Installation Guide

1. **Clone the Repository**
    ```sh
    git clone https://github.com/asaad2691/jhand_lang.git
    cd jhand_lang
    ```

2. **(Optional) Create Virtual Environment**

    **Windows:**
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

    **Linux / Mac:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Install the Package Locally**
    ```sh
    pip install .
    ```
    👉 Yeh step project ko system mein `jhand` command ke taur par register karta hai.

---

## 🧠 Running Your First JHAND Program

### Step 1: Create a `.jhand` File

`examples/main2.jhand`
```jhand
bol("JHAND language mein aapka swagat hai!")

bhenchod hello(name):
    bol(f"Hello {name}, aaj ka code chalega ya phatega?")

hello("Bhai")
```

### Step 2: Run with CLI

**Option A: Transpile + Show Python Code**
```sh
jhand -t examples/main2.jhand
```

**Option B: Direct Run**
```sh
jhand examples/main2.jhand
```

---

## 🧱 Project Structure

```
jhand_lang/
├─ jhand/
│  ├─ __init__.py
│  ├─ astnode.py
│  ├─ cli.py
│  ├─ transpiler.py
│  ├─ lexer.py
│  ├─ parser.py
│  └─ runtime.py
├─ examples/
│  └─ main2.jhand
├─ requirements.txt
├─ setup.py
└─ README.md
```

---

## 🧠 Transpilation Flow

```
JHAND Source File → Lexer → Parser → Transpiler → Python Code → Execution
```

---

## 🛠 Developer Guide

```sh
git clone https://github.com/asaad2691/jhand_lang.git
cd jhand_lang
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

---

## 🛤 Roadmap

- ✅ Core transpiler engine
- ✅ CLI entry point
- ✅ JSON-based persistence
- 🖼 Tkinter GUI demo
- 📦 Publish to PyPI
- 🧠 Async/await sugar syntax
- 🧩 Plugin system for custom gali packs

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch
3. Commit your changes
4. Push and open a PR

---

## 🧾 License

MIT License © asaad2691  
Galiyon mein free likho, lekin credit dena mat bhoolna 😎

---

## ⭐ Show Some Love

```sh
gh repo star asaad2691/jhand_lang
```

---

## ⚡ Quick Cheat Sheet

| JHAND Word      | Python Equivalent |
|-----------------|------------------|
| bhenchod        | def              |
| madarchod       | class            |
| bol             | print            |
| agar            | if               |
| warna           | else             |
| jabtak          | while            |
| haramkhor       | for              |
| nikalja         | break            |
| lagateraha      | continue         |
| koshish         | try              |
| phaansi         | except           |
| aakhir          | finally          |
| tez_bhenchod    | async            |

---

> 🧠 **Pro Tip:** JHAND code is 100% valid Python after transpilation —  
> aap transpiled file ko `.py` mein dump karke VSCode mein debug bhi kar sakte ho like a boss 😎

---

Agar chaaho to main isey `.html` ke liye bhi format kar sakta hoon — sirf readable content ke saath, bina kisi tag ke. Batao kis format mein chahiye: `.txt` ke liye ready hai, aur agar HTML chahiye to batao kis style mein render karna hai (e.g. monospace, sectioned, etc).