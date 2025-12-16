import google.generativeai as genai
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

def verify():
    print("Reading config.properties...")
    if not os.path.exists('config.properties'):
        print("❌ Error: config.properties file not found!")
        return

    config = load_properties('config.properties')
    api_key = config.get('GEMINI_API_KEY')

    if not api_key:
        print("❌ Error: GEMINI_API_KEY key not found.")
        return
    
    if "your_gemini_api_key_here" in api_key:
        print("❌ Error: Still using placeholder key.")
        return

    print(f"Found API Key: {api_key[:5]}...{api_key[-5:]}")
    
    print("\nTesting connection and listing available models...")
    try:
        genai.configure(api_key=api_key)
        
        # List available models
        print("Fetching available models...")
        found_working_model = False
        
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - Found model: {m.name}")
                # Try to use the first valid model we find
                if not found_working_model:
                    try:
                        print(f"\nTrying to generate with {m.name}...")
                        model = genai.GenerativeModel(m.name)
                        response = model.generate_content("Hello")
                        print(f"✅ Success! {m.name} is working.")
                        print(f"Response: {response.text}")
                        found_working_model = True
                    except Exception as e:
                        print(f"⚠️ Failed with {m.name}: {e}")

        if not found_working_model:
            print("\n❌ Could not generate content with any available model.")
            
    except Exception as e:
        print(f"❌ API Error: {str(e)}")

if __name__ == "__main__":
    verify()
