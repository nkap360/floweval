# Installation Guide

This guide covers setting up Flow Builder for development, testing, or evaluation. Follow these steps to get Flow Builder running on your local machine.

## 🎯 Prerequisites

### System Requirements

**Minimum Requirements:**
- **Operating System**: Windows 10, macOS 10.15, or Ubuntu 18.04+
- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free space (10GB recommended)
- **CPU**: 2 cores (4 cores recommended)

**Required Software:**
- **Node.js**: 18.x or later
- **Python**: 3.9 or later
- **Git**: For version control
- **Modern Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+

### Optional Software

**For Enhanced Features:**
- **Docker**: 20.x or later (for containerized deployment)
- **Docker Compose**: For multi-container setup
- **VS Code**: Recommended IDE with extensions

## 🚀 Quick Installation

### Option 1: Clone and Run (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/nkap360/flowbuilder.git
cd flowbuilder

# 2. Install frontend dependencies
npm install

# 3. Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Start the application
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Start frontend
npm run dev
```

### Option 2: Docker Installation

```bash
# 1. Clone the repository
git clone https://github.com/nkap360/flowbuilder.git
cd flowbuilder

# 2. Copy environment file
cp .env.example .env
# Edit .env with your configuration

# 3. Run with Docker Compose
docker-compose up -d

# 4. Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
```

## 📋 Detailed Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the main repository
git clone https://github.com/nkap360/flowbuilder.git

# Navigate to the project directory
cd flowbuilder

# Verify the structure
ls -la
```

**Expected Structure:**
```
flowbuilder/
├── backend/           # FastAPI backend
├── src/              # React frontend
├── docs/             # Documentation
├── flow_engine/      # Flow templates
├── public/           # Static assets
├── scripts/          # Utility scripts
├── .env.example      # Environment template
├── docker-compose.yml
├── package.json
└── README.md
```

### Step 2: Install Frontend Dependencies

```bash
# Install Node.js dependencies
npm install

# Verify installation
npm --version  # Should be 18.x or later
```

**If you encounter issues:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Step 3: Set Up Backend Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python --version  # Should be 3.9 or later
pip list          # Should show installed packages
```

**Common Python Issues:**

**Issue:** `python: command not found`
```bash
# Try python3 instead
python3 --version
python3 -m venv venv
source venv/bin/activate
```

**Issue:** Permission errors on macOS
```bash
# Install with user permissions
pip install --user -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit the environment file
# Use VS Code, nano, or your preferred editor
code .env  # VS Code
# or
nano .env   # Terminal editor
```

**Required Environment Variables:**

```bash
# Backend Configuration
GOOGLE_API_KEY=your_google_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
DATA_DIR=./data

# Frontend Configuration
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_API_URL=http://localhost:8000

# AI Provider (at least one required)
VITE_DEEPSEEK_API_KEY=your_deepseek_api_key
# Optional: VITE_OPENAI_API_KEY, VITE_GEMINI_API_KEY
```

**Getting API Keys:**

1. **Google Gemini API**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create new API key
   - Copy key to `GOOGLE_API_KEY`

2. **Supabase Setup**:
   - Go to [supabase.com](https://supabase.com/dashboard)
   - Create new project
   - Go to Project Settings → API
   - Copy Project URL and anon public key

3. **DeepSeek API (Optional)**:
   - Visit [DeepSeek Platform](https://platform.deepseek.com)
   - Generate API key
   - Add to `VITE_DEEPSEEK_API_KEY`

### Step 5: Start the Application

#### Method A: Manual Start (Development)

```bash
# Terminal 1: Start Backend
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend (new terminal)
npm run dev
```

**Expected Output:**

**Backend:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
✅ Backend imports successful! All modules loaded correctly.
```

**Frontend:**
```
  VITE v4.x.x  ready in 500 ms

➜  Local:   http://localhost:3001
➜  Network: http://192.168.1.100:3001
```

#### Method B: Docker Start (All-in-One)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 6: Verify Installation

#### Frontend Verification

1. **Open Browser**: Navigate to `http://localhost:3001`
2. **Check Features**:
   - Page loads without errors
   - No console errors (F12 → Console)
   - Navigation works
   - Login/signup page accessible

#### Backend Verification

```bash
# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Test API documentation
curl http://localhost:8000/docs
# Should return API documentation page
```

#### Integration Verification

1. **Test API Connection**:
   - Open frontend in browser
   - Go to Settings → AI Provider Configuration
   - Test connection with your API keys
   - Should show "Connection successful"

