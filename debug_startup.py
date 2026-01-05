import sys
import os
import platform

def log(msg):
    print(f"[DEBUG] {msg}", flush=True)

def check_import(module_name):
    try:
        __import__(module_name)
        log(f"✅ Import successful: {module_name}")
        return True
    except ImportError as e:
        log(f"❌ Import FAILED: {module_name} - {e}")
        return False
    except Exception as e:
        log(f"❌ Import CRASHED: {module_name} - {e}")
        return False

def main():
    log("="*50)
    log("🔍 STARTUP DIAGNOSTIC")
    log("="*50)
    
    # System Info
    log(f"Python Version: {sys.version}")
    log(f"Platform: {platform.platform()}")
    log(f"CWD: {os.getcwd()}")
    log(f"Path: {sys.path}")
    
    # Critical Dependencies
    dependencies = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic_settings",
        "pandas",
        "numpy",
        "sklearn",
        "shap",
        "lime",
        "git",
        "yaml",
        "jinja2", 
        "dotenv"
    ]
    
    success = True
    for dep in dependencies:
        if not check_import(dep):
            success = False

    # Check App Imports
    log("-" * 30)
    log("Checking App Imports...")
    
    app_modules = [
        "src.api.config",
        "src.api.main"
    ]
    
    for mod in app_modules:
        if not check_import(mod):
            success = False

    log("="*50)
    if success:
        log("✅ ALL CHECKS PASSED - Ready to start server")
    else:
        log("❌ CHECKS FAILED - Server may crash")
    log("="*50)

if __name__ == "__main__":
    main()
