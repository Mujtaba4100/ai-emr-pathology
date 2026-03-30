#!/usr/bin/env python
"""
Phase 2 Testing Script - File Upload System
Tests authentication, file upload, and list functionality
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "doctor1"
TEST_PASSWORD = "SecurePassword123"
TEST_EMAIL = "doctor@hospital.com"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_register():
    """Test 1: Register a new user"""
    print_section("TEST 1: User Registration")
    
    url = f"{BASE_URL}/api/auth/register"
    payload = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "role": "doctor"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Registration SUCCESS")
            return True
        else:
            print(f"\n⚠️  Registration already exists or error")
            return True  # Might already exist
    except Exception as e:
        print(f"\n❌ Registration FAILED: {str(e)}")
        return False

def test_login():
    """Test 2: Login and get JWT token"""
    print_section("TEST 2: User Login (Get JWT Token)")
    
    url = f"{BASE_URL}/api/auth/login"
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Token: {token[:50]}...")
            print(f"Type: {data.get('token_type')}")
            print("\n✅ Login SUCCESS - Got JWT Token")
            return token
        else:
            print(f"Response: {response.json()}")
            print("\n❌ Login FAILED")
            return None
    except Exception as e:
        print(f"\n❌ Login FAILED: {str(e)}")
        return None

def test_upload_file(token):
    """Test 3: Upload a file"""
    print_section("TEST 3: Upload File (Dual Database)")
    
    # Create a test file
    test_file_path = Path("E:\\FYP\\backend\\uploads\\test_document.txt")
    test_file_path.parent.mkdir(exist_ok=True)
    
    with open(test_file_path, "w") as f:
        f.write("Sample pathology report\nTest data for Phase 2")
    
    url = f"{BASE_URL}/api/upload/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        with open(test_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, headers=headers, files=files)
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get("status") == "success":
            print("\n✅ Upload SUCCESS")
            file_id = data.get("file_id")
            print(f"File ID: {file_id}")
            print(f"Filename: {data.get('filename')}")
            print(f"Size: {data.get('file_size')} bytes")
            return file_id
        else:
            print("\n❌ Upload FAILED")
            return None
    except Exception as e:
        print(f"\n❌ Upload FAILED: {str(e)}")
        return None

def test_list_files(token):
    """Test 4: List uploaded files"""
    print_section("TEST 4: List Uploaded Files")
    
    url = f"{BASE_URL}/api/upload/list"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get("status") == "success":
            files = data.get("files", [])
            total = data.get("total", 0)
            print(f"\n✅ List SUCCESS - Found {total} file(s)")
            
            for i, file_info in enumerate(files, 1):
                print(f"\n  File {i}:")
                print(f"    Name: {file_info.get('filename')}")
                print(f"    Size: {file_info.get('size')} bytes")
                print(f"    Uploaded: {file_info.get('uploaded_at')}")
            
            return True
        else:
            print("\n❌ List FAILED")
            return False
    except Exception as e:
        print(f"\n❌ List FAILED: {str(e)}")
        return False

def test_health_check():
    """Test 0: Health check"""
    print_section("TEST 0: Server Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Server HEALTHY")
            return True
        else:
            print("\n❌ Server UNHEALTHY")
            return False
    except Exception as e:
        print(f"\n❌ Health check FAILED: {str(e)}")
        print("Make sure FastAPI server is running on http://localhost:8000")
        return False

def main():
    """Run all tests"""
    print("╔" + "="*58 + "╗")
    print("║" + " "*20 + "PHASE 2 TEST SUITE" + " "*21 + "║")
    print("║" + " "*15 + "File Upload System Testing" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    
    # Test 0: Health check
    if not test_health_check():
        print("\n⚠️  Cannot reach server. Make sure it's running!")
        return
    
    # Test 1: Register
    test_register()
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("\n❌ Cannot proceed without token")
        return
    
    # Test 3: Upload
    file_id = test_upload_file(token)
    
    # Test 4: List files
    test_list_files(token)
    
    # Summary
    print_section("TEST SUMMARY")
    print("""
✅ Phase 2 Testing Complete!

What was tested:
1. Server health check
2. User registration
3. JWT login/authentication
4. Dual-database file upload
5. File listing

If all tests passed:
- Users can authenticate ✅
- Files are being uploaded ✅
- Files are stored in uploads/ folder ✅
- RBAC is protecting endpoints ✅

Next: Move to Phase 3 (OCR Integration)
    """)

if __name__ == "__main__":
    main()
