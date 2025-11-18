# installer.py - Sets up the environment and installs all dependencies for Geforce-Hybrid-Capture
import os
import sys
import subprocess
import json
import platform

VENV_DIR = ".venv"

# Global list of Python dependencies with compatible versions
# Using versions with pre-built wheels to avoid compilation issues
PYTHON_REQUIREMENTS = [
    "av>=12.0.0",  # PyAV - Use 12.0+ which has pre-built wheels for Windows
]

def get_python_version():
    """Returns the Python version as a tuple (major, minor)."""
    return sys.version_info[:2]

def create_venv():
    """Creates a virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
            print("✓ Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create virtual environment: {e}")
            sys.exit(1)
    else:
        print("✓ Virtual environment already exists.")

def get_python_executable():
    """Returns the path to the Python executable in the virtual environment."""
    if os.name == 'nt':
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def get_pip_executable():
    """Returns the path to the pip executable in the virtual environment."""
    if os.name == 'nt':
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "pip")

def upgrade_pip():
    """Upgrades pip to the latest version in the virtual environment."""
    python_executable = get_python_executable()
    print("\nUpgrading pip to latest version...")
    try:
        # Use python -m pip instead of calling pip directly to avoid the lock issue
        subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ Pip upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"⚠ Warning: Failed to upgrade pip: {e}")
        print("  Continuing with current pip version...")

def check_system_requirements():
    """Checks if the system meets the basic requirements."""
    print("\nChecking system requirements...")
    
    py_version = get_python_version()
    print(f"  Python version: {py_version[0]}.{py_version[1]}")
    
    if py_version < (3, 7):
        print("  ✗ Python 3.7 or higher is required!")
        return False
    
    if py_version > (3, 11):
        print("  ⚠ Warning: Python 3.12+ may have compatibility issues with some packages.")
        print("    Python 3.8-3.11 is recommended.")
    
    print(f"  Platform: {platform.system()} {platform.release()}")
    print("  ✓ System requirements check passed.")
    return True

def install_dependencies():
    """Installs all required dependencies using pip."""
    python_executable = get_python_executable()
    
    print("\nInstalling Python dependencies...")
    print(f"  Dependencies to install: {len(PYTHON_REQUIREMENTS)}")
    
    failed_packages = []
    
    for idx, requirement in enumerate(PYTHON_REQUIREMENTS, 1):
        print(f"\n  [{idx}/{len(PYTHON_REQUIREMENTS)}] Installing {requirement}...")
        try:
            # Use python -m pip for more reliable installation
            # Add --prefer-binary to prefer pre-built wheels over source
            subprocess.check_call([
                python_executable, "-m", "pip", "install",
                "--prefer-binary",  # Prefer binary wheels over source
                requirement
            ])
            print(f"    ✓ {requirement} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"    ✗ Failed to install {requirement}")
            failed_packages.append(requirement)
    
    if failed_packages:
        print(f"\n✗ Failed to install {len(failed_packages)} package(s):")
        for pkg in failed_packages:
            print(f"    - {pkg}")
        
        print("\n" + "="*60)
        print("TROUBLESHOOTING:")
        print("="*60)
        print("If PyAV (av) failed to install, try these solutions:")
        print("\n1. Install pre-built wheel manually:")
        print("   .venv\\Scripts\\pip.exe install av --only-binary av")
        print("\n2. Or download from: https://pypi.org/project/av/#files")
        print("   Look for a wheel (.whl) matching your Python version")
        print("   Example: av-12.0.0-cp311-cp311-win_amd64.whl for Python 3.11")
        print("\n3. Install with conda if available:")
        print("   conda install -c conda-forge av")
        print("="*60)
        
        sys.exit(1)
    
    print("\n✓ All dependencies installed successfully.")

def create_output_dir():
    """Creates the Output directory if it doesn't exist."""
    if not os.path.exists("Output"):
        print("\nCreating Output directory...")
        try:
            os.makedirs("Output")
            print("✓ Output directory created.")
        except OSError as e:
            print(f"✗ Failed to create Output directory: {e}")
            sys.exit(1)
    else:
        print("✓ Output directory already exists.")

