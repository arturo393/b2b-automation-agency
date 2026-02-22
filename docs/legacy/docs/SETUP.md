# 🚀 Portfolio Setup Guide

## Quick Customization Checklist

### 1. Update Personal Info (docs/index.html)

#### Google Analytics (Line ~13)
```html
<!-- Replace with your GA4 measurement ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    gtag('config', 'G-XXXXXXXXXX'); // Your actual ID
</script>
```

**Get GA4 ID:**
1. Go to [analytics.google.com](https://analytics.google.com)
2. Create property → Get Measurement ID
3. Copy `G-XXXXXXXXXX`

#### Contact Form (Line ~557)
```html
<!-- Replace with your Formspree endpoint -->
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

**Setup Formspree (FREE):**
1. Go to [formspree.io](https://formspree.io)
2. Sign up (free plan: 50 submissions/month)
3. Create new form
4. Copy form ID (format: `xnnqpzzz`)
5. Replace `YOUR_FORM_ID` in HTML

#### Email & Social Links (Line ~565)
```html
<a href="https://github.com/arturo393" target="_blank">GitHub</a>
<a href="https://linkedin.com/in/YOUR_LINKEDIN" target="_blank">LinkedIn</a>
<a href="https://twitter.com/YOUR_HANDLE" target="_blank">Twitter</a>
<a href="mailto:YOUR_EMAIL@domain.com">Email</a>
```

#### Project Links (Lines ~422, ~463, ~521)
Update GitHub repo URLs:
```html
<!-- Decision Maker -->
<a href="https://github.com/YOUR_USERNAME/decision-maker" target="_blank">

<!-- DeFi Monitor -->
<a href="https://github.com/YOUR_USERNAME/defi-monitor" target="_blank">
```

---

### 2. Add Your Projects

#### Option A: Replace Existing Projects
Edit the 3 project cards (lines ~361-380) with your actual projects.

#### Option B: Add New Projects
Copy this template:

```html
<div class="card" onclick="openModal('YOUR_PROJECT_ID')">
    <h3>Your Project Name</h3>
    <p>Short description of what the project does and tech used.</p>
    <div class="meta">Technology Stack · Status</div>
    <span class="view-demo">View Demo →</span>
</div>

<!-- Add corresponding modal -->
<div id="modal-YOUR_PROJECT_ID" class="modal" onclick="closeModal('YOUR_PROJECT_ID')">
    <div class="modal-content" onclick="event.stopPropagation()">
        <button class="modal-close" onclick="closeModal('YOUR_PROJECT_ID')">×</button>
        <h3>Your Project Name</h3>
        <p class="modal-meta">Tech Stack · Timeline · Status</p>
        
        <p style="color: #ccc; line-height: 1.6; margin-bottom: 20px;">
            Detailed description of the project, problem solved, and results.
        </p>
        
        <div class="modal-demo">
            <!-- Code output or demo here -->
        </div>
        
        <div class="modal-links">
            <a href="YOUR_GITHUB_URL" target="_blank" class="modal-link">View Code →</a>
            <a href="#contact" class="modal-link" onclick="closeModal('YOUR_PROJECT_ID')">Hire Me →</a>
        </div>
    </div>
</div>
```

---

### 3. Update Services & Pricing

Edit service cards (lines ~529-552) to match your offerings:

```html
<div class="service-card">
    <h4>Your Service Name</h4>
    <span class="price">$XXX (Xd)</span>
</div>
```

Pricing recommendations:
- Small scripts: $100-$300 (1-2d)
- Data pipelines: $400-$800 (3-5d)
- Full dashboards: $800-$1,500 (1-2w)
- Complex systems: $1,500+ (2-4w)

---

### 4. Add Project Screenshots

```bash
# Create assets directory
mkdir -p docs/assets/projects

# Add screenshots (PNG recommended)
# - decision-maker-demo.png
# - defi-monitor-dashboard.png
# - project-name-screenshot.png
```

Then embed in HTML:
```html
<img src="assets/projects/your-screenshot.png" 
     alt="Project Screenshot" 
     style="width: 100%; border-radius: 6px; margin: 16px 0;">
```

---

### 5. Deploy to GitHub Pages

```bash
# 1. Commit changes
git add -A
git commit -m "feat: Customize portfolio with my info"
git push origin master

# 2. Enable GitHub Pages
# Go to: Settings → Pages
# Source: Deploy from branch
# Branch: master → /docs
# Save

# 3. Your site will be live at:
# https://YOUR_USERNAME.github.io/REPO_NAME/
```

**Custom domain (optional):**
1. Buy domain (Namecheap, Google Domains)
2. Add `CNAME` file in docs/:
   ```
   yourdomain.com
   ```
3. Configure DNS records (GitHub docs)

---

## 🎨 Customization Tips

### Change Color Scheme

Find and replace these colors in `<style>` section:

```css
/* Primary blue */
#0066ff → Your color

/* Green (prices) */
#00ff88 → Your color

/* Background */
#0a0a0a → Your color

/* Cards */
#111 → Your color
```

### Update Hero Text (Line ~332)
```html
<h2>Build. <span class="highlight">Automate.</span> Scale.</h2>
<p>Your custom tagline here...</p>
```

### Update Stats (Lines ~344-356)
```html
<div class="stat">
    <div class="stat-value">48h</div>
    <div class="stat-label">Demo Delivery</div>
</div>
```

---

## 📊 Track Performance

### Google Analytics Events (Optional)

Add event tracking for buttons:

```html
<button onclick="gtag('event', 'contact_click', {'event_category': 'engagement'});">
    Contact Me
</button>
```

### Formspree Analytics

- Login to Formspree dashboard
- View submission stats
- Export leads to CSV

---

## 🚀 Next Steps

After basic setup:

1. ✅ Test contact form (send yourself a message)
2. ✅ Verify GA tracking (check Real-Time in dashboard)
3. ✅ Test on mobile (responsive design)
4. ✅ Run Lighthouse audit (aim for 90+ score)
5. ✅ Share on LinkedIn/Twitter

---

## 🐛 Troubleshooting

**Contact form not working:**
- Verify Formspree form ID is correct
- Check spam folder for confirmation email
- Ensure `method="POST"` in form tag

**Analytics not tracking:**
- Wait 24-48h for data to appear
- Check GA4 property ID is correct
- Use browser extension to verify (Google Tag Assistant)

**GitHub Pages not deploying:**
- Verify Settings → Pages is configured
- Check Actions tab for deploy status
- Ensure /docs folder has index.html

---

**Questions?** Open an issue or check [GitHub Pages docs](https://docs.github.com/en/pages)
