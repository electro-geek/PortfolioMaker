# Social Login Setup Guide

To enable "Login with Google" and "Login with GitHub", you need to register your application with these providers and get Client IDs and Secrets.

## 1. Google Login Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Search for "OAuth consent screen" and configure it:
   - User Type: External
   - Fill in required fields (App name, email, etc.)
4. Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
5. Application type: **Web application**.
6. Add **Authorized redirect URIs**:
   - Local: `http://127.0.0.1:8000/accounts/google/login/callback/`
   - Production (Vercel): `https://your-project.vercel.app/accounts/google/login/callback/`
7. Copy the **Client ID** and **Client Secret**.
8. Add them to your `config.properties` file:
   ```properties
   GOOGLE_CLIENT_ID=your_copied_client_id
   GOOGLE_CLIENT_SECRET=your_copied_client_secret
   ```

## 2. GitHub Login Setup

1. Go to [GitHub Developer Settings](https://github.com/settings/developers).
2. Click **New OAuth App**.
3. Fill in the details:
   - Application Name: PortfolioMaker
   - Homepage URL: `http://127.0.0.1:8000/` (or your Vercel URL)
   - Authorization callback URL: `http://127.0.0.1:8000/accounts/github/login/callback/`
     (For Vercel: `https://your-project.vercel.app/accounts/github/login/callback/`)
4. Click **Register application**.
5. Copy the **Client ID** and generate a new **Client Secret**.
6. Add them to your `config.properties` file:
   ```properties
   GITHUB_CLIENT_ID=your_copied_client_id
   GITHUB_CLIENT_SECRET=your_copied_client_secret
   ```

## 3. Database Requirement for Vercel

**IMPORTANT**: 
Since user accounts need to be stored permanently, you **cannot use the default SQLite database on Vercel** (it resets every time).

For production login to work, you must:
1. Create a Postgres database (e.g., on [Neon](https://neon.tech/), [Supabase](https://supabase.com/), or Vercel Postgres).
2. Get the `DATABASE_URL`.
3. Update `settings.py` to use `dj_database_url` to connect to this database.
4. Run migrations on that production database.

If you deploy to Vercel with just SQLite, users will be able to login, but their accounts will disappear after a few minutes/hours when the server restarts.
