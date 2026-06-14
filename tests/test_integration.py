import httpx
import pytest

@pytest.mark.asyncio
async def test_student_chat():
    async with httpx.AsyncClient() as c:
        r = await c.post('http://localhost:8000/api/v1/chat',
            json={'message': 'What is my attendance?'},
            headers={
                'x-user-role': 'Student',
                'x-user-id': 'STU-0001',
                'x-session-id': 'STU-0001'
            })
        assert r.status_code == 200
        assert 'response' in r.json()

@pytest.mark.asyncio
async def test_faculty_chat():
    async with httpx.AsyncClient() as c:
        r = await c.post('http://localhost:8000/api/v1/chat',
            json={'message': 'Which students have low attendance?'},
            headers={
                'x-user-role': 'Faculty',
                'x-user-id': 'FAC-0001',
                'x-session-id': 'FAC-0001'
            })
        assert r.status_code == 200

@pytest.mark.asyncio
async def test_admin_chat():
    async with httpx.AsyncClient() as c:
        r = await c.post('http://localhost:8000/api/v1/chat',
            json={'message': 'Total students enrolled?'},
            headers={
                'x-user-role': 'Admin',
                'x-user-id': 'ADM-0001',
                'x-session-id': 'ADM-0001'
            })
        assert r.status_code == 200

@pytest.mark.asyncio
async def test_empty_rejected():
    async with httpx.AsyncClient() as c:
        r = await c.post('http://localhost:8000/api/v1/chat',
            json={'message': ''},
            headers={
                'x-user-role': 'Student',
                'x-user-id': 'STU-0001'
            })
        assert 'Please provide' in r.json()['response']

@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:8000/health')
        assert r.json()['status'] == 'healthy'