@echo off
echo ================================
echo 🚀 Pushing BACKEND to GitHub...
echo ================================
cd "C:\Users\Harsh\Desktop\Boutique Order Via Pinterest App Ready\backend"

git init
git remote remove origin
git remote add origin https://github.com/harshdeepkaur097/boutique_order_link_backend.git

git add .
git status
git commit -m "Updated backend"
git branch -M main
git push -u origin main

echo.
echo ================================
echo 🚀 Pushing MAIN APP to GitHub...
echo ================================
cd "C:\Users\Harsh\Desktop\Boutique Order Via Pinterest App Ready"

git init
git remote remove origin
git remote add origin https://github.com/harshdeepkaur097/boutique_order_link.git

git add .
git status
git commit -m "Updated frontend Streamlit app"
git branch -M main
git push -u origin main

echo.
echo ✅ All done!
pause
