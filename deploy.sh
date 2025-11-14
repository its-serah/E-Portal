#!/bin/bash

# 🚂 Railway Deployment Script for Face Recognition System
# This script prepares and pushes your project to GitHub for Railway deployment

set -e  # Exit on error

echo "🚀 Face Recognition System - Railway Deployment"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    USE_GH_CLI=true
    echo -e "${GREEN}✓${NC} GitHub CLI detected"
else
    USE_GH_CLI=false
    echo -e "${YELLOW}⚠${NC} GitHub CLI not found (will use manual method)"
fi

# Step 1: Prepare project
echo ""
echo -e "${BLUE}[1/4]${NC} Preparing project..."

# Create .env.example for Railway
cat > .env.railway << EOF
# Railway Environment Variables
# Copy these to Railway dashboard under Variables tab

DEBUG=False
SECRET_KEY=CHANGE-THIS-TO-A-RANDOM-SECRET-KEY-12345678
USE_POSTGRESQL=True
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# Optional: Telegram notifications
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHANNEL_ID=

# Railway will automatically provide DATABASE_URL
EOF

echo -e "${GREEN}✓${NC} Created .env.railway with example config"

# Step 2: Git operations
echo ""
echo -e "${BLUE}[2/4]${NC} Committing changes..."

git add .
git commit -m "Deploy: FastAPI Face Recognition System to Railway" || echo "No changes to commit"

echo -e "${GREEN}✓${NC} Changes committed"

# Step 3: Create/Update GitHub repo
echo ""
echo -e "${BLUE}[3/4]${NC} Setting up GitHub repository..."

REPO_NAME="Face-Recognition"
GITHUB_USER="its-serah"

if [ "$USE_GH_CLI" = true ]; then
    # Using GitHub CLI
    echo "Creating GitHub repository using gh CLI..."
    
    # Check if repo exists
    if gh repo view "$GITHUB_USER/$REPO_NAME" &> /dev/null; then
        echo -e "${YELLOW}⚠${NC} Repository already exists"
    else
        gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
        echo -e "${GREEN}✓${NC} Repository created and pushed"
    fi
else
    # Manual method
    echo ""
    echo -e "${YELLOW}Manual Setup Required:${NC}"
    echo ""
    echo "1. Go to: ${BLUE}https://github.com/new${NC}"
    echo "2. Repository name: ${GREEN}Face-Recognition${NC}"
    echo "3. Make it ${GREEN}Public${NC}"
    echo "4. ${RED}DON'T${NC} initialize with README"
    echo "5. Click ${GREEN}Create repository${NC}"
    echo ""
    read -p "Press ENTER after creating the repository..."
    
    # Set remote
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    
    echo ""
    echo "Pushing to GitHub..."
    git branch -M main
    
    if git push -u origin main; then
        echo -e "${GREEN}✓${NC} Code pushed to GitHub"
    else
        echo -e "${RED}✗${NC} Push failed. You may need to authenticate:"
        echo ""
        echo "Option 1: Use Personal Access Token"
        echo "  - Go to: https://github.com/settings/tokens"
        echo "  - Generate new token with 'repo' scope"
        echo "  - Run: git push -u origin main"
        echo "  - Username: $GITHUB_USER"
        echo "  - Password: [paste your token]"
        echo ""
        echo "Option 2: Use SSH"
        echo "  - Run: git remote set-url origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
        echo "  - Run: git push -u origin main"
        exit 1
    fi
fi

# Step 4: Railway deployment instructions
echo ""
echo -e "${BLUE}[4/4]${NC} Ready to deploy on Railway!"
echo ""
echo -e "${GREEN}✓${NC} GitHub repository ready at:"
echo -e "  ${BLUE}https://github.com/$GITHUB_USER/$REPO_NAME${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Go to: ${BLUE}https://railway.app${NC}"
echo "2. Click ${GREEN}Login${NC} → Sign in with GitHub"
echo "3. Click ${GREEN}New Project${NC} → Deploy from GitHub repo"
echo "4. Select ${GREEN}$REPO_NAME${NC}"
echo "5. Click ${GREEN}+ New${NC} → Database → ${GREEN}PostgreSQL${NC}"
echo "6. Go to service → ${GREEN}Variables${NC} tab"
echo "7. Copy variables from ${BLUE}.env.railway${NC} file"
echo "8. Go to ${GREEN}Settings${NC} → Click ${GREEN}Generate Domain${NC}"
echo ""
echo -e "${GREEN}⏱${NC}  Build time: ~5-10 minutes (ML libraries are large)"
echo ""
echo -e "${GREEN}🎉 Your app will be live at:${NC}"
echo "   https://your-app.up.railway.app"
echo ""
echo -e "${BLUE}Endpoints:${NC}"
echo "   🏠 Face Detection: https://your-app.up.railway.app/"
echo "   📊 Admin Dashboard: https://your-app.up.railway.app/admin"
echo "   ➕ Add Face: https://your-app.up.railway.app/faces/add"
echo "   📚 API Docs: https://your-app.up.railway.app/docs"
echo ""
echo -e "${GREEN}✅ Deployment preparation complete!${NC}"
