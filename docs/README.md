# Flow Builder Documentation

Welcome to the Flow Builder documentation hub. This comprehensive guide covers everything from getting started to advanced deployment and customization.

## 🚀 Quick Start

- **New to Flow Builder?** Start with [Installation](getting-started/installation.md)
- **Want to test quickly?** Follow the [Quick Start](getting-started/quick-start.md) guide
- **Ready for production?** See our [Deployment Guide](deployment/overview.md)

## 📚 Documentation Sections

### 🆕 Getting Started
- [Installation Guide](getting-started/installation.md) - Set up Flow Builder locally
- [Quick Start](getting-started/quick-start.md) - Get started in 5 minutes
- [Basic Concepts](getting-started/concepts.md) - Understanding Flow Builder fundamentals

### 👥 User Guides
- [Core Features](user-guide/core-features.md) - PDF processing & golden review workflows
- [Chatbot Features](user-guide/chatbot.md) - AI assistant with multiple chat spaces
- [Flow Builder](user-guide/flow-builder.md) - Creating and managing workflows
- [Dataset Management](user-guide/datasets.md) - Working with documents and annotations

### 🚀 Deployment
- [Deployment Overview](deployment/overview.md) - Choose your deployment strategy
- [Leapcell Platform](deployment/leapcell.md) - One-click deployment to Leapcell.io
- [Production Checklist](deployment/production-checklist.md) - Pre-deployment verification
- [Security Guide](deployment/security.md) - Best practices for production

### 🛠️ Development
- [Architecture Guide](developer/architecture.md) - System design and components
- [Extending Flow Builder](developer/extending.md) - Adding custom actions and providers
- [API Reference](developer/api-reference.md) - REST API documentation
- [Contributing](developer/contributing.md) - Development guidelines and best practices

### 🔧 Troubleshooting
- [Common Issues](troubleshooting/common-issues.md) - Solutions to frequent problems
- [Debugging Guide](troubleshooting/debugging.md) - Debugging techniques and tools
- [FAQ](troubleshooting/faq.md) - Frequently asked questions

## 🎯 Popular Topics

### For New Users
- [Getting Started](getting-started/installation.md) - Install and run Flow Builder
- [Your First Flow](user-guide/flow-builder.md) - Create your first workflow
- [PDF Processing](user-guide/core-features.md) - Upload and process PDFs

### For Administrators
- [Production Deployment](deployment/production-checklist.md) - Deploy to production
- [Security Configuration](deployment/security.md) - Secure your deployment
- [Monitoring](deployment/leapcell.md#monitoring--logs) - Monitor your application

### For Developers
- [Adding Custom Actions](developer/extending.md#adding-new-actions) - Extend functionality
- [API Documentation](developer/api-reference.md) - Integration guide
- [Architecture Overview](developer/architecture.md) - Understanding the system

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│               Frontend (React)           │
│  ┌─────────────┐  ┌──────────────────┐   │
│  │ Flow Builder│  │   Chatbot UI     │   │
│  │   (Editor)  │  │  (Multi-space)   │   │
│  └─────────────┘  └──────────────────┘   │
└────────────────────────┬────────────────┘
                         │ REST API
┌────────────────────────┴────────────────┐
│            Backend (FastAPI)            │
│  ┌──────────────────────────────────┐  │
│  │         Core Engine               │  │
│  │  • Flow Executor  • Actions      │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │        Services Layer            │  │
│  │  • Auth  • Datasets  • AI APIs   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
             │
             ▼
┌─────────────────┐  ┌─────────────────┐
│   Supabase      │  │  AI Providers   │
│  (Database)     │  │ (OpenAI, Gemini) │
└─────────────────┘  └─────────────────┘
```

## 🔗 Key Features

### 📄 Document Processing
- **Structured PDF Extraction**: Preserves headings, lists, and formatting
- **Multi-format Support**: PDF, TXT, MD, CSV, JSON
- **Golden Generation**: AI-powered Q&A pair creation
- **Review Workflow**: Human-in-the-loop quality control

### 🤖 AI Integration
- **Multiple Providers**: OpenAI, Google Gemini, DeepSeek, Custom endpoints
- **Configurable Settings**: Per-provider configuration with API key management
- **Chat Spaces**: Default, Document-aware, and Web-enhanced chat modes
- **Security-first**: Local storage, export protection, masked API keys

### 🔄 Workflow Engine
- **Visual Flow Builder**: Drag-and-drop interface for creating workflows
- **Pre-built Templates**: Common workflows ready to use
- **Custom Actions**: Extensible action system
- **Real-time Execution**: Live flow execution with status tracking

## 🆘 Getting Help

### Documentation Resources
- **Quick Questions**: Use the [Chatbot](user-guide/chatbot.md) in Document space
- **Common Issues**: Check [Troubleshooting](troubleshooting/common-issues.md)
- **API Help**: See [API Reference](developer/api-reference.md)

### Community Support
- **GitHub Issues**: [Report bugs or request features](https://github.com/nkap360/flowbuilder/issues)
- **GitHub Discussions**: [Community discussions](https://github.com/nkap360/flowbuilder/discussions)
- **Security Issues**: [Report security vulnerabilities](mailto:security@flowbuilder.com)

### Professional Support
- **Enterprise Deployment**: Contact enterprise@flowbuilder.com
- **Custom Development**: Contact consulting@flowbuilder.com
- **Training and Onboarding**: Contact training@flowbuilder.com

## 📊 Project Status

- **Version**: 1.0.0
- **Last Updated**: December 3, 2025
- **Status**: Production Ready ✅
- **Backend**: 7 registered actions, modular architecture
- **Frontend**: React 18 + TypeScript, professional UI
- **Documentation**: Comprehensive guides and API reference
- **Tests**: Unit tests + validation tools

## 🗺️ Roadmap

### Upcoming Features
- **Table Detection & Rendering**: Enhanced PDF processing
- **OCR Support**: Process scanned PDFs with Tesseract.js
- **Collaborative Review**: Multi-user golden review system
- **Advanced Analytics**: Usage metrics and insights
- **Custom Themes**: Dark mode and styling options

### Platform Enhancements
- **Multi-language Support**: Internationalization
- **Mobile App**: React Native mobile application
- **Desktop App**: Electron desktop application
- **API Rate Limiting**: Built-in rate limiting and quotas
- **Backup & Restore**: Automated backup system

---

## 📖 How to Use This Documentation

### For New Users
1. Start with [Installation](getting-started/installation.md)
2. Follow the [Quick Start](getting-started/quick-start.md)
3. Read [Core Features](user-guide/core-features.md) for main workflows
4. Explore [User Guides](user-guide/) for specific features

### For Administrators
1. Review [Security Guide](deployment/security.md)
2. Follow [Production Checklist](deployment/production-checklist.md)
3. Choose your [Deployment Strategy](deployment/overview.md)
4. Configure monitoring and alerts

### For Developers
1. Read [Architecture Guide](developer/architecture.md)
2. Check [Contributing Guidelines](developer/contributing.md)
3. Explore [API Reference](developer/api-reference.md)
4. See [Extending Flow Builder](developer/extending.md)

---

**Tip**: Use the search function in your editor to quickly find information across all documentation files. Each guide includes cross-references to related topics for easy navigation.

**Need immediate help?** Start a chat with our AI assistant by opening Flow Builder and clicking the chat icon in the bottom-right corner.