import traceback
import random
import sys
import builtins
import subprocess
import re

# -------------------------
# UTF-8 Console & File patch
# -------------------------
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    # Kuch environments mein reconfigure nahi hota (e.g. Windows old PowerShell)
    pass

_builtin_open = open

def utf8_open(*args, **kwargs):
    """Globally patch open() to default to UTF-8 encoding (non-binary)."""
    mode = kwargs.get("mode", args[1] if len(args) > 1 else "r")
    if "b" not in mode and "encoding" not in kwargs:
        kwargs["encoding"] = "utf-8"
    return _builtin_open(*args, **kwargs)

builtins.open = utf8_open

# -------------------------
# Syntax Roasts
# -------------------------
ROAST_SYNTAX = [
    "BSDK! Syntax aise likhta hai? JHAND ne ulti kar di 🤮",
    "Abe chutiye, indentation dekh... tabs aur spaces ki shaadi 💔",
    "Ye code hai ya chhapr phaad ke bakwaas daal di 🫠",
    "Oye ullu ke pathe! Beghairat tarike se likha hai... compiler bhi roya 🥲",
]

# -------------------------
# Runtime Roasts (Generic)
# -------------------------
ROAST_RUNTIME = [
    "Program phat gaya BC 💥 CPU bhi bola: 'Band kar iski maa ka' 💻🔥",
    "Ye error dekh ke debugger bhi roya 😭",
    "Stack trace itna lamba jaise kisi ne galiyon ki lambi ladi chala di ho 🚨📜",
    "Code aise chala jaise brake fail truck 🛻💨",
]

# -------------------------
# Specific Exception Roasts + Fixes
# -------------------------
EXCEPTION_HANDLERS = {
    "NameError": (
        [
            "Naam likhna bhi nahi aata? Variable declare kiya tha ya hawa mein uda diya? 🤡",
            "Bhai! Yeh variable to kahin bana hi nahi… fir bhi use kar liya 😭",
        ],
        "Check karo variable/function ka naam sahi likha hai ya define kiya hai ya nahi."
    ),
    "TypeError": (
        [
            "BSDK types mila diye jaise chai mein mirchi daal di 🫡☕",
            "Yeh operation allowed nahi hai… int ko string se shadi nahi karwa sakte 💔",
        ],
        "Data types check karo — type conversion (int(), str(), float()) sahi jagah karo."
    ),
    "ZeroDivisionError": (
        [
            "Bhai ne math ka rape kar diya — zero se divide 🧮💥",
            "Zero se divide? Arey bhagwan bhi nahi kar sakta yeh 😤",
        ],
        "Denominator ko check karo, zero aane pe divide mat karo ya condition daal do."
    ),
    "FileNotFoundError": (
        [
            "File dhund raha jaise girlfriend ka pichla message 😭📁",
            "File ka path galat hai ya file gayab ho gayi 🫠",
        ],
        "File ka path verify karo ya file exist karti hai ya nahi check karo."
    ),
    "ImportError": (
        [
            "Library import mein error? PIP install bhool gaya kya bhai? 🧠📦",
            "Yeh module mil nahi raha... system ne bhi haath utha diye 👐",
        ],
        "Library install hai ya nahi check karo: 'pip install <library>' ya spelling sahi karo."
    ),
    "ValueError": (
        [
            "Value aisi di jaise biryani mein rubber daal diya 🍚🤢",
            "Input ya conversion mein gadbad hai bhai 😤",
        ],
        "Input ya value ko sahi format mein do — int/float conversion check karo."
    ),
    "KeyError": (
        [
            "Dictionary mein yeh key to exist hi nahi karti 🤦‍♂️🔑",
            "KeyError aaya... matlab dict ko random thappad maar diya 😭",
        ],
        "Check karo key exist karti hai ya nahi ya dict.get() use karo."
    ),
    "IndexError": (
        [
            "Index aise nikaal raha jaise khali fridge mein doodh dhund raha ho 🥶",
            "List ka index range se bahar chala gaya 🚪👻",
        ],
        "List/array ki length check karo before indexing."
    ),
    "AttributeError": (
        [
            "Bhai attribute hi galat likh diya… object ne kaha 'yeh mera field hi nahi' 😡",
            "Aisi attribute maang raha jaise aadmi se 'fly()' kehna 🪽",
        ],
        "Object ke attributes check karo ya dir(object) use karo debugging ke liye."
    ),
}

