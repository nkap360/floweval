# Core Features Guide

Flow Builder's core features provide a complete workflow for processing PDF documents, generating golden datasets with AI assistance, and reviewing the quality through a human-in-the-loop system. This guide covers the PDF processing engine, golden generation, and review workflow.

## 🎯 Overview

Flow Builder enables you to:

1. **Process PDFs** - Extract structured text while preserving formatting
2. **Generate Goldens** - Create Q&A pairs automatically using AI
3. **Review Quality** - Human review and editing of generated content
4. **Export Results** - Export validated datasets for evaluation

### Workflow Architecture

```
[Upload PDF] → [Extract Text] → [Generate Goldens] → [Review Goldens] → [Export JSON] → [DeepEval]
     ↓              ↓                    ↓                   ↓                 ↓
   Backend       AI Processing       Human Review      Ready for Use    Evaluation
```

## 📄 PDF Processing & Annotation

The Annotation Studio provides **structured PDF viewing** that preserves document formatting, headings, lists, and page layout using PDF.js for text extraction.

### PDF Processing Features

#### ✨ Advanced Text Extraction

**Position-Based Analysis:**
- Groups text items by Y-coordinate to identify lines
- Sorts lines by X-position for correct reading order
- Preserves document structure and hierarchy

**Font Intelligence:**
- Detects headings based on font size (>1.3x average = H2, >1.15x = H3)
- Identifies list items using bullet point recognition
- Recognizes page breaks through spacing analysis

**Formatting Preservation:**
- Page separators with clear markers
- Markdown-like structure for headings
- Bullet point formatting for lists
- Proper spacing and paragraph breaks

### PDF Upload Process

#### Supported Formats

**Primary:**
- **PDF** - Full structured extraction with headings and formatting
- **TXT** - Plain text files
- **MD** - Markdown files (preserves formatting)
- **CSV** - Data files (tabular content)
- **JSON** - Structured data

**Future Support:**
- DOCX - Word documents (planned)
- Images with OCR - Scanned PDFs (planned)

#### Step-by-Step Upload

1. **Navigate to Datasets**: Click "Datasets" in the sidebar
2. **Create Dataset**: Click "New Dataset" or select existing
3. **Upload Documents**:
   - Drag & drop PDF files onto upload area
   - Or click "Browse Files" to select files
4. **Processing**: System automatically extracts and structures text
5. **Review**: Check processed content in Annotation Studio

### Technical Implementation

#### PDF Processor (`services/pdfProcessor.ts`)

**Main Function:**
```typescript
export async function extractStructuredPDFText(file: File): Promise<string>
```

