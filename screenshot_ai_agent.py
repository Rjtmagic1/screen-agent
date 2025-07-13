#!/usr/bin/env python3
"""
Screenshot AI Agent - Step 2
Takes a screenshot and allows LLM queries on it using Gemini.
"""

import os
import time
from PIL import ImageGrab
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ScreenshotAIAgent:
    def __init__(self, api_key=None):
        """Initialize the AI agent with Gemini client"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def take_screenshot(self):
        """Take a screenshot and save it with timestamp"""
        try:
            # Take screenshot
            screenshot = ImageGrab.grab()
            
            # Create filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            # Save the screenshot
            screenshot.save(filename)
            print(f"Screenshot saved as: {filename}")
            
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def query_screenshot(self, image_path, question):
        """Query the LLM about the screenshot"""
        try:
            # Open the image with PIL
            from PIL import Image
            image = Image.open(image_path)
            
            # Create the prompt
            prompt = f"{question}\n\nPlease analyze this screenshot and provide a detailed response."
            
            # Generate response with image
            response = self.model.generate_content([prompt, image])
            
            return response.text
        except Exception as e:
            print(f"Error querying screenshot: {e}")
            return None

def main():
    """Main function to demonstrate the agent"""
    try:
        # Initialize the agent
        agent = ScreenshotAIAgent()
        
        # Take a screenshot
        print("Taking screenshot in 3 seconds...")
        time.sleep(3)
        screenshot_path = agent.take_screenshot()
        
        if screenshot_path:
            # Query the screenshot
            question = "What do you see in this screenshot? Please describe the main elements and any text that's visible."
            print(f"\nQuerying: {question}")
            
            response = agent.query_screenshot(screenshot_path, question)
            if response:
                print(f"\nAI Response:\n{response}")
            else:
                print("Failed to get AI response")
        else:
            print("Failed to take screenshot")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 