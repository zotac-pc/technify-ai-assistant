import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic")

# Test 1: Check all files exist
def test_data_files_exist():
    files = ["students.json", "faculty.json", "courses.json", 
             "attendance.json", "exams.json", "timetable.json", "assignments.json"]
    for file in files:
        filepath = os.path.join(DATA_DIR, file)
        assert os.path.exists(filepath), f"{file} not found!"

# Test 2: Check students count
def test_students_count():
    with open(os.path.join(DATA_DIR, "students.json")) as f:
        data = json.load(f)
    assert len(data) == 1000, f"Expected 1000 students, got {len(data)}"

# Test 3: Check student IDs are unique
def test_student_ids_unique():
    with open(os.path.join(DATA_DIR, "students.json")) as f:
        data = json.load(f)
    ids = [s["student_id"] for s in data]
    assert len(ids) == len(set(ids)), "Duplicate student IDs found!"

# Test 4: Check CGPA is valid range
def test_student_cgpa_range():
    with open(os.path.join(DATA_DIR, "students.json")) as f:
        data = json.load(f)
    for student in data:
        assert 2.0 <= student["cgpa"] <= 4.0, f"Invalid CGPA: {student['cgpa']}"

# Test 5: Check attendance status is valid
def test_attendance_status_valid():
    with open(os.path.join(DATA_DIR, "attendance.json")) as f:
        data = json.load(f)
    valid_statuses = ["Present", "Absent", "Late"]
    for record in data:
        assert record["status"] in valid_statuses, f"Invalid status: {record['status']}"