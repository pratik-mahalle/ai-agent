"""
Setup script for Cloud-Native AI Agent

This script helps set up the environment and install dependencies.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    print("📝 Creating .env file...")
    
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Linux Foundation Credentials (Optional)
LINUX_FOUNDATION_USERNAME=your_username
LINUX_FOUNDATION_PASSWORD=your_password

# CNCF Credentials (Optional)
CNCF_USERNAME=your_username
CNCF_PASSWORD=your_password

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO

# Database Configuration (for future use)
DATABASE_URL=sqlite:///cloud_native_agent.db

# Web Scraping Configuration
REQUEST_TIMEOUT=30
MAX_RETRIES=3
USER_AGENT=Mozilla/5.0 (compatible; CloudNativeAIAgent/1.0)

# Cache Configuration
CACHE_EXPIRY_HOURS=6
MAX_CACHE_SIZE=1000
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print("✅ .env file created")
    print("⚠️  Please edit .env file and add your OpenAI API key")

def create_directories():
    """Create necessary directories."""
    directories = ["data", "logs", "exports"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")

def run_tests():
    """Run basic tests."""
    print("🧪 Running tests...")
    
    try:
        subprocess.check_call([sys.executable, "test_agent.py"])
        print("✅ Tests completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Tests failed: {e}")
        print("This might be due to missing API keys")

def main():
    """Main setup function."""
    print("🚀 Cloud-Native AI Agent Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Run tests
    run_tests()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run 'streamlit run app.py' to start the application")
    print("3. Open your browser and go to http://localhost:8501")

if __name__ == "__main__":
    main() 