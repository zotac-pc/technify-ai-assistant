import requests, time

# Send chat request
requests.post(
    'http://localhost:8000/api/v1/chat',
    json={'message': 'What is my attendance?'},
    headers={'x-user-role': 'Student', 'x-user-id': 'STU-0001'}
)

time.sleep(1)

# Check audit logs
r = requests.get('http://localhost:8000/api/v1/admin/audit-logs')
print(r.json())

# Check usage stats
r2 = requests.get('http://localhost:8000/api/v1/admin/usage-stats')
print(r2.json())