"""
Synthetic Data Generator for Technify Academic AI Assistant
==========================================================
Generates realistic fake university data for development and testing.

Generates:
- 1,000 Students
- 100 Faculty Members
- 100 Courses
- 10,000 Attendance Records
- 5,000 Exam Records
- 2,000 Timetable Records
- 3,000 Assignment Records

Usage:
    python generate_data.py

Output:
    data/synthetic/students.json
    data/synthetic/faculty.json
    data/synthetic/courses.json
    data/synthetic/attendance.json
    data/synthetic/exams.json
    data/synthetic/timetable.json
    data/synthetic/assignments.json

Author: AI Team 1 - Data Engineer
"""

import json
import random
import os
from datetime import datetime, timedelta

# Try to use Faker if available, otherwise use basic random data
try:
    from faker import Faker
    fake = Faker()
    USE_FAKER = True
except ImportError:
    USE_FAKER = False
    print("[WARNING] Faker not installed. Using basic random data.")
    print("          Install with: pip install faker")

# ============================================================
# Configuration
# ============================================================
NUM_STUDENTS = 1000
NUM_FACULTY = 100
NUM_COURSES = 100
NUM_ATTENDANCE_RECORDS = 10000
NUM_EXAM_RECORDS = 5000
NUM_TIMETABLE_RECORDS = 2000
NUM_ASSIGNMENT_RECORDS = 3000

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "synthetic")

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Software Engineering",
    "Artificial Intelligence",
    "Data Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Business Administration",
    "Mathematics",
    "Physics",
]

COURSE_NAMES = [
    "Programming Fundamentals", "Object Oriented Programming", "Data Structures",
    "Algorithms", "Database Systems", "Web Engineering", "Software Engineering",
    "Operating Systems", "Computer Networks", "Artificial Intelligence",
    "Machine Learning", "Deep Learning", "Natural Language Processing",
    "Computer Vision", "Data Mining", "Cloud Computing", "Cyber Security",
    "Mobile App Development", "Digital Logic Design", "Discrete Mathematics",
    "Linear Algebra", "Probability & Statistics", "Calculus I", "Calculus II",
    "Physics I", "Physics II", "Technical Writing", "Professional Ethics",
    "Project Management", "Software Testing", "Human Computer Interaction",
    "Information Security", "Compiler Construction", "Theory of Automata",
    "Numerical Methods", "Parallel Computing", "Distributed Systems",
    "Internet of Things", "Blockchain Technology", "DevOps Engineering",
    "Big Data Analytics", "Data Warehousing", "Business Intelligence",
    "Entrepreneurship", "Communication Skills", "Islamic Studies",
    "Pakistan Studies", "English I", "English II", "Accounting",
]

DESIGNATIONS = ["Lecturer", "Assistant Professor", "Associate Professor", "Professor"]

FIRST_NAMES_MALE = [
    "Ahmed", "Ali", "Muhammad", "Hassan", "Usman", "Bilal", "Hamza", "Omar",
    "Saad", "Zain", "Fahad", "Rehan", "Kamran", "Imran", "Tariq", "Junaid",
    "Faisal", "Adeel", "Waqar", "Shahid", "Arslan", "Nabeel", "Kashif", "Sohail",
]

FIRST_NAMES_FEMALE = [
    "Ayesha", "Fatima", "Zainab", "Maryam", "Hira", "Sana", "Amna", "Noor",
    "Rabia", "Sumaya", "Kiran", "Mehwish", "Sadia", "Nimra", "Iqra", "Bushra",
    "Samina", "Tahira", "Uzma", "Asma", "Mahnoor", "Laiba", "Anum", "Mishal",
]

LAST_NAMES = [
    "Khan", "Ahmed", "Ali", "Hussain", "Shah", "Malik", "Butt", "Iqbal",
    "Raza", "Siddiqui", "Qureshi", "Sheikh", "Chaudhry", "Aslam", "Javed",
    "Nawaz", "Akram", "Saleem", "Farooq", "Rehman", "Umar", "Haider",
    "Zaidi", "Naqvi", "Abbasi", "Mirza", "Baig", "Mughal", "Awan", "Gill",
]


def generate_name():
    """Generate a random Pakistani name."""
    if USE_FAKER:
        return fake.name()

    gender = random.choice(["M", "F"])
    first = random.choice(FIRST_NAMES_MALE if gender == "M" else FIRST_NAMES_FEMALE)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"


def generate_email(name, domain="technify.edu.pk"):
    clean = name.lower().replace(" ", ".").replace("'", "")
    rand_num = random.randint(1, 999)
    return f"{clean}{rand_num}@{domain}"


def generate_phone():
    return f"+92-3{random.randint(0,4)}{random.randint(0,9)}-{random.randint(1000000, 9999999)}"


