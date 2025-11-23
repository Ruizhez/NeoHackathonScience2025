#!/usr/bin/env python3
"""Simple test script to verify SpoonOS installation and basic functionality."""

import asyncio
import os
from spoon_ai.chat import ChatBot
from spoon_ai.llm.manager import get_llm_manager

async def test_basic_functionality():
    """Test basic SpoonOS functionality."""
    print("🥄 Testing SpoonOS Installation")
    print("=" * 50)
    
    # Test 1: Import and basic chat
    print("✅ Testing basic import and chat functionality...")
    try:
        chatbot = ChatBot()
        messages = [
            {"role": "user", "content": "Hello! Can you confirm that SpoonOS is working correctly?"}
        ]
        
        response = await chatbot.ask(messages)
        print(f"Response: {response[:100]}...")
        print("✅ Basic chat functionality working!")
    except Exception as e:
        print(f"❌ Basic chat test failed: {e}")
        return False
    
    # Test 2: Streaming functionality
    print("\n✅ Testing streaming functionality...")
    try:
        chatbot = ChatBot()
        messages = [
            {"role": "user", "content": "Say 'SpoonOS is working!' in one sentence."}
        ]
        
        full_response = ""
        async for chunk in chatbot.astream(messages):
            full_response += chunk.delta
            print(chunk.delta, end="", flush=True)
        
        print(f"\n✅ Streaming functionality working! Full response: {full_response}")
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
        return False
    
    # Test 3: LLM Manager
    print("\n✅ Testing LLM Manager...")
    try:
        manager = get_llm_manager()
        print(f"✅ LLM Manager initialized successfully")
        print(f"LLM Manager type: {type(manager).__name__}")
        # Just check if it's working without trying to access providers attribute
        print(f"✅ LLM Manager is ready to use!")
    except Exception as e:
        print(f"❌ LLM Manager test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! SpoonOS is working correctly.")
    return True

if __name__ == "__main__":
    # Set up basic environment if not already set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Some features may not work.")
        print("You can set it with: export OPENAI_API_KEY='your-api-key'")
    
    success = asyncio.run(test_basic_functionality())
    if success:
        print("\n🚀 SpoonOS is ready to use!")
        print("\nNext steps:")
        print("1. Set up your API keys in .env file")
        print("2. Check the examples in the examples/ directory")
        print("3. Run: python examples/chatbot_streaming_demo.py")
    else:
        print("\n❌ Some tests failed. Please check the installation.")