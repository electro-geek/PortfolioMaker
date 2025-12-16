import os

def load_properties(filepath):
    props = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    props[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading config file: {e}")
    return props

def check_firebase_config():
    print("Checking Firebase Configuration...")
    if not os.path.exists('config.properties'):
        print("❌ Error: config.properties file not found!")
        return

    config = load_properties('config.properties')
    
    required_keys = [
        'FIREBASE_API_KEY',
        'FIREBASE_AUTH_DOMAIN',
        'FIREBASE_PROJECT_ID',
        'FIREBASE_STORAGE_BUCKET',
        'FIREBASE_MESSAGING_SENDER_ID',
        'FIREBASE_APP_ID'
    ]
    
    missing = []
    placeholders = []
    
    for key in required_keys:
        val = config.get(key)
        if not val:
            missing.append(key)
        elif "your_" in val:
            placeholders.append(key)
            
    if missing:
        print(f"❌ Missing keys in config.properties: {', '.join(missing)}")
    elif placeholders:
        print(f"❌ The following keys still have placeholder values: {', '.join(placeholders)}")
        print("👉 You need to get these values from the Firebase Console -> Project Settings -> General -> Your Apps -> Web App")
    else:
        print("✅ Firebase configuration looks correct in config.properties!")

if __name__ == "__main__":
    check_firebase_config()
