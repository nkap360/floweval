# Security Guide - Flow Builder

## 🔒 API Key Protection

### Overview

Flow Builder takes API key security seriously. This document outlines the measures in place to protect your sensitive credentials.

## ✅ Security Measures

### 1. Local Storage Only

- **API keys are stored locally** in your browser's localStorage
- **Never sent to external servers** (except when making API calls to AI providers)
- **Never transmitted** over the network outside of authenticated API requests
- **Cleared when you log out** or clear browser data

### 2. Export Protection

When you export settings:

✅ **API keys are EXCLUDED** from the export file automatically
✅ You receive a confirmation dialog warning you about this
✅ Export includes all other settings (models, preferences, features)
❌ API keys must be re-entered after importing

**Example exported JSON:**
```json
{
  "aiConfigs": {
    "google": {
      "apiKey": "",  // ← Intentionally blank
      "model": "gemini-2.5-flash",
      "enabled": true
    }
  }
}
```

### 3. UI Masking

- API keys are masked by default with `•••••••••••`
- Toggle visibility with the 👁️ icon (only for current session)
- Masked state persists when taking screenshots

### 4. Import Safety

When importing settings:

- Settings file is validated before applying
- API keys from import are ignored (even if present)
- You're prompted to re-enter API keys after import
- Invalid files are rejected with error messages

## 🚨 Best Practices

### DO ✅

1. **Keep API keys private**
   - Never share screenshots showing visible API keys
   - Never commit `.env` files to Git
   - Never post API keys in public forums or tickets

2. **Use masked view for screenshots**
   - Ensure eye icon is closed (keys masked) before taking screenshots
   - Verify screenshot doesn't show sensitive data

3. **Rotate keys regularly**
   - Change API keys every 90 days
   - Immediately rotate if compromised
   - Use different keys for dev/staging/production

4. **Use environment variables in production**
   - For deployed instances, use Leapcell/cloud environment variables
   - Never hardcode API keys in source code

5. **Review exported files**
   - Check exported JSON before sharing
   - Verify API keys are blank
   - Only share with trusted team members

### DON'T ❌

1. **Never share visible API keys**
   - Don't take screenshots with keys visible
   - Don't copy-paste keys in chat/email
   - Don't share exported files containing keys (they shouldn't, but verify)

2. **Don't use production keys for development**
   - Use separate API keys for dev/test/prod
   - Easier to track usage and rotate

3. **Don't commit credentials**
   - Never commit `.env` files
   - Use `.gitignore` to exclude sensitive files
   - Use environment variables for CI/CD

4. **Don't store keys in plain text files**
   - Avoid saving keys in documents
   - Use password managers for key storage
   - Delete old keys from notes/docs

## 🔐 Key Management

### Getting API Keys

**Google Gemini:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Copy and paste into Settings → AI Providers → Google GenAI

**OpenAI:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy immediately (shown only once)
4. Paste into Settings → AI Providers → OpenAI

