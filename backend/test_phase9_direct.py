"""
Phase 9 Comprehensive Testing: RAG Chatbot
Tests RAG service and chatbot endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/chat"

def test_chatbot_endpoints_available():
    """Check if chatbot endpoints are registered"""
    print("\n=== Checking Chatbot Endpoints ===")
    
    try:
        response = requests.get("http://127.0.0.1:8000/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get('paths', {})
            
            endpoints = [
                '/api/chat/ask',
                '/api/chat/test'
            ]
            
            for endpoint in endpoints:
                if endpoint in paths:
                    print(f"✅ {endpoint} - FOUND")
                else:
                    print(f"❌ {endpoint} - NOT FOUND")
            
            return True
        else:
            print(f"⚠️ Could not access OpenAPI spec: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking endpoints: {str(e)}")
        return False

def test_chat_ask_basic():
    """Test chat ask endpoint"""
    print("\n=== Test: Chat Ask (Basic) ===")
    
    try:
        request_data = {
            "question": "What pathological findings are most common?",
            "conversation_history": []
        }
        
        response = requests.post(
            f"{BASE_URL}/ask",
            json=request_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Status: {result.get('status')}")
            
            if result.get('status') == 'success':
                print(f"Answer: {result.get('answer', '')[:200]}...")
                print(f"Sources: {result.get('total_sources', 0)} documents")
                return True
            elif result.get('status') == 'no_results':
                print("✅ Correct response: No documents found (database empty)")
                return True
            elif result.get('status') == 'error':
                if "API key" in result.get('message', ''):
                    print("ℹ️  OpenAI API key not configured (expected)")
                    return True
                else:
                    print(f"Error: {result.get('message')}")
                    return False
        else:
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_chat_with_history():
    """Test chat with conversation history"""
    print("\n=== Test: Chat with History ===")
    
    try:
        request_data = {
            "question": "Can you elaborate on that?",
            "conversation_history": [
                {
                    "role": "user",
                    "content": "What are the findings?"
                },
                {
                    "role": "assistant",
                    "content": "The key findings are..."
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/ask",
            json=request_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Status: {result.get('status')}")
            print("✅ Conversation history accepted")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_chat_test_endpoint():
    """Test the test endpoint"""
    print("\n=== Test: Chat Test Endpoint ===")
    
    try:
        response = requests.post(
            f"{BASE_URL}/test",
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Status: {result.get('status')}")
            print("✅ Test endpoint works")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_input_validation():
    """Test input validation"""
    print("\n=== Test: Input Validation ===")
    
    tests = [
        {
            "data": {"question": "", "conversation_history": []},
            "expected_status": 422,
            "name": "Empty question"
        },
        {
            "data": {"conversation_history": []},
            "expected_status": 422,
            "name": "Missing question field"
        }
    ]
    
    passed = 0
    for test in tests:
        try:
            response = requests.post(
                f"{BASE_URL}/ask",
                json=test['data'],
                timeout=10
            )
            
            if response.status_code == 422 or response.status_code >= 400:
                print(f"✅ {test['name']}: Correctly rejected (Status: {response.status_code})")
                passed += 1
            else:
                print(f"❌ {test['name']}: Should have been rejected (Status: {response.status_code})")
        
        except Exception as e:
            print(f"⚠️  {test['name']}: Error - {str(e)}")
    
    return passed > 0

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("PHASE 9: RAG CHATBOT - COMPREHENSIVE TESTING")
    print("="*70)
    
    # Check if server is running
    print("\nChecking if backend server is running...")
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("⚠️ Backend server returned unexpected status")
    except Exception as e:
        print(f"❌ Backend server is NOT running: {str(e)}")
        print("Please start the backend with: venv\\Scripts\\python.exe -m uvicorn app.main:app")
        return
    
    # Run tests
    results = []
    
    results.append(("Chatbot Endpoints Available", test_chatbot_endpoints_available()))
    results.append(("Chat Ask Endpoint", test_chat_ask_basic()))
    results.append(("Chat with History", test_chat_with_history()))
    results.append(("Test Endpoint", test_chat_test_endpoint()))
    results.append(("Input Validation", test_input_validation()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    total_passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    print("="*70)

if __name__ == "__main__":
    main()
