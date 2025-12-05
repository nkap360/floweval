# Chatbot Features Guide

Flow Builder includes an intelligent chatbot with multiple chat spaces, markdown rendering, and AI provider integration. This comprehensive guide covers all chatbot features and how to use them effectively.

## 🎯 Overview

The Flow Builder chatbot provides three distinct chat spaces, each designed for different use cases:

### 1. **Default Space** 🗨️
- **Purpose**: Raw AI assistance for general questions
- **Features**: Fast responses from configured AI provider
- **Best for**: Creative writing, brainstorming, general knowledge

### 2. **Document Space** 📄
- **Purpose**: AI assistance with full codebase knowledge
- **Features**: Context-aware responses about Flow Builder implementation
- **Best for**: "How do I add a feature?", "Where is this code?", "How does X work?"

### 3. **Web Space** 🌐
- **Purpose**: AI assistance with web search + codebase knowledge
- **Features**: Combines current information from the web with internal documentation
- **Best for**: "What are the latest best practices?", "Current standards + implementation"

## 🚀 Getting Started

### Initial Setup

1. **Open Chatbot**: Click the chat icon in the bottom-right corner
2. **Configure AI Provider**: Go to Settings → Application Settings → Chatbot AI Provider
3. **Set API Key**: Configure your preferred AI provider (DeepSeek recommended)
4. **Start Chatting**: Choose your chat space and start asking questions

### Required Configuration

#### Minimum Setup
```bash
# For chatbot functionality
VITE_DEEPSEEK_API_KEY=your_deepseek_api_key
VITE_DEEPSEEK_MODEL=deepseek-chat
```

#### Full Configuration
```bash
# Chatbot provider
VITE_DEEPSEEK_API_KEY=your_key_here
VITE_DEEPSEEK_MODEL=deepseek-chat

# Optional web search feature
SERPER_API_KEY=your_serper_api_key

# Alternative providers
VITE_OPENAI_API_KEY=your_openai_key
VITE_GEMINI_API_KEY=your_gemini_key
VITE_CUSTOM_OPENAI_ENDPOINT_API_KEY=your_custom_openai_endpoint_key
```

## 🗨️ Chat Spaces Explained

### Default Space - General AI Assistant

**Icon**: MessageCircle
**Use Case**: General AI conversations without additional context

**Features:**
- Direct AI responses from configured provider
- Fastest response time
- No additional context injection
- Pure AI conversation

**Example Usage:**
```
User: "Write a poem about artificial intelligence"
AI: [Creative response, no codebase context]

User: "What are the benefits of RAG systems?"
AI: [General AI knowledge response]
```

**Best for:**
- Creative writing and brainstorming
- General knowledge questions
- Learning about new topics
- Quick AI assistance

### Document Space - Codebase Expert

**Icon**: FileCode
**Use Case**: Questions about Flow Builder implementation and architecture

**Features:**
- Full codebase context automatically injected
- Access to:
  - Architecture documentation
  - Component structure
  - API endpoints
  - Service functions
  - Configuration patterns
  - Best practices

**Example Usage:**
```
User: "How do I add a new AI provider?"
AI: "To add a new AI provider in Flow Builder, you need to:
1. Update services/aiService.ts - add provider type to AIProvider union
2. Add provider configuration in getDefaultAIConfig()
3. Implement API call in getAIResponse() and getAIStream()
4. Add UI in pages/Settings.tsx for API key input
5. Add environment variable VITE_[PROVIDER]_API_KEY"

User: "Where is PDF processing implemented?"
AI: "PDF processing is in services/pdfProcessor.ts with the extractStructuredPDFText() function. It uses pdf.js to extract text while preserving structure like headings, lists, and page breaks."
```

**Best for:**
- Implementation questions
- Code examples and patterns
- Architecture understanding
- Troubleshooting code issues
- Adding new features

### Web Space - Current Information + Codebase

**Icon**: Globe
**Use Case**: Questions requiring external/current information plus codebase knowledge

**Features:**
- All Document Space features PLUS
- Web search via Serper API
- Combines external information with internal codebase knowledge
- Up-to-date information from the internet