**Algorithm Steps:**
1. Load PDF using PDF.js library
2. Extract text items with position metadata
3. Group items into lines by Y-coordinate (2-unit tolerance)
4. Sort lines by position and analyze font sizes
5. Apply formatting markers (## headings, • bullets, === page breaks)
6. Return structured text with markdown-like formatting

**Recognition Patterns:**
```typescript
// Heading detection
const LARGE_FONT = avgFontSize * 1.3;  // H2 headings
const MEDIUM_FONT = avgFontSize * 1.15; // H3 headings

// Spacing detection
const LARGE_GAP = avgFontSize * 2;     // Page breaks
const MEDIUM_GAP = avgFontSize * 1.5;  // Paragraph breaks

// Bullet point patterns
const BULLET_PATTERNS = ['•', '·', '○', '●', '▪', '▫', '◦', '‣', '⁃', '∙'];
```

#### Example Output

**Input:** Technical specification PDF

**Output (Structured):**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## WELDING LOG – EXCHANGER E-101

Reference: CS-E101-Rev.2

### PED Context

The E-101 equipment is a tubular exchanger subject to directive 2014/68/EU (PED)...

### Welding Procedures

  • WPS-101-GTAW-01: welding shell/bottom, process 141
  • WPS-102-SMAW-01: welding connections, process 111
  • WPS-103-GTAW-02: welding tubes, process 141

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Quality Control

### Inspection Requirements
...
```

### Using the Annotation Studio

#### Navigation and Viewing

**Page Navigation:**
- Clear page separators with visual indicators
- Page numbers displayed in separators
- Smooth scrolling between pages

**Content Structure:**
- **H2 Headings**: Large, bold text (20px)
- **H3 Headings**: Medium, semibold text (18px)
- **Bullet Points**: Amber-colored list items
- **Regular Text**: Normal spacing and readability

**Interaction Features:**
- **Text Selection**: Select any portion for highlighting
- **Context Extraction**: Selected text preserves structure
- **Search**: Find specific content within documents
- **Zoom**: Adjustable text size for readability

#### Highlight and Context Features

**Creating Highlights:**
1. **Select Text**: Click and drag to select content
2. **Add Context**: Selection automatically formatted
3. **Structure Preserved**: Headings and lists maintained
4. **Golden Generation**: Use highlights for focused Q&A creation

**Context Examples:**
- **Selected**: "## Section 1: Definitions" + content
- **For AI**: Clean text without markdown markers
- **Preserves**: Document structure and relationships

## 🤖 AI-Powered Golden Generation

Once documents are processed, Flow Builder uses AI to generate high-quality question-answer pairs (goldens) for evaluation datasets.

### What Are Goldens?

**Goldens** are curated question-answer pairs used to evaluate AI system performance:

```json
{
  "input": "What is the purpose of PED directive in welding?",
  "expected_output": "The PED directive 2014/68/EU ensures safety of pressure equipment, establishing essential safety requirements for welding procedures and equipment design.",
  "context": ["Extracted relevant text from document"]
}
```

### Generation Process

#### AI-Powered Analysis

**Document Understanding:**
- AI reads structured text with full context
- Identifies key concepts, procedures, and requirements
- Extracts technical specifications and parameters
- Recognizes relationships between different sections

**Question Generation:**
- Creates relevant questions based on document content
- Covers different difficulty levels (basic to advanced)
- Ensures questions are answerable from provided context
- Includes practical, scenario-based questions

**Answer Generation:**
- Provides accurate, concise answers
- Cites specific information from documents
- Maintains technical accuracy
- Includes relevant details and parameters

#### Supported AI Providers

**Default Provider - Custom_openai_endpoint:**
- Custom OpenAI Enterprise endpoint
- Optimized for technical content
- High-quality structured responses
-  reliability

**Alternative Providers:**
- **DeepSeek** - Cost-effective, good for technical content
- **Google Gemini** - Strong reasoning capabilities
- **OpenAI** - GPT-4 with advanced understanding

### Generation Templates

#### Quick Generation (Single Document)
1. **Upload PDF**: Add document to dataset
2. **Select Template**: "PDF to Golden Dataset"
3. **Configure Settings**:
   - Number of goldens to generate (5-50)
   - Difficulty level (Basic, Intermediate, Advanced)
   - Question types (Factual, Procedural, Scenario)
4. **Generate**: Click "Generate Goldens"
5. **Review**: Enter golden review workflow

#### Batch Generation (Multiple Documents)
1. **Upload Multiple**: Add several related documents
2. **Select Batch**: Choose documents for generation
3. **Configure Settings**:
   - Cross-document questions
   - Comparative analysis questions
   - Procedure-based scenarios
4. **Generate**: Process all documents together
5. **Review**: Comprehensive review workflow

### Generation Quality Control

#### Content Quality Features

**Relevance Checking:**
- Questions directly related to document content
- Answers supported by provided text
- No external knowledge assumptions
- Technical accuracy maintained

**Diversity Ensuring:**
- Mix of question types and difficulties
- Coverage of different document sections
- Both specific details and general concepts
- Practical application scenarios

**Validation Rules:**
- Answers must be extractable from context
- Questions must be clear and unambiguous
- Length constraints for usability
- Format consistency across pairs

## 👥 Golden Review Workflow

The Golden Review System provides a professional human-in-the-loop workflow to ensure quality control before using AI-generated goldens in evaluations.

### Review System Architecture

#### Flow Integration

**Workflow Steps:**
```
PDF Upload → Generate Goldens → REVIEW STEP → Export → DeepEval
                            ↓
                       Human Quality Control
```

**Review Node:**
- **Type**: `REVIEW_GOLDENS` (custom node type)
- **Icon**: ClipboardCheck with green styling
- **Purpose**: Pauses flow for human review
- **Integration**: Seamless flow execution with quality gate

#### Review Interface

**Side-by-Side Layout:**
- **Document Panel**: Original PDF content with structure
- **Golden Panel**: Generated Q&A pairs for review
- **Context Panel**: Source text for each golden
- **Actions Panel**: Approve, edit, reject controls

**Keyboard Shortcuts:**
- **A** - Approve current golden
- **R** - Reject current golden
- **E** - Edit current golden
- **Arrow Keys** - Navigate between goldens
- **Space** - Toggle selection
- **Enter** - Confirm action

#### Review States

**State Management:**
- **pending** - Not yet reviewed (default)
- **approved** - Approved as-is (green check)
- **edited** - Modified by reviewer (orange edit)
- **rejected** - Rejected, won't be exported (red X)

**Progress Tracking:**
- Total goldens generated
- Number approved, edited, rejected
- Completion percentage
- Time spent reviewing

### Review Process

#### Step-by-Step Review

1. **Automatic Navigation**:
   - Flow execution pauses at review step
   - Browser automatically opens review page
   - Review session created with unique ID

2. **Review Interface Loads**:
   - Goldens displayed with context
   - Document content accessible
   - Review tools available

3. **Quality Assessment**:
   - **Review Question**: Check accuracy and relevance
   - **Verify Answer**: Ensure correctness and completeness
   - **Check Context**: Confirm answer supported by source text
   - **Assess Quality**: Evaluate technical accuracy

4. **Take Action**:
   - **Approve**: Golden is correct as-is
   - **Edit**: Modify question or answer for improvement
   - **Reject**: Remove golden from dataset

5. **Progress Tracking**:
   - Real-time updates of review statistics
   - Visual progress bar
   - Time estimation for completion

#### Editing Features

**Inline Editing:**
- Edit questions directly in interface
- Modify answers with real-time preview
- Add or modify context references
- Track original vs. edited versions

**Quality Improvements:**
- Fix technical inaccuracies
- Improve question clarity
- Add missing details to answers
- Expand context for better evaluation

**Edit History:**
- Track all changes made
- Show original and edited versions
- Timestamp for each modification
- Reviewer identification

### Export and Finalization

#### Completion Criteria

**All Goldens Reviewed:**
- No pending items remain
- All items have approved, edited, or rejected status
- Review session marked complete

**Quality Thresholds:**
- Minimum approval rate (configurable)
- Maximum rejection rate
- Required edit completion

#### Export Format

**DeepEval Compatible JSON:**
```json
{
  "dataset_id": "ds_123",
  "reviewed_by": "user_id",
  "reviewed_at": "2025-12-03T10:00:00Z",
  "session_id": "session-1234567890-abc123",
  "generation_config": {
    "model": "custom_openai_endpoint",
    "temperature": 0.1,
    "max_tokens": 500
  },
  "statistics": {
    "total_generated": 25,
    "approved": 18,
    "edited": 5,
    "rejected": 2,
    "review_time_minutes": 45
  },
  "goldens": [
    {
      "id": "golden-1",
      "dataset_id": "ds_123",
      "input": "What welding procedure is used for shell-to-bottom connections?",
      "expected_output": "WPS-101-GTAW-01 is used for welding shell/bottom connections using process 141 (GTAW).",
      "context": ["Relevant text from document..."],
      "metadata": {
        "difficulty": "intermediate",
        "category": "procedural",
        "page_reference": 1,
        "review_status": "approved",
        "reviewed_by": "user_id",
        "reviewed_at": "2025-12-03T10:05:00Z"
      }
    }
  ]
}
```

#### Export Features

**Provenance Tracking:**
- Complete audit trail of all changes
- Reviewer identification and timestamps
- Original vs. edited versions
- Session metadata and configuration

**Quality Metrics:**
- Approval and rejection rates
- Edit statistics
- Time spent reviewing
- Quality score calculations

**Multiple Formats:**
- JSON for DeepEval integration
- CSV for spreadsheet analysis
- Markdown for documentation
- Custom export configurations

## 🔄 Integration with Flow Builder

### Flow Templates

#### PDF to Golden Dataset Template

**Template ID**: `pdf-to-goldens`

**Nodes**:
1. **Manual Trigger** - Start flow execution
2. **File Upload** - Upload PDF documents
3. **Golden Generation** - AI-powered Q&A creation
4. **Golden Review** - Human quality control
5. **Export JSON** - Final dataset export

**Configuration**:
```json
{
  "id": "pdf-to-goldens",
  "name": "PDF to Golden Dataset",
  "category": "CLM Enablement",
  "description": "Convert PDF documents to evaluation datasets with human review",
  "requiredParams": [
    {
      "name": "num_goldens",
      "label": "Number of Goldens",
      "type": "number",
      "default": 10,
      "description": "How many Q&A pairs to generate"
    }
  ]
}
```

#### Custom Flow Creation

**Adding Review Step**:
1. **Add Node**: Drag "Review Goldens" node to canvas
2. **Connect**: Link from golden generation to review
3. **Configure**: Set review requirements
4. **Execute**: Run flow with review step

**Review Node Configuration**:
- **Required Approvals**: Minimum number of approvals
- **Quality Threshold**: Minimum quality score
- **Review Type**: Individual or batch review
- **Timeout**: Maximum review time

### API Integration

#### Backend Actions

**Generate Goldens Action**:
```python
@action("dataset.generate_goldens")
async def generate_goldens(dataset_id: str, config: dict):
    # AI generation logic
    return {
        "status": "success",
        "session_id": "session-1234567890-abc123",
        "goldens": generated_goldens,
        "review_url": f"/datasets/{dataset_id}/review-goldens?session=session-1234567890-abc123"
    }
```

**Export Action**:
```python
@action("dataset.export_goldens")
async def export_goldens(dataset_id: str, session_id: str):
    # Export reviewed goldens
    return {
        "status": "success",
        "export_url": "/api/datasets/{dataset_id}/export",
        "statistics": export_stats
    }
```

## 📊 Performance and Optimization

### Processing Performance

#### PDF Extraction Speed

**Performance Metrics**:
- **Small PDF** (< 10 pages): ~2-3 seconds
- **Medium PDF** (10-50 pages): ~5-10 seconds
- **Large PDF** (50+ pages): ~10-30 seconds
- **Very Large PDF** (100+ pages): ~30-60 seconds

**Optimization Techniques**:
- Batch processing of pages
- Memory-efficient text extraction
- Progressive rendering during extraction
- Caching of processed documents

#### AI Generation Speed

**Provider Performance**:
- **Custom_openai_endpoint**: ~2-3 seconds per golden
- **DeepSeek**: ~1-2 seconds per golden
- **Gemini**: ~3-4 seconds per golden
- **OpenAI**: ~2-3 seconds per golden

**Batch Generation**:
- Parallel processing for multiple goldens
- Efficient token usage
- Context optimization for speed
- Cost-effective provider selection

### Quality Metrics

#### Generation Quality

**Accuracy Metrics**:
- **Factual Accuracy**: >95% correct answers
- **Relevance Score**: >90% relevant questions
- **Completeness**: >85% comprehensive answers
- **Technical Accuracy**: >90% technical correctness

**Diversity Metrics**:
- **Question Type Distribution**: Balanced across types
- **Difficulty Distribution**: Mix of complexity levels
- **Coverage**: >80% of document sections represented
- **Redundancy**: <10% duplicate questions

#### Review Efficiency

**Review Speed**:
- **Average Review Time**: 30-60 seconds per golden
- **Edit Rate**: 15-25% of goldens require editing
- **Rejection Rate**: 5-15% of goldens rejected
- **Approval Rate**: 60-80% approved as-is

**Quality Improvement**:
- **Post-Review Accuracy**: >99% factual accuracy
- **User Satisfaction**: >95% satisfaction with final quality
- **Evaluation Performance**: Improved evaluation metrics
- **Reduced False Positives**: Better evaluation results

## 🔧 Advanced Configuration

### Generation Settings

#### AI Provider Configuration

**Model Selection**:
```json
{
  "provider": "custom_openai_endpoint",
  "model": "gpt-4-turbo-preview",
  "temperature": 0.1,
  "max_tokens": 500,
  "top_p": 0.9,
  "frequency_penalty": 0.0
}
```

**Generation Parameters**:
- **Temperature**: Lower for more factual responses (0.1-0.3)
- **Max Tokens**: Limit response length for consistency
- **Top P**: Control diversity vs. focus
- **Frequency Penalty**: Reduce repetition

#### Quality Controls

**Content Filtering**:
- **Length Requirements**: Minimum/maximum question/answer length
- **Complexity Filters**: Filter by difficulty level
- **Technical Accuracy**: Validate technical content
- **Relevance Scoring**: Ensure document relevance

**Diversity Controls**:
- **Section Coverage**: Ensure all document sections covered
- **Question Types**: Balance factual, procedural, scenario questions
- **Difficulty Distribution**: Mix of complexity levels
- **Redundancy Prevention**: Avoid duplicate content

### Review Configuration

#### Review Workflow Settings

**Quality Thresholds**:
```json
{
  "min_approval_rate": 0.7,
  "max_rejection_rate": 0.3,
  "required_reviewers": 1,
  "edit_suggestions": true,
  "auto_approve_threshold": 0.9
}
```

**Review Options**:
- **Bulk Operations**: Approve/reject multiple goldens
- **Edit Suggestions**: AI suggestions for improvements
- **Quality Scoring**: Automatic quality assessment
- **Review Assignments**: Assign specific reviewers

#### Custom Review Rules

**Business Rules**:
- **Technical Accuracy**: Require technical expert review
- **Compliance Checking**: Verify regulatory compliance
- **Documentation Standards**: Ensure proper documentation
- **Quality Gates**: Minimum quality requirements

**Validation Rules**:
- **Answer Verification**: Check answer completeness
- **Question Clarity**: Ensure question clarity
- **Context Relevance**: Verify context support
- **Format Consistency**: Maintain formatting standards

## 🚀 Future Enhancements

### PDF Processing Improvements

**Table Detection and Rendering**:
- Detect and extract tabular data from PDFs
- Render tables as structured data
- Export to CSV/Excel formats
- Table-based question generation

**Multi-Column Layout Support**:
- Detect column structures in documents
- Maintain reading order across columns
- Handle complex page layouts
- Improved text extraction accuracy

**OCR Integration**:
- Support for scanned PDFs using Tesseract.js
- Image-based text extraction
- Confidence scoring for OCR results
- Handwriting recognition support

### Golden Generation Enhancements

**Advanced Question Types**:
- **Scenario-based Questions**: Complex situational questions
- **Comparative Questions**: Compare different aspects
- **Procedural Questions**: Step-by-step process questions
- **Troubleshooting Questions**: Problem-solving scenarios

**Quality Improvements**:
- **Context Optimization**: Better context selection
- **Answer Enhancement**: More comprehensive answers
- **Technical Validation**: Improved technical accuracy
- **Domain Expertise**: Industry-specific knowledge

### Review System Upgrades

**Collaborative Review**:
- **Multiple Reviewers**: Team-based review process
- **Consensus Building**: Agreement mechanisms
- **Comment System**: Threaded discussions on goldens
- **Review Assignment**: Automatic reviewer assignment

**AI-Assisted Review**:
- **Quality Prediction**: AI predicts golden quality
- **Edit Suggestions**: AI suggests improvements
- **Duplicate Detection**: Identify similar goldens
- **Auto-Categorization**: Automatic topic categorization

**Analytics Dashboard**:
- **Review Metrics**: Detailed review statistics
- **Quality Trends**: Quality improvement over time
- **Reviewer Performance**: Individual reviewer analytics
- **Generation Analysis**: Golden generation effectiveness

## 🔍 Troubleshooting

### Common Issues and Solutions

#### PDF Processing Issues

**Problem**: PDF shows as plain text without structure
**Solution**: Ensure latest version with pdfProcessor.ts is loaded

**Problem**: Headings not detected in PDF
**Cause**: PDF uses uniform font size throughout
**Solution**: Manual heading detection or adjust font size thresholds

**Problem**: Text out of order
**Cause**: Multi-column layout or non-standard positioning
**Solution**: Custom X-coordinate sorting algorithms

**Problem**: Lists not formatted as bullet points
**Cause**: PDF uses custom bullet characters
**Solution**: Add new patterns to BULLET_PATTERNS array

#### Golden Generation Issues

**Problem**: Low quality generated goldens
**Solutions**:
- Check AI provider configuration
- Adjust temperature parameter (lower for more accuracy)
- Verify document quality and structure
- Review generation prompts

**Problem**: Questions not relevant to document
**Solutions**:
- Improve context extraction
- Adjust relevance thresholds
- Fine-tune generation parameters
- Check document preprocessing

**Problem**: Answers too short or incomplete
**Solutions**:
- Increase max_tokens parameter
- Adjust temperature for creativity
- Modify generation prompts
- Check AI provider capabilities

#### Review System Issues

**Problem**: Review page not opening
**Solutions**:
- Check session ID generation
- Verify routing configuration
- Check browser console for errors
- Ensure flow executor paused correctly

**Problem**: Cannot save review changes
**Solutions**:
- Check localStorage availability
- Verify session data integrity
- Check network connectivity
- Review browser console errors

**Problem**: Export not working
**Solutions**:
- Verify all goldens reviewed
- Check export configuration
- Validate data format
- Review browser download settings

### Performance Issues

**Slow PDF Processing**:
- Process large PDFs in batches
- Implement progressive loading
- Optimize memory usage
- Use web workers for processing

**Slow Golden Generation**:
- Use faster AI providers (DeepSeek)
- Implement parallel processing
- Optimize prompts for efficiency
- Cache generation results

**Slow Review Interface**:
- Implement virtual scrolling for large datasets
- Optimize rendering performance
- Use efficient data structures
- Implement lazy loading

## 📚 Related Documentation

- [Chatbot Guide](chatbot.md) - AI assistant features
- [Flow Builder Guide](flow-builder.md) - Creating workflows
- [Security Guide](../deployment/security.md) - Data protection
- [API Reference](../developer/api-reference.md) - Integration details

## 🆘 Support and Resources

### Getting Help

**For Technical Issues:**
1. Check browser console for error messages
2. Review troubleshooting section above
3. Verify configuration settings
4. File GitHub issue with details

**For Feature Requests:**
1. Check GitHub Issues for existing requests
2. Provide detailed use case and requirements
3. Include mockups or examples if helpful
4. Consider contribution if open source

**For General Questions:**
1. Use the chatbot in Document space for implementation questions
2. Review related documentation
3. Search GitHub Discussions
4. Contact support if needed

### Community Resources

**GitHub Repository**:
- [Issues](https://github.com/nkap360/flowbuilder/issues) - Bug reports and feature requests
- [Discussions](https://github.com/nkap360/flowbuilder/discussions) - Community discussions
- [Wiki](https://github.com/nkap360/flowbuilder/wiki) - Additional documentation

**Documentation**:
- [API Documentation](../developer/api-reference.md) - Technical integration
- [Architecture Guide](../developer/architecture.md) - System design
- [Deployment Guide](../deployment/overview.md) - Production deployment

---

**Master the core features to create high-quality evaluation datasets efficiently!** The combination of AI-powered generation and human review ensures the best possible results for your evaluation needs.

---

**Last Updated:** December 3, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