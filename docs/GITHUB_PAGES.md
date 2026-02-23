# GitHub Pages Setup

This repository includes a GitHub Pages site for browsing and copying Python code snippets.

## Features

- 📋 **One-click copy** - Copy any code snippet to clipboard instantly
- 🔍 **Search** - Quickly find files by name or path
- 📱 **Responsive** - Works on desktop and mobile devices
- 🌳 **Tree/Flat views** - Toggle between hierarchical and flat file views
- 🎨 **Syntax highlighting** - Code is highlighted with Prism.js

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** in the left sidebar
3. Under **Source**, select **GitHub Actions** (the included workflow handles deployment automatically)

### 2. Verify Deployment

After pushing to `main`, the GitHub Actions workflow will automatically deploy the site. You can check the deployment status:

1. Go to the **Actions** tab
2. Look for the "Deploy GitHub Pages" workflow
3. Once complete, your site will be available at:
   ```
   https://[username].github.io/Python-Playground/
   ```

### 3. Custom Domain (Optional)

If you want to use a custom domain:

1. Add a `CNAME` file in the root with your domain
2. Configure DNS records as per GitHub Pages documentation
3. Update the domain in repository settings → Pages

## How It Works

The site uses the GitHub API to:
- Fetch the list of `.py` files from the repository
- Load file contents on demand
- Display code with syntax highlighting
- Enable easy copying of code snippets

## Troubleshooting

### Site not loading
- Ensure GitHub Pages is enabled in repository settings
- Check that the workflow completed successfully in the Actions tab
- Verify the repository is public (or update API authentication for private repos)

### Files not showing
- Make sure you have `.py` files in the repository
- Check browser console for API errors
- Verify the repository name matches `TMHSDigital/Python-Playground` in `assets/js/app.js`

### API Rate Limits
- GitHub API has rate limits for unauthenticated requests
- For high traffic, consider using a GitHub token (update `app.js`)

## Local Development

To test the site locally:

```bash
# Using Python's built-in server
python -m http.server 8000

# Or using Node.js
npx serve .

# Then open http://localhost:8000
```

Note: The GitHub API allows CORS from any origin for public repos, so the site should work locally. If you see rate limit errors, consider adding a GitHub token in `app.js`.

