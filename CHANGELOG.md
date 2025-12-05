# Changelog

All notable changes to Flow Builder will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Table detection and rendering in PDF viewer
- OCR support for scanned PDFs
- Real-time collaboration for golden review
- Advanced analytics dashboard
- Multi-language support

---

## [1.0.0] - 2025-12-03

### 🎉 Initial Production Release

The first production-ready release of Flow Builder with complete dataset management, PDF processing, golden review, and flow execution capabilities.

### Added

#### Core Features
- **Visual Flow Builder** - Drag-and-drop workflow designer with ReactFlow
- **Dataset Management** - Complete CRUD operations for datasets, documents, and goldens
- **PDF Processing** - Structured text extraction preserving headings, lists, and formatting
- **Golden Review System** - Human-in-the-loop workflow with approve/edit/reject
- **AI Integration** - Support for 4 AI providers (Google Gemini, OpenAI, DeepSeek, Custom)
- **Flow Templates** - 8 pre-built templates for common use cases
- **Export Functionality** - JSON, CSV, and Markdown export formats

#### AI Chatbot
- **Multi-Space Chat** - Three chat modes (Default, Document, Web)
- **Document Space** - AI with full codebase context for development help
- **Web Space** - AI with web search integration (Serper API)
- **Markdown Rendering** - Beautiful formatting with syntax highlighting
- **Streaming Responses** - Real-time response generation

#### Authentication & Security
- **Supabase Integration** - JWT-based authentication
- **Workspace Authorization** - Multi-tenant support with role-based access
- **API Key Management** - Secure local storage with export protection
- **Environment Variables** - All secrets in .env files (gitignored)

#### Developer Tools
- **Comprehensive API** - RESTful API with OpenAPI documentation
- **Type Safety** - Full TypeScript and Python type hints
- **Testing Suite** - Unit and integration tests
- **Documentation** - 10+ documentation files covering all aspects

#### UI/UX
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode Ready** - Tailwind CSS with customizable themes
- **Keyboard Shortcuts** - A/E/R for golden review, other workflows
- **Real-time Feedback** - Loading states, progress bars, status updates

#### Deployment
- **Leapcell Support** - One-click deployment configuration
- **Docker Support** - Multi-stage Dockerfiles for frontend and backend
- **Production Ready** - Environment-based configuration, health checks

### Technical Details

#### Frontend
- React 18.2.0 with TypeScript
- Vite 7.2.4 for fast builds
- React Flow 11.11.4 for visual workflows
- React Markdown 10.1.0 with syntax highlighting
- TailwindCSS 4.1.17 for styling
- Lucide React 0.344.0 for icons

#### Backend
- FastAPI (Python 3.9+)
- DeepEval integration for golden generation
- CrewAI for multi-agent workflows
- Google Generative AI SDK
- Supabase client for authentication

### Documentation
- Complete API reference
- Contributing guidelines
- FAQ with 40+ questions
- Security policy
- Deployment guides
- Troubleshooting documentation
- Architecture overview
- Developer guides

### Security
- API keys stored locally, never transmitted unnecessarily
- Environment variables for all secrets
- Export protection (keys excluded from exports)
- CORS properly configured
- JWT token validation
- Row Level Security support via Supabase

---

## [0.9.0] - 2025-11-15 (Beta)

### Added
- Beta release for testing
- Core flow execution engine
- Basic PDF processing
- Initial AI provider integration

### Changed
- Refactored backend structure for better modularity
- Improved error handling throughout application

### Fixed
- Memory leaks in PDF viewer
- CORS configuration issues
- Authentication edge cases

---

## [0.5.0] - 2025-10-01 (Alpha)

### Added
- Initial alpha release
- Basic dataset management
- Simple flow builder
- Google Gemini integration

---

## Release Categories

### 🎉 Major Releases (X.0.0)
- Significant new features
- Breaking changes
- Architecture updates

### ✨ Minor Releases (1.X.0)
- New features (backwards compatible)
- Significant improvements
- New integrations

### 🐛 Patch Releases (1.0.X)
- Bug fixes
- Performance improvements
- Documentation updates
- Dependency updates

---

## Upgrade Guide

### Upgrading to 1.0.0

**From 0.9.0 (Beta):**

1. **Update Dependencies:**
```bash
# Frontend
npm install

# Backend
cd backend
pip install -r requirements.txt
```

2. **Update Environment Variables:**
```bash
# Add new variables to .env
VITE_SERPER_API_KEY=your_key_here  # For web search
```

3. **Database Migration:**
```bash
# No database changes in 1.0.0
# Future releases will include migration scripts
```

4. **Configuration Changes:**
- Review `.env.example` for new variables
- Update Leapcell configuration if deploying
- Check CORS settings if custom domain

---

## Contributing

See [CONTRIBUTING.md](docs/developer/contributing.md) for how to contribute to Flow Builder.

---

## Support

- **Documentation:** [docs/README.md](docs/README.md)
- **Issues:** [GitHub Issues](https://github.com/nkap360/flowbuilder/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nkap360/flowbuilder/discussions)

---

**Maintained by:** Flow Builder Contributors  
**License:** MIT  
**Website:** https://flowbuilder.io (coming soon)
