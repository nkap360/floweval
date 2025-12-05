# Frequently Asked Questions (FAQ)

Common questions and answers about Flow Builder.

## 📋 Quick Navigation

- [General](#general)
- [Installation & Setup](#installation--setup)
- [Features & Usage](#features--usage)
- [AI Providers](#ai-providers)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [Development](#development)

---

## 🌟 General

### What is Flow Builder?

Flow Builder is a production-grade application for creating and executing AI evaluation workflows. It combines dataset management, PDF annotation, golden review systems, and visual flow building to streamline the entire AI development lifecycle.

### Who is Flow Builder for?

- **ML Engineers** building evaluation datasets
- **Data Scientists** creating training data
- **AI Teams** needing quality assurance workflows
- **Developers** building AI applications
- **QA Teams** reviewing AI-generated content

### Is Flow Builder open source?

Yes! Flow Builder is open source under the MIT License. You can use it commercially, modify it, and contribute back to the project.

### What's included?

- Visual flow builder with drag-and-drop interface
- PDF processing and annotation tools
- Dataset and golden management
- AI-powered Q&A generation
- Human-in-the-loop review system
- Multiple AI provider support (OpenAI, Google Gemini, DeepSeek, Custom)
- Pre-built flow templates
- Export capabilities (JSON, CSV)

---

## 🚀 Installation & Setup

### What are the system requirements?

**Minimum:**
- Node.js 18+ and npm 9+
- Python 3.9+
- 4GB RAM
- 2GB disk space

**Recommended:**
- Node.js 20+ and npm 10+
- Python 3.11+
- 8GB RAM
- 5GB disk space

### Do I need a Supabase account?

**For development:** Optional - can use local storage  
**For production:** Recommended for multi-user deployments

You can start with local storage and migrate to Supabase later if needed.

### Which AI provider should I use?

**Quick start:** Google Gemini (generous free tier)  
**Production:** OpenAI (most reliable)  
**Custom needs:** Any OpenAI-compatible API (Custom_openai_endpoint)  
**Budget-conscious:** DeepSeek (cost-effective)

You can configure multiple providers and switch between them.

### How do I get API keys?

**Google Gemini:**
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create new project and generate key

**OpenAI:**
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Go to API keys section
4. Create new secret key

**DeepSeek:**
1. Visit https://platform.deepseek.com/
2. Create account
3. Navigate to API keys
4. Generate new key

### Can I use Flow Builder without any API keys?

No, AI providers require API keys for generating content. However, you can:
- Use the PDF annotation features manually
- Create datasets and goldens manually
- Use the review system
- Build and visualize flows (without execution)

---

## 💡 Features & Usage

### How do I create my first dataset?

1. Click "Datasets" in navigation
2. Click "Create Dataset"
3. Fill in name, description, use case
4. Upload PDF documents
5. Generate goldens using AI or manually
6. Review and approve goldens
7. Export dataset

See [Quick Start Guide](../getting-started/quick-start.md) for detailed walkthrough.

### What file formats are supported?

**Document upload:**
- PDF (text-based preferred)
- TXT (plain text)
- MD (Markdown)
- JSON (structured data)
- CSV (tabular data)

**Export formats:**
- JSON (DeepEval compatible)
- CSV (spreadsheet-friendly)
- Markdown (documentation)

**Note:** Scanned PDFs require OCR (not currently supported).

### How does the golden review workflow work?

1. AI generates Q&A pairs from documents
2. Review session is created automatically
3. Human reviewer approves, edits, or rejects each golden
4. Changes are tracked with full provenance
5. Approved goldens are added to dataset
6. Dataset can be exported with metadata

Keyboard shortcuts: A (approve), E (edit), R (reject)

### Can I edit AI-generated goldens?

Yes! The review system allows you to:
- Edit questions for clarity
- Improve answers for accuracy
- Add or modify context
- Track all changes with timestamps
- See before/after versions

### How many goldens should I create?

**Minimum viable:**
- Chatbot: 50-100 goldens
- RAG system: 100-200 goldens
- QA system: 200-500 goldens
- Production AI: 500+ goldens

**Best practices:**
- Start small (20-30 goldens)
- Test and iterate
- Scale up gradually
- Focus on quality over quantity

### Can I use multiple AI providers?

Yes! Flow Builder supports:
- Google Gemini
- OpenAI (GPT-4, GPT-3.5)
- DeepSeek
- Custom OpenAI-compatible endpoints (Custom_openai_endpoint)

Configure all providers in Settings and switch between them as needed.

---

## 🤖 AI Providers

### Which model should I use?

**For accuracy:**
- OpenAI GPT-4: Best overall quality
- Google Gemini Pro: Strong performance

**For speed:**
- OpenAI GPT-3.5 Turbo: Fast responses
- DeepSeek: Cost-effective and fast

**For specific domains:**
- Use fine-tuned models when available
- Test different models for your use case

### How much do API calls cost?

**Approximate costs per 1000 goldens:**

| Provider | Cost | Notes |
|----------|------|-------|
| Google Gemini | $5-10 | Free tier available |
| OpenAI GPT-4 | $20-40 | Higher quality |
| OpenAI GPT-3.5 | $2-5 | Faster, cheaper |
| DeepSeek | $1-3 | Very cost-effective |

Actual costs vary based on document length and prompt complexity.

### Can I use my own AI model?

Yes! If your model has an OpenAI-compatible API:

1. Go to Settings → AI Provider Configuration
2. Add custom provider (Custom_openai_endpoint)
3. Enter your API endpoint and key
4. Select your custom model

### What if my API key stops working?

**Common issues:**
1. **Quota exceeded:** Check usage on provider dashboard
2. **Key expired:** Generate new key
3. **Invalid key:** Verify you copied full key correctly
4. **Rate limited:** Wait or upgrade plan

Test keys in Settings → AI Provider Configuration.

---

## 🔧 Troubleshooting

### Frontend won't start

**Check Node version:**
```bash
node --version  # Should be 18+
npm --version   # Should be 9+
```

**Try:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend won't start

**Check Python version:**
```bash
python --version  # Should be 3.9+
```

**Try:**
```bash
cd backend
pip install --upgrade -r requirements.txt
uvicorn main:app --reload
```

### PDF upload fails

**Possible causes:**
- File too large (>50MB)
- PDF is scanned (no text layer)
- CORS issues (check backend logs)
- Missing permissions

**Solutions:**
1. Compress large PDFs
2. Use text-based PDFs only
3. Check browser console for errors
4. Verify backend is running

### Goldens not generating

**Check:**
1. AI provider configured correctly
2. API key is valid and has quota
3. Document has extractable text
4. Backend logs for errors

**Try:**
- Test with different AI provider
- Use shorter documents first
- Check API provider status page

### Web search not working in chatbot

**Requirements:**
- `VITE_SERPER_API_KEY` environment variable set
- Serper API account (2,500 free searches/month)
- Internet connection

**Verify:**
```bash
# Check if key is set
echo $VITE_SERPER_API_KEY

# Test Serper API directly
curl -H "X-API-KEY: your_key" \
     https://google.serper.dev/search?q=test
```

### Memory issues or slow performance

**Optimize:**
- Close unused browser tabs
- Restart dev servers regularly
- Clear browser cache
- Use lighter AI models
- Process smaller batches

---

## 🚀 Deployment

### Can I deploy Flow Builder to production?

Yes! Flow Builder is production-ready. Recommended platforms:
- **Leapcell.io** (recommended, one-click deploy)
- **Docker** (self-hosted)
- **AWS/Azure/GCP** (enterprise)

See [Deployment Guide](../deployment/overview.md) for details.

### How do I deploy to Leapcell?

1. Click the "Deploy to Leapcell" button in README
2. Connect your GitHub repository
3. Add environment variables (API keys)
4. Click "Deploy"
5. Wait for build to complete (~5 minutes)

Full guide: [Leapcell Deployment](../deployment/leapcell.md)

### Do I need a database for production?

**Recommended:** Yes, use Supabase for:
- Multi-user support
- Data persistence
- Workspace collaboration
- Backup and recovery

**Alternative:** File-based storage works for:
- Single-user deployments
- Development environments
- Small-scale usage

### How do I backup my data?

**Local development:**
- Export datasets regularly from UI
- Copy data/ directory
- Backup .env file (securely)

**Production with Supabase:**
- Automatic daily backups
- Point-in-time recovery
- Export via Supabase dashboard

### What about security in production?

**Essential:**
- Use HTTPS (SSL certificates)
- Store API keys in environment variables
- Enable Supabase RLS (Row Level Security)
- Use strong JWT secrets
- Regular security updates

See [Security Guide](../deployment/security.md) for complete checklist.

---

## 💻 Development

### How do I add a new action?

1. Create file in `backend/actions/`
2. Register action with decorator
3. Implement handler function
4. Add to ACTION_MODULES in main.py
5. Test and document

See [Developer Guide](developer/DEVELOPER.md#adding-new-actions) for detailed steps.

### Can I customize the UI?

Yes! The UI is built with:
- React + TypeScript
- TailwindCSS (easy styling)
- Lucide icons
- Modular components

Modify files in `components/` and `pages/` directories.

### How do I create a flow template?

1. Build flow in Flow Builder UI
2. Test execution thoroughly
3. Export flow definition
4. Create template file in `flow_engine/templates/`
5. Add to template registry
6. Document usage

See [Flow Templates Guide](../../flow_engine/README.md).

### Can I integrate other AI providers?

Yes! To add a new provider:

**Frontend:**
1. Update `services/aiService.ts`
2. Add provider configuration in Settings
3. Handle provider-specific auth

**Backend:**
1. Add client library to requirements.txt
2. Create provider adapter
3. Update action handlers

### How do I run tests?

**Frontend:**
```bash
npm test                    # All tests
npm test -- --watch         # Watch mode
npm test -- --coverage      # With coverage
```

**Backend:**
```bash
cd backend
pytest                      # All tests
pytest -v                   # Verbose
pytest --cov=backend        # With coverage
```

### Where can I get help?

**Resources:**
1. Check [Documentation](../README.md)
2. Search [GitHub Issues](https://github.com/nkap360/flowbuilder/issues)
3. Ask in [GitHub Discussions](https://github.com/nkap360/flowbuilder/discussions)
4. Use Document Space chatbot in app

**Reporting bugs:**
1. Check if issue already exists
2. Provide clear reproduction steps
3. Include error messages and logs
4. Specify your environment (OS, versions)

---

## 🎯 Best Practices

### Dataset Creation

✅ **DO:**
- Start with high-quality source documents
- Review all AI-generated content
- Use consistent naming conventions
- Tag datasets appropriately
- Export regularly for backup

❌ **DON'T:**
- Auto-approve all AI generations
- Mix unrelated topics in one dataset
- Skip the review process
- Forget to version your datasets

### Golden Review

✅ **DO:**
- Take time to understand context
- Edit for clarity and accuracy
- Reject low-quality goldens
- Track review metrics
- Document special cases

❌ **DON'T:**
- Rush through reviews
- Approve without reading context
- Make arbitrary changes
- Ignore review statistics

### API Usage

✅ **DO:**
- Monitor API usage and costs
- Implement rate limiting
- Cache responses when appropriate
- Use appropriate models for tasks
- Handle errors gracefully

❌ **DON'T:**
- Share API keys publicly
- Ignore rate limits
- Use expensive models unnecessarily
- Skip error handling

---

## 📞 Still Have Questions?

**Quick Help:**
- Use the in-app chatbot (Document space)
- Check [Troubleshooting Guide](../troubleshooting/common-issues.md)
- Review [Getting Started](../getting-started/quick-start.md)

**Community:**
- [GitHub Discussions](https://github.com/nkap360/flowbuilder/discussions)
- [GitHub Issues](https://github.com/nkap360/flowbuilder/issues)

**Documentation:**
- [Complete Documentation](../README.md)
- [API Reference](developer/api-reference.md)
- [Architecture Guide](developer/architecture.md)

---

**Last Updated:** December 3, 2025  
**Version:** 1.0.0  
**Contributors Welcome!** See [Contributing Guide](developer/contributing.md)
