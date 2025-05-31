"""
Install missing dependencies for the stock analysis system
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def check_package(package):
    """Check if a package is installed"""
    try:
        __import__(package)
        print(f"✅ {package} is already installed")
        return True
    except ImportError:
        print(f"❌ {package} is not installed")
        return False

def main():
    """Install all required dependencies"""
    print("🔧 Stock Analysis System - Dependency Installer")
    print("=" * 50)
    
    # Required packages
    required_packages = [
        "pandas",
        "yfinance", 
        "requests",
        "numpy"
    ]
    
    # Optional packages for enhanced functionality
    optional_packages = [
        "transformers",
        "torch",
        "newsapi-python"
    ]
    
    print("\n📋 Checking required dependencies...")
    missing_required = []
    
    for package in required_packages:
        if not check_package(package):
            missing_required.append(package)
    
    print("\n📋 Checking optional dependencies...")
    missing_optional = []
    
    for package in optional_packages:
        if not check_package(package):
            missing_optional.append(package)
    
    # Install missing required packages
    if missing_required:
        print(f"\n🔧 Installing {len(missing_required)} required packages...")
        success_count = 0
        
        for package in missing_required:
            if install_package(package):
                success_count += 1
        
        print(f"\n📊 Installation Results: {success_count}/{len(missing_required)} required packages installed")
        
        if success_count == len(missing_required):
            print("✅ All required dependencies installed successfully!")
        else:
            print("⚠️ Some required packages failed to install")
            return False
    else:
        print("\n✅ All required dependencies are already installed!")
    
    # Ask about optional packages
    if missing_optional:
        print(f"\n📦 Optional packages available: {', '.join(missing_optional)}")
        print("These provide enhanced functionality but are not required.")
        
        try:
            install_optional = input("\nInstall optional packages? (y/n): ").lower().strip()
            
            if install_optional in ['y', 'yes']:
                print("\n🔧 Installing optional packages...")
                for package in missing_optional:
                    install_package(package)
        except KeyboardInterrupt:
            print("\n⏭️ Skipping optional packages")
    
    print("\n🧪 Testing installation...")
    
    # Test imports
    test_results = []
    for package in required_packages:
        try:
            __import__(package)
            test_results.append((package, True))
            print(f"✅ {package} import test passed")
        except ImportError as e:
            test_results.append((package, False))
            print(f"❌ {package} import test failed: {e}")
    
    # Summary
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"\n📊 Test Results: {passed}/{total} packages working")
    
    if passed == total:
        print("\n🎉 All dependencies installed and working!")
        print("\n🚀 Next steps:")
        print("1. Set up your Groq API key (see GROQ_SETUP_GUIDE.md)")
        print("2. Run: python test_ai_integration.py")
        print("3. Start the app: python app.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} package(s) still have issues")
        print("Try running this script again or install manually:")
        for package, result in test_results:
            if not result:
                print(f"  pip install {package}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