**DeepSeek:**
1. Visit [DeepSeek Platform](https://platform.deepseek.com)
2. Navigate to API Keys section
3. Generate new key
4. Paste into Settings → AI Providers → DeepSeek

### Rotating Keys

**When to rotate:**
- Every 90 days (recommended)
- If key is compromised or exposed
- When team member leaves
- After security incident

**How to rotate:**
1. Generate new key in provider dashboard
2. Update key in Flow Builder Settings
3. Test the new key (use Test button)
4. Delete old key from provider dashboard
5. Update production environment variables (if deployed)

## 🌐 Production Deployment

### Environment Variables

For production deployments (Leapcell, Docker, etc.):

**DO:**
```bash
# Use environment variables
export GOOGLE_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
```

**DON'T:**
```python
# Never hardcode in source code
api_key = "AIzaSy123456..."  # ❌ BAD
```

### Leapcell Deployment

When deploying to Leapcell:

1. Add API keys in Leapcell Dashboard → Environment Variables
2. Keys are encrypted by Leapcell
3. Never accessible in build logs
4. Not included in exported settings

See [DEPLOYMENT.md](../DEPLOYMENT.md) for full guide.

## 🔍 Auditing

### Check Your Security

**Quick Security Audit:**

- [ ] API keys are masked in UI (eye icon closed)
- [ ] Export file checked (no API keys present)
- [ ] `.env` file in `.gitignore`
- [ ] No API keys in Git history
- [ ] Production uses environment variables
- [ ] Keys rotated in last 90 days
- [ ] Different keys for dev/prod
- [ ] Team members use their own keys

### Finding Exposed Keys

**Check Git history:**
```bash
# Search for potential API keys in Git history
git log -S "AIzaSy" --all
git log -S "sk-" --all  # OpenAI keys
```

**Check files:**
```bash
# Search for API keys in files
grep -r "AIzaSy" .
grep -r "sk-proj" .
```

If you find exposed keys:
1. **Immediately rotate** the key
2. Delete from Git history (use `git filter-branch` or BFG Repo Cleaner)
3. Notify your team
4. Review access logs for unauthorized usage

## 🆘 If API Key is Compromised

**Immediate Actions:**

1. **Revoke the key immediately**
   - Go to provider dashboard
   - Delete or disable the compromised key

2. **Generate new key**
   - Create fresh API key
   - Update in Flow Builder Settings
   - Update in production environment

3. **Review usage logs**
   - Check provider dashboard for suspicious activity
   - Look for unusual API calls or usage spikes
   - Check for unauthorized access

4. **Notify if needed**
   - If key was used by others, notify them
   - If billing impact, contact provider support
   - Document the incident

5. **Update security practices**
   - Review how key was exposed
   - Implement additional protections
   - Train team on security best practices

## 📊 Monitoring

### Track API Usage

**Google Gemini:**
- Dashboard: [Google Cloud Console](https://console.cloud.google.com)
- Monitor quota and usage
- Set up billing alerts

**OpenAI:**
- Dashboard: [OpenAI Usage](https://platform.openai.com/usage)
- Track API calls and costs
- Set spending limits

**DeepSeek:**
- Dashboard: [DeepSeek Console](https://platform.deepseek.com)
- Monitor usage and quotas

**Warning Signs:**
- Unexpected usage spikes
- API calls from unknown IPs
- Usage when you're not using the app
- Quota exhausted unexpectedly

## 🛡️ Additional Security

### Browser Security

- Use HTTPS only (automatic in production)
- Keep browser updated
- Use private/incognito mode on shared computers
- Clear browser data after use on shared machines

### Network Security

- Avoid public WiFi when entering API keys
- Use VPN on untrusted networks
- Enable 2FA on AI provider accounts

### Team Security

- Each team member uses their own API keys
- Use workspace access controls
- Regular security training
- Document security procedures

## 📞 Support

**Security Concerns:**
- GitHub Issues: [Report security issue](https://github.com/nkap360/flowbuilder/security)
- Email: security@flowbuilder.com (for sensitive issues)

**Provider Support:**
- Google: [Support](https://support.google.com)
- OpenAI: [Help Center](https://help.openai.com)
- DeepSeek: [Support](https://platform.deepseek.com/support)

## 📝 Compliance

### Data Storage

- **API keys**: Stored in browser localStorage only
- **Settings**: Stored locally, not transmitted to servers
- **User data**: Managed through Supabase (see Supabase privacy policy)
- **Logs**: Stored locally, contain no API keys

### Privacy

- No telemetry or analytics tracking API keys
- Export/import features exclude sensitive data
- Open source - verify security yourself

## ✅ Security Checklist

Before going to production:

- [ ] All API keys stored in environment variables
- [ ] No hardcoded credentials in source code
- [ ] `.env` in `.gitignore`
- [ ] Git history clean (no exposed keys)
- [ ] Team trained on security practices
- [ ] Key rotation schedule established
- [ ] Monitoring and alerts configured
- [ ] Incident response plan documented
- [ ] Regular security audits scheduled

---

**Last Updated:** December 3, 2025  
**Version:** 1.0.0  
**Maintainer:** Flow Builder Security Team

**Remember:** When in doubt, treat API keys like passwords - never share them!
