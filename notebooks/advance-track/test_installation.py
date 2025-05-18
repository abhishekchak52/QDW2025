import sys


def check_python_version():
    """Ensure Python 3.11 is being used."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major != 3 or version.minor != 11:
        print("⚠️  Warning: This tutorial was developed with Python 3.11.x")

def check_imports():
    """Check if each required package is importable and print its version."""
    print("\n=== Package Import Check ===")
    all_ok = True
    
    # Try importing each package directly
    try:
        import numpy
        print(f"✅ numpy version {numpy.__version__} installed")
    except ImportError:
        print("❌ numpy not installed")
        all_ok = False

    try:
        import pandas
        print(f"✅ pandas version {pandas.__version__} installed")
    except ImportError:
        print("❌ pandas not installed")
        all_ok = False

    try:
        import matplotlib
        print(f"✅ matplotlib version {matplotlib.__version__} installed")
    except ImportError:
        print("❌ matplotlib not installed")
        all_ok = False

    try:
        import seaborn
        print(f"✅ seaborn version {seaborn.__version__} installed")
    except ImportError:
        print("❌ seaborn not installed")
        all_ok = False

    try:
        import sklearn
        print(f"✅ scikit-learn version {sklearn.__version__} installed")
    except ImportError:
        print("❌ scikit-learn not installed")
        all_ok = False

    try:
        import tensorflow
        print(f"✅ tensorflow version {tensorflow.__version__} installed")
    except ImportError:
        print("❌ tensorflow not installed")
        all_ok = False

    try:
        import torch
        print(f"✅ torch version {torch.__version__} installed")
    except ImportError:
        print("❌ torch not installed")
        all_ok = False

    try:
        import sympy
        print(f"✅ sympy version {sympy.__version__} installed")
    except ImportError:
        print("❌ sympy not installed")
        all_ok = False

    try:
        import kan
        print(f"✅ pykan installed")
    except ImportError:
        print("❌ pykan not installed")
        all_ok = False

    return all_ok

if __name__ == "__main__":
    print("🔍 Checking environment...\n")
    check_python_version()
    success = check_imports()
    if success:
        print("\n✅ All required packages are installed.")
    else:
        print("\n⚠️  Some required packages are missing. Please install them before proceeding.")