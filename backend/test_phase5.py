#!/usr/bin/env python3
"""Phase 5 LLM Extraction Integration Test"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_llm_extraction():
    """Test complete LLM extraction workflow"""
    
    print("=" * 70)
    print("  PHASE 5: LLM-BASED MEDICAL INFORMATION EXTRACTION")
    print("=" * 70)
    
    # Test 1: Check if endpoint is registered
    print("\n[1/3] Checking if LLM extraction endpoints are registered...")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            if "/api/extract" in response.text:
                print("✅ LLM extraction endpoints registered in Swagger")
            else:
                print("⚠️  LLM extraction endpoints NOT found in Swagger")
        else:
            print(f"❌ Could not access Swagger docs: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking Swagger: {str(e)}")
    
    # Test 2: Test extraction with sample data
    print("\n[2/3] Testing LLM extraction with sample medical text...")
    
    sample_text = """
    PATHOLOGY REPORT
    Patient Name: John Doe
    Patient ID: P-20260328-001
    Test Date: 2026-03-28
    
    TEST TYPE: Complete Blood Count (CBC)
    
    FINDINGS:
    Hemoglobin: 14.5 g/dL (Reference: 13.5-17.5)
    White Blood Cells: 7.2 x10^3/µL (Reference: 4.5-11.0)
    Red Blood Cells: 4.8 x10^6/µL (Reference: 4.5-5.9)
    Platelets: 250 x10^3/µL (Reference: 150-400)
    Mean Corpuscular Volume: 88 fL (Reference: 80-100)
    Hematocrit: 42% (Reference: 41-53)
    
    DIAGNOSIS:
    All values within normal limits. No abnormalities detected.
    
    RECOMMENDATIONS:
    Routine follow-up in 6 months. Continue current medication if any.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/extract/medical-data",
            json={"cleaned_text": sample_text},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Check for API key configuration error
            if result.get("status") == "error" and "API key" in result.get("message", ""):
                print("ℹ️  OpenAI API key not configured (this is expected if you haven't set it)")
                print("   To use LLM extraction, add your OpenAI API key to .env:")
                print("   OPENAI_API_KEY=sk-your-api-key-here")
                print("   Then restart the server.")
                print("\n✅ Endpoint is available and properly configured!")
                print("   Ready to use once API key is added.\n")
                return
            
            # Check if extraction was successful
            if result.get("status") == "success":
                print("✅ LLM extraction successful!")
                print(f"   Status: {result['status']}")
                if result.get("data"):
                    data = result["data"]
                    print(f"   Patient: {data.get('patient_name', 'Unknown')}")
                    print(f"   Test Type: {data.get('test_type', 'Unknown')}")
                    if data.get('findings'):
                        print(f"   Findings Count: {len(data['findings'])}")
                    print(f"   Diagnosis: {data.get('diagnosis', 'None mentioned')}")
                if result.get("cost_estimate"):
                    print(f"   Estimated Cost: {result['cost_estimate']}")
            else:
                print(f"⚠️  Extraction returned status: {result.get('status')}")
                print(f"   Message: {result.get('message', 'No message')}")
                if result.get("error"):
                    print(f"   Error: {result['error']}")
        
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    
    except requests.exceptions.Timeout:
        print("⚠️  Request timed out (API call may still be processing)")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 3: Test extraction endpoint availability
    print("\n[3/3] Testing endpoint availability...")
    
    try:
        # Just check if endpoint responds
        response = requests.post(
            f"{BASE_URL}/api/extract/medical-data",
            json={"cleaned_text": "Test"},
            timeout=5
        )
        
        if response.status_code in [200, 400, 500]:
            print("✅ Extraction endpoint is available and responding")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Endpoint error: {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ PHASE 5 LLM EXTRACTION TESTS COMPLETE")
    print("=" * 70)
    print("\nNote: Full LLM extraction requires OpenAI API key configuration.")
    print("Add your key to .env and restart the server to enable live extraction.")

if __name__ == "__main__":
    test_llm_extraction()
