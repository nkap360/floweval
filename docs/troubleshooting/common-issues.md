# Common Issues & Solutions

This guide covers frequently encountered problems and their solutions when installing, running, or developing with Flow Builder.

## 🔍 Quick Issue Finder

- [Installation Issues](#installation-issues)
- [Runtime Issues](#runtime-issues)
- [Performance Issues](#performance-issues)
- [API & Integration Issues](#api--integration-issues)
- [Frontend Issues](#frontend-issues)
- [Backend Issues](#backend-issues)
- [Database Issues](#database-issues)
- [Deployment Issues](#deployment-issues)

---

## 🚀 Installation Issues

### Node.js & npm Problems

**Issue**: `npm install` fails with permission errors
```bash
Error: EACCES: permission denied
```

**Solutions:**
```bash
# Option 1: Use npx (temporary)
npx npm install

# Option 2: Fix npm permissions
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH

# Option 3: Use Node Version Manager (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

**Issue**: Node.js version too old
```bash
Error: Node.js version 16.x is not supported. Please use Node.js 18.x or higher.
```

**Solution:**
```bash
# Install nvm and update Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
node --version  # Should show 18.x or higher
```

**Issue**: npm install hangs or very slow
```bash
Solution:
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use different registry if needed
npm install --registry https://registry.npmjs.org/
```

### Python & Virtual Environment Issues

**Issue**: `python: command not found`
```bash
# On Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# On macOS (with Homebrew)
brew install python3

# On Windows
# Download from python.org and ensure "Add to PATH" is checked
```

**Issue**: Virtual environment activation fails
```bash
# Verify venv exists
ls backend/venv/

# Recreate if corrupted
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

**Issue**: pip install requirements fails
```bash
# Update pip first
pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir -r requirements.txt

# If specific package fails, try installing individually
pip install fastapi uvicorn
pip install python-multipart
# ... and so on
```

---

## 🏃 Runtime Issues

### Port Conflicts

**Issue**: Port 3001 or 8000 already in use
```bash
Error: listen EADDRINUSE :::3001
```

**Solutions:**
```bash
# Find process using the port
# macOS/Linux:
lsof -i :3001
lsof -i :8000

# Windows:
netstat -ano | findstr :3001
netstat -ano | findstr :8000

# Kill the process
kill -9 <PID>  # macOS/Linux

# Or use different ports
npm run dev -- --port 3002
uvicorn main:app --port 8001
```

### Environment Variable Issues

**Issue**: API keys not working or not found
```bash
# Check if environment variables are loaded
printenv | grep -E "(GOOGLE|VITE|SUPABASE)"

# Verify .env file syntax
cat .env

# Test API key validity
curl -H "x-goog-api-key: YOUR_KEY" \
     "https://generativelanguage.googleapis.com/v1/models"
```

**Issue**: CORS errors in browser
```bash
Error: Access to fetch at 'http://localhost:8000/api/...' has been blocked by CORS policy
```

**Solution:**
```python
# In backend/main.py, update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://localhost:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Application Startup Failures

**Issue**: Backend fails to start with import errors
```bash
Error: ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Verify fastapi is installed
pip list | grep fastapi

# Reinstall if missing
pip install fastapi
```

**Issue**: Frontend fails to start with TypeScript errors
```bash
Error: TypeScript compilation failed
```

**Solutions:**
```bash
# Check Node.js version
node --version  # Must be 18.x or higher

# Clear TypeScript cache
rm -rf .vite

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors in specific files
npx tsc --noEmit
```

---

## ⚡ Performance Issues

### Slow Startup

**Issue**: Application takes >30 seconds to start

**Solutions:**
```bash
# Check available RAM
free -h  # Linux
# or check Activity Monitor (macOS) / Task Manager (Windows)

# Close unnecessary applications
# Use SSD storage if available
# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
npm run dev
```

**Issue**: PDF processing very slow
```bash
# Check PDF file size
ls -lh your-large-pdf.pdf

# For large PDFs (>50MB), consider:
# 1. Splitting into smaller files
# 2. Using more powerful machine
# 3. Implementing batch processing
```

### Memory Issues

**Issue**: Out of memory errors
```bash
JavaScript heap out of memory
```

**Solutions:**
```bash
# Increase Node.js memory
export NODE_OPTIONS="--max-old-space-size=4096"

# For backend, increase Python process limits
ulimit -n 65536  # Increase file descriptor limit

# Monitor memory usage
# Linux/macOS:
top -p $(pgrep node)
top -p $(pgrep python)
```

**Issue**: Browser becomes unresponsive
```bash
# Solutions:
# 1. Close other tabs
# 2. Restart browser
# 3. Check memory leaks in Chrome DevTools
# 4. Use lighter browser for testing
```

---

## 🔌 API & Integration Issues

### AI Provider Connection Issues

**Issue**: Google Gemini API not working
```bash
# Test API key manually
curl -H "Content-Type: application/json" \
     -H "x-goog-api-key: YOUR_KEY" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Common fixes:
# 1. Check API key is correct
# 2. Verify API key has quota
# 3. Check network connectivity
# 4. Try different model (gemini-1.5-flash)
```

**Issue**: DeepSeek API not working
```bash
# Test DeepSeek API
curl -H "Authorization: Bearer YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}' \
     "https://api.deepseek.com/v1/chat/completions"
```

**Issue**: Supabase connection fails
```bash
# Test Supabase connection
curl -H "apikey: YOUR_ANON_KEY" \
     -H "Authorization: Bearer YOUR_ANON_KEY" \
     "https://YOUR_PROJECT.supabase.co/rest/v1/"

# Common fixes:
# 1. Check project URL is correct
# 2. Verify anon key is valid
# 3. Check RLS policies if data insertion fails
# 4. Ensure project is not paused
```

### API Response Issues

**Issue**: AI responses are empty or truncated
```bash
# Solutions:
# 1. Check API key quota
# 2. Increase max_tokens parameter
# 3. Check for content filtering
# 4. Try simpler prompts
```

**Issue**: API rate limiting
```bash
# Solutions:
# 1. Implement request delays
# 2. Use different API keys
# 3. Upgrade API plan
# 4. Cache responses when possible
```

---

## 🎨 Frontend Issues

### React/TypeScript Issues

**Issue**: Component not updating or state not changing
```bash
# Check React DevTools for state changes
# Verify useEffect dependencies
# Look for infinite re-renders in console
# Check for stale closures
```

**Issue**: Routing not working
```bash
# Solutions:
# 1. Check BrowserRouter configuration
# 2. Verify route paths
# 3. Check for 404 errors in console
# 4. Ensure server supports SPA routing
```

**Issue**: Tailwind CSS styles not applying
```bash
# Check if Tailwind is configured correctly
# Verify build process includes Tailwind
# Check for CSS conflicts
# Inspect elements for applied styles
```

### Browser Compatibility

**Issue**: Application not working in specific browser
```bash
# Check browser compatibility:
# Chrome 90+: Full support
# Firefox 88+: Full support
# Safari 14+: Full support
# Edge 90+: Full support

# Solutions:
# 1. Update browser to latest version
# 2. Check for polyfill issues
# 3. Test in different browser
# 4. Check browser console for errors
```

### UI/UX Issues

**Issue**: Chatbot not displaying properly
```bash
# Solutions:
# 1. Check if ReactMarkdown is installed
npm list react-markdown

# 2. Verify highlight.js is loaded
# Check index.html for highlight.js script

# 3. Check browser console for CSS/JS errors
# 4. Clear browser cache (Ctrl+Shift+R)
```

**Issue**: PDF viewer showing plain text
```bash
# Check if pdfProcessor.ts is loaded
# Verify PDF.js library is available
# Check for console errors during PDF processing
# Ensure PDF is text-based (not scanned images)
```

---

## 🖥️ Backend Issues

### FastAPI Issues

**Issue**: API endpoints not responding
```bash
# Check if server is running
curl http://localhost:8000/health

# Check API documentation
curl http://localhost:8000/docs

# Common fixes:
# 1. Verify uvicorn is running
# 2. Check for import errors
# 3. Verify port isn't blocked
# 4. Check firewall settings
```

**Issue**: CORS errors persist
```python
# Ensure this is in backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Python Module Issues

**Issue**: Import errors for backend modules
```bash
Error: ModuleNotFoundError: No module named 'backend.core.actions'
```

**Solutions:**
```bash
# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run from correct directory
cd backend
python -m uvicorn main:app --reload

# Check module structure
ls backend/core/actions.py
```

**Issue**: Database connection issues
```bash
# Check Supabase credentials
# Test connection manually
curl -H "apikey: YOUR_KEY" \
     "https://YOUR_PROJECT.supabase.co/rest/v1/"

# Common fixes:
# 1. Verify URL and keys
# 2. Check if project is active
# 3. Test RLS policies
# 4. Check network connectivity
```

---

## 🗄️ Database Issues

### Supabase Connection Issues

**Issue**: Cannot connect to Supabase
```bash
# Test connection
curl -H "apikey: YOUR_ANON_KEY" \
     -H "Authorization: Bearer YOUR_ANON_KEY" \
     "https://YOUR_PROJECT.supabase.co/rest/v1/"

# Check project status at supabase.com/dashboard
# Verify project is not paused
# Check API key permissions
```

**Issue**: Data not saving to database
```bash
# Check RLS (Row Level Security) policies
# In Supabase SQL Editor:
SELECT * FROM pg_policies WHERE tablename = 'your_table';

# Common fixes:
# 1. Add RLS policy for inserts
# 2. Check user authentication
# 3. Verify table exists
# 4. Check column types match data
```

**Issue**: Authentication not working
```bash
# Check Supabase auth configuration
# Verify email templates are configured
# Test with a simple auth call
# Check CORS settings in Supabase dashboard
```

### Local Database Issues

**Issue**: Local database not starting
```bash
# Check if database service is running
# For PostgreSQL:
sudo systemctl status postgresql

# Check connection string
psql postgresql://user:password@localhost:5432/dbname
```

---

## 🚀 Deployment Issues

### Docker Deployment Issues

**Issue**: Docker build fails
```bash
# Check Docker logs
docker-compose logs backend
docker-compose logs frontend

# Common fixes:
# 1. Check Dockerfile syntax
# 2. Verify dependencies exist
# 3. Check for missing .dockerignore
# 4. Rebuild without cache
docker-compose build --no-cache
```

**Issue**: Containers not communicating
```bash
# Check network configuration
docker network ls
docker network inspect flowbuilder_default

# Verify service names in docker-compose.yml
# Check if ports are correctly exposed
```

### Cloud Deployment Issues

**Issue**: Application crashes on deployment
```bash
# Check environment variables
printenv | grep -E "(VITE|GOOGLE|SUPABASE)"

# Common fixes:
# 1. Verify all required env vars are set
# 2. Check API keys are correct
# 3. Ensure compatible Node.js/Python versions
# 4. Check resource limits (memory/CPU)
```

**Issue**: SSL/HTTPS not working
```bash
# Solutions:
# 1. Check SSL certificate configuration
# 2. Verify DNS settings
# 3. Check if port 443 is open
# 4. Test with curl -v https://yourdomain.com
```

### Leapcell Deployment Issues

**Issue**: Deployment fails on Leapcell
```bash
# Check Leapcell deployment logs
# Verify leapcell.yaml configuration
# Check build logs for specific errors

# Common fixes:
# 1. Ensure all environment variables are set
# 2. Check for missing dependencies
# 3. Verify Docker configuration
# 4. Check resource limits
```

---

## 🔧 Debugging Techniques

### General Debugging

**1. Check Console Logs**
```bash
# Frontend: F12 → Console tab
# Backend: Terminal where server is running
# Docker: docker-compose logs -f service-name
```

**2. Network Debugging**
```bash
# Frontend: F12 → Network tab
# Backend: Check request/response logs
# Test with curl for isolated testing
```

**3. Environment Debugging**
```bash
# Check environment variables
printenv | grep -E "(NODE|PYTHON|PATH)"

# Python environment
which python
pip list
python --version

# Node.js environment
which node
npm list --depth=0
node --version
```

### Performance Debugging

**Frontend Performance:**
```bash
# Chrome DevTools → Performance tab
# Check for:
# - Long-running tasks
# - Memory leaks
# - Slow network requests
# - JavaScript execution time
```

**Backend Performance:**
```bash
# Monitor CPU and memory
top -p $(pgrep python)

# Profile Python code
python -m cProfile your_script.py

# Check database query performance
# Add logging to measure query times
```

---

## 🆘 Getting Help

### Self-Service Resources

1. **Check Console Errors**: Always start with browser and terminal logs
2. **Review This Guide**: Look for similar issues
3. **Search GitHub Issues**: Check if others have similar problems
4. **Use Chatbot**: Try Document Space for implementation questions

### Reporting Issues

When reporting an issue, include:

**Essential Information:**
- Operating system and version
- Node.js and Python versions
- Browser and version
- Error messages (full stack traces)
- Steps to reproduce
- Expected vs actual behavior

**Optional but Helpful:**
- Configuration files (remove sensitive data)
- Screenshots or screen recordings
- Logs from console or terminal
- System specifications

**Example Issue Report:**
```
**Description**: PDF upload fails with 500 error
**Environment**:
- OS: macOS 13.0
- Node.js: 18.17.0
- Python: 3.9.16
- Browser: Chrome 119.0

**Steps to reproduce**:
1. Go to Datasets page
2. Create new dataset
3. Click "Upload Files"
4. Select PDF file
5. Click Upload

**Expected**: PDF processes successfully
**Actual**: 500 error, console shows "Internal Server Error"

**Error message**:
{"detail": "PDF processing failed: File format not supported"}

**Additional info**:
Works with text files, PDF is 5MB, text-based document
```

### Community Support Channels

- **GitHub Issues**: [Report bugs](https://github.com/nkap360/flowbuilder/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/nkap360/flowbuilder/discussions)
- **Documentation**: [Complete docs](../README.md)

---

**Remember**: Most issues have simple solutions. Start with the basics (check logs, verify configuration, test components individually) before diving into complex debugging.

---

**Last Updated**: December 3, 2025
**Version**: 1.0.0
**Status**: Community-Maintained ✅