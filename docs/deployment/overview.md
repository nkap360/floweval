# Deployment Overview

Flow Builder offers multiple deployment options to suit different needs, from quick testing to enterprise-grade production deployments. This guide helps you choose the right deployment strategy for your use case.

## 🚀 Deployment Options

### 1. Leapcell.io (Recommended) ⭐

**Best for:** Production applications, teams, quick deployment

**Pros:**
- ✅ One-click deployment from GitHub
- ✅ Automatic SSL certificates
- ✅ Built-in monitoring and scaling
- ✅ Managed infrastructure
- ✅ Free tier available
- ✅ Auto-deploy on git push

**Cons:**
- ❌ Vendor lock-in
- ❌ Less control over infrastructure

**Cost:** Free tier + $20-50/month for production

[**📖 Full Guide**](leapcell.md)

---

### 2. Docker Self-Hosted

**Best for:** On-premises deployment, custom infrastructure

**Pros:**
- ✅ Full control over infrastructure
- ✅ Can run on any cloud provider
- ✅ Custom configuration possible
- ✅ No vendor lock-in

**Cons:**
- ❌ Requires DevOps expertise
- ❌ Manual SSL setup
- ❌ Self-managed scaling
- ❌ Manual monitoring setup

**Cost:** Infrastructure costs only

**Setup:**
```bash
# Clone and build
git clone https://github.com/nkap360/flowbuilder
cd flowbuilder
docker-compose up -d

# Configure environment variables
cp .env.example .env
# Edit .env with your keys
```

---

### 3. Cloud Provider (AWS/GCP/Azure)

**Best for:** Enterprise deployments, compliance requirements

**Pros:**
- ✅ Enterprise-grade security
- ✅ High availability
- ✅ Global distribution
- ✅ Advanced networking
- ✅ Compliance certifications

**Cons:**
- ❌ Complex setup
- ❌ Higher cost
- ❌ Requires cloud expertise
- ❌ Longer deployment time

**Cost:** $100-500+/month depending on scale

---

## 🏗️ Architecture Comparison

### Leapcell.io Architecture
```
┌─────────────────────────────────────────┐
│  Leapcell Platform (Managed)            │
│  ┌─────────────────────────────────────┐ │
│  │  Load Balancer + Auto SSL           │ │
│  └─────────────┬───────────────────────┘ │
│                │                       │
│  ┌─────────────┴─────────┐             │
│  │                       │             │
│  ▼                       ▼             │
│  ┌─────────┐        ┌──────────┐      │
│  │Frontend │        │ Backend  │      │
│  │Nginx +  │◄──────►│FastAPI   │      │
│  │React    │        │Python    │      │
│  └─────────┘        └──────────┘      │
│                              │         │
│                              ▼         │
│                    ┌─────────────────┐ │
│                    │ Persistent      │ │
│                    │ Storage (10GB)  │ │
│                    └─────────────────┘ │
└─────────────────────────────────────────┘
```

### Self-Hosted Architecture
```
┌─────────────────────────────────────────┐
│              Your Infrastructure         │
│  ┌─────────────────────────────────────┐ │
│  │  Reverse Proxy (Nginx/Traefik)     │ │
│  └─────────────┬───────────────────────┘ │
│                │                       │
│  ┌─────────────┴─────────┐             │
│  │                       │             │
│  ▼                       ▼             │
│  ┌─────────┐        ┌──────────┐      │
│  │Frontend │        │ Backend  │      │
│  │Nginx +  │◄──────►│FastAPI   │      │
│  │React    │        │Python    │      │
│  └─────────┘        └─────┬────┘      │
│                            │          │
│          ┌─────────────────┼─────────┐ │
│          │                 │         │ │
│          ▼                 ▼         │ │
│  ┌─────────────┐   ┌──────────────┐  │
│  │ PostgreSQL  │   │    Redis     │  │
│  │ (Optional)  │   │  (Optional)  │  │
│  └─────────────┘   └──────────────┘  │
└─────────────────────────────────────────┘
```

## 📊 Feature Comparison