def roast(choice_list):
    return random.choice(choice_list)

# -------------------------
# Auto Package Installer
# -------------------------
def try_auto_install(module_name: str):
    """Try to install a missing module using pip."""
    print(f"📦 Auto-Installer: '{module_name}' dhoond liya. Installing via pip... 🚀")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"✅ '{module_name}' install ho gaya bhai! Code dobara chala ke dekh 😎")
    except Exception as e:
        print(f"❌ Auto install fail ho gaya for '{module_name}' 😭 — {e}")

# -------------------------
# Builtins for JHAND
# -------------------------
def bol(*args, **kwargs):
    """JHAND's desi print()"""
    print(*args, **kwargs)

builtins.bol = bol

# -------------------------
# Main JHAND runner
# -------------------------
def run_jhand(source_code: str, filename="<jhand>"):
    """Run JHAND code with trolling + proper debug info"""
    # 🧠 Syntax Error Roast
    try:
        compiled = compile(source_code, filename, "exec")
    except SyntaxError as se:
        print("\n🔴 [ JHAND SYNTAX ERROR ]")
        print("💬 " + roast(ROAST_SYNTAX))
        print(f"📍 Line: {se.lineno}, Char: {se.offset}")
        print(f"📝 Text: {se.text.strip() if se.text else 'Empty'}")
        print(f"⚠️ Python Error: {se.msg}")
        print("💡 Possible Fix: Check indentation, missing colons, ya galat likhi expression.")
        return

    # 🧠 Runtime Error Roast (Detailed)
    try:
        env = {"__name__": "__main__"}
        exec(compiled, env, env)
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        etype_name = exc_type.__name__
        print("\n💥 [ JHAND RUNTIME ERROR ]")
        print("💬 " + roast(ROAST_RUNTIME))
        print("📍 Python Traceback (most recent call last):")
        traceback.print_exception(exc_type, exc_value, exc_tb)

        print(f"⚠️ Error Type: {etype_name}")
        print(f"💡 Likely Cause: {str(exc_value)}")

        # Special handling for ImportError to extract module name
        if etype_name == "ImportError":
            match = re.search(r"named '([^']+)'", str(exc_value))
            if match:
                module_name = match.group(1)
                print(f"🧠 Roast: {roast(EXCEPTION_HANDLERS['ImportError'][0])}")
                print(f"🛠️ Fix: pip install {module_name}")
                try_auto_install(module_name)
            else:
                print("🧠 Roast: ImportError aaya lekin module naam pakad nahi paya 😅")
        elif etype_name in EXCEPTION_HANDLERS:
            roast_msg, fix_msg = EXCEPTION_HANDLERS[etype_name]
            print("🧠 Roast: " + roast(roast_msg))
            print("🛠️ Fix: " + fix_msg)
        else:
            print("🧠 Roast: Is exception ka bhi jawab nahi hai bhai... generic error 🥲")
            print("🛠️ Fix: Traceback padh ke debugging shuru kar 😎")

# -------------------------
# Simple run_code (no trolling)
# -------------------------
def run_code(source_code: str, filename="<jhand>"):
    try:
        compiled = compile(source_code, filename, "exec")
        env = {"__name__": "__main__"}
        exec(compiled, env, env)
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        print("\n💥 [ JHAND RUNTIME ERROR ]")
        traceback.print_exception(exc_type, exc_value, exc_tb)

# -------------------------
# Test runner
# -------------------------
if __name__ == "__main__":
    sample = """
bol("Salaam duniya 👋")
import kuch_bhi_nahi  # Non-existent lib to trigger auto install
bol(1 / 0)
"""
    run_jhand(sample)
