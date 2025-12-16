# Firebase Authentication Setup Guide

To enable "Sign in with Google" using Firebase, follow these steps:

## 1. Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click **Add project** and follow the setup wizard.
3. Once created, go to **Authentication** -> **Sign-in method**.
4. Enable **Google** as a sign-in provider.
5. Configure the support email and save.
6. Click **Add new provider** and select **GitHub**.
7. To get the **Client ID** and **Client Secret**:
    - Go to [GitHub Developer Settings](https://github.com/settings/developers).
    - Create a **New OAuth App**.
    - **Homepage URL**: `http://localhost:8000` (or your production URL).
    - **Authorization callback URL**: Copy the callback URL shown in the Firebase Console setup window (e.g., `https://your-project.firebaseapp.com/__/auth/handler`).
    - Register the app and copy the Client ID and Client Secret back to Firebase Console.
8. Save the GitHub provider configuration.

## 2. Get Web App Configuration

1. In Project Overview, click the **Web** icon (</>) to add a web app.
2. Register the app (e.g., "PortfolioMaker").
3. Copy the `firebaseConfig` object values.
4. Add them to your `config.properties` file:

```properties
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

## 3. Get Admin SDK Credentials (Backend)

1. In Project Settings, go to the **Service accounts** tab.
2. Click **Generate new private key**.
3. Save the JSON file as `firebase-adminsdk.json` in your project root folder (same level as `manage.py`).
4. **IMPORTANT**: Do NOT commit this file to GitHub! It is already added to `.gitignore`.

## 4. Configure Authorized Domains

1. In Firebase Console -> Authentication -> Settings -> Authorized domains.
2. Add your Vercel domain (e.g., `your-app.vercel.app`).
3. `localhost` is authorized by default.

## 5. Vercel Deployment Note

For Vercel deployment, you cannot upload the `firebase-adminsdk.json` file. Instead:
1. Convert the JSON content to a single line string or base64.
2. Store it in a Vercel Environment Variable (e.g., `FIREBASE_CREDENTIALS_JSON`).
3. Update `settings.py` to read from this environment variable if the file doesn't exist.

(The current setup assumes the file exists for local development. For production, you might need to adjust `settings.py` to read from an ENV variable string).