**Requirements:** Additional `SERPER_API_KEY` environment variable

**Example Usage:**
```
User: "What's the best way to handle streaming responses in React?"
AI: [Searches web for current React streaming patterns]
     [Combines with codebase examples from aiService.ts]
     [Provides recommendation with code samples]

User: "How should I implement rate limiting for the API?"
AI: [Searches for FastAPI rate limiting best practices]
     [Shows how to integrate with existing backend/main.py]
     [Provides implementation guide specific to your architecture]
```

**Best for:**
- Current best practices and standards
- External API documentation + integration
- Technology trends + application
- Security recommendations + implementation
- Latest framework features

## 🎨 Markdown Rendering & Formatting

The chatbot supports beautiful markdown rendering with syntax highlighting for code blocks.

### Supported Markdown Features

#### Basic Formatting
- **Bold**: `**text**` or `__text__`
- *Italic*: `*text*` or `_text_`
- ~~Strikethrough~~: `~~text~~` (GFM)
- `Inline code`: `` `code` ``

#### Headings
```markdown
# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading
```

#### Lists
```markdown
- Unordered list
  - Nested item

1. Ordered list
2. Second item

- [ ] Task list (GFM)
- [x] Completed task
```

#### Code Blocks
````markdown
```python
def hello():
    print("Syntax highlighted!")
```

```typescript
const greeting: string = "Hello!";
```

```bash
npm install react-markdown
```
````

#### Links & Images
```markdown
[Link text](https://example.com)
![Alt text](image-url.jpg)
```

#### Tables (GFM)
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

### Syntax Highlighting

The chatbot supports syntax highlighting for 190+ programming languages:

**Popular Languages:**
- Python, JavaScript, TypeScript
- Java, C#, C++, Go, Rust
- HTML, CSS, SCSS
- SQL, GraphQL
- JSON, YAML, TOML
- Markdown, LaTeX
- Shell/Bash scripts
- Dockerfile, NGINX configs

**Auto-Detection:** If no language is specified, the system automatically detects the language.

### Typography Features

- **Responsive Design**: Chat bubbles adapt to content
- **Code Styling**: Dark theme for code blocks, amber highlighting for inline code
- **Readability**: Optimized fonts and spacing
- **Mobile Support**: Responsive on all devices

## 🔧 Configuration & Settings

### Chatbot Provider Settings

1. **Navigate to Settings**: Click the settings icon in the sidebar
2. **Application Settings**: Find the "Chatbot AI Provider" section
3. **Choose Provider**: Select your preferred AI provider
   - `deepseek` (recommended, cost-effective)
   - `google` (Google Gemini)
   - `openai` (GPT models)
   - `custom_openai_endpoint` (Custom OpenAI Enterprise)

### API Key Management

#### Adding API Keys

1. **Settings Page**: Go to Settings → AI Provider Configuration
2. **Add Provider**: Click "Add Provider" for your chosen AI
3. **Enter API Key**: Paste your API key
4. **Test Connection**: Click "Test" to verify the key works
5. **Save Settings**: Click "Save" to apply changes

#### Security Features

- **Masked Display**: API keys shown as `•••••••••••`
- **Toggle Visibility**: Click eye icon to show/hide keys
- **Export Protection**: Keys never included in settings export
- **Local Storage**: Keys stored only in browser localStorage

### Environment Variables

For production deployments, set these in your hosting platform:

```bash
# Required for chatbot
VITE_DEEPSEEK_API_KEY=sk-your-deepseek-key
VITE_DEEPSEEK_MODEL=deepseek-chat

# Optional - web search feature
SERPER_API_KEY=your-serper-api-key

# Alternative providers
VITE_OPENAI_API_KEY=sk-your-openai-key
VITE_GEMINI_API_KEY=AIza-your-gemini-key
VITE_CUSTOM_OPENAI_ENDPOINT_API_KEY=your-custom_openai_endpoint-key
```

## 🎛️ Using Different Chat Spaces

### Switching Between Spaces

