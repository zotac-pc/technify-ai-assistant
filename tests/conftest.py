import pytest
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic")

@pytest.fixture
def students_data():
    with open(os.path.join(DATA_DIR, "students.json")) as f:
        return json.load(f)

@pytest.fixture
def faculty_data():
    with open(os.path.join(DATA_DIR, "faculty.json")) as f:
        return json.load(f)

@pytest.fixture
def courses_data():
    with open(os.path.join(DATA_DIR, "courses.json")) as f:
        return json.load(f)

@pytest.fixture
def attendance_data():
    with open(os.path.join(DATA_DIR, "attendance.json")) as f:
        return json.load(f)

@pytest.fixture
def exams_data():
    with open(os.path.join(DATA_DIR, "exams.json")) as f:
        return json.load(f)