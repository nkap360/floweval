# Production Deployment Checklist

Complete this comprehensive checklist before deploying Flow Builder to production. This guide ensures security, performance, and reliability for your production deployment.

## 📋 Table of Contents

- [Pre-Deployment Checklist](#-pre-deployment-checklist)
- [Security Verification](#-security-verification)
- [Configuration Checklist](#-configuration-checklist)
- [Testing Checklist](#-testing-checklist)
- [Deployment Steps](#-deployment-steps)
- [Post-Deployment Verification](#-post-deployment-verification)
- [Monitoring & Operations](#-monitoring--operations)
- [Emergency Rollback Plan](#-emergency-rollback-plan)

## ✅ Pre-Deployment Checklist

### 🏗️ Code Quality & Preparation

- [ ] **All TypeScript errors resolved**
  ```bash
  npm run build
  # No build errors
  ```

- [ ] **Python dependencies up to date**
  ```bash
  cd backend
  pip list --outdated
  # Update if needed
  ```

- [ ] **All changes committed to Git**
  ```bash
  git status
  git add .
  git commit -m "Production ready deployment"
  ```

- [ ] **Code pushed to GitHub**
  ```bash
  git push origin main
  ```

- [ ] **Version tag created**
  ```bash
  git tag -a v1.0.0 -m "Production release"
  git push origin v1.0.0
  ```

- [ ] **Debug logs removed** - Clean production code
- [ ] **TODO comments addressed** - Either implement or remove
- [ ] **No console.log in production** - Use proper logging

### 🔧 Configuration Files

- [ ] **leapcell.yaml** - All environment variables listed
  - ✅ VITE_CUSTOM_OPENAI_ENDPOINT_API_KEY
  - ✅ VITE_CUSTOM_OPENAI_ENDPOINT_ENDPOINT
  - ✅ VITE_CUSTOM_OPENAI_ENDPOINT_MODEL
  - ✅ VITE_DEEPSEEK_API_KEY
  - ✅ VITE_OPENAI_API_KEY (optional)
  - ✅ VITE_GEMINI_API_KEY (optional)
  - ✅ VITE_SUPABASE_URL
  - ✅ VITE_SUPABASE_ANON_KEY

- [ ] **Dockerfile** - Multi-stage build optimized
- [ ] **Dockerfile.frontend** - Nginx config correct
- [ ] **.dockerignore** - Excludes unnecessary files
- [ ] **nginx.conf** - CORS and security headers configured

### 🔒 Security Verification

#### API Key Protection

- [ ] **Remove all API keys from code** - Check no hardcoded secrets
  ```bash
  grep -r "sk-" --include="*.ts" --include="*.tsx" --include="*.py" .
  grep -r "AIza" --include="*.ts" --include="*.tsx" --include="*.py" .
  # Should return no results
  ```

- [ ] **Verify .env is in .gitignore**
  ```bash
  git check-ignore .env
  # Should output: .env
  ```

- [ ] **Update .env.example** - Template with placeholder values only

- [ ] **Check for sensitive data in logs** - No API keys in log files

#### Environment Variables Security

- [ ] **No hardcoded secrets** in source code
- [ ] **All secrets in environment variables only**
- [ ] **API keys tested** - Verify each works before deployment
- [ ] **Different keys for dev/staging/prod** (recommended)

#### Code Security

- [ ] **Dependencies audited** - No known vulnerabilities
  ```bash
  npm audit
  pip-audit
  ```

- [ ] **CORS configured** for production domains only
- [ ] **Rate limiting enabled** (if implemented)
- [ ] **Input validation** on all API endpoints
- [ ] **SQL injection prevention** - Use parameterized queries

## 🌐 Environment Variables

### Required for Backend

- [ ] `GOOGLE_API_KEY` - Google Gemini API key
- [ ] `SUPABASE_URL` - Supabase project URL
- [ ] `SUPABASE_KEY` - Supabase anon key
- [ ] `SUPABASE_SERVICE_ROLE_KEY` - Supabase service key
- [ ] `DATA_DIR=/app/data` - Data directory path
- [ ] `ENVIRONMENT=production` - Environment flag

### Required for Frontend

- [ ] `VITE_API_URL` - Backend API URL (will be set by Leapcell)
- [ ] `VITE_SUPABASE_URL` - Supabase project URL
- [ ] `VITE_SUPABASE_ANON_KEY` - Supabase anon key

### AI Provider Keys (at least one required)

- [ ] `VITE_CUSTOM_OPENAI_ENDPOINT_API_KEY` (recommended - default provider)
- [ ] `VITE_CUSTOM_OPENAI_ENDPOINT_ENDPOINT` - Custom endpoint URL
- [ ] `VITE_CUSTOM_OPENAI_ENDPOINT_MODEL` - Model name
- [ ] `VITE_DEEPSEEK_API_KEY` (recommended - chatbot default)
- [ ] `VITE_DEEPSEEK_MODEL` - DeepSeek model
- [ ] `VITE_OPENAI_API_KEY` (optional)
- [ ] `VITE_GEMINI_API_KEY` (optional)

### Optional Configuration

- [ ] `SERPER_API_KEY` - For web search feature
- [ ] `LOG_LEVEL` - Logging verbosity
- [ ] `MAX_FILE_SIZE` - File upload limit
- [ ] `REDIS_URL` - For caching (optional)

## 🧪 Testing Checklist

### Local Testing

- [ ] **Backend runs locally**
  ```bash
  cd backend
  source venv/bin/activate
  uvicorn main:app --reload
  # Test: http://localhost:8000/health
  ```

- [ ] **Frontend runs locally**
  ```bash
  npm run dev
  # Test: http://localhost:3001
  ```

- [ ] **Docker build successful**
  ```bash
  docker-compose build
  docker-compose up
  # Test: http://localhost
  ```

- [ ] **Health endpoints working**
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status": "healthy"}
  ```

### Functional Testing

- [ ] **Test all AI providers** - Verify API connections work
  ```
  Settings → AI Provider Configuration → Test Connection
  ```

- [ ] **Test chatbot** - Verify DeepSeek integration
  ```
  Navigate to Chatbot → Send test message
  ```

- [ ] **Test PDF upload** - End-to-end workflow
  ```
  Annotation Studio → Upload PDF → Generate goldens
  ```

- [ ] **Test flow execution** - Run sample flow
  ```
  Flow Builder → Execute flow → Check output
  ```

- [ ] **Test authentication** - Login/logout flow
  ```
  Login → Access admin features → Logout
  ```

### Performance Testing

- [ ] **Load testing completed** - Test with realistic traffic
- [ ] **Memory usage acceptable** - No memory leaks
- [ ] **Response times acceptable** - < 2 seconds for most operations
- [ ] **Concurrent user testing** - Multiple users simultaneously

## 🚀 Deployment Steps

### Step 1: Platform Setup

- [ ] **Leapcell account created** - [Sign up](https://leapcell.io/signup)
- [ ] **GitHub repository connected** - Link to your repo
- [ ] **Project created** - New project in Leapcell dashboard
- [ ] **Branch selected** - `main` or `production`

### Step 2: Environment Configuration

- [ ] **All required environment variables set** in Leapcell dashboard
- [ ] **API keys tested** - Verify each works
- [ ] **Custom domain configured** (optional)
- [ ] **SSL certificates** - Auto-provisioned by Leapcell

### Step 3: Deployment

- [ ] **Initial deployment triggered**
- [ ] **Build logs monitored** - No build errors
- [ ] **Health checks passing** - All services healthy
- [ ] **DNS configured** - Custom domain pointing correctly

### Step 4: Verification

- [ ] **Frontend accessible** - Loads without errors
- [ ] **Backend API responding** - All endpoints work
- [ ] **Database connected** - Supabase connection successful
- [ ] **AI providers working** - All configured providers respond

## ✅ Post-Deployment Verification

### Health Checks

```bash
# Backend health
curl https://your-app-api.leapcell.app/health
# Expected: {"status": "healthy"}

# Frontend accessibility
curl https://your-app.leapcell.app
# Expected: HTML page loads

# API endpoints test
curl https://your-app-api.leapcell.app/flow-templates
# Expected: List of templates
```

### Application Testing

- [ ] **Login functionality works**
- [ ] **PDF upload and processing** - Test with actual PDF
- [ ] **Golden generation** - AI creates Q&A pairs
- [ ] **Golden review workflow** - Review interface loads
- [ ] **Export functionality** - JSON download works
- [ ] **Flow builder** - Create and execute flows
- [ ] **Chatbot** - All chat spaces working
- [ ] **Settings** - Configuration changes persist

### Performance Verification

- [ ] **Page load times** - < 3 seconds for initial load
- [ ] **API response times** - < 2 seconds average
- [ ] **File upload speeds** - Acceptable for large PDFs
- [ ] **Memory usage** - Under 80% of allocated memory
- [ ] **CPU usage** - Under 70% under normal load

## 📊 Monitoring & Operations

### Log Monitoring

- [ ] **Access logs configured** - Track all requests
- [ ] **Error logs monitored** - Alert on critical errors
- [ ] **Application logs reviewed** - Check for warnings
- [ ] **Log retention policy** - Set appropriate retention

```bash
# View logs with Leapcell CLI
leapcell logs backend --tail 100
leapcell logs frontend --tail 100

# Follow logs in real-time
leapcell logs backend --follow
```

### Metrics & Alerts

- [ ] **CPU monitoring** - Alert if >80% for 5 minutes
- [ ] **Memory monitoring** - Alert if >90% for 5 minutes
- [ ] **Error rate monitoring** - Alert if >5%
- [ ] **Response time monitoring** - Alert if >5 seconds
- [ ] **Disk space monitoring** - Alert if >85% full

### Backup & Recovery

- [ ] **Database backups configured** - Daily automatic backups
- [ ] **File backups configured** - User uploaded data
- [ ] **Configuration backups** - Environment variables and settings
- [ ] **Recovery procedures documented** - Steps to restore from backup
- [ ] **Restore testing completed** - Verify backups can be restored

## 🔐 Security Checklist

### Production Security

- [ ] **HTTPS enforced** - All traffic encrypted
- [ ] **Security headers configured**
  - [ ] X-Frame-Options: DENY
  - [ ] X-Content-Type-Options: nosniff
  - [ ] X-XSS-Protection: 1; mode=block
  - [ ] Referrer-Policy: no-referrer

- [ ] **API rate limiting** - Prevent abuse
- [ ] **Input validation** - All user inputs sanitized
- [ ] **SQL injection protection** - Parameterized queries only
- [ ] **XSS prevention** - Output encoding implemented

### Access Control

- [ ] **Strong password policy** - For admin accounts
- [ ] **Multi-factor authentication** - Enabled where possible
- [ ] **Least privilege principle** - Minimal required permissions
- [ ] **Access logging** - All admin actions logged
- [ ] **Session management** - Secure session handling

### Data Protection

- [ ] **Sensitive data encrypted** - At rest and in transit
- [ ] **API key rotation schedule** - Every 90 days
- [ ] **Data retention policy** - Clear data lifecycle
- [ ] **User data privacy** - GDPR compliance if applicable
- [ ] **Anonymous data collection** - No PII in analytics

## 🔄 Continuous Deployment

### Auto-Deploy Configuration

- [ ] **Auto-deploy enabled** - On push to main branch
- [ ] **Health checks configured** - Automatic rollback on failure
- [ ] **Deployment notifications** - Team alerted on deploy
- [ ] **Rollback procedures tested** - Quick recovery if issues

### Deployment Pipeline

- [ ] **Automated testing** - Tests run before deploy
- [ ] **Security scanning** - Automated vulnerability scanning
- [ ] **Performance testing** - Load testing in staging
- [ ] **Manual approval** - Required for production changes
- [ ] **Deploy documentation** - Clear steps and procedures

## 🚨 Emergency Rollback Plan

### Immediate Actions

If deployment fails or issues detected:

1. **Assess Impact** (5 minutes)
   - [ ] Identify affected systems
   - [ ] Determine user impact
   - [ ] Estimate recovery time

2. **Communication** (10 minutes)
   - [ ] Notify stakeholders
   - [ ] Post status update
   - [ ] Set up response team

3. **Rollback Decision** (15 minutes)
   - [ ] Evaluate rollback options
   - [ ] Consider hot fix vs rollback
   - [ ] Make decision and communicate

### Rollback Procedures

#### Database Rollback
```bash
# If database migration failed
# 1. Identify migration version
leapcell env get MIGRATION_VERSION

# 2. Rollback to previous version
leapcell env set MIGRATION_VERSION=previous_version

# 3. Restart services
leapcell restart backend
```

#### Application Rollback
```bash
# Rollback to previous deployment
leapcell rollback backend --version previous
leapcell rollback frontend --version previous

# Verify rollback success
curl https://your-app-api.leapcell.app/health
```

#### Configuration Rollback
```bash
# Export current configuration
leapcell env export > current-config.json

# Restore previous configuration
leapcell env import < previous-config.json

# Restart services
leapcell restart
```

### Post-Rollback Verification

- [ ] **Services healthy** - All components running
- [ ] **Data integrity** - No data corruption
- [ ] **Functionality restored** - Core features working
- [ ] **Performance acceptable** - No degradation
- [ ] **Security maintained** - No new vulnerabilities

## 📝 Documentation Updates

- [ ] **Deployment documentation updated** - Current procedures documented
- [ ] **Configuration changes documented** - All settings recorded
- [ ] **Troubleshooting guide updated** - New issues and solutions added
- [ ] **User notification sent** - Users informed of changes
- [ ] **Team training completed** - Team aware of new procedures

## ✅ Final Verification

Before marking deployment complete:

### Technical Verification

- [ ] ✅ Application accessible at production URL
- [ ] ✅ All API endpoints responding correctly
- [ ] ✅ Frontend loads without JavaScript errors
- [ ] ✅ Database queries executing successfully
- [ ] ✅ File uploads working properly
- [ ] ✅ AI providers responding correctly
- [ ] ✅ Authentication flows working
- [ ] ✅ Email notifications sending (if configured)

### Performance Verification

- [ ] ✅ Page load times < 3 seconds
- [ ] ✅ API response times < 2 seconds
- [ ] ✅ Memory usage < 80% of allocation
- [ ] ✅ CPU usage < 70% under normal load
- [ ] ✅ Error rate < 1% of total requests

### Security Verification

- [ ] ✅ SSL certificate valid and trusted
- [ ] ✅ Security headers properly configured
- [ ] ✅ No sensitive data exposed in logs
- [ ] ✅ API keys properly secured
- [ ] ✅ CORS correctly configured

### Operational Verification

- [ ] ✅ Monitoring and alerts configured
- [ ] ✅ Backup procedures tested
- [ ] ✅ Rollback procedures documented and tested
- [ ] ✅ Team notified and trained
- [ ] ✅ Documentation updated and accessible

---

## 🎊 Deployment Success! 🎉

Once all checklists are complete, your Flow Builder application is ready for production use.

### Next Steps

1. **Monitor closely** for first 24 hours
2. **Collect user feedback** and address issues
3. **Plan improvements** based on usage patterns
4. **Schedule regular maintenance** and updates
5. **Scale resources** based on actual usage

### Support Contacts

- **Technical Support**: support@flowbuilder.com
- **Emergency Issues**: emergency@flowbuilder.com
- **Documentation**: [docs/README.md](../README.md)
- **GitHub Issues**: [Report issues](https://github.com/nkap360/flowbuilder/issues)

---

**Checklist Completed**: _______________
**Deployed By**: _______________
**Deployment Date**: _______________
**Production URL**: _______________

**Notes**: _______________
_______________________________
_______________________________