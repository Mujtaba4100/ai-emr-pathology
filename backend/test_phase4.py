import requests
import json

# Test text cleaning endpoint
test_text = 'Patient:  John DOE\n\nHGB:  14.5  g/dL\n\nWBC:  7.2 THOUSAND\n\nDM and HTN patient'
payload = {'text': test_text}

try:
    response = requests.post(
        'http://localhost:8000/api/clean/text',
        json=payload,
        timeout=5
    )
    print('Status Code:', response.status_code)
    result = response.json()
    print('✅ Text Cleaning Endpoint Working!')
    print('  Original Length:', result['original_length'])
    print('  Cleaned Length:', result['cleaned_length'])
    print('  Status:', result['status'])
    print('  Cleaned Text Preview:', result['cleaned_preview'][:80])
except Exception as e:
    print('❌ Error:', str(e))
