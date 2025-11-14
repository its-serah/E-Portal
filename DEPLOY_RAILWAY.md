# Deploy to Railway 🚂

## Step 1: Prepare GitHub Repo

1. **Initialize Git** (if not already):
```bash
cd /home/serah/Face-Recognition
git init
git add .
git commit -m "Initial commit - FastAPI Face Recognition"
```

2. **Create GitHub repo**:
   - Go to https://github.com/new
   - Name it: `Face-Recognition`
   - Don't initialize with README
   - Click "Create repository"

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/its-serah/Face-Recognition.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Railway

1. **Sign up for Railway**:
   - Go to https://railway.app
   - Click "Login" → Sign up with GitHub
   - Authorize Railway

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Face-Recognition` repo
   - Click "Deploy Now"

3. **Add PostgreSQL Database**:
   - In your project, click "+ New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will create database and add `DATABASE_URL` automatically

4. **Set Environment Variables**:
   - Click on your service
   - Go to "Variables" tab
   - Add these variables:

```
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
USE_POSTGRESQL=True
ACCESS_TOKEN_EXPIRE_MINUTES=30
TELEGRAM_BOT_TOKEN=your-telegram-bot-token (optional)
TELEGRAM_CHANNEL_ID=your-channel-id (optional)
```

5. **Generate Domain**:
   - Go to "Settings" tab
   - Click "Generate Domain"
   - You'll get: `your-app.up.railway.app`

## Step 3: Wait for Build

Railway will:
1. ✅ Detect Python
2. ✅ Install dependencies from requirements.txt
3. ✅ Run database migrations
4. ✅ Start your FastAPI server
5. ✅ Assign public URL

Build takes ~5-10 minutes (ML libraries are large).

## Step 4: Access Your App

Once deployed:
- 🏠 **Face Detection**: https://your-app.up.railway.app/
- 📊 **Admin Dashboard**: https://your-app.up.railway.app/admin
- 📚 **API Docs**: https://your-app.up.railway.app/docs

## Troubleshooting

### Build fails?
Check logs in Railway dashboard. Common issues:
- Missing dependencies: Update requirements.txt
- Memory issues: Upgrade Railway plan

### App crashes?
- Check environment variables are set
- Verify DATABASE_URL is connected

### Can't upload files?
Railway has ephemeral filesystem. For production:
- Use S3/Cloudinary for image storage
- Or use Railway volumes

## Cost

- **Free Tier**: $5 credit/month (enough for small usage)
- **Hobby Plan**: $5/month
- **Pro Plan**: $20/month (for heavy usage)

## Notes

- Railway auto-deploys on every GitHub push
- Database persists across deployments
- Uploaded faces stored temporarily (use external storage for production)
