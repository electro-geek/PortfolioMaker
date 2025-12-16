# Deploying to Vercel

This project has been configured for **free, stateless deployment** on Vercel.

## Prerequisites

1.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com).
2.  **GitHub Account**: Push this code to a GitHub repository.

## Steps to Deploy

1.  **Push to GitHub**:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/your-username/your-repo-name.git
    git push -u origin main
    ```

2.  **Import to Vercel**:
    *   Go to your Vercel Dashboard.
    *   Click **"Add New..."** -> **"Project"**.
    *   Import your GitHub repository.

3.  **Configure Environment Variables**:
    *   In the Vercel project settings, go to **"Environment Variables"**.
    *   Add the following variables:
        *   **Key**: `GEMINI_API_KEY`, **Value**: (Your Gemini API key)
        *   **Key**: `GOOGLE_CLIENT_ID`, **Value**: (Your Google Client ID)
        *   **Key**: `GOOGLE_CLIENT_SECRET`, **Value**: (Your Google Client Secret)
        *   **Key**: `GITHUB_CLIENT_ID`, **Value**: (Your GitHub Client ID)
        *   **Key**: `GITHUB_CLIENT_SECRET`, **Value**: (Your GitHub Client Secret)
    *   (Optional) Add `DEBUG` = `False`.

4.  **Deploy**:
    *   Click **"Deploy"**.
    *   Vercel will build your project and give you a live URL (e.g., `https://your-project.vercel.app`).

## Important Notes

*   **Database**: This deployment is **stateless**. It does NOT use a database.
    *   Uploaded resumes are processed in memory.
    *   Extracted data is stored in your browser cookies (Session).
    *   Generated portfolios are created on-the-fly.
*   **Files**: You cannot save files to the server. The "Download" button generates the ZIP file in memory.
*   **Limitations**:
    *   Sessions expire after 24 hours.
    *   Maximum upload size is limited by Vercel (usually 4.5MB for serverless functions, but we handle it in memory so it might be slightly higher, though keep it under 4MB to be safe).

## Troubleshooting

*   **Static Files 404**: If CSS/JS is missing, ensure `whitenoise` is in `requirements.txt` and `MIDDLEWARE` (it has been added).
*   **Deployment Error**: Check Vercel logs. Common issues are missing environment variables.
