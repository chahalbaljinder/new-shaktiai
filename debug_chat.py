#!/usr/bin/env python3
"""
Debug script to test the chat functionality directly
"""

import sys
import os
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_chat():
    try:
        print("🔍 Starting chat debug test...")
        
        # Import the function
        from core.crew import ask_shakti_ai
        print("✅ Successfully imported ask_shakti_ai")
        
        # Test with a simple query
        query = "I'm feeling anxious about work"
        agent_types = ["mental"]
        
        print(f"🧪 Testing query: {query}")
        print(f"🤖 Using agents: {agent_types}")
        
        # Call the function
        response = ask_shakti_ai(query, agent_types)
        
        print("✅ Successfully got response!")
        print(f"📄 Response length: {len(response)} characters")
        print("\n" + "="*50)
        print("RESPONSE:")
        print("="*50)
        print(response)
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
        print("\n📍 Full Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_chat()
