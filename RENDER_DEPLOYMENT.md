# 🚀 Deploy News Management App to Render.com

## Step-by-Step Deployment Guide

### Prerequisites
- GitHub account with your code pushed
- Render.com account (free tier available)

---

## Step 1: Prepare Your Application

### 1.1 Create `requirements.txt` (if not exists)
Make sure all dependencies are listed:
```bash
pip freeze > requirements.txt
```

### 1.2 Create `render.yaml` (Optional but recommended)
```yaml
services:
  - type: web
    name: news-management-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.1
```

### 1.3 Update `app.py` for production
Change the last lines to:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 1.4 Add `gunicorn` to requirements.txt
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

---

## Step 2: Push Code to GitHub

```bash
git add -A
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Step 3: Deploy on Render.com

### 3.1 Sign Up / Log In
1. Go to https://render.com
2. Click **"Get Started"** or **"Sign In"**
3. Sign up with GitHub (recommended)

### 3.2 Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### 3.3 Connect Repository
1. Click **"Connect account"** if not connected
2. Select your **News-app** repository
3. Click **"Connect"**

### 3.4 Configure Service

**Basic Settings:**
- **Name:** `news-management-app` (or your choice)
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`

**Build Settings:**
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  gunicorn app:app
  ```

**Instance Type:**
- Select **"Free"** (or paid plan for better performance)

### 3.5 Environment Variables (Optional)
Click **"Advanced"** → **"Add Environment Variable"**

Add these if needed:
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

### 3.6 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Render will show build logs

---

## Step 4: Initialize Database

### 4.1 After Deployment Completes
1. Your app URL will be: `https://news-management-app.onrender.com`
2. Visit: `https://news-management-app.onrender.com/initdb`
3. This creates the database tables

### 4.2 Add Sample Data (Optional)
You can manually create articles through the UI or run seed script

---

## Step 5: Verify Deployment

### 5.1 Test Your App
Visit these URLs:
- **Home:** `https://your-app.onrender.com/`
- **Articles:** `https://your-app.onrender.com/articles`
- **Create:** `https://your-app.onrender.com/articles/create`

### 5.2 Check Logs
In Render dashboard:
1. Click on your service
2. Go to **"Logs"** tab
3. Monitor for any errors

---

## Step 6: Custom Domain (Optional)

### 6.1 Add Custom Domain
1. Go to **"Settings"** tab
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `news.yourdomain.com`

### 6.2 Update DNS
Add CNAME record in your domain provider:
```
Type: CNAME
Name: news
Value: your-app.onrender.com
```

---

## 🔧 Troubleshooting

### Issue: App Not Starting
**Solution:** Check logs for errors
```bash
# In Render dashboard → Logs tab
```

### Issue: Database Not Persisting
**Solution:** Render free tier uses ephemeral storage
- Upgrade to paid plan for persistent disk
- Or use external database (PostgreSQL)

### Issue: Slow Cold Starts
**Solution:** Free tier spins down after inactivity
- Upgrade to paid plan for always-on
- Or use a ping service to keep it alive

### Issue: News API Not Working
**Solution:** Check API key in environment variables
```
NEWS_API_KEY=your-api-key-here
```

---

## 📊 Render Free Tier Limits

- ✅ 750 hours/month free
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ⚠️ Spins down after 15 min inactivity
- ⚠️ Ephemeral storage (data lost on restart)

---

## 🚀 Upgrade Options

### Starter Plan ($7/month)
- Always-on (no spin down)
- Faster builds
- More resources

### Standard Plan ($25/month)
- Persistent disk (10GB)
- Better performance
- Priority support

---

## 📝 Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] Database initialized (`/initdb`)
- [ ] All pages load correctly
- [ ] News API fetching live news
- [ ] Dark/Light mode toggle works
- [ ] Like/Bookmark features work
- [ ] Load More button works
- [ ] Custom domain configured (if applicable)

---

## 🔗 Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **Render Docs:** https://render.com/docs
- **Your App URL:** `https://your-app.onrender.com`
- **GitHub Repo:** https://github.com/Praveen-hub-source/News-app

---

## 🎉 Success!

Your News Management App is now live on Render.com!

**Share your app:**
- URL: `https://your-app.onrender.com`
- Add to portfolio
- Share on social media

---

## 💡 Tips

1. **Monitor Usage:** Check Render dashboard for usage stats
2. **Auto-Deploy:** Push to GitHub → Auto-deploys to Render
3. **Environment Variables:** Store secrets in Render dashboard
4. **Logs:** Always check logs for debugging
5. **Backups:** Export database regularly (if using SQLite)

---

**Need Help?**
- Render Support: https://render.com/support
- GitHub Issues: https://github.com/Praveen-hub-source/News-app/issues

**Happy Deploying! 🚀**
