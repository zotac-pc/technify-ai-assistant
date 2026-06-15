import os, json
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'audit.log')

def log_request(user_id: str, role: str, query: str,
               response_type: str, response_time: float):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'role': role,
        'query': query,
        'response_type': response_type,
        'response_time_seconds': response_time
    }
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
    print(f'[AUDIT] {user_id} ({role}): {response_type} in {response_time}s')
