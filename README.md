# Environment Setup and Reproduction Guide

This guide outlines the steps required to replicate the development environment for the Climate Challenge Project on Windows using VS Code and PowerShell.

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.11** (or higher)
- **Git**
- **Visual Studio Code** (with the official _Python_ extension installed)

---

## Step-by-Step Setup

### 1. Clone the Repository

Open your PowerShell terminal, navigate to your desired working directory, and clone the repository:

```powershell
git clone <your-repository-url>
cd climate-challenge-project
```

### 2. Generate the Project Structure

If you are initializing a fresh copy of the workspace structure, execute the following script in your PowerShell terminal to build the standard directories and tracking files:

```powershell
# Create all required folders
New-Item -ItemType Directory -Force -Path (
    ".vscode", ".github/workflows", "src", "notebooks", "tests", "scripts"
)

# Create all primary files
New-Item -ItemType File -Force -Path (
    ".vscode/settings.json", ".github/workflows/ci.yml", ".gitignore",
    "requirements.txt", "README.md", "notebooks/__init__.py", "notebooks/README.md",
    "tests/__init__.py", "scripts/__init__.py", "scripts/README.md"
)
```

### 3. Configure the Virtual Environment (`venv`)

Create and isolate your dependencies inside the root of your project folder:

```powershell
# Create the local virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

> 💡 **Troubleshooting Script Execution:** If PowerShell throws an error stating that script execution is disabled, temporarily bypass the execution policy for this terminal session using:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

Once successfully activated, your terminal prompt will be prefixed with `(venv)`.

### 4. Install Dependencies

Ensure your environment is active, then upgrade package management tools and install the required modules directly from the configuration file:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Environment & Tooling Specifications

### Git Architecture (`.gitignore`)

The repository is pre-configured to systematically ignore ephemeral runtimes, large data sets, and local IDE configurations. The primary ignored layers include:

- **Runtimes:** Local virtual environments (`venv/`, `.venv/`)
- **Data Layers:** All data directories (`data/`) and analytical exports (`*.csv`)
- **Jupyter Metadata:** Automated local checkpoints (`.ipynb_checkpoints/`)

### Automated Integration (CI)

A continuous integration pipeline (`.github/workflows/ci.yml`) triggers on every push targeting the `main` or `setup-task` branches. It targets a clear sequence:

1. Provisions an ephemeral **Ubuntu Linux VM**
2. Sets up standard **Python runtime** environments
3. Audits and syncs runtime targets via **`pip install -r requirements.txt`**
