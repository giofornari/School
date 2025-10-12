# Quick Start Guide for GitHub Pages Showcase 🚀

## What Was Created

A complete GitHub Actions workflow that:
1. ✅ Compiles all your Java projects
2. ✅ Runs them and captures output
3. ✅ Generates a beautiful showcase website
4. ✅ Deploys to GitHub Pages automatically

## Setup Steps (5 minutes)

### Step 1: Push the Changes

```bash
git add .github/ docs/ README.md
git commit -m "Add GitHub Actions workflow for showcase website"
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to: https://github.com/bigBrodyG/JavaProjects/settings/pages
2. Under "Build and deployment":
   - **Source**: Select `GitHub Actions`
3. Click **Save**

### Step 3: Run the Workflow

Option A - Automatic (recommended):
- Just push any commit to `main` branch - it runs automatically!

Option B - Manual:
1. Go to: https://github.com/bigBrodyG/JavaProjects/actions
2. Click "Build Java Showcase Website"
3. Click "Run workflow" → "Run workflow"

### Step 4: View Your Website

After ~2-3 minutes, visit:
```
https://bigBrodyG.github.io/JavaProjects/
```

## What You'll See

Your website will display each Java project with:
- 📝 **Source code** - Syntax highlighted and formatted
- 🔨 **Build status** - Shows if compilation succeeded
- ▶️ **Program output** - Live results from running the code
- 🎨 **Beautiful design** - Modern, responsive interface

## Files Created

```
.github/
├── workflows/
│   └── build-showcase.yml    # GitHub Actions workflow
├── scripts/
│   └── generate-site.py      # Website generator
└── README.md                 # Documentation

docs/
└── .gitkeep                  # Placeholder (replaced by generated site)
```

## Troubleshooting

### "Page not found" after setup
- Wait 2-3 minutes for the first deployment
- Check Actions tab for workflow status
- Ensure GitHub Pages source is set to "GitHub Actions"

### Workflow fails
- Check the Actions tab for error logs
- Most common: Java compilation errors in code
- Fix any syntax errors and push again

### Want to test locally?
```bash
# Install Python 3 if needed
python3 --version

# Run the generator locally
mkdir -p docs
python3 .github/scripts/generate-site.py

# Open the generated site
xdg-open docs/index.html  # Linux
open docs/index.html      # macOS
```

## Customization

### Change Colors/Styling
Edit the CSS in `.github/scripts/generate-site.py` (look for the `<style>` section)

### Add New Projects
1. Add your project folder with `src/` directory
2. Edit `.github/scripts/generate-site.py` - add to `projects` list
3. Update workflow to compile and run it

### Change Workflow Triggers
Edit `.github/workflows/build-showcase.yml` - modify the `on:` section

## Support

- 📖 Full documentation: `.github/README.md`
- 🐛 Issues: https://github.com/bigBrodyG/JavaProjects/issues
- 💬 Questions: Open a discussion or issue

## Next Steps

1. ✅ Push the changes
2. ✅ Enable GitHub Pages
3. ✅ Watch the workflow run
4. ✅ Share your showcase website!

Enjoy your automated Java showcase! 🎉
