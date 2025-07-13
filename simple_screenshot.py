#!/usr/bin/env python3
"""
Simple screenshot test - Step 1
Just takes a screenshot and saves it to verify the basic functionality works.
"""

import os
from PIL import ImageGrab
import time

def take_screenshot():
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

if __name__ == "__main__":
    print("Taking screenshot in 3 seconds...")
    time.sleep(3)
    take_screenshot() 