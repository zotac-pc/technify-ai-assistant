import requests

print("--- TEST 1: Valid Token ---")
# Step 1: Login to get a token from Mock ERP
r = requests.post('http://localhost:8001/api/v1/auth/login',
                  json={'user_id': 'STU-0001', 'role': 'student'})

# Extract token securely
response_data = r.json()
if 'token' in response_data:
    token = response_data['token']
    print(f"Token Received: {token[:20]}...") 
    
    # Step 2: Use the token in the chat AI gateway
    r2 = requests.post('http://localhost:8000/api/v1/chat',
                       json={'message': 'What is my attendance?'},
                       headers={'Authorization': f'Bearer {token}'})
    print("Valid Token Response:", r2.json())
else:
    print("Error getting token:", response_data)

print("\n--- TEST 2: Invalid Token ---")
# Step 3: Test rejection of an invalid token
r3 = requests.post('http://localhost:8000/api/v1/chat',
                   json={'message': 'What is my attendance?'},
                   headers={'Authorization': 'Bearer invalid-token-here'})
print("Invalid Token Response:", r3.json()) # Should return 401 Unauthorized