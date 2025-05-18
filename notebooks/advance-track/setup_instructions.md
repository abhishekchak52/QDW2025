# Environment Setup Instructions for the Workshop

These instructions will help you set up the environment needed for the ML components of this workshop.

## 🧪 Quick Check for Existing ML Users

If you already have a Python environment with ML packages, you can quickly verify if it meets our requirements:

```bash
python test_installation.py
```

If the test passes, you're all set! If not, follow the setup instructions below.

## 🐍 Python Version

This tutorial was developed using:

```
Python 3.11.4 | packaged by conda-forge | (main, Jun 10 2023) [Clang 15.0.7] on Darwin
```

## 🛠️ Setup Options

### Option 1: Using pip (Recommended)

```bash
# Create a new virtual environment (optional but recommended)
python -m venv ml-env
source ml-env/bin/activate  # On Windows: ml-env\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Option 2: Using Conda

1. **Install Miniconda** (if you don't have it):  
   [Miniconda Download](https://docs.conda.io/en/latest/miniconda.html)

2. **Create and activate the environment:**

   ```bash
   # Create from YAML file
   conda env create -f ml-env.yaml

   # Activate the environment
   conda activate ml-env
   ```

## 📦 Required Packages

The environment includes:

- numpy==1.26.4
- pandas==2.2.3
- matplotlib==3.7.0
- seaborn==0.12.2
- scikit-learn==1.6.1
- tensorflow==2.15.0
- torch==2.5.1
- sympy==1.13.1
- pykan==0.2.8
- ipykernel

## ⚡ Make Your Environment Available in Jupyter

After installing the requirements, run the following command to add your environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name ml-env --display-name "Python (ml-env)"
```

- `--name` is the internal name (no spaces, usually the env name)
- `--display-name` is what you'll see in the Jupyter interface

Now, when you open Jupyter Notebook or JupyterLab, you can select "Python (ml-env)" as your kernel.

## ⚠️ Platform-Specific Notes

### macOS

- Install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

### Windows

- Install C++ build tools (required for `scikit-learn` and `torch`)
- Consider using WSL2 for better compatibility

### Linux

- Install Python development headers:
  ```bash
  sudo apt install python3-dev
  ```

## 🔍 Verifying Your Setup

After installation, verify everything works:

```bash
# Activate your environment (if not already activated)
source ml-env/bin/activate  # or conda activate ml-env for conda users

# Run the test script
python test_installation.py
```

---
