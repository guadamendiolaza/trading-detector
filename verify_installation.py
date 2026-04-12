#!/usr/bin/env python
"""
Script para verificar instalación de Trading Opportunity Detector
Ejecutar: python verify_installation.py
"""

import os
import sys
import subprocess

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print("✓ Python 3.9+ detectado:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("✗ Python 3.9+ requerido")
        return False

def check_venv():
    """Verificar virtual environment del backend"""
    venv_path = "backend/venv"
    
    # Windows
    if os.path.exists(f"{venv_path}/Scripts/python.exe"):
        print("✓ Virtual environment Python detectado (Windows)")
        return True
    
    # macOS/Linux
    if os.path.exists(f"{venv_path}/bin/python"):
        print("✓ Virtual environment Python detectado (Unix)")
        return True
    
    print("✗ Virtual environment no encontrado en backend/venv")
    return False

def check_node():
    """Verificar Node.js"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✓ Node.js detectado: {version}")
        return True
    except:
        print("✗ Node.js no encontrado")
        return False

def check_npm():
    """Verificar npm"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✓ npm detectado: {version}")
        return True
    except:
        print("✗ npm no encontrado")
        return False

def check_env_files():
    """Verificar archivos .env"""
    backend_env = os.path.exists("backend/.env")
    
    print(f"{'✓' if backend_env else '✗'} backend/.env: {'existe' if backend_env else 'no existe (requerido)'}")
    
    return backend_env

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("\nVerificando dependencias...")
    
    backend_ok = os.path.exists("backend/venv")
    frontend_ok = os.path.exists("frontend/node_modules")
    
    print(f"{'✓' if backend_ok else '✗'} Backend dependencies: {'instaladas' if backend_ok else 'no instaladas'}")
    print(f"{'✓' if frontend_ok else '✗'} Frontend dependencies: {'instaladas' if frontend_ok else 'no instaladas'}")
    
    return backend_ok and frontend_ok

def check_supabase_config():
    """Verificar configuración de Supabase"""
    if not os.path.exists("backend/.env"):
        print("✗ backend/.env no encontrado")
        return False
    
    with open("backend/.env") as f:
        content = f.read()
        has_url = "SUPABASE_URL" in content and "https://" in content
        has_key = "SUPABASE_KEY" in content
        
        print(f"{'✓' if has_url else '✗'} SUPABASE_URL configurada: {has_url}")
        print(f"{'✓' if has_key else '✗'} SUPABASE_KEY configurada: {has_key}")
        
        return has_url and has_key

def main():
    print("=" * 60)
    print("Trading Opportunity Detector - Installation Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_venv),
        ("Node.js", check_node),
        ("npm", check_npm),
        ("Environment Files", check_env_files),
        ("Dependencies", check_dependencies),
        ("Supabase Configuration", check_supabase_config),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ ¡Todo está listo! Puedes ejecutar:")
        print("  - Windows: run.bat")
        print("  - macOS/Linux: bash run.sh")
    else:
        print("\n✗ Necesitas solucionar los siguientes problemas:")
        for name, result in results:
            if not result:
                print(f"  - {name}")
        print("\n  Ejecuta: setup.bat (Windows) o bash setup.sh (macOS/Linux)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
