#!/usr/bin/env python3
"""
Simple test to verify Gemini API connectivity
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test basic Gemini API connectivity"""
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("❌ Please set your actual Gemini API key in the .env file")
            return False
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple text test
        response = model.generate_content("Say 'Hello, Gemini is working!'")
        print(f"✅ Gemini API test successful: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

if __name__ == "__main__":
    test_gemini_connection() 