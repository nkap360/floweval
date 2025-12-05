# Logging Guide

This document describes the comprehensive logging enhancements added to investigate and debug errors in the Flow Builder backend.

## Overview

Logging has been added across three critical areas:
1. **Request/Response Middleware** - Detailed HTTP request tracking
2. **AI Proxy Service** - Complete AI API call logging
3. **Flow Templates Service** - Path resolution and file access logging

## Configuration

### Environment Variable

Set the log level using the `LOG_LEVEL` environment variable:

```bash
# In production (default)
LOG_LEVEL=INFO

# For debugging
LOG_LEVEL=DEBUG

# For minimal logging
LOG_LEVEL=WARNING
```

### Log Format

All logs follow this format:
```
YYYY-MM-DD HH:MM:SS | LEVEL | module:line | message
```

Example:
```
2024-12-05 07:29:45 | INFO | ai_proxy:56 | [AI_PROXY] Starting chat completion request | Provider: openai
```

## Enhanced Logging Areas

### 1. Request Middleware (`main.py`)

**What's logged:**
- Client IP address and port
- HTTP method and path
- Query parameters
- Request headers (excluding sensitive ones)
- Response status code
- Request duration in milliseconds
- Content-Type of response
- Full exception stack traces on errors

**Log Tags:**
- `>>> INCOMING REQUEST` - Request received
- `<<< RESPONSE` - Successful response
- `<<< ERROR` - Request failed with exception

**Example logs:**
```
>>> INCOMING REQUEST: POST /ai/chat/completions | Client: 139.178.9.197:0 | Query: {}
Request Headers: {'host': 'example.com', 'user-agent': 'Mozilla/5.0', ...}
<<< RESPONSE: POST /ai/chat/completions - Status: 200 - Duration: 1234.56ms
Response Content-Type: application/json
```

### 2. AI Proxy Service (`services/ai_proxy.py`)

**What's logged:**
- Provider name (openai, deepseek, custom)
- Model name
- Stream mode (streaming vs non-streaming)
- Number of messages
- API endpoint URL
- API key presence (not the key itself)
- Response status codes
- Error details from upstream APIs
- Complete exception information

**Log Tags:**
- `[AI_PROXY]` - All AI proxy operations

**Example logs:**
```
[AI_PROXY] Starting chat completion request | Provider: openai
[AI_PROXY] Model: gpt-4 | Stream: False | Messages: 3
[AI_PROXY] Proxying to openai | URL: https://api.openai.com/v1/chat/completions
[AI_PROXY] API Key: present
[AI_PROXY] Using non-streaming mode
[AI_PROXY] Received successful response
[AI_PROXY] Extracted content length: 1024 characters
```

**Error logs:**
```
[AI_PROXY] Non-streaming API error
Status: 500 | Provider: openai | Model: gpt-4
Response: {"error": {"message": "Rate limit exceeded"}}
```

### 3. Flow Templates Service (`services/flow_templates.py`)

**What's logged:**
- Module initialization with directory paths
- Directory existence checks
- Directory contents listing
- Template file discovery
- Template loading and validation
- JSON parsing errors
- File access errors

**Log Tags:**
- `[FLOW_TEMPLATES]` - All flow template operations

**Example logs:**
```
[FLOW_TEMPLATES] Module initialized
FLOW_ENGINE_DIR: /flow_engine | TEMPLATES_DIR: /flow_engine/templates
Templates dir exists: True
[FLOW_TEMPLATES] Listing templates request
TEMPLATES_DIR: /flow_engine/templates | Exists: True | Is dir: True
[FLOW_TEMPLATES] Templates directory contents
Total files: 8 | Files: ['analytics-quality-sweep.json', 'dataset-upload-and-eval.json', ...]
[FLOW_TEMPLATES] Found 8 JSON template files: [...]
[FLOW_TEMPLATES] Successfully loaded 8 templates
```

**Error logs:**
```
[FLOW_TEMPLATES] Templates directory does not exist: /flow_engine/templates
Parent exists: True | Parent contents: ['other_file.txt']
```

