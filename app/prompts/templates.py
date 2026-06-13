from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate

# Main System Persona for the AI
SYSTEM_PERSONA = """You are TAIA (Technify Academic AI Assistant), an official AI agent for Technify University.
Your job is to provide polite, professional, and highly accurate answers to students and faculty.
If you do not have enough information to answer a question, politely state that you do not have access to that data.
Never reveal sensitive student data to another student.
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(SYSTEM_PERSONA)

# Template for Attendance queries
ATTENDANCE_PROMPT = PromptTemplate(
    input_variables=["student_id", "question", "attendance_data"],
    template="""Based on the following attendance data for student {student_id}, answer their question clearly.
Attendance Data:
{attendance_data}

Question: {question}

Response:"""
)

# Template for Results/GPA queries
RESULTS_PROMPT = PromptTemplate(
    input_variables=["student_id", "question", "results_data"],
    template="""Based on the following academic results for student {student_id}, answer their question clearly.
Academic Results:
{results_data}

Question: {question}

Response:"""
)

# Template for Course/Timetable queries
COURSE_PROMPT = PromptTemplate(
    input_variables=["student_id", "question", "course_data"],
    template="""Based on the following course and timetable data for student {student_id}, answer their question clearly.
Course Data:
{course_data}

Question: {question}

Response:"""
)
