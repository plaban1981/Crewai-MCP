#!/usr/bin/env python3
"""
Setup script for Node.js installation and MCP server configuration
"""

import subprocess
import sys
import os
import webbrowser
from pathlib import Path

def check_current_nodejs():
    """Check current Node.js installation"""
    print("🔍 Checking current Node.js installation...")
    
    try:
        result = subprocess.run(["node", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            major_version = int(version.lstrip('v').split('.')[0])
            print(f"📦 Current Node.js version: {version}")
            
            if major_version >= 18:
                print("✅ Node.js version is compatible with MCP servers!")
                return True
            else:
                print(f"⚠️  Node.js version {version} is too old for MCP servers")
                print("🎯 Recommended: Node.js v18+ or v20+")
                return False
        else:
            print("❌ Node.js check failed")
            return False
    except Exception as e:
        print(f"❌ Node.js not found: {e}")
        return False

def check_npm():
    """Check npm installation"""
    try:
        result = subprocess.run(["npm", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"📦 NPM version: {version}")
            return True
        else:
            print("❌ NPM check failed")
            return False
    except Exception as e:
        print(f"❌ NPM not found: {e}")
        return False

def download_nodejs():
    """Open Node.js download page"""
    print("\n🌐 Opening Node.js download page...")
    webbrowser.open("https://nodejs.org/en/download/")
    print("📥 Please download and install Node.js v20.x LTS (recommended)")
    print("🔄 After installation, restart your terminal and run this script again")

def test_mcp_servers():
    """Test if MCP servers can be installed"""
    print("\n🧪 Testing MCP server installation...")
    
    npx_cmd = "npx.cmd" if os.name == 'nt' else "npx"
    
    # Test filesystem server
    print("Testing @modelcontextprotocol/server-filesystem...")
    try:
        result = subprocess.run([
            npx_cmd, "-y", "@modelcontextprotocol/server-filesystem", "--help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Filesystem server can be installed!")
        else:
            print(f"⚠️  Filesystem server test failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Filesystem server test error: {e}")
    
    # Test brave search server
    print("Testing @modelcontextprotocol/server-brave-search...")
    try:
        result = subprocess.run([
            npx_cmd, "-y", "@modelcontextprotocol/server-brave-search", "--help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Brave search server can be installed!")
        else:
            print(f"⚠️  Brave search server test failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Brave search server test error: {e}")

def check_environment():
    """Check environment variables"""
    print("\n🔧 Checking environment variables...")
    
    env_vars = {
        "GROQ_API_KEY": "Groq LLM API",
        "OPENAI_API_KEY": "OpenAI GPT API", 
        "ANTHROPIC_API_KEY": "Anthropic Claude API",
        "BRAVE_API_KEY": "Brave Search API",
        "SEGMIND_API_KEY": "Segmind Image API"
    }
    
    env_file = Path(".env")
    if env_file.exists():
        print(f"✅ Found .env file: {env_file.absolute()}")
    else:
        print("⚠️  No .env file found - you may want to create one")
    
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = value[:4] + "***" + value[-4:] if len(value) > 8 else "***"
            print(f"✅ {var}: {masked_value} ({description})")
        else:
            print(f"⚠️  {var}: Not set ({description})")

def main():
    """Main setup function"""
    print("🚀 CrewAI MCP Setup Helper")
    print("=" * 50)
    
    # Check current Node.js
    nodejs_ok = check_current_nodejs()
    
    # Check npm
    npm_ok = check_npm()
    
    # Check environment
    check_environment()
    
    if not nodejs_ok:
        print("\n📋 Next Steps:")
        print("1. Install Node.js v18+ or v20+ LTS")
        print("2. Restart your terminal")
        print("3. Run this script again to verify")
        print("4. Run main.py to test MCP servers")
        
        choice = input("\n❓ Open Node.js download page? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            download_nodejs()
    else:
        print("\n✅ Node.js setup looks good!")
        
        # Test MCP servers if Node.js is OK
        choice = input("\n❓ Test MCP server installation? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            test_mcp_servers()
        
        print("\n🎉 You can now run main.py to use all MCP servers!")
    
    print("\n💡 Tips:")
    print("   - Add API keys to .env file for full functionality")
    print("   - GROQ_API_KEY is recommended for fast LLM responses")
    print("   - BRAVE_API_KEY enables web search capabilities")
    print("   - SEGMIND_API_KEY enables image generation")

if __name__ == "__main__":
    main() 