def create_data_dir():
    """Creates the data directory if it doesn't exist."""
    if not os.path.exists("data"):
        print("\nCreating data directory...")
        try:
            os.makedirs("data")
            print("✓ Data directory created.")
        except OSError as e:
            print(f"✗ Failed to create data directory: {e}")
            sys.exit(1)
    else:
        print("✓ Data directory already exists.")

def create_scripts_dir():
    """Creates the scripts directory if it doesn't exist."""
    if not os.path.exists("scripts"):
        print("\nCreating scripts directory...")
        try:
            os.makedirs("scripts")
            print("✓ Scripts directory created.")
        except OSError as e:
            print(f"✗ Failed to create scripts directory: {e}")
            sys.exit(1)
    else:
        print("✓ Scripts directory already exists.")

def create_default_configuration():
    """Creates a default configuration file if it doesn't exist."""
    config_path = os.path.join("data", "configuration.json")
    
    if not os.path.exists(config_path):
        print("\nCreating default configuration file...")
        default_config = {
            "resolution": {
                "width": 1920,
                "height": 1080
            },
            "fps": 30,
            "codec": "libx264",
            "output_path": "Output"
        }
        
        try:
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=4)
            print("✓ Default configuration file created.")
            print(f"  Location: {config_path}")
        except IOError as e:
            print(f"✗ Failed to create configuration file: {e}")
            sys.exit(1)
    else:
        print("✓ Configuration file already exists.")

def verify_installation():
    """Verifies that all required components are installed correctly."""
    print("\n" + "="*60)
    print("Verifying Installation...")
    print("="*60)
    
    issues = []
    warnings = []
    
    # Check venv
    if not os.path.exists(VENV_DIR):
        issues.append("Virtual environment directory not found")
    
    # Check Python executable
    python_executable = get_python_executable()
    if not os.path.exists(python_executable):
        issues.append("Python executable not found in virtual environment")
    
    # Check pip
    pip_executable = get_pip_executable()
    if not os.path.exists(pip_executable):
        issues.append("Pip executable not found in virtual environment")
    
    # Check directories
    if not os.path.exists("Output"):
        issues.append("Output directory not found")
    if not os.path.exists("data"):
        issues.append("Data directory not found")
    if not os.path.exists("scripts"):
        warnings.append("Scripts directory not found (may need to be created manually)")
    
    # Check configuration
    if not os.path.exists("data/configuration.json"):
        issues.append("Configuration file not found")
    
    # Check installed packages
    print("\nVerifying installed packages...")
    for requirement in PYTHON_REQUIREMENTS:
        package_name = requirement.split(">=")[0].split("==")[0]
        try:
            result = subprocess.run(
                [python_executable, "-m", "pip", "show", package_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Extract version from output
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':')[1].strip()
                        print(f"  ✓ {package_name} {version} is installed")
                        break
            else:
                issues.append(f"{package_name} is not installed")
        except Exception as e:
            issues.append(f"Failed to verify {package_name}: {e}")
    
    # Display results
    if warnings:
        print("\n" + "="*60)
        print("⚠ Warnings:")
        print("="*60)
        for warning in warnings:
            print(f"  ⚠ {warning}")
    
    if issues:
        print("\n" + "="*60)
        print("✗ Installation Issues Detected:")
        print("="*60)
        for issue in issues:
            print(f"  ✗ {issue}")
        return False
    else:
        print("\n" + "="*60)
        print("✓ Installation Verified Successfully!")
        print("="*60)
        return True

def main():
    """Main installation routine."""
    print("="*60)
    print("Geforce-Hybrid-Capture Installer")
    print("="*60)
    print("\nThis installer will set up your environment for")
    print("Geforce-Hybrid-Capture, including:")
    print("  • Python virtual environment")
    print("  • Required Python packages (with pre-built binaries)")
    print("  • Output directories")
    print("  • Default configuration")
    print("\n" + "="*60)
    
    # Check system requirements first
    if not check_system_requirements():
        print("\n✗ System requirements not met.")
        sys.exit(1)
    
    # Run installation steps
    create_venv()
    upgrade_pip()
    install_dependencies()
    create_output_dir()
    create_data_dir()
    create_scripts_dir()
    create_default_configuration()
    
    # Verify everything
    if verify_installation():
        print("\n✓ Installation complete!")
        print("\nYou can now run the application.")
    else:
        print("\n⚠ Installation completed with issues.")
        print("Please review the errors above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error during installation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)