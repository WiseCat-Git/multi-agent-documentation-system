# Multi-Agent Documentation System Setup Script
# Run this with: .\setup.ps1

Write-Host "🚀 Setting up Multi-Agent Documentation System..." -ForegroundColor Cyan

# Check if venv exists and is activated
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Create requirements.txt
Write-Host "Creating requirements.txt..." -ForegroundColor Yellow
@"
# Core AI Framework
crewai==0.86.0
crewai-tools==0.17.0

# LLM and AI
openai==1.54.3
langchain==0.3.7
langchain-openai==0.2.8
langchain-community==0.3.7

# Web Interface
streamlit==1.39.0

# Document Processing
python-docx==1.1.2
PyPDF2==3.0.1
openpyxl==3.1.5
pandas==2.2.3

# Environment Management
python-dotenv==1.0.1

# Additional Tools
requests==2.32.3
beautifulsoup4==4.12.3
lxml==5.3.0
"@ | Out-File -FilePath requirements.txt -Encoding utf8

# Install dependencies
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
# OpenAI API Key (Required)
# REPLACE WITH YOUR NEW KEY - The one you shared should be regenerated!
OPENAI_API_KEY=your-new-openai-key-here

# Serper API Key (Optional - for enhanced web research)
SERPER_API_KEY=your-serper-key-here
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "⚠️  IMPORTANT: Edit .env file and add your API keys!" -ForegroundColor Red
} else {
    Write-Host ".env file already exists, skipping..." -ForegroundColor Green
}

# Check if main.py exists
if (-not (Test-Path "main.py")) {
    Write-Host "⚠️  main.py not found! Please create it or copy from the artifacts." -ForegroundColor Red
} else {
    Write-Host "✓ main.py found" -ForegroundColor Green
}

# Check if app.py exists
if (-not (Test-Path "app.py")) {
    Write-Host "⚠️  app.py not found! Please create it or copy from the artifacts." -ForegroundColor Red
} else {
    Write-Host "✓ app.py found" -ForegroundColor Green
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Make sure main.py and app.py are in this directory"
Write-Host "2. Edit .env and add your API keys (regenerate them first!)"
Write-Host "3. Run: streamlit run app.py"
Write-Host "`nFor help, see README.md" -ForegroundColor Yellow