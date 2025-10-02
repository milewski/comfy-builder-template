import subprocess
import sys
import os
import glob

try:
    import tomllib
except ImportError:
    import toml as tomllib

def run_command(command):
    subprocess.check_call(command)

def install_rust():
    try:
        run_command(["rustc", "--version"])
        print("✅ Rust toolchain already installed")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("📦 Installing Rust toolchain via rustup...")
        run_command(["curl", "-sSf", "https://sh.rustup.rs", "-o", "rustup-init.sh"])
        run_command(["sh", "rustup-init.sh", "-y"])
        os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.cargo/bin")

def build():
    run_command([sys.executable, "-m", "maturin", "build", "--release"])

def install_wheels():
    wheels = glob.glob("target/wheels/*.whl")
    if not wheels:
        print("⚠️ No wheel files found in target/wheels")
        return
    for wheel in wheels:
        print(f"📦 Installing {wheel} ...")
        run_command([sys.executable, "-m", "pip", "install", "--force-reinstall", wheel])

def clean_up():
    print("🧹 Running cargo clean to trim dependencies...")
    try:
        run_command(["cargo", "clean"])
        print("✅ cargo clean completed")
    except FileNotFoundError:
        print("⚠️ cargo not found (is Rust installed?)")

def generate_init():
    print("📝 Generating __init__.py ...")
    with open("Cargo.toml", "rb") as f:
        crate_name = tomllib.load(f).get("lib", {}).get("name")
    if crate_name:
        with open("__init__.py", "w", encoding="utf-8") as f:
            f.write(f"# Auto-generated __init__.py\nfrom {crate_name} import *\n")
        print(f"✅ __init__.py generated for crate '{crate_name}'")
    else:
        print("⚠️ Could not find [lib] name in Cargo.toml")

if __name__ == "__main__":
    try:
        import maturin
    except ImportError:
        run_command([sys.executable, "-m", "pip", "install", "maturin"])

    install_rust()
    build()
    install_wheels()
    clean_up()
    generate_init()
