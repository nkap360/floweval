# Deploying to Leapcell.io

This comprehensive guide covers deploying Flow Builder to **Leapcell.io**, a modern platform for containerized applications. Leapcell provides automatic SSL, scaling, monitoring, and one-click deployment from GitHub.

## 🎯 Quick Deploy (5 Minutes)

### Option 1: One-Click Deploy

1. Click the deploy button:
   [![Deploy to Leapcell](https://leapcell.io/deploy-button.svg)](https://leapcell.io/new/clone?repository-url=https://github.com/nkap360/flowbuilder)

2. Configure environment variables in Leapcell:
   ```bash
   VITE_CUSTOM_OPENAI_ENDPOINT_API_KEY=your_key
   VITE_CUSTOM_OPENAI_ENDPOINT_ENDPOINT=https://custom_openai_endpoint.nimbusplane.io/v1
   VITE_DEEPSEEK_API_KEY=your_key
   VITE_SUPABASE_URL=your_url
   VITE_SUPABASE_ANON_KEY=your_key
   ```

3. Click "Deploy" and wait 5-10 minutes

### Option 2: Manual Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Leapcell deployment"
   git push origin main
   ```

2. **Create Leapcell Project**
   - Log in to [Leapcell.io](https://leapcell.io)
   - Click "New Project"
   - Connect your GitHub repository: `nkap360/flowbuilder`
   - Leapcell will auto-detect `leapcell.yaml`

3. **Configure Environment Variables**

   In the Leapcell dashboard, add these environment variables:

   **Required:**
   - `GOOGLE_API_KEY` - Your Google Gemini API key
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anonymous key
   - `VITE_SUPABASE_URL` - Same as SUPABASE_URL
   - `VITE_SUPABASE_ANON_KEY` - Same as SUPABASE_KEY
   - `VITE_API_URL` - Will be auto-set to your backend URL

   **Optional:**
   - `OPENAI_API_KEY` - For OpenAI models
   - `DEEPSEEK_API_KEY` - For DeepSeek models

4. **Deploy**
   - Click "Deploy"
   - Leapcell will build and deploy both frontend and backend
   - Wait 5-10 minutes for initial deployment

## 📋 Prerequisites

Before deploying, ensure you have:

- [ ] **Leapcell.io Account** - [Sign up here](https://leapcell.io)
- [ ] **GitHub Repository** - Your code pushed to GitHub
- [ ] **API Keys** - Google Gemini, Supabase (OpenAI/DeepSeek optional)
- [ ] **Docker** (for local testing) - [Install Docker](https://docs.docker.com/get-docker/)

### Getting Required API Keys

**Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Copy for Leapcell environment variables

**Supabase Setup:**
1. Create account at [supabase.com](https://supabase.com/dashboard)
2. Create new project
3. Go to Project Settings → API
4. Copy Project URL and anon public key

**Optional AI Providers:**
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **DeepSeek**: [platform.deepseek.com](https://platform.deepseek.com)

## 🏗️ Architecture on Leapcell

```
┌─────────────────────────────────────────┐
│  Leapcell Load Balancer + SSL (HTTPS)   │
└────────────┬────────────────────────────┘
             │
    ┌────────┴─────────┐
    │                  │
    ▼                  ▼
┌─────────┐      ┌──────────┐
│Frontend │      │ Backend  │
│ (Nginx) │◄────►│(FastAPI) │
│ Port 80 │      │ Port 8000│
└─────────┘      └──────────┘
                      │
                      ▼
              ┌────────────────┐
              │ Persistent     │
              │ Volume (10GB)  │
              └────────────────┘
```

### What's Deployed

**Frontend Service:**
- React 18 + TypeScript application
- Nginx web server
- Static file serving
- SPA routing support

**Backend Service:**
- FastAPI Python application
- AI provider integrations
- PDF processing capabilities
- Flow execution engine

**Storage:**
- 10GB persistent volume for user data
- Automatic backups (configurable)
- File upload storage

## 🔧 Configuration Files

Your repository includes these Leapcell-ready files:

- ✅ `leapcell.yaml` - Service configuration
- ✅ `Dockerfile` - Backend container
- ✅ `Dockerfile.frontend` - Frontend container
- ✅ `.dockerignore` - Build optimization
- ✅ `.env.example` - Environment template
- ✅ `backend/start.sh` - Production startup script

### leapcell.yaml

```yaml
version: "1.0"
name: flowbuilder
services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - 80:80
    environment:
      - VITE_API_URL=${LEAPCELL_API_URL}

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 8000:8000
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - DATA_DIR=/app/data
    volumes:
      - /app/data
```

## ✅ Verify Deployment

After deployment completes:

### Health Checks

```bash
# Backend health
curl https://your-app-api.leapcell.app/health
# Should return: {"status": "healthy"}

# Frontend
curl https://your-app.leapcell.app
# Should return HTML page
```

### Test Application

1. **Open Frontend**
   - Navigate to: `https://your-app.leapcell.app`
   - Page loads without errors
   - No console errors in browser DevTools

2. **Test Backend API**
   ```bash
   curl https://your-app-api.leapcell.app/flow-templates
   # Should return list of templates
   ```

3. **Test Full Workflow**
   - [ ] Login/signup works
   - [ ] Navigate to Flow Builder
   - [ ] Load "PDF to Golden Dataset" template
   - [ ] Upload test PDF
   - [ ] Generate goldens
   - [ ] Review page opens
   - [ ] Export works

### View Logs

```bash
# Install Leapcell CLI
npm install -g @leapcell/cli

# View logs
leapcell logs backend --tail 100
leapcell logs frontend --tail 100

# Follow logs in real-time
leapcell logs backend --follow
```

## 🌐 Custom Domain Setup

### 1. Add Domain in Leapcell

In Leapcell Dashboard → Domains:
- Add frontend domain: `flowbuilder.yourdomain.com`
- Add backend domain: `api.flowbuilder.yourdomain.com`

### 2. Update DNS Records

Add CNAME records:
- `flowbuilder` → `your-app.leapcell.app`
- `api` → `your-app-api.leapcell.app`

### 3. Update Environment Variables

Set `VITE_API_URL=https://api.flowbuilder.yourdomain.com` and redeploy frontend.

### 4. SSL/HTTPS

Leapcell automatically provisions SSL certificates via Let's Encrypt:
- ✅ Auto-renewal every 90 days
- ✅ HTTPS enforced by default
- ✅ HTTP → HTTPS redirect enabled

## 🔄 Auto-Deploy Setup

### Enable Automatic Deployments

1. **In Leapcell Dashboard:**
   - Go to Project Settings → Deployment
   - Enable "Auto-deploy on push"
   - Select branch: `main` or `production`

2. **Deploy Workflow:**
   ```bash
   # Make changes
   git add .
   git commit -m "feat: new feature"
   git push origin main

   # Leapcell automatically:
   # 1. Detects push
   # 2. Builds Docker images
   # 3. Runs health checks
   # 4. Deploys if successful
   # 5. Notifies via webhook
   ```

3. **Rollback if Needed:**
   ```bash
   # Via CLI
   leapcell rollback backend --version previous

   # Via Dashboard
   # Project → Deployments → Select version → Rollback
   ```

## 📊 Monitoring & Scaling

### Built-in Monitoring

Leapcell provides built-in metrics in the dashboard:
- **CPU Usage** - Monitor backend load
- **Memory Usage** - Track memory consumption
- **Request Rate** - API calls per minute
- **Response Time** - Average latency
- **Error Rate** - Failed requests

### Setting Up Alerts

1. **In Monitoring section:**
   - Enable alerts for high CPU (>80%)
   - Enable alerts for high memory (>90%)
   - Enable alerts for error rate (>5%)
   - Add email for notifications
   - Test alerts

### Auto-Scaling

Configure in `leapcell.yaml`:

```yaml
services:
  backend:
    # ... other config
    scaling:
      min: 1      # Minimum instances
      max: 3      # Maximum instances
      cpu_threshold: 80  # Scale up at 80% CPU
    resources:
      memory: 4Gi # Memory allocation
```

### Manual Scaling

```bash
# Scale backend to 3 instances
leapcell scale backend --replicas 3

# Scale frontend to 2 instances
leapcell scale frontend --replicas 2

# Check current scale
leapcell ps
```

## 🔒 Security Configuration

### Environment Variables Security

✅ **DO:**
- Use Leapcell's environment variable management
- Rotate API keys regularly (every 90 days)
- Use different keys for dev/staging/prod

❌ **DON'T:**
- Commit `.env` files to Git
- Hardcode API keys in source code
- Share production keys in public channels

### CORS Configuration

Update `backend/main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://flowbuilder.yourdomain.com",  # Your production domain
        "https://api.flowbuilder.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Key Rotation

```bash
# Rotate keys regularly
# 1. Generate new key in provider dashboard
# 2. Update environment variable in Leapcell
# 3. Trigger redeploy
# 4. Revoke old key after verification
```

## 💰 Cost Optimization

### Pricing Tiers

**Free Tier** (Good for testing):
- 1 CPU, 2GB RAM
- 10GB storage
- 100GB bandwidth/month

**Production Tier** (~$20-50/month):
- 2 CPUs, 4GB RAM
- 50GB storage
- Unlimited bandwidth
- Auto-scaling enabled

### Optimization Tips

1. **Right-size Resources**
   - Start small (1 CPU, 2GB RAM)
   - Monitor usage for 1 week
   - Adjust based on actual needs

2. **Use Auto-Scaling**
   - Scale down during low traffic
   - Scale up during peak hours
   - Set reasonable max limits

3. **Optimize Images**
   - Use Alpine Linux base images
   - Multi-stage builds (already implemented)
   - Remove unnecessary dependencies

4. **Cache Effectively**
   - Enable Redis for session caching
   - Cache AI responses when possible
   - Use CDN for static assets

## 🐛 Troubleshooting

### Common Issues

**Issue: Build Failed**
```bash
# Solution: Check build logs
leapcell logs --build backend
```

**Issue: Backend Unhealthy**
```bash
# Solution: Verify environment variables
leapcell env list
```

**Issue: CORS Error**
```python
# Solution: Update CORS in backend/main.py
allow_origins=["https://your-domain.com"]
```

**Issue: Out of Memory**
```yaml
# Solution: Increase resources in leapcell.yaml
resources:
  memory: 4Gi  # Increase from 2Gi
```

**Issue: Frontend shows "API not reachable"**
1. Check `VITE_API_URL` environment variable
2. Verify backend health endpoint responds
3. Check CORS configuration in backend

### Debugging Steps

1. **Check Deployment Status**
   - Backend: "Running" status ✓
   - Frontend: "Running" status ✓
   - No error messages in logs

2. **Verify Environment Variables**
   ```bash
   leapcell env list
   # Check all required variables are set
   ```

3. **Test Connectivity**
   ```bash
   curl https://your-app-api.leapcell.app/health
   ```

4. **Review Logs**
   ```bash
   leapcell logs backend --tail 200
   leapcell logs frontend --tail 200
   ```

## 📈 Performance Optimization

### Application Performance

1. **Enable Caching**
   - Redis for session management
   - CDN for static assets
   - Browser caching headers

2. **Database Optimization**
   - Add indexes on frequent queries
   - Optimize Supabase queries
   - Enable connection pooling

3. **Load Testing**
   ```bash
   # Install k6 or Apache Bench
   k6 run load-test.js

   # Monitor performance under load
   leapcell metrics backend --follow
   ```

### Cost Management

1. **Monitor Usage**
   - Check daily costs in Leapcell dashboard
   - Set budget alerts
   - Review resource usage weekly

2. **Right-Size Resources**
   - Start with minimum (1 CPU, 2GB RAM)
   - Monitor for 1 week
   - Adjust based on metrics

## 🆘 Support Resources

### Leapcell Support
- **Documentation**: https://docs.leapcell.io
- **Discord**: https://discord.gg/leapcell
- **Email**: support@leapcell.io

### Flow Builder Support
- **GitHub Issues**: https://github.com/nkap360/flowbuilder/issues
- **Documentation**: See user guides in this repository
- **Discussions**: https://github.com/nkap360/flowbuilder/discussions

### Emergency Contacts
- **Critical Issues**: emergency@flowbuilder.com
- **Security Issues**: security@flowbuilder.com
- **Enterprise Support**: enterprise@flowbuilder.com

---

## ✅ Deployment Success Checklist

Before marking deployment complete:

- [ ] ✅ Application accessible at production URL
- [ ] ✅ All API endpoints responding
- [ ] ✅ Frontend loads without errors
- [ ] ✅ Core workflows tested end-to-end
- [ ] ✅ SSL certificate active
- [ ] ✅ Monitoring and alerts configured
- [ ] ✅ Team notified and trained
- [ ] ✅ Documentation updated
- [ ] ✅ Backup strategy in place

## 🎉 Next Steps

Once deployed successfully:

1. **Test all workflows** end-to-end
2. **Monitor performance** for first 24 hours
3. **Set up alerts** for critical errors
4. **Document any custom** configurations
5. **Share access** with your team
6. **Train users** on the new system

---

**Version**: 1.0.0
**Last Updated**: December 3, 2025
**Platform**: Leapcell.io
**Status**: Production Ready ✅

**Your Flow Builder is now live on Leapcell!** 🚀