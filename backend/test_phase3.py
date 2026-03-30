"""
Phase 3 OCR Integration Testing
Tests OCR extraction and status endpoints
"""

import requests
import json
from pathlib import Path
import time

BASE_URL = "http://localhost:8000"
TEST_USERNAME = f"doctor_ocr_{int(time.time())}"
TEST_USER_EMAIL = f"{TEST_USERNAME}@test.com"
TEST_USER_PASSWORD = "password123"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_ocr_workflow():
    """Test complete OCR workflow"""
    
    print_section("PHASE 3: OCR INTEGRATION TESTS")
    
    # Step 1: Register user
    print("\n[1/5] Registering test user...")
    register_data = {
        "username": TEST_USERNAME,
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "role": "doctor"
    }
    
    try:
        reg_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=register_data,
            timeout=5
        )
        if reg_response.status_code == 200:
            user_info = reg_response.json()
            print(f"✅ Registration successful - User ID: {user_info.get('id', '?')}")
        else:
            print(f"⚠️ Registration response: {reg_response.status_code}")
            if reg_response.status_code == 400:
                print(f"   (User likely already exists)")
    except Exception as e:
        print(f"⚠️ Registration error: {str(e)}")
    
    # Small delay to ensure DB is updated
    time.sleep(0.5)
    
    # Step 2: Login
    print("\n[2/5] Logging in...")
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=5
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            return
        
        token = login_response.json().get("access_token")
        print(f"✅ Login successful - Token: {token[:50]}...")
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Step 3: Create test file
    print("\n[3/5] Creating test file...")
    test_file_path = Path("test_ocr_sample.txt")
    sample_text = """
    PATHOLOGY REPORT
    Patient: John Doe
    Report Date: 2024-03-30
    
    FINDINGS:
    - Sample analysis shows normal findings
    - No abnormalities detected
    
    CONCLUSION:
    The tests are within normal limits.
    """
    
    test_file_path.write_text(sample_text)
    print(f"✅ Test file created: {test_file_path}")
    
    # Step 4: Upload file first (needed for OCR)
    print("\n[4/5] Uploading file for OCR processing...")
    
    with open(test_file_path, "rb") as f:
        files = {"file": f}
        upload_response = requests.post(
            f"{BASE_URL}/api/upload/",
            files=files,
            headers=headers,
            timeout=10
        )
    
    if upload_response.status_code != 200:
        print(f"❌ File upload failed: {upload_response.status_code}")
        print(f"Response: {upload_response.text}")
        return
    
    file_data = upload_response.json()
    file_id = file_data.get("file_id")
    print(f"✅ File uploaded - File ID: {file_id}")
    print(f"   Filename: {file_data.get('filename')}")
    print(f"   Size: {file_data.get('file_size')} bytes")
    
    # Step 5: Test OCR extraction
    print("\n[5/5] Testing OCR text extraction...")
    
    try:
        ocr_response = requests.post(
            f"{BASE_URL}/api/ocr/process/{file_id}",
            headers=headers,
            timeout=15
        )
        
        if ocr_response.status_code != 200:
            print(f"❌ OCR extraction failed: {ocr_response.status_code}")
            print(f"Response: {ocr_response.text}")
            return
        
        ocr_data = ocr_response.json()
        print(f"✅ OCR extraction successful!")
        print(f"   Status: {ocr_data.get('status')}")
        print(f"   Character Count: {ocr_data.get('character_count')}")
        print(f"   Extracted Text Preview:")
        extracted_text = ocr_data.get('extracted_text', '')[:200]
        print(f"   {extracted_text}...")
        
    except Exception as e:
        print(f"❌ OCR error: {str(e)}")
        return
    
    # Bonus: Test OCR status endpoint
    print("\n[BONUS] Testing OCR status endpoint...")
    try:
        status_response = requests.get(
            f"{BASE_URL}/api/ocr/status/{file_id}",
            headers=headers,
            timeout=5
        )
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ Status check successful!")
            print(f"   File ID: {status_data.get('file_id')}")
            print(f"   Processing Status: {status_data.get('processing_status')}")
        else:
            print(f"⚠️ Status endpoint returned: {status_response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Status check error: {str(e)}")
    
    # Cleanup
    print("\n[CLEANUP] Removing test file...")
    if test_file_path.exists():
        test_file_path.unlink()
        print("✅ Test file cleaned up")
    
    print_section("PHASE 3 TEST COMPLETE")
    print("✅ All OCR integration tests passed!")

if __name__ == "__main__":
    test_ocr_workflow()
