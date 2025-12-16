# Deploying PortfolioMaker to Vercel (Free Tier)

This guide will help you deploy your project to Vercel with full functionality, including persistent user data (Premium status) using a free Vercel Postgres database.

## Prerequisites
1.  A [GitHub](https://github.com/) account.
2.  A [Vercel](https://vercel.com/) account (Login with GitHub).

## Step 1: Push Code to GitHub
1.  Create a new repository on GitHub (e.g., `portfolio-maker`).
2.  Push your local code to this repository:
    ```bash
    git init
    git add .
    git commit -m "Initial commit for Vercel deployment"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/portfolio-maker.git
    git push -u origin main
    ```

## Step 2: Import Project in Vercel
1.  Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Find your `portfolio-maker` repository and click **"Import"**.

## Step 3: Configure Project
In the "Configure Project" screen:
1.  **Framework Preset**: Select **Django** (or leave as Other).
2.  **Root Directory**: Leave as `./`.

## Step 4: Add Environment Variables
Expand the **"Environment Variables"** section and add the following keys. Copy the values from your local `config.properties` file:

| Key | Value |
| --- | --- |
| `GEMINI_API_KEY` | (Your Gemini API Key) |
| `FIREBASE_API_KEY` | (Your Firebase API Key) |
| `FIREBASE_AUTH_DOMAIN` | (Your Auth Domain) |
| `FIREBASE_PROJECT_ID` | (Your Project ID) |
| `FIREBASE_STORAGE_BUCKET` | (Your Storage Bucket) |
| `FIREBASE_MESSAGING_SENDER_ID` | (Your Sender ID) |
| `FIREBASE_APP_ID` | (Your App ID) |
| `FIREBASE_CREDENTIALS_JSON` | (See Note Below*) |
| `DJANGO_SECRET_KEY` | (Generate a random string or use your local one) |
| `DEBUG` | `False` |

**(*) For `FIREBASE_CREDENTIALS_JSON`:**
Since you cannot upload the `firebase-adminsdk.json` file directly, you must:
1.  Open your `firebase-adminsdk.json` file locally.
2.  Copy the **entire content**.
3.  Paste it as the value for this variable.
4.  (My code is already set up to read this variable if the file is missing).

## Step 5: Add Database (Crucial for Premium Features)
1.  Before clicking "Deploy", look for the **Storage** tab in the Vercel dashboard (or create the project first, then go to Storage).
2.  Actually, the easiest way is:
    *   Click **"Deploy"** now. It might fail or work but lack the DB. That's fine.
    *   Once the project is created, go to the **Storage** tab in your project dashboard.
    *   Click **"Create Database"** -> **"Postgres"**.
    *   Accept the terms and create the free database.
    *   In the "Quickstart" step, click **"Connect Project"** and select your `portfolio-maker` project.
    *   **IMPORTANT**: This automatically adds the `POSTGRES_URL` (and others) to your Environment Variables.
    *   Go to the **Deployments** tab, click the three dots on the latest deployment, and select **"Redeploy"** to pick up the new database variables.

## Step 6: Run Migrations
Vercel doesn't run migrations automatically. You can run them from your local machine connecting to the remote DB, or use a workaround.
**Easiest Workaround:**
1.  Install the Vercel CLI: `npm i -g vercel`
2.  Link your project: `vercel link`
3.  Pull env vars: `vercel env pull .env.local`
4.  Run migrations locally pointing to cloud DB (advanced).

**Better Cloud Option:**
I have added a special command to `wsgi.py` or you can use the Vercel console if available.
Actually, for this setup, simply **Redeploying** usually works if `manage.py migrate` is in the build command.
**Update Build Command:**
1.  Go to Settings -> General -> Build & Development Settings.
2.  Change **Build Command** to: `python3 manage.py migrate && python3 manage.py collectstatic --noinput`
3.  Redeploy.

## Step 7: Done!
Your app should now be live at `https://portfolio-maker.vercel.app`.
- Login with Google.
- Upload a resume.
- It will persist your "Premium" status because it's using the Vercel Postgres database!
