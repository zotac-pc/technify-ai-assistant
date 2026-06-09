"""Mock ERP API routes — serves synthetic data as if it were the real Laravel ERP."""
import json, os, random
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic")

def _load(name):
    path = os.path.join(DATA_DIR, f"{name}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Cache data on first load
_cache = {}
def get_data(name):
    if name not in _cache:
        _cache[name] = _load(name)
    return _cache[name]

# ──────────────── AUTH ────────────────
from app.auth.jwt_handler import create_token

@router.post("/auth/login")
def login(body: dict):
    """Issue a JWT token for testing. Send: {user_id, role}"""
    uid = body.get("user_id", "STU-0001")
    role = body.get("role", "student")
    students = get_data("students")
    faculty = get_data("faculty")
    name, dept, email = "", "", ""
    if role == "student":
        s = next((s for s in students if s["student_id"] == uid), None)
        if s:
            name, dept, email = s["name"], s["department"], s["email"]
    elif role == "faculty":
        f = next((f for f in faculty if f["faculty_id"] == uid), None)
        if f:
            name, dept, email = f["name"], f["department"], f["email"]
    else:
        name = "Admin User"
    token = create_token(uid, role, name, dept, email)
    return {"token": token, "user_id": uid, "role": role, "name": name}

# ──────────────── STUDENT ENDPOINTS ────────────────
@router.get("/student/{student_id}")
def get_student(student_id: str):
    s = next((s for s in get_data("students") if s["student_id"] == student_id), None)
    if not s:
        raise HTTPException(404, "Student not found")
    return s

@router.get("/student/{student_id}/attendance")
def get_student_attendance(student_id: str):
    records = [r for r in get_data("attendance") if r["student_id"] == student_id]
    if not records:
        return {"student_id": student_id, "overall_percentage": 0, "courses": []}
    # Group by course
    courses = {}
    for r in records:
        cid = r["course_id"]
        if cid not in courses:
            courses[cid] = {"course_id": cid, "course_name": r["course_name"], "present": 0, "absent": 0, "late": 0, "total": 0}
        courses[cid]["total"] += 1
        if r["status"] == "Present":
            courses[cid]["present"] += 1
        elif r["status"] == "Absent":
            courses[cid]["absent"] += 1
        else:
            courses[cid]["late"] += 1
    course_list = []
    for c in courses.values():
        pct = round((c["present"] + c["late"] * 0.5) / max(c["total"], 1) * 100, 1)
        c["percentage"] = pct
        course_list.append(c)
    total_p = sum(c["present"] for c in courses.values())
    total_l = sum(c["late"] for c in courses.values())
    total_all = sum(c["total"] for c in courses.values())
    overall = round((total_p + total_l * 0.5) / max(total_all, 1) * 100, 1)
    return {"student_id": student_id, "overall_percentage": overall, "courses": course_list}

@router.get("/student/{student_id}/results")
def get_student_results(student_id: str):
    records = [r for r in get_data("exams") if r["student_id"] == student_id]
    return {"student_id": student_id, "results": records}

@router.get("/student/{student_id}/gpa")
def get_student_gpa(student_id: str):
    s = next((s for s in get_data("students") if s["student_id"] == student_id), None)
    if not s:
        raise HTTPException(404, "Student not found")
    return {"student_id": student_id, "cgpa": s["cgpa"], "semester": s["semester"]}

@router.get("/student/{student_id}/courses")
def get_student_courses(student_id: str):
    s = next((s for s in get_data("students") if s["student_id"] == student_id), None)
    if not s:
        raise HTTPException(404, "Student not found")
    all_courses = get_data("courses")
    dept_courses = [c for c in all_courses if c["department"] == s["department"] and c["semester"] <= s["semester"]]
    return {"student_id": student_id, "courses": dept_courses[:6]}

@router.get("/student/{student_id}/timetable")
def get_student_timetable(student_id: str):
    s = next((s for s in get_data("students") if s["student_id"] == student_id), None)
    if not s:
        raise HTTPException(404, "Student not found")
    all_courses = get_data("courses")
    dept_courses = [c for c in all_courses if c["department"] == s["department"] and c["semester"] <= s["semester"]][:6]
    timetable = []
    for c in dept_courses:
        timetable.append({"course": c["course_name"], "code": c["course_code"], "days": c["schedule"]["days"], "time": c["schedule"]["time"], "room": c["schedule"]["room"], "faculty": c["faculty_name"]})
    return {"student_id": student_id, "timetable": timetable}

@router.get("/student/{student_id}/assignments")
def get_student_assignments(student_id: str):
    exams = [r for r in get_data("exams") if r["student_id"] == student_id and "Assignment" in r["exam_type"]]
    pending = [{"course": e["course_name"], "assignment": e["exam_type"], "status": "Submitted", "marks": e["marks_obtained"], "total": e["total_marks"]} for e in exams]
    # Add some fake pending ones
    pending.append({"course": "Web Engineering", "assignment": "Assignment 3", "status": "Pending", "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")})
    pending.append({"course": "Database Systems", "assignment": "Project Proposal", "status": "Pending", "due_date": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")})
    return {"student_id": student_id, "assignments": pending}

@router.get("/student/{student_id}/fees")
def get_student_fees(student_id: str):
    s = next((s for s in get_data("students") if s["student_id"] == student_id), None)
    if not s:
        raise HTTPException(404, "Student not found")
    return {"student_id": student_id, "fee_status": s["fee_status"], "fee_amount": s["fee_amount"], "due_date": s["fee_due_date"], "program": s["department"]}

# ──────────────── FACULTY ENDPOINTS ────────────────
@router.get("/faculty/{faculty_id}/courses")
def get_faculty_courses(faculty_id: str):
    courses = [c for c in get_data("courses") if c["faculty_id"] == faculty_id]
    return {"faculty_id": faculty_id, "courses": courses}

@router.get("/faculty/{faculty_id}/course/{course_id}/attendance")
def get_course_attendance(faculty_id: str, course_id: str):
    records = [r for r in get_data("attendance") if r["course_id"] == course_id]
    students_att = {}
    for r in records:
        sid = r["student_id"]
        if sid not in students_att:
            students_att[sid] = {"student_id": sid, "student_name": r["student_name"], "present": 0, "absent": 0, "late": 0, "total": 0}
        students_att[sid]["total"] += 1
        if r["status"] == "Present":
            students_att[sid]["present"] += 1
        elif r["status"] == "Absent":
            students_att[sid]["absent"] += 1
        else:
            students_att[sid]["late"] += 1
    result = []
    for sa in students_att.values():
        sa["percentage"] = round((sa["present"] + sa["late"]*0.5) / max(sa["total"],1) * 100, 1)
        result.append(sa)
    low = [s for s in result if s["percentage"] < 75]
    return {"course_id": course_id, "total_students": len(result), "low_attendance_students": low, "all_students": result}

@router.get("/faculty/{faculty_id}/assignments")
def get_faculty_assignments(faculty_id: str):
    courses = [c for c in get_data("courses") if c["faculty_id"] == faculty_id]
    ungraded = []
    for c in courses:
        ungraded.append({"course": c["course_name"], "assignment": "Assignment 2", "submissions": random.randint(30, 50), "graded": 0})
    return {"faculty_id": faculty_id, "ungraded_assignments": ungraded}

@router.get("/faculty/{faculty_id}/course/{course_id}/students")
def get_course_students(faculty_id: str, course_id: str):
    exams = get_data("exams")
    course_exams = [e for e in exams if e["course_id"] == course_id]
    students = {}
    for e in course_exams:
        sid = e["student_id"]
        if sid not in students:
            students[sid] = {"student_id": sid, "student_name": e["student_name"], "avg_marks": 0, "count": 0, "total_pct": 0}
        students[sid]["count"] += 1
        students[sid]["total_pct"] += e["percentage"]
    result = []
    for s in students.values():
        s["avg_percentage"] = round(s["total_pct"] / max(s["count"], 1), 1)
        s["at_risk"] = s["avg_percentage"] < 50
        result.append(s)
    at_risk = [s for s in result if s["at_risk"]]
    return {"course_id": course_id, "total_students": len(result), "at_risk_students": at_risk}

# ──────────────── ADMIN ENDPOINTS ────────────────
@router.get("/admin/statistics/students")
def admin_students():
    students = get_data("students")
    depts = {}
    for s in students:
        d = s["department"]
        depts[d] = depts.get(d, 0) + 1
    return {"total_students": len(students), "by_department": depts, "active": sum(1 for s in students if s["status"] == "Active")}

@router.get("/admin/statistics/admissions")
def admin_admissions():
    students = get_data("students")
    by_year = {}
    for s in students:
        y = str(s["enrollment_year"])
        by_year[y] = by_year.get(y, 0) + 1
    return {"total_enrolled": len(students), "by_year": by_year}

@router.get("/admin/statistics/fees")
def admin_fees():
    students = get_data("students")
    paid = sum(1 for s in students if s["fee_status"] == "Paid")
    pending = sum(1 for s in students if s["fee_status"] == "Pending")
    overdue = sum(1 for s in students if s["fee_status"] == "Overdue")
    total_amount = sum(s["fee_amount"] for s in students)
    collected = sum(s["fee_amount"] for s in students if s["fee_status"] == "Paid")
    return {"total_students": len(students), "paid": paid, "pending": pending, "overdue": overdue, "total_expected": total_amount, "total_collected": collected, "collection_rate": round(collected/max(total_amount,1)*100, 1)}

@router.get("/admin/statistics/departments")
def admin_departments():
    students = get_data("students")
    depts = {}
    for s in students:
        d = s["department"]
        if d not in depts:
            depts[d] = {"students": 0, "total_cgpa": 0}
        depts[d]["students"] += 1
        depts[d]["total_cgpa"] += s["cgpa"]
    result = []
    for name, data in depts.items():
        result.append({"department": name, "students": data["students"], "avg_cgpa": round(data["total_cgpa"]/max(data["students"],1), 2)})
    result.sort(key=lambda x: x["avg_cgpa"], reverse=True)
    return {"departments": result}