1. **Open Chatbot**: Click chat icon in bottom-right corner
2. **Check Current Space**: Look at the green provider badge in header
3. **Click Dropdown**: Click the badge showing current space
4. **Select Space**: Choose from:
   - **Default Space** - No extra context
   - **Document Space** - Codebase knowledge
   - **Web Space** - Web search + codebase

### Visual Indicators

- **Badge Color**: Green (configured) or Red (not configured)
- **Current Space**: Displayed in badge text `(Default)`, `(Document)`, or `(Web)`
- **Dropdown Icons**:
  - 🗨️ MessageCircle = Default
  - 📄 FileCode = Document
  - 🌐 Globe = Web

### When to Use Each Space

#### Use Default Space for:
- Creative writing tasks
- General knowledge questions
- Brainstorming sessions
- Learning new topics unrelated to Flow Builder

#### Use Document Space for:
- "How do I implement X in Flow Builder?"
- "Where is the Y functionality located?"
- "How does the Z component work?"
- "What are the available API endpoints?"
- Code examples and implementation details

#### Use Web Space for:
- "What are the current best practices for X?"
- "How should I implement Y based on latest standards?"
- "What are the security recommendations for Z?"
- External API documentation + integration examples
- Latest technology trends + implementation guidance

## 🛠️ Advanced Features

### Web Search Integration

**Setup:**
1. Get Serper API key at https://serper.dev (Free tier: 2,500 searches/month)
2. Add `SERPER_API_KEY` to environment variables
3. Restart application

**How it Works:**
1. User asks question in Web space
2. System searches web using Serper API
3. Top 5 results formatted and added to prompt
4. AI responds using web results + codebase context

**Example Web Search Results:**
```
Search: "React 2025 best practices"

Results:
1. React Official Documentation - react.dev
   "React 18+ features and best practices for modern applications..."

2. State Management Guide - reactpatterns.com
   "Choosing the right state management solution in 2025..."

3. Performance Optimization - web.dev/react-performance
   "Latest React performance optimization techniques..."
```

### Code Examples in Responses

The chatbot automatically includes code examples when helpful:

```typescript
// Example response for "How to add a new action"
// In backend/actions/actions_custom.ts

import { register_action, ActionParam } from '../core/actions';
import { FlowNode } from '../core/models';

register_action(
    action_id="my_custom_action",
    name="My Custom Action",
    description="Does something useful",
    params=[
        ActionParam(
            name="input_data",
            label="Input Data",
            param_type="string",
            required=True,
            description="Data to process"
        )
    ]
);

@register_handler("my_custom_action")
async def handle_my_action(node: FlowNode, context: dict) -> dict:
    # Your implementation here
    input_data = node.data.get("input_data")
    result = process_data(input_data)
    return {"output": result}
```

### Context Awareness

In Document and Web spaces, the AI has full awareness of:

**Architecture:**
- System components and their relationships
- Data flow between frontend and backend
- Service layer organization
- Database schema and models

**Implementation Details:**
- File locations and organization
- Function signatures and usage
- Configuration patterns
- Error handling approaches

**Best Practices:**
- Code organization principles
- TypeScript patterns used
- Testing strategies
- Performance considerations

## 🔍 Troubleshooting

### Common Issues

**Chatbot not responding:**
1. Check API key configuration in Settings
2. Verify internet connection
3. Check browser console for errors
4. Test with different AI provider

**Web search not working:**
1. Verify `SERPER_API_KEY` environment variable
2. Check Serper API quota (2,500 searches/month free)
3. Test Serper API directly: `curl -H "X-API-KEY: your_key" https://google.serper.dev/search?q=test`

**Document space not providing context:**
1. Check browser console for `getCodebaseContext()` errors
2. Verify codebaseService.ts is loaded
3. Context is injected automatically, no user action needed

**Markdown not rendering:**
1. Clear browser cache (Ctrl+Shift+R)
2. Check ReactMarkdown imported correctly
3. Verify Tailwind CSS loaded
4. Test with simple markdown: `**test**`