| Feature | Leapcell.io | Docker Self-Hosted | Cloud Provider |
|---------|-------------|-------------------|----------------|
| **Setup Time** | 5 minutes | 1-2 hours | 1-2 days |
| **SSL Certificate** | ✅ Auto | 🔧 Manual | ✅ Auto |
| **Monitoring** | ✅ Built-in | 🔧 Manual setup | ✅ Advanced |
| **Scaling** | ✅ Auto | 🔧 Manual | ✅ Advanced |
| **Backups** | ✅ Auto | 🔧 Manual | ✅ Auto |
| **Cost** | $0-50/month | Infrastructure only | $100-500/month |
| **Control** | Medium | High | Full |
| **Expertise Required** | Low | Medium | High |
| **Compliance** | Standard | Self-managed | Enterprise |

## 🎯 Choosing the Right Option

### Choose Leapcell.io if:

- ✅ You want to deploy quickly (minutes)
- ✅ You don't have DevOps expertise
- ✅ You want managed infrastructure
- ✅ You're okay with vendor lock-in
- ✅ Your budget is under $100/month
- ✅ You want built-in monitoring

**Use Cases:**
- Startups and small teams
- MVPs and prototypes
- Internal tools
- Educational projects
- Quick production deployments

### Choose Docker Self-Hosted if:

- ✅ You have DevOps expertise
- ✅ You need full control over infrastructure
- ✅ You want to avoid vendor lock-in
- ✅ You have specific security requirements
- ✅ You want to optimize costs at scale
- ✅ You need custom configurations

**Use Cases:**
- Enterprise with on-premises requirements
- Applications with strict compliance needs
- High-traffic applications needing optimization
- Multi-cloud strategies
- Custom integration requirements

### Choose Cloud Provider if:

- ✅ You need enterprise-grade security
- ✅ You have compliance requirements (HIPAA, SOC2, etc.)
- ✅ You need global distribution
- ✅ You have dedicated DevOps team
- ✅ Budget is not a constraint
- ✅ You need advanced networking

**Use Cases:**
- Large enterprises
- Regulated industries
- High-traffic public applications
- Applications requiring specific compliance
- Global deployment requirements

## 🔄 Migration Paths

### From Leapcell.io to Self-Hosted

1. **Export Data:**
   ```bash
   # Export datasets and configurations
   leapcell export-data > flowbuilder-backup.json
   ```

2. **Setup Infrastructure:**
   ```bash
   # Deploy Docker setup
   git clone https://github.com/nkap360/flowbuilder
   cd flowbuilder
   docker-compose up -d
   ```

3. **Import Data:**
   ```bash
   # Import your data
   curl -X POST http://localhost:8000/import \
     -H "Content-Type: application/json" \
     -d @flowbuilder-backup.json
   ```

### From Self-Hosted to Leapcell.io

1. **Backup Data:**
   ```bash
   # Export from self-hosted
   docker exec flowbuilder-backend \
     python backup.py > backup.json
   ```

2. **Deploy to Leapcell:**
   - Push code to GitHub
   - Deploy to Leapcell
   - Configure environment variables

3. **Import Data:**
   - Import backup file via API
   - Verify all data migrated correctly

## 📋 Prerequisites Checklist

Before deploying to any platform:

### Infrastructure Requirements

**Minimum Requirements:**
- **CPU:** 1 core (2 cores recommended)
- **Memory:** 2GB RAM (4GB recommended)
- **Storage:** 10GB (50GB recommended)
- **Network:** 1Gbps preferred

**Software Dependencies:**
- **Node.js:** 18.x or later
- **Python:** 3.9 or later
- **Docker:** 20.x or later (for self-hosted)
- **Git:** For version control

### API Keys Required

**Essential:**
- [ ] **Google Gemini API Key** - Primary AI provider
- [ ] **Supabase Credentials** - Database and auth
  - Project URL
  - Anon public key
  - Service role key

**Optional:**
- [ ] **OpenAI API Key** - Alternative AI provider
- [ ] **DeepSeek API Key** - Cost-effective AI provider
- [ ] **Serper API Key** - Web search functionality

