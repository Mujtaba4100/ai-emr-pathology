"""
Phase 8 Comprehensive Testing: Semantic Search
Tests semantic search, keyword search, and combined search endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/search"

def test_semantic_search():
    """Test semantic search endpoint"""
    print("\n=== Testing Semantic Search ===")
    
    test_cases = [
        {
            "query": "malignant tumor diagnosis",
            "top_k": 5,
            "description": "Search for malignant tumors"
        },
        {
            "query": "normal findings",
            "top_k": 3,
            "description": "Search for normal findings"
        },
        {
            "query": "inflammation infection",
            "top_k": 5,
            "description": "Search for inflammation and infection"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['description']}")
        print(f"  Query: {test_case['query']}")
        print(f"  Top K: {test_case['top_k']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/semantic",
                json={
                    "query": test_case["query"],
                    "top_k": test_case["top_k"]
                }
            )
            
            result = response.json()
            print(f"  Status: {response.status_code}")
            print(f"  Response Status: {result.get('status')}")
            
            if result.get('status') == 'success':
                print(f"  Total Results: {result.get('total_results')}")
                
                # Show top results
                for j, r in enumerate(result.get('results', [])[:3], 1):
                    print(f"\n    Result {j}:")
                    print(f"      Document ID: {r.get('document_id')}")
                    print(f"      Similarity: {r.get('similarity_score')}")
                    print(f"      Test Type: {r.get('test_type')}")
                    print(f"      Diagnosis: {r.get('diagnosis')}")
                    print(f"      Preview: {r.get('text_preview', '')[:100]}...")
            else:
                print(f"  Error: {result.get('message')}")
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")

def test_keyword_search():
    """Test keyword search endpoint"""
    print("\n=== Testing Keyword Search ===")
    
    test_cases = [
        {
            "keyword": "cancer",
            "top_k": 5,
            "description": "Search for cancer"
        },
        {
            "keyword": "benign",
            "top_k": 3,
            "description": "Search for benign conditions"
        },
        {
            "keyword": "pathology",
            "top_k": 5,
            "description": "Search for pathology reports"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['description']}")
        print(f"  Keyword: {test_case['keyword']}")
        print(f"  Top K: {test_case['top_k']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/keyword",
                json={
                    "keyword": test_case["keyword"],
                    "top_k": test_case["top_k"]
                }
            )
            
            result = response.json()
            print(f"  Status: {response.status_code}")
            print(f"  Response Status: {result.get('status')}")
            
            if result.get('status') == 'success':
                print(f"  Total Results: {result.get('total_results')}")
                
                # Show top results
                for j, r in enumerate(result.get('results', [])[:3], 1):
                    print(f"\n    Result {j}:")
                    print(f"      Document ID: {r.get('document_id')}")
                    print(f"      Test Type: {r.get('test_type')}")
                    print(f"      Diagnosis: {r.get('diagnosis')}")
                    print(f"      Patient: {r.get('patient_name')}")
                    print(f"      Summary: {r.get('summary', '')[:100]}...")
            else:
                print(f"  Error: {result.get('message')}")
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")

def test_combined_search():
    """Test combined search endpoint"""
    print("\n=== Testing Combined Search (Semantic + Keyword) ===")
    
    test_cases = [
        {
            "query": "breast cancer diagnosis",
            "top_k": 3,
            "description": "Search for breast cancer"
        },
        {
            "query": "lymphoma treatment",
            "top_k": 3,
            "description": "Search for lymphoma"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['description']}")
        print(f"  Query: {test_case['query']}")
        print(f"  Top K: {test_case['top_k']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/combined",
                json={
                    "query": test_case["query"],
                    "top_k": test_case["top_k"]
                }
            )
            
            result = response.json()
            print(f"  Status: {response.status_code}")
            print(f"  Response Status: {result.get('status')}")
            
            # Semantic search results
            semantic = result.get('semantic_search', {})
            print(f"\n  Semantic Search Results: {semantic.get('total_results', 0)}")
            for j, r in enumerate(semantic.get('results', [])[:2], 1):
                print(f"    {j}. Similarity: {r.get('similarity_score')}")
            
            # Keyword search results
            keyword = result.get('keyword_search', {})
            print(f"\n  Keyword Search Results: {keyword.get('total_results', 0)}")
            for j, r in enumerate(keyword.get('results', [])[:2], 1):
                print(f"    {j}. {r.get('diagnosis')}")
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")

def test_input_validation():
    """Test input validation"""
    print("\n=== Testing Input Validation ===")
    
    invalid_tests = [
        {
            "endpoint": "/semantic",
            "data": {"query": ""},
            "expected": 400,
            "description": "Empty semantic query"
        },
        {
            "endpoint": "/semantic",
            "data": {"query": "test", "top_k": 100},
            "expected": 400,
            "description": "Semantic query with top_k > 50"
        },
        {
            "endpoint": "/keyword",
            "data": {"keyword": ""},
            "expected": 400,
            "description": "Empty keyword"
        },
        {
            "endpoint": "/keyword",
            "data": {"keyword": "test", "top_k": 0},
            "expected": 400,
            "description": "Keyword with top_k < 1"
        }
    ]
    
    for i, test in enumerate(invalid_tests, 1):
        print(f"\n  Test {i}: {test['description']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}{test['endpoint']}",
                json=test['data']
            )
            
            print(f"  Status Code: {response.status_code}")
            print(f"  Expected: {test['expected']}")
            print(f"  Result: {'PASS' if response.status_code == test['expected'] else 'FAIL'}")
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("PHASE 8: SEMANTIC SEARCH - COMPREHENSIVE TESTING")
    print("="*60)
    
    # Run tests
    test_semantic_search()
    test_keyword_search()
    test_combined_search()
    test_input_validation()
    
    print("\n" + "="*60)
    print("PHASE 8 TESTING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
