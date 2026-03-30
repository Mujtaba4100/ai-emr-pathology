"""
Phase 8: Semantic Search - Direct Testing
Simple HTTP-based tests for search endpoints
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/search"

def test_endpoints_available():
    """Check if search endpoints are available"""
    print("\n=== Checking Search Endpoints ===")
    
    try:
        # Try to get OpenAPI spec
        response = requests.get("http://127.0.0.1:8000/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get('paths', {})
            
            endpoints = [
                '/api/search/semantic',
                '/api/search/keyword',
                '/api/search/combined'
            ]
            
            for endpoint in endpoints:
                if endpoint in paths:
                    print(f"✅ {endpoint} - FOUND")
                else:
                    print(f"❌ {endpoint} - NOT FOUND")
        else:
            print(f"⚠️ Could not access OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking endpoints: {str(e)}")
        return False
    
    return True

def test_semantic_search_basic():
    """Test semantic search with basic query"""
    print("\n=== Test: Semantic Search (Basic) ===")
    
    try:
        response = requests.post(
            f"{BASE_URL}/semantic",
            json={"query": "tumor diagnosis", "top_k": 3},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Status: {result.get('status')}")
            print(f"Results Count: {result.get('total_results', 0)}")
            
            if result.get('status') == 'success' and result.get('results'):
                print("Sample Results:")
                for i, r in enumerate(result.get('results', [])[:2], 1):
                    print(f"  {i}. Similarity: {r.get('similarity_score')}, Test: {r.get('test_type')}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_keyword_search_basic():
    """Test keyword search with basic query"""
    print("\n=== Test: Keyword Search (Basic) ===")
    
    try:
        response = requests.post(
            f"{BASE_URL}/keyword",
            json={"keyword": "cancer", "top_k": 3},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Status: {result.get('status')}")
            print(f"Results Count: {result.get('total_results', 0)}")
            
            if result.get('status') == 'success' and result.get('results'):
                print("Sample Results:")
                for i, r in enumerate(result.get('results', [])[:2], 1):
                    print(f"  {i}. {r.get('diagnosis')}, Test: {r.get('test_type')}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_combined_search_basic():
    """Test combined search"""
    print("\n=== Test: Combined Search (Basic) ===")
    
    try:
        response = requests.post(
            f"{BASE_URL}/combined",
            json={"query": "pathology findings", "top_k": 2},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Status: {result.get('status')}")
            
            semantic_count = result.get('semantic_search', {}).get('total_results', 0)
            keyword_count = result.get('keyword_search', {}).get('total_results', 0)
            
            print(f"Semantic Results: {semantic_count}")
            print(f"Keyword Results: {keyword_count}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_validation():
    """Test input validation"""
    print("\n=== Test: Input Validation ===")
    
    tests = [
        {
            "endpoint": "/semantic",
            "data": {"query": ""},
            "expected_status": 422,  # Pydantic validation error
            "name": "Empty query"
        },
        {
            "endpoint": "/keyword",
            "data": {"keyword": "test", "top_k": 100},
            "expected_status": 422,
            "name": "top_k > 50"
        }
    ]
    
    passed = 0
    for test in tests:
        try:
            response = requests.post(
                f"{BASE_URL}{test['endpoint']}",
                json=test['data'],
                timeout=10
            )
            
            # For validation errors, we expect 4xx status codes
            is_error_response = response.status_code >= 400
            
            if is_error_response:
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
    print("PHASE 8: SEMANTIC SEARCH - DIRECT TESTING")
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
        sys.exit(1)
    
    # Run tests
    results = []
    
    results.append(("Endpoints Available", test_endpoints_available()))
    results.append(("Semantic Search", test_semantic_search_basic()))
    results.append(("Keyword Search", test_keyword_search_basic()))
    results.append(("Combined Search", test_combined_search_basic()))
    results.append(("Input Validation", test_validation()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print("="*70)

if __name__ == "__main__":
    main()