2. **Test Core Features**:
   - Create a new dataset
   - Upload a test PDF
   - Generate goldens
   - Review generated content

## 🔧 Development Setup

### VS Code Extensions (Recommended)

Install these extensions for optimal development experience:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-json",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

### Development Commands

```bash
# Frontend Development
npm run dev          # Start development server
npm run build        # Production build
npm run preview      # Preview production build
npm test             # Run tests
npm run lint         # Lint code

# Backend Development
cd backend
uvicorn main:app --reload           # Start development server
pytest                             # Run tests
pytest --cov=backend                # Run tests with coverage
python -m flake8 .                  # Lint Python code

# Validation
python scripts/validate_templates.py  # Validate flow templates
```

### Code Quality Tools

**Python Linting:**
```bash
pip install flake8 black pytest pytest-cov

# Format code
black .

# Lint code
flake8 .

# Run tests with coverage
pytest --cov=backend --cov-report=html
```

**JavaScript/TypeScript Linting:**
```bash
# Already included in package.json
npm run lint
npm run type-check
```

## 🐳 Docker Installation (Advanced)

### Production Docker Setup

```bash
# Build backend image
docker build -t flowbuilder-backend -f Dockerfile .

# Build frontend image
docker build -t flowbuilder-frontend -f Dockerfile.frontend .

# Run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### Custom Docker Configuration

**Environment File for Docker:**
```bash
# .env.docker
GOOGLE_API_KEY=your_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_key
VITE_API_URL=http://backend:8000
```

**Custom docker-compose.yml:**
```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3001:80"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_SUPABASE_URL=${SUPABASE_URL}
      - VITE_SUPABASE_ANON_KEY=${SUPABASE_KEY}
```

## 🔍 Troubleshooting

### Common Installation Issues

#### Node.js Issues

**Issue:** `npm install` fails with permission errors
```bash
# Solution 1: Use npx
npx npm install

# Solution 2: Clear npm cache
npm cache clean --force
rm -rf node_modules
npm install
```

**Issue:** Node.js version too old
```bash
# Check current version
node --version

# Update Node.js (using nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

#### Python Issues

**Issue:** Python command not found
```bash
# On macOS, install Python 3
brew install python3

# On Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# On Windows, download from python.org
```

**Issue:** Virtual environment problems
```bash
# Remove and recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Port Issues

**Issue:** Port 3001 or 8000 already in use
```bash
# Find process using port
lsof -i :3001  # macOS/Linux
netstat -ano | findstr :3001  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux

# Or use different ports
npm run dev -- --port 3002
uvicorn main:app --port 8001
```

#### Environment Variable Issues

**Issue:** API keys not working
```bash
# Verify environment variables are loaded
printenv | grep GOOGLE_API_KEY
printenv | grep VITE_API_KEY

# Check .env file syntax
cat .env
```

**Issue:** CORS errors in browser
```bash
# Update backend CORS settings in main.py
# Add your frontend URL to allow_origins
```

### Verification Commands

```bash
# Check all services are running
curl http://localhost:8000/health  # Backend
curl http://localhost:3001        # Frontend

# Check environment variables
echo "Frontend: $VITE_API_URL"
echo "Backend: $GOOGLE_API_KEY"

# Check Python packages
pip list | grep fastapi
pip list | grep uvicorn

# Check Node packages
npm list --depth=0
```

### Performance Issues

**Slow startup:**
- Check available RAM and CPU
- Close unnecessary applications
- Consider using SSD storage

**Memory issues:**
```bash
# Check memory usage
top  # macOS/Linux
Task Manager  # Windows

# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
npm run dev
```

## 📚 Next Steps

After successful installation:

1. **Read the User Guide**: [Core Features Guide](../user-guide/core-features.md)
2. **Try the Quick Start**: [Quick Start Guide](quick-start.md)
3. **Explore Features**: Test PDF processing and golden generation
4. **Join the Community**: GitHub Discussions for questions

### Learning Resources

- [Core Features Documentation](../user-guide/core-features.md)
- [Chatbot Features Guide](../user-guide/chatbot.md)
- [Flow Builder Guide](../user-guide/flow-builder.md)
- [API Reference](../developer/api-reference.md)

### Getting Help

- **GitHub Issues**: [Report bugs](https://github.com/nkap360/flowbuilder/issues)
- **Discussions**: [Community support](https://github.com/nkap360/flowbuilder/discussions)
- **Documentation**: [Complete docs](../README.md)

---

**Congratulations! 🎉 Flow Builder is now installed and ready to use.**

---

**Last Updated:** December 3, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