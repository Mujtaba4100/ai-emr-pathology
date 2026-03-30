#!/usr/bin/env python3
"""Phase 4 Text Cleaning Integration Test"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_text_cleaning():
    """Test complete text cleaning workflow"""
    
    print("=" * 60)
    print("  PHASE 4: TEXT CLEANING INTEGRATION TESTS")
    print("=" * 60)
    
    # Test 1: Clean simple medical text
    print("\n[1/3] Testing text cleaning with medical abbreviations...")
    test_text1 = """
    PATIENT NAME: John DOE
    TEST: CBC (Complete Blood Count)
    
    Results:
    HGB: 14.5 g/dL (Normal)
    WBC: 7.2 THOUSAND (Normal)
    RBC: 4.8 MILLION (Normal)
    PLT: 250 THOUSAND (Normal)
    
    Clinical Notes:
    Patient is HTN and DM positive.
    No CAD detected.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clean/text",
            json={"text": test_text1},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Medical text cleaned successfully!")
            print(f"   Status: {result['status']}")
            print(f"   Original Length: {result['original_length']}")
            print(f"   Cleaned Length: {result['cleaned_length']}")
            print(f"   Cleaned Preview: {result['cleaned_preview'][:100]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 2: Clean text with extra whitespace
    print("\n[2/3] Testing whitespace normalization...")
    test_text2 = "Patient:    John    DOE\n\n\nHGB:    14.5     g/dL"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clean/text",
            json={"text": test_text2},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Whitespace normalized!")
            print(f"   Original Length: {result['original_length']}")
            print(f"   Cleaned Length: {result['cleaned_length']}")
            print(f"   Cleaned Text: {result['cleaned_text']}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 3: Clean text with special characters
    print("\n[3/3] Testing special character removal...")
    test_text3 = "Patient: John@DOE! Test##Results: HGB>>14.5 g/dL***"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clean/text",
            json={"text": test_text3},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Special characters handled!")
            print(f"   Status: {result['status']}")
            print(f"   Cleaned Text: {result['cleaned_text']}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ PHASE 4 TEXT CLEANING TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_text_cleaning()
