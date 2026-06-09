# Data Dictionary - Technify Academic AI Assistant

## Overview
This document describes all synthetic data files used for development and testing.

---

## 1. students.json
Total Records: 1,000

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| student_id | String | Unique student ID | STU-0001 |
| name | String | Student full name | Ahmed Khan |
| email | String | Student email | ahmed.khan1@student.technify.edu.pk |
| phone | String | Pakistani phone number | +92-321-1234567 |
| department | String | Department name | Computer Science |
| semester | Integer | Current semester (1-8) | 3 |
| section | String | Class section | A, B, or C |
| cgpa | Float | GPA (2.0-4.0) | 3.5 |
| enrollment_year | Integer | Year of enrollment | 2024 |
| status | String | Student status | Active, On Leave |
| fee_status | String | Fee payment status | Paid, Pending, Overdue |
| fee_amount | Integer | Fee in PKR | 95000 |
| fee_due_date | String | Fee due date | 2026-07-15 |

---

## 2. faculty.json
Total Records: 100

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| faculty_id | String | Unique faculty ID | FAC-0001 |
| name | String | Faculty full name | Dr. Ali Shah |
| email | String | Faculty email | ali.shah1@faculty.technify.edu.pk |
| phone | String | Pakistani phone number | +92-321-1234567 |
| department | String | Department name | Computer Science |
| designation | String | Job title | Professor |
| qualification | String | Highest degree | PhD, MS, MPhil |
| joining_year | Integer | Year joined | 2018 |
| office | String | Office room | Room A-101 |

---

## 3. courses.json
Total Records: 100

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| course_id | String | Unique course ID | CRS-0001 |
| course_name | String | Course title | Data Structures |
| course_code | String | Course code | CS-301 |
| credit_hours | Integer | Credit hours | 3 |
| department | String | Department | Computer Science |
| semester | Integer | Semester (1-8) | 3 |
| faculty_id | String | Assigned teacher ID | FAC-0001 |
| faculty_name | String | Assigned teacher name | Dr. Ali Shah |
| schedule.days | Array | Class days | Monday, Wednesday |
| schedule.time | String | Class time | 09:30-11:00 |
| schedule.room | String | Class room | Room LH-5 |
| total_classes | Integer | Total classes in semester | 35 |
| max_students | Integer | Max enrollment | 40 |

---

## 4. attendance.json
Total Records: 10,000

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| record_id | String | Unique record ID | ATT-000001 |
| student_id | String | Student reference | STU-0001 |
| student_name | String | Student name | Ahmed Khan |
| course_id | String | Course reference | CRS-0001 |
| course_name | String | Course name | Data Structures |
| date | String | Attendance date | 2026-02-15 |
| status | String | Attendance status | Present, Absent, Late |
| marked_by | String | Faculty ID who marked | FAC-0001 |

---

## 5. exams.json
Total Records: 5,000

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| record_id | String | Unique record ID | EXM-000001 |
| student_id | String | Student reference | STU-0001 |
| student_name | String | Student name | Ahmed Khan |
| course_id | String | Course reference | CRS-0001 |
| course_name | String | Course name | Data Structures |
| exam_type | String | Type of exam | Quiz 1, Midterm, Final |
| marks_obtained | Float | Marks scored | 25.5 |
| total_marks | Integer | Total marks | 30 |
| percentage | Float | Score percentage | 85.0 |
| grade | String | Letter grade | A, B+, C |
| date | String | Exam date | 2026-03-15 |

---

## 6. timetable.json

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| student_id | String | Student reference | STU-0001 |
| student_name | String | Student name | Ahmed Khan |
| course_id | String | Course reference | CRS-0001 |
| course_name | String | Course name | Data Structures |
| course_code | String | Course code | CS-301 |
| faculty_name | String | Teacher name | Dr. Ali Shah |
| days | Array | Class days | Monday, Wednesday |
| time | String | Class time | 09:30-11:00 |
| room | String | Class room | Room LH-5 |
| semester | Integer | Student semester | 3 |

---

## 7. assignments.json

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| assignment_id | String | Unique assignment ID | ASN-000001 |
| course_id | String | Course reference | CRS-0001 |
| course_name | String | Course name | Data Structures |
| student_id | String | Student reference | STU-0001 |
| student_name | String | Student name | Ahmed Khan |
| title | String | Assignment title | Assignment 1 - Data Structures |
| due_date | String | Due date | 2026-04-15 |
| status | String | Submission status | Submitted, Pending, Late |
| marks_obtained | Integer | Marks scored | 12 |
| total_marks | Integer | Total marks | 15 |