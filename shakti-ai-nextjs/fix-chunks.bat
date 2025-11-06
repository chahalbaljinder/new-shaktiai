@echo off
echo Fixing chunk loading errors...
echo.

echo Step 1: Stopping any running Next.js processes...
taskkill /f /im node.exe >nul 2>&1

echo Step 2: Clearing build cache...
if exist .next rmdir /s /q .next
if exist node_modules\.cache rmdir /s /q node_modules\.cache

echo Step 3: Clearing npm cache...
npm cache clean --force

echo Step 4: Reinstalling dependencies...
npm install

echo Step 5: Starting development server...
start cmd /k "npm run dev"

echo.
echo Done! The development server should start in a new window.
echo If you still see chunk loading errors, try refreshing your browser or opening in incognito mode.
pause