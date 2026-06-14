import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.prompts.templates import SYSTEM_PERSONA
from app.prompts.templates import ATTENDANCE_PROMPT, RESULTS_PROMPT, COURSE_PROMPT

# Store memories in memory by session_id
_memories = {}

def get_chatbot_chain(session_id: str):
    """Build a conversational model."""
    
    # Initialize the LLM (Using OpenRouter/OpenAI via config)(store)
    api_key = os.getenv("LLM_API_KEY", "sk-placeholder")
    base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    model_name = os.getenv("LLM_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
    
    # Fallback to a valid key format to avoid validation errors if missing
    if not api_key or len(api_key) < 5:
        api_key = "sk-placeholder-key-for-langchain"

    llm = ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model_name,
        temperature=0.3
    )
    return llm

async def generate_chat_response(session_id: str, user_message: str) -> str:
    """Entry point to invoke the chain with the user message."""
    try:
        llm = get_chatbot_chain(session_id)
        
        if session_id not in _memories:
            _memories[session_id] = [SystemMessage(content=SYSTEM_PERSONA)]
            
        _memories[session_id].append(HumanMessage(content=user_message))
        
        response = await llm.ainvoke(_memories[session_id])
        
        _memories[session_id].append(AIMessage(content=response.content))
        return response.content
    except Exception as e:
        print(f"LangChain Error: {e}")
        return f"I'm sorry, I encountered an error connecting to my AI brain. (Error: {e})"

def classify_intent(message: str, role: str = 'Student') -> str:
    msg = message.lower()
    # Student intents
    if any(w in msg for w in ['attendance','absent','present']): return 'attendance'
    if any(w in msg for w in ['result','marks','grade','gpa','cgpa']): return 'results'
    if any(w in msg for w in ['course','registered','enrolled']): return 'courses'
    if any(w in msg for w in ['timetable','schedule','class time']): return 'timetable'
    if any(w in msg for w in ['fee','dues','payment','tuition']): return 'fees'
    if any(w in msg for w in ['assignment','homework','pending','due']): return 'assignments'
    if any(w in msg for w in ['study plan','prepare','how to study','weak']): return 'study_plan'
    if any(w in msg for w in ['exam','test','quiz','when is']): return 'exams'
    if any(w in msg for w in ['policy','rule','regulation','calendar']): return 'policy'
    # Faculty intents
    if role == 'Faculty':
        if any(w in msg for w in ['low attendance','absent']): return 'faculty_attendance'
        if any(w in msg for w in ['ungraded','not graded']): return 'faculty_ungraded'
        if any(w in msg for w in ['at risk','failing','weak']): return 'faculty_at_risk'
        if any(w in msg for w in ['performance','stats']): return 'faculty_stats'
    # Admin intents
    if role == 'Admin':
        if any(w in msg for w in ['total student','enrollment']): return 'admin_students'
        if any(w in msg for w in ['admission','intake']): return 'admin_admissions'
        if any(w in msg for w in ['fee','collection','revenue']): return 'admin_fees'
        if any(w in msg for w in ['department','performance']): return 'admin_departments'
    return 'general'

async def generate_contextual_response(sid, msg, data, intent):
    if intent == 'attendance':
        prompt = ATTENDANCE_PROMPT.format(student_id=sid,
            attendance_data=data, question=msg)
    elif intent == 'results':
        prompt = RESULTS_PROMPT.format(student_id=sid,
            results_data=data, question=msg)
    elif intent in ('courses','timetable'):
        prompt = COURSE_PROMPT.format(student_id=sid,
            course_data=data, question=msg)
    else:
        prompt = f'Data: {data}\nQuestion: {msg}'
    return await generate_chat_response(sid, prompt)