### Domain and SSL

**For Production:**
- [ ] **Custom Domain** - Your brand domain
- [ ] **DNS Configuration** - Point to deployment
- [ ] **SSL Certificate** - HTTPS required for production

## 🚦 Deployment Process Overview

### Step 1: Preparation (1-2 hours)
1. Set up accounts (Leapcell, cloud providers)
2. Generate API keys
3. Configure DNS
4. Test local deployment

### Step 2: Configuration (30 minutes)
1. Set environment variables
2. Configure domain settings
3. Set up monitoring
4. Prepare backups

### Step 3: Deployment (5-30 minutes)
1. Deploy application
2. Verify health checks
3. Test functionality
4. Configure SSL

### Step 4: Verification (30 minutes)
1. Test all features
2. Verify security settings
3. Set up monitoring alerts
4. Document configuration

## 🔧 Customization Options

### Environment-Specific Configurations

**Development:**
```bash
# .env.development
ENVIRONMENT=development
LOG_LEVEL=debug
VITE_API_URL=http://localhost:8000
```

**Staging:**
```bash
# .env.staging
ENVIRONMENT=staging
LOG_LEVEL=info
VITE_API_URL=https://staging-api.yourapp.com
```

**Production:**
```bash
# .env.production
ENVIRONMENT=production
LOG_LEVEL=warn
VITE_API_URL=https://api.yourapp.com
```

### Feature Flags

```bash
# Enable/disable features
ENABLE_PDF_PROCESSING=true
ENABLE_GOLDEN_GENERATION=true
ENABLE_CHAT_SPACES=true
ENABLE_WEB_SEARCH=false
```

### Custom Themes

```css
/* Custom branding */
:root {
  --primary-color: #your-brand-color;
  --secondary-color: #your-accent-color;
  --font-family: 'Your Font', sans-serif;
}
```

## 📈 Scaling Considerations

### Vertical Scaling (More Power)
- Increase CPU cores
- Add more RAM
- Faster storage
- Better network bandwidth

### Horizontal Scaling (More Instances)
- Load balancer setup
- Multiple app instances
- Database replication
- Content delivery network (CDN)

### Database Scaling
- Read replicas for better performance
- Database connection pooling
- Query optimization
- Caching layer (Redis)

## 🔍 Monitoring and Observability

### Key Metrics to Monitor

**Application Metrics:**
- Response time
- Error rate
- Request throughput
- Active users

**Infrastructure Metrics:**
- CPU usage
- Memory usage
- Disk I/O
- Network traffic

**Business Metrics:**
- User engagement
- Feature usage
- Conversion rates
- Error patterns

### Alerting Strategy

**Critical Alerts (immediate):**
- Service down
- Database connection lost
- Error rate > 10%
- Response time > 10 seconds

**Warning Alerts (within hour):**
- High CPU usage > 80%
- High memory usage > 90%
- Disk space > 85%
- Error rate > 5%

## 🆘 Getting Help

### Documentation Resources
- [**Leapcell Deployment Guide**](leapcell.md) - Step-by-step instructions
- [**Production Checklist**](production-checklist.md) - Complete verification
- [**Security Guide**](security.md) - Security best practices
- [**Troubleshooting**](../troubleshooting/common-issues.md) - Common issues and solutions

### Community Support
- **GitHub Issues:** [Report bugs or request features](https://github.com/nkap360/flowbuilder/issues)
- **GitHub Discussions:** [Community discussions](https://github.com/nkap360/flowbuilder/discussions)
- **Discord Community:** [Join our Discord](https://discord.gg/flowbuilder)

### Professional Support
- **Enterprise Support:** enterprise@flowbuilder.com
- **Consulting Services:** consulting@flowbuilder.com
- **Training Programs:** training@flowbuilder.com

---

**Ready to deploy?** Start with our [Leapcell Quick Deploy Guide](leapcell.md) for the fastest path to production!

---

**Last Updated:** December 3, 2025
**Version:** 1.0.0
**Status:** Production Ready ✅