**Code blocks not highlighting:**
1. Verify language specified: ````python ```` not ```` ``` ````
2. Check highlight.js CSS imported in index.html
3. Some languages need explicit names (tsx not ts)

### Performance Issues

**Slow responses:**
1. Check API provider response times
2. For Document/Web spaces, context loading adds ~2 seconds
3. Web search adds additional ~1-2 seconds
4. Consider using Default space for faster responses

**Large responses not rendering:**
1. Markdown parsing is ~5ms for typical responses
2. Syntax highlighting ~10ms per code block
3. Very large responses may need pagination
4. Monitor memory usage in browser dev tools

### Security Issues

**API key exposure:**
1. Never share screenshots with visible API keys
2. Use masked view (eye icon closed) for screenshots
3. Keys are stored only in browser localStorage
4. Keys are never included in settings exports

## 📊 Performance & Optimization

### Bundle Size Impact

The chatbot features add approximately:
- **336KB** to bundle (gzipped: ~102KB)
- react-markdown: ~140KB
- highlight.js: ~190KB
- Additional dependencies: ~6KB

### Rendering Performance

- **Markdown parsing**: ~5ms for typical responses
- **Syntax highlighting**: ~10ms per code block
- **Streaming support**: No lag during typing
- **Mobile optimization**: Responsive on all devices

### Optimization Tips

**For Large Codebases:**
- Limit codebase context to most relevant files
- Use file prioritization (core files first)
- Implement incremental context loading

**For Better Performance:**
- Use Default space for quick questions
- Pre-load common context in Document space
- Cache web search results when possible

## 🚀 Future Enhancements

### Planned Features

**Chat Features:**
- [ ] **Chat History** - Persist conversations across sessions
- [ ] **Space Memory** - Remember last used space per session
- [ ] **Context Selection** - Let users choose specific files to inject
- [ ] **Search Preview** - Show search results before AI response
- [ ] **Token Usage** - Display token count per space

**UI/UX Improvements:**
- [ ] **Copy Code Button** - One-click copy for code blocks
- [ ] **Line Numbers** - Optional line numbers in code blocks
- [ ] **Dark Mode** - Switch highlight themes for dark mode
- [ ] **Message Reactions** - 👍 👎 ❤️ reactions to responses
- [ ] **Follow-up Questions** - Quick reply suggestions

**Advanced Features:**
- [ ] **Export Conversations** - Save as Markdown/PDF
- [ ] **Code Execution** - Run code snippets in sandbox
- [ ] **File Editing** - Suggest and apply code changes
- [ ] **Diagram Generation** - Create visual diagrams from descriptions

### Integration Possibilities

**With Flow Builder:**
- [ ] **Chat-powered Flow Creation** - Describe flows in natural language
- [ ] **Debugging Assistant** - Help troubleshoot flow execution issues
- [ ] **Template Generation** - AI suggests flow templates based on needs

**With External Services:**
- [ ] **Slack/Discord Integration** - Use chatbot in team channels
- [ ] **API Integration** - External applications can use chat API
- [ ] **Voice Interface** - Voice input/output for hands-free use

## 📚 Related Documentation

- [Core Features Guide](core-features.md) - PDF processing and golden review
- [Flow Builder Guide](flow-builder.md) - Creating workflows
- [Security Guide](../deployment/security.md) - API key protection best practices
- [Developer Guide](../developer/architecture.md) - System architecture

## 🆘 Support

### Getting Help

**For Questions:**
1. Use **Document Space** to ask about implementation
2. Check browser console for technical errors
3. Review this documentation for common issues
4. File issue on GitHub if bug found

**For API Key Issues:**
1. Check provider dashboard for key status
2. Verify key has sufficient quota
3. Test key with provider's API directly
4. Contact provider support if needed

**For Feature Requests:**
1. Check GitHub Issues for existing requests
2. Upvote existing features you want
3. Create new issue with detailed description
4. Include use case and expected behavior

---

**Enjoy using the Flow Builder chatbot!** It's designed to make your development experience more productive and enjoyable.

---

**Last Updated:** December 3, 2025
**Version:** 1.0.0
**Status**: Production Ready ✅