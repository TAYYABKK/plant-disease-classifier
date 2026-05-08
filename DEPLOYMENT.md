# Deploy to Render.com - Complete Guide

## Step 1: Create Render.com Account (FREE!)

1. Go to: https://render.com
2. Click **Sign Up** (use GitHub, Google, or email)
3. Verify your email
4. Done! ✅

---

## Step 2: Prepare Your Code (Already Done!)

I've created these deployment files:
- ✅ `render.yaml` - Deployment configuration
- ✅ `.gitignore` - What NOT to upload  
- ✅ `backend/app.py` - Updated to serve frontend & use PORT env var
- ✅ `frontend/script.js` - Updated to use relative URLs

---

## Step 3: Push to GitHub

### Create GitHub Account (if needed)
1. Go to: https://github.com
2. Sign up (free)
3. Verify email

### Push Your Code

```powershell
cd "c:\Users\tayya\Desktop\machine learning project"

# Initialize git
git init
git config user.email "your@email.com"
git config user.name "Your Name"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Plant Disease Classifier"

# Create new repo on GitHub
# 1. Go to https://github.com/new
# 2. Repository name: "plant-disease-classifier"
# 3. Click Create Repository
# 4. Copy the commands shown (should be like below):

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/plant-disease-classifier.git
git push -u origin main
```

---

## Step 4: Deploy on Render

1. Go to: https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Click **Connect Repository**
4. Select **plant-disease-classifier**
5. Fill in:
   - **Name**: `plant-disease-classifier` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python app.py`
   - **Plan**: Select `Free`
6. Click **Create Web Service**
7. Wait 2-3 minutes for deployment ⏳

---

## Step 5: Access Your App!

Once deployment is complete:
- Your app will be at: `https://plant-disease-classifier.onrender.com` (or whatever name you chose)
- You'll see a loading message first time (Render spins down free tier apps)
- Click the link and start using! 🎉

---

## Important Notes

### Model Files
- The trained models (`*.pkl` files) will be included in the deployment
- Models take up space but work fine on free tier
- If you retrain locally, push to GitHub and it auto-deploys

### Limitations of Free Tier
- Spins down after 15 minutes of inactivity (cold start)
- Limited memory (512MB)
- For this app: Should be fine! 
- Models load in ~10 seconds on first request

### Keep Backend Running Locally
While you test locally, keep running:
```powershell
python backend/app.py
```
Then open: `file:///c:/Users/tayya/Desktop/machine%20learning%20project/frontend/index.html`

---

## Troubleshooting

### Deployment Failed
- Check the build logs in Render dashboard
- Make sure `render.yaml` exists
- Make sure all files committed to GitHub

### App loading slowly
- First request takes 10-15 seconds (model loading)
- Subsequent requests are instant

### 502 Bad Gateway
- App may be spinning up (free tier spins down after 15 min inactivity)
- Refresh page, wait a moment
- Check logs: Dashboard → Your App → Logs

---

## Next Steps

1. ✅ Files prepared (DONE)
2. ⏭️ Push to GitHub (your turn)
3. ⏭️ Deploy on Render (your turn)
4. 🎉 Share with friends!

Let me know when you've deployed and I'll help troubleshoot! 🚀
