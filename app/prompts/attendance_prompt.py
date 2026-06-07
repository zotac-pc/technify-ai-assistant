"""
TAIA - Prompt Templates
File location: app/prompts/attendance_prompt.py
"""

from langchain_core.prompts import PromptTemplate


# -----------------------------------------
# 1. ATTENDANCE PROMPT
# -----------------------------------------
attendance_prompt = PromptTemplate(
    input_variables=["student_name", "course_name", "course_code", "attended", "total", "percentage"],
    template="""
You are TAIA, a friendly university AI assistant.

Student Name: {student_name}
Course: {course_name} ({course_code})
Classes Attended: {attended} out of {total}
Attendance Percentage: {percentage}%

Response rules:
- Below 75%: Give a warning and advise improvement.
- 75% to 85%: Encourage improvement.
- Above 85%: Praise the student.

Give a friendly and short response (2-3 lines max).
"""
)


# -----------------------------------------
# 2. RESULTS / GPA PROMPT
# -----------------------------------------
results_prompt = PromptTemplate(
    input_variables=["student_name", "semester", "gpa", "courses_passed", "courses_failed"],
    template="""
You are TAIA, a friendly university AI assistant.

Student: {student_name}
Semester: {semester}
GPA: {gpa} / 4.0
Courses Passed: {courses_passed}
Courses Failed: {courses_failed}

Response rules:
- GPA 3.5 and above: Excellent, encourage the student.
- GPA 2.5 to 3.5: Good, suggest improvements.
- GPA below 2.5: Show concern, suggest academic help.

Give a short and caring response.
"""
)


# -----------------------------------------
# 3. COURSES / TIMETABLE PROMPT
# -----------------------------------------
courses_prompt = PromptTemplate(
    input_variables=["student_name", "semester", "courses_list"],
    template="""
You are TAIA, a friendly university AI assistant.

Student: {student_name}
Current Semester: {semester}
Registered Courses:
{courses_list}

List the courses in a clean and readable format.
Mention if any course has a double period.
"""
)


# -----------------------------------------
# 4. FEE STATUS PROMPT
# -----------------------------------------
fee_prompt = PromptTemplate(
    input_variables=["student_name", "total_fee", "paid_amount", "due_amount", "due_date"],
    template="""
You are TAIA, a friendly university AI assistant.

Student: {student_name}
Total Fee: PKR {total_fee}
Amount Paid: PKR {paid_amount}
Amount Due: PKR {due_amount}
Due Date: {due_date}

If due amount is 0, congratulate the student.
If due amount is remaining, politely remind them with the due date.
Keep the response short (2-3 lines).
"""
)


# -----------------------------------------
# 5. STUDY PLAN PROMPT
# -----------------------------------------
study_plan_prompt = PromptTemplate(
    input_variables=["student_name", "weak_courses", "exam_date", "days_left"],
    template="""
You are TAIA, a helpful university AI assistant.

Student: {student_name}
Weak Courses (low marks/attendance): {weak_courses}
Next Exam Date: {exam_date}
Days Left: {days_left}

Create a practical and achievable study plan:
- Suggest daily study hours.
- Prioritize weak courses.
- Include short breaks.
- Keep a motivational tone.

Give the plan in 5-7 lines.
"""
)


# -----------------------------------------
# Quick Test
# -----------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("Prompt Templates - Test")
    print("=" * 50)

    # Test attendance prompt
    filled = attendance_prompt.format(
        student_name="Ali Hassan",
        course_name="Web Engineering",
        course_code="CS-301",
        attended=25,
        total=32,
        percentage=78
    )
    print("\nATTENDANCE PROMPT:")
    print(filled)

    # Test results prompt
    filled2 = results_prompt.format(
        student_name="Ali Hassan",
        semester="Fall 2025",
        gpa=3.2,
        courses_passed=4,
        courses_failed=1
    )
    print("\nRESULTS PROMPT:")
    print(filled2)

    print("\nAll prompts working!")