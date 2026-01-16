# 🚀 Quick Deploy to Render.com

## 5-Minute Deployment

### 1️⃣ Push to GitHub
```bash
git add -A
git commit -m "Ready for deployment"
git push origin main
```

### 2️⃣ Go to Render
👉 https://render.com → Sign in with GitHub

### 3️⃣ Create Web Service
- Click **"New +"** → **"Web Service"**
- Connect your **News-app** repository
- Click **"Connect"**

### 4️⃣ Configure
- **Name:** `news-management-app`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Instance Type:** Free
- Click **"Create Web Service"**

### 5️⃣ Initialize Database
After deployment completes, visit:
```
https://your-app.onrender.com/initdb
```

## ✅ Done!
Your app is live at: `https://your-app.onrender.com`

---

## 📌 Important Notes

- **Free Tier:** Spins down after 15 min inactivity
- **First Load:** May take 30-60 seconds (cold start)
- **Auto-Deploy:** Push to GitHub = Auto-deploy
- **Logs:** Check Render dashboard for errors

---

## 🔗 Your URLs
- **Home:** `https://your-app.onrender.com/`
- **Articles:** `https://your-app.onrender.com/articles`
- **Create:** `https://your-app.onrender.com/articles/create`
- **Indian News:** `https://your-app.onrender.com/category/india`

---

**Full Guide:** See `RENDER_DEPLOYMENT.md`