## Investigating Specific Errors

### 500 Internal Server Error on `/ai/chat/completions`

**Logs to check:**
1. Request received log with provider and model
2. API key presence check
3. Upstream API response status and body
4. Exception type and stack trace

**Common causes:**
- Missing or invalid API key
- Rate limiting from upstream provider
- Invalid request format
- Network connectivity issues

**Debug steps:**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Look for these patterns in logs:
grep "\[AI_PROXY\]" logs/backend.log
grep "500" logs/backend.log
grep "Exception" logs/backend.log
```

### 404 Not Found on `/flow-engine/templates`

**Logs to check:**
1. Module initialization log showing directory paths
2. Directory existence checks
3. Parent directory contents
4. File listing results

**Common causes:**
- Templates directory not mounted in Docker
- Incorrect path configuration
- Missing template files
- Permissions issues

**Debug steps:**
```bash
# Check directory structure
grep "\[FLOW_TEMPLATES\]" logs/backend.log

# Verify paths
grep "TEMPLATES_DIR" logs/backend.log

# Check for file system errors
grep "Templates directory does not exist" logs/backend.log
```

## Production Deployment

### Docker Configuration

Ensure logging outputs to stdout for container log collection:

```dockerfile
# Logs will appear in docker logs
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Log Aggregation

For production, consider piping logs to a log aggregation service:

```bash
# Example with CloudWatch
docker logs -f <container_id> | aws logs push --log-group flowbuilder
```

### Monitoring Alerts

Set up alerts for error patterns:
- `500 Internal Server Error` frequency
- `404 Not Found` on critical endpoints
- Exception stack traces
- High request durations

## Performance Considerations

- **INFO level**: Minimal performance impact, suitable for production
- **DEBUG level**: More detailed, may impact performance under high load
- **Sensitive data**: API keys are masked, only showing presence
- **Headers**: Authorization and Cookie headers are excluded from logs

## Security Notes

⚠️ **What's NOT logged:**
- Complete API keys (only first 10 chars or presence indicator)
- Authorization headers
- Cookie values
- User passwords

✅ **What's logged:**
- Request paths and methods
- Query parameters
- Non-sensitive headers
- Error messages (sanitized)
- Client IP addresses

## Troubleshooting Tips

1. **Enable DEBUG logging temporarily:**
   ```bash
   export LOG_LEVEL=DEBUG
   # Restart service
   # Reproduce issue
   # Collect logs
   # Revert to INFO
   ```

2. **Filter logs by component:**
   ```bash
   grep "\[AI_PROXY\]" logs/app.log
   grep "\[FLOW_TEMPLATES\]" logs/app.log
   grep ">>> INCOMING REQUEST" logs/app.log
   ```

3. **Check request flow:**
   ```bash
   # Find a specific request by timestamp
   grep "2024-12-05 07:29:45" logs/app.log
   ```

4. **Analyze error patterns:**
   ```bash
   grep "ERROR" logs/app.log | cut -d'|' -f3 | sort | uniq -c
   ```

## Contributing

When adding new features, follow these logging guidelines:

1. Use structured log messages with clear prefixes
2. Include relevant context (IDs, names, counts)
3. Log at appropriate levels:
   - DEBUG: Detailed flow information
   - INFO: Important state changes
   - WARNING: Recoverable issues
   - ERROR: Failures requiring attention
4. Use `exc_info=True` for exceptions
5. Avoid logging sensitive data

## Example Debugging Session

```bash
# 1. Enable debug logging
export LOG_LEVEL=DEBUG

# 2. Reproduce the error
curl -X POST http://localhost:8000/ai/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai", "model": "gpt-4", "messages": [...]}'

# 3. Check logs
docker logs flowbuilder-backend | grep -A 20 "07:29:45"

# 4. Look for error indicators
docker logs flowbuilder-backend | grep -E "(ERROR|Exception|500)"

# 5. Trace the request path
docker logs flowbuilder-backend | grep "POST /ai/chat/completions"
```
