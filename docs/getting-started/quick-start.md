# Quick Start Guide

Get Flow Builder running in 5 minutes with this streamlined setup guide. Perfect for testing, evaluation, or quick development.

## 🚀 5-Minute Quick Start

### Prerequisites

- **Node.js 18+** and **Python 3.9+**
- **Git** installed
- **Modern web browser**

### Step 1: Clone & Install (2 minutes)

```bash
# Clone and enter directory
git clone https://github.com/nkap360/flowbuilder.git
cd flowbuilder

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### Step 2: Configure API Keys (2 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file (add your API keys)
# You need at least one AI provider key:
```

**Required .env Configuration:**
```bash
# Minimum working setup
GOOGLE_API_KEY=your_google_gemini_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Frontend
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_key
VITE_API_URL=http://localhost:8000
```

**Getting Keys (1 minute each):**
- **Google Gemini**: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **Supabase**: [supabase.com/dashboard](https://supabase.com/dashboard) → New Project → Settings → API

### Step 3: Start Application (1 minute)

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Start frontend (new terminal)
npm run dev
```

### Step 4: Test & Verify (30 seconds)

1. **Open Frontend**: http://localhost:3001
2. **Verify Backend**: http://localhost:8000/health
3. **Test Features**:
   - Upload a PDF file
   - Generate golden datasets
   - Try the chatbot

## 🎯 What You Can Do Immediately

### 1. Process PDF Documents

**Upload any PDF and see structured extraction:**

1. Click "Datasets" in sidebar
2. Create new dataset
3. Upload PDF file
4. See structured text with headings, lists, page breaks

**Expected Result:**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## DOCUMENT TITLE

Content extracted with proper formatting...
```

### 2. Generate Golden Datasets

**Create Q&A pairs for AI evaluation:**

1. In Flow Builder, load "PDF to Golden Dataset" template
2. Upload your PDF
3. Execute flow
4. AI generates question-answer pairs
5. Review and export results

**Sample Output:**
```json
{
  "input": "What is the purpose of this document?",
  "expected_output": "This document outlines the procedures for...",
  "context": ["Extracted relevant text..."]
}
```

### 3. Use AI Chatbot

**Three different chat spaces:**

1. **Default Space**: General AI assistance
2. **Document Space**: AI with full codebase knowledge
3. **Web Space**: Web search + codebase (requires SERPER_API_KEY)

**Test Questions:**
- *Default*: "Write a poem about AI"
- *Document*: "How do I add a new AI provider?"
- *Web*: "What are React best practices for 2025?"

## 🔧 Alternative: Docker Quick Start

If you have Docker installed, use this even faster method:

```bash
# Clone and configure
git clone https://github.com/nkap360/flowbuilder.git
cd flowbuilder
cp .env.example .env
# Edit .env with your API keys

# Start everything
docker-compose up -d

# Access application
# Frontend: http://localhost
# Backend: http://localhost:8000/health
```

## ⚡ Testing Your Setup

### Quick Functionality Test

Run these commands to verify everything works:

```bash
# Test backend health
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# Test frontend access
curl http://localhost:3001
# Should return HTML page
```

### Browser Test Checklist

- [ ] Frontend loads at http://localhost:3001
- [ ] No console errors (F12 → Console)
- [ ] Can navigate between pages
- [ ] Settings page accessible
- [ ] Can create new dataset
- [ ] PDF upload works
- [ ] Chatbot responds to messages

### Sample Workflow Test

1. **Create Dataset**: Datasets → New Dataset
2. **Upload PDF**: Upload any PDF file
3. **Generate Goldens**: Use Flow Builder template
4. **Review Results**: Check generated Q&A pairs
5. **Export Data**: Download JSON file

## 🛠️ Common Quick Issues & Fixes

### Port Already in Use

```bash
# Find what's using port 3001 or 8000
lsof -i :3001  # macOS/Linux
netstat -ano | findstr :3001  # Windows

# Kill the process or use different ports
npm run dev -- --port 3002
uvicorn main:app --port 8001
```

### API Key Issues

```bash
# Test your API key (replace with your key)
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY"

# If this works, your key is valid
```

### Python Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### npm Install Issues

```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📚 What to Try Next

### Explore Features

1. **PDF Processing**: Upload different PDF types (technical docs, reports, manuals)
2. **Flow Builder**: Create custom workflows
3. **Golden Review**: Use human-in-the-loop quality control
4. **Chatbot Spaces**: Try all three chat modes
5. **API Integration**: Test REST endpoints

### Create Your First Workflow

**Simple "Document Processor" Workflow:**

1. Open Flow Builder
2. Add nodes: Start → Upload PDF → Generate Goldens → Export
3. Connect nodes
4. Execute with a PDF file
5. See results

**Advanced "Quality Control" Workflow:**

1. Load "PDF to Goldens with Review" template
2. Upload PDF
3. Generate goldens
4. Review and edit generated content
5. Export validated dataset

### Test with Sample Data

**Sample PDFs to try:**
- Technical specifications
- User manuals
- Research papers
- Legal documents
- Process documentation

**Expected behavior for each:**
- Headings preserved as `## Section Title`
- Lists converted to bullet points
- Page separators with clear markers
- Context extraction works for highlighting

## 🔍 Getting Help Quickly

### Self-Service Resources

1. **Use Document Space Chatbot**: Ask about implementation
2. **Check Console**: F12 → Console for errors
3. **Review Logs**: Backend terminal for API issues
4. **Browse Documentation**: [docs/README.md](../README.md)

### Common Issues Solutions

**"Frontend not loading"**:
- Check if backend is running on port 8000
- Verify `VITE_API_URL=http://localhost:8000` in .env
- Clear browser cache (Ctrl+Shift+R)

**"API not responding"**:
- Check environment variables in .env
- Verify API keys are valid and have quota
- Check backend terminal for error messages

**"PDF upload not working"**:
- Ensure backend is running
- Check file size (PDFs under 50MB work best)
- Verify browser console for errors

### Community Support

- **GitHub Issues**: [Report problems](https://github.com/nkap360/flowbuilder/issues)
- **Discussions**: [Ask questions](https://github.com/nkap360/flowbuilder/discussions)
- **Chatbot**: Use Document space for implementation questions

## 🎊 Success!

You now have Flow Builder running locally! Here's what to explore:

### Immediate Next Steps

1. **Upload a PDF** and see the structured extraction
2. **Generate goldens** from your document
3. **Try the chatbot** in all three spaces
4. **Create a custom flow** for your specific use case
5. **Review and export** your first dataset

### Learning Path

**Beginner (First 30 minutes):**
- ✅ Basic PDF upload and processing
- ✅ Generate your first golden dataset
- ✅ Try the chatbot features

**Intermediate (First hour):**
- 🔄 Create custom workflows
- 🔄 Use golden review system
- 🔄 Export and use datasets

**Advanced (Next session):**
- 📚 Read full [User Guide](../user-guide/core-features.md)
- 📚 Explore [API Reference](../developer/api-reference.md)
- 📚 Learn about [Deployment](../deployment/overview.md)

### Quick Reference Commands

```bash
# Start development servers
npm run dev                          # Frontend (port 3001)
cd backend && uvicorn main:app --reload  # Backend (port 8000)

# Useful checks
curl http://localhost:8000/health   # Backend status
npm run build                       # Production build
npm test                            # Run tests
```

---

**🎉 Congratulations! You're ready to use Flow Builder!**

---

**Last Updated:** December 3, 2025
**Version**: 1.0.0
**Status**: Quick Start Ready ✅