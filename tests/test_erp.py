import httpx, pytest

@pytest.mark.asyncio
async def test_student():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:8001/api/v1/student/STU-0001')
        assert r.status_code == 200

@pytest.mark.asyncio
async def test_attendance():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:8001/api/v1/student/STU-0001/attendance')
        assert r.status_code == 200
        assert 'overall_percentage' in r.json()

@pytest.mark.asyncio
async def test_admin_stats():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:8001/api/v1/admin/statistics/students')
        assert r.status_code == 200
        assert r.json()['total_students'] == 1000