# ============================================================
# Generate Students
# ============================================================
def generate_students():
    print(f"[STUDENTS] Generating {NUM_STUDENTS} students...")
    students = []
    for i in range(1, NUM_STUDENTS + 1):
        name = generate_name()
        semester = random.randint(1, 8)
        students.append({
            "student_id": f"STU-{i:04d}",
            "name": name,
            "email": generate_email(name, "student.technify.edu.pk"),
            "phone": generate_phone(),
            "department": random.choice(DEPARTMENTS),
            "semester": semester,
            "section": random.choice(["A", "B", "C"]),
            "cgpa": round(random.uniform(2.0, 4.0), 2),
            "enrollment_year": 2026 - (semester // 2) - 1,
            "status": random.choice(["Active"] * 9 + ["On Leave"]),
            "fee_status": random.choice(["Paid", "Paid", "Paid", "Pending", "Overdue"]),
            "fee_amount": random.choice([85000, 90000, 95000, 100000, 120000]),
            "fee_due_date": f"2026-07-{random.randint(1,28):02d}",
        })
    return students


# ============================================================
# Generate Faculty
# ============================================================
def generate_faculty():
    print(f"[FACULTY] Generating {NUM_FACULTY} faculty members...")
    faculty = []
    for i in range(1, NUM_FACULTY + 1):
        name = generate_name()
        faculty.append({
            "faculty_id": f"FAC-{i:04d}",
            "name": name,
            "email": generate_email(name, "faculty.technify.edu.pk"),
            "phone": generate_phone(),
            "department": random.choice(DEPARTMENTS),
            "designation": random.choice(DESIGNATIONS),
            "qualification": random.choice(["PhD", "MS", "MPhil"]),
            "joining_year": random.randint(2015, 2025),
            "office": f"Room {random.choice(['A','B','C','D'])}-{random.randint(100,499)}",
        })
    return faculty


# ============================================================
# Generate Courses
# ============================================================
def generate_courses(faculty_list):
    print(f"[COURSES] Generating {NUM_COURSES} courses...")
    courses = []
    used_names = set()

    for i in range(1, NUM_COURSES + 1):
        course_name = random.choice(COURSE_NAMES)
        while course_name in used_names and len(used_names) < len(COURSE_NAMES):
            course_name = random.choice(COURSE_NAMES)
        used_names.add(course_name)

        assigned_faculty = random.choice(faculty_list)

        courses.append({
            "course_id": f"CRS-{i:04d}",
            "course_name": course_name,
            "course_code": f"{random.choice(['CS', 'IT', 'SE', 'AI', 'DS', 'EE', 'MT', 'PH', 'BA'])}-{random.randint(100,499)}",
            "credit_hours": random.choice([2, 3, 3, 3, 4]),
            "department": assigned_faculty["department"],
            "semester": random.randint(1, 8),
            "faculty_id": assigned_faculty["faculty_id"],
            "faculty_name": assigned_faculty["name"],
            "schedule": {
                "days": random.choice([
                    ["Monday", "Wednesday"],
                    ["Tuesday", "Thursday"],
                    ["Monday", "Wednesday", "Friday"],
                ]),
                "time": random.choice([
                    "08:00-09:30", "09:30-11:00", "11:00-12:30",
                    "14:00-15:30", "15:30-17:00",
                ]),
                "room": f"Room {random.choice(['LH','CR','Lab'])}-{random.randint(1,20)}",
            },
            "total_classes": random.randint(28, 45),
            "max_students": random.choice([30, 40, 50, 60]),
        })
    return courses


# ============================================================
# Generate Attendance Records
# ============================================================
def generate_attendance(students, courses):
    print(f"[ATTENDANCE] Generating {NUM_ATTENDANCE_RECORDS} attendance records...")
    attendance = []
    start_date = datetime(2026, 1, 15)

    for i in range(1, NUM_ATTENDANCE_RECORDS + 1):
        student = random.choice(students)
        course = random.choice(courses)
        days_offset = random.randint(0, 120)
        record_date = start_date + timedelta(days=days_offset)

        while record_date.weekday() >= 5:
            record_date += timedelta(days=1)

        attendance.append({
            "record_id": f"ATT-{i:06d}",
            "student_id": student["student_id"],
            "student_name": student["name"],
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "date": record_date.strftime("%Y-%m-%d"),
            "status": random.choices(
                ["Present", "Absent", "Late"],
                weights=[75, 18, 7],
                k=1,
            )[0],
            "marked_by": course["faculty_id"],
        })

    return attendance


# ============================================================
# Generate Exam Records
# ============================================================
def generate_exams(students, courses):
    print(f"[EXAMS] Generating {NUM_EXAM_RECORDS} exam records...")
    exams = []

    exam_types = [
        {"type": "Quiz 1", "total_marks": 10},
        {"type": "Quiz 2", "total_marks": 10},
        {"type": "Quiz 3", "total_marks": 10},
        {"type": "Assignment 1", "total_marks": 15},
        {"type": "Assignment 2", "total_marks": 15},
        {"type": "Midterm", "total_marks": 30},
        {"type": "Final", "total_marks": 50},
    ]

    for i in range(1, NUM_EXAM_RECORDS + 1):
        student = random.choice(students)
        course = random.choice(courses)
        exam_type = random.choice(exam_types)
        total = exam_type["total_marks"]

        percentage = random.gauss(70, 15)
        percentage = max(10, min(100, percentage))
        marks = round(total * percentage / 100, 1)

        exams.append({
            "record_id": f"EXM-{i:06d}",
            "student_id": student["student_id"],
            "student_name": student["name"],
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "exam_type": exam_type["type"],
            "marks_obtained": marks,
            "total_marks": total,
            "percentage": round(percentage, 1),
            "grade": (
                "A+" if percentage >= 90 else
                "A" if percentage >= 85 else
                "A-" if percentage >= 80 else
                "B+" if percentage >= 75 else
                "B" if percentage >= 70 else
                "B-" if percentage >= 65 else
                "C+" if percentage >= 60 else
                "C" if percentage >= 55 else
                "C-" if percentage >= 50 else
                "D" if percentage >= 45 else
                "F"
            ),
            "date": f"2026-{random.choice(['02','03','04','05'])}-{random.randint(1,28):02d}",
        })

    return exams


# ============================================================
# Generate Timetable Records (NEW)
# ============================================================
def generate_timetable(students, courses):
    print(f"[TIMETABLE] Generating {NUM_TIMETABLE_RECORDS} timetable records...")
    timetable = []

    time_slots = [
        "08:00-09:30", "09:30-11:00", "11:00-12:30",
        "13:00-14:30", "14:30-16:00", "16:00-17:30",
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for i in range(1, NUM_TIMETABLE_RECORDS + 1):
        student = random.choice(students)
        course = random.choice(courses)

        timetable.append({
            "timetable_id": f"TT-{i:06d}",
            "student_id": student["student_id"],
            "student_name": student["name"],
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "course_code": course["course_code"],
            "faculty_name": course["faculty_name"],
            "day": random.choice(days),
            "time_slot": random.choice(time_slots),
            "room": f"Room {random.choice(['LH','CR','Lab'])}-{random.randint(1,20)}",
            "semester": student["semester"],
            "section": student["section"],
        })

    return timetable


# ============================================================
# Generate Assignment Records (NEW)
# ============================================================
def generate_assignments(students, courses):
    print(f"[ASSIGNMENTS] Generating {NUM_ASSIGNMENT_RECORDS} assignment records...")
    assignments = []

    statuses = ["Submitted", "Submitted", "Submitted", "Pending", "Late", "Missing"]

    for i in range(1, NUM_ASSIGNMENT_RECORDS + 1):
        student = random.choice(students)
        course = random.choice(courses)
        due_date = datetime(2026, 1, 15) + timedelta(days=random.randint(0, 150))
        status = random.choice(statuses)

        submitted_date = None
        marks_obtained = None

        if status == "Submitted":
            submitted_date = (due_date - timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d")
            marks_obtained = round(random.uniform(7, 15), 1)
        elif status == "Late":
            submitted_date = (due_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
            marks_obtained = round(random.uniform(3, 10), 1)

        assignments.append({
            "assignment_id": f"ASN-{i:06d}",
            "student_id": student["student_id"],
            "student_name": student["name"],
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "assignment_title": f"Assignment {random.randint(1,5)} - {course['course_name']}",
            "total_marks": 15,
            "marks_obtained": marks_obtained,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "submitted_date": submitted_date,
            "status": status,
            "faculty_id": course["faculty_id"],
        })

    return assignments


# ============================================================
# Main Execution
# ============================================================
def main():
    print("=" * 60)
    print("Technify University - Synthetic Data Generator")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    students = generate_students()
    faculty = generate_faculty()
    courses = generate_courses(faculty)
    attendance = generate_attendance(students, courses)
    exams = generate_exams(students, courses)
    timetable = generate_timetable(students, courses)
    assignments = generate_assignments(students, courses)
    datasets = {
        "students": students,
        "faculty": faculty,
        "courses": courses,
        "attendance": attendance,
        "exams": exams,
        "timetable": timetable,
        "assignments": assignments,
    }

    print("\nSaving data...")
    for name, data in datasets.items():
        filepath = os.path.join(OUTPUT_DIR, f"{name}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"   [OK] {name}.json ({len(data):,} records)")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"   Students:           {len(students):>8,}")
    print(f"   Faculty:            {len(faculty):>8,}")
    print(f"   Courses:            {len(courses):>8,}")
    print(f"   Attendance Records: {len(attendance):>8,}")
    print(f"   Exam Records:       {len(exams):>8,}")
    print(f"   Timetable Records:  {len(timetable):>8,}")
    print(f"   Assignment Records: {len(assignments):>8,}")
    print(f"   Total Records:      {sum(len(d) for d in datasets.values()):>8,}")
    print(f"\n   Output Directory: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)
    print("Data generation complete!")


if __name__ == "__main__":
    main()