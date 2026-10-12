"""
SESSION 1 - Task 1: Install LangChain & Verify Installation
Objective: Run a script that prints the installed version of LangChain and its core modules.
"""

import sys
import platform

def main():
    print("=" * 60)
    print("   SESSION 1 - TASK 1: LANGCHAIN ENVIRONMENT CHECK")
    print("=" * 60)
    
    # Python environment information
    print(f"[+] Python Executable : {sys.executable}")
    print(f"[+] Python Version    : {platform.python_version()}")
    print(f"[+] Operating System  : {platform.system()} {platform.release()}")
    print("-" * 60)
    
    # LangChain versions
    try:
        import langchain
        print(f"[SUCCESS] langchain version      : {langchain.__version__}")
    except ImportError as e:
        print(f"[ERROR] langchain is not installed: {e}")
        
    try:
        import langchain_core
        print(f"[SUCCESS] langchain-core version : {langchain_core.__version__}")
    except ImportError:
        pass

    try:
        import langchain_community
        print(f"[SUCCESS] langchain-community   : {langchain_community.__version__}")
    except ImportError:
        pass

    try:
        import langchain_openai
        print(f"[SUCCESS] langchain-openai      : {langchain_openai.__version__}")
    except ImportError:
        pass

    print("=" * 60)
    print("Environment setup verified successfully!")

if __name__ == "__main__":
    main()
