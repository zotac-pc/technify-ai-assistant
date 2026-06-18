"""
TAIA Chatbot Chain — Phase 3
Member 3: Redis Persistent Conversation Memory

Replaces volatile Python dict (_memories = {}) with Redis so that
conversation history survives server restarts.

If Redis is not running, the code automatically falls back to in-memory
storage so the app never crashes.
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.prompts.templates import SYSTEM_PERSONA, ATTENDANCE_PROMPT, RESULTS_PROMPT, COURSE_PROMPT


# ── Step 1: Try to connect to Redis. Fall back to in-memory if unavailable. ──

_use_redis = False
_memories = {}  # fallback in-memory store

try:
    import redis
    from langchain_community.chat_message_histories import RedisChatMessageHistory

    _redis_client = redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        decode_responses=True,
        socket_connect_timeout=2   # fail fast if Redis is not reachable
    )
    _redis_client.ping()           # raises ConnectionError if Redis is down
    _use_redis = True
    print("[TAIA] Redis connected. Using persistent session memory.")

except Exception as e:
    print(f"[TAIA] Redis not available ({e}). Using in-memory fallback.")


# ── Step 2: Helper — get history for a session ────────────────────────────────

def _get_history(session_id: str):
    """
    Return (list_of_messages, redis_history_object_or_None) for a session.

    - If Redis is available: loads full conversation history from Redis.
    - If not: uses the in-memory dict as fallback.
    Always prepends the System Persona message so the LLM stays in character.
    """
    if _use_redis:
        history = RedisChatMessageHistory(
            session_id=f"taia:{session_id}",
            url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
        )
        msgs = [SystemMessage(content=SYSTEM_PERSONA)]
        msgs.extend(history.messages)   # previous turns loaded from Redis
        return msgs, history
    else:
        if session_id not in _memories:
            _memories[session_id] = [SystemMessage(content=SYSTEM_PERSONA)]
        return _memories[session_id], None


# ── Step 3: Helper — save exchange to history ─────────────────────────────────

def _save_to_history(session_id: str, human_msg: str, ai_msg: str, redis_history):
    """
    Persist the latest human + AI message pair.

    - Redis mode: appends to the Redis list (survives restarts).
    - Fallback mode: appends to the in-memory dict (lost on restart).
    """
    if _use_redis and redis_history is not None:
        redis_history.add_user_message(human_msg)
        redis_history.add_ai_message(ai_msg)
    else:
        if session_id in _memories:
            _memories[session_id].append(HumanMessage(content=human_msg))
            _memories[session_id].append(AIMessage(content=ai_msg))


# ── Step 4: Build the LLM model ───────────────────────────────────────────────

def get_chatbot_chain(session_id: str):
    """
    Create and return the ChatOpenAI LLM instance.
    session_id is accepted for interface compatibility but not used here
    (history management is handled separately).
    """
    api_key   = os.getenv("LLM_API_KEY", "sk-placeholder")
    base_url  = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    model_name = os.getenv("LLM_MODEL", "openrouter/free")

    # Guard: LangChain requires a non-empty key string
    if not api_key or len(api_key) < 5:
        api_key = "sk-placeholder-key-for-langchain"

    return ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model_name,
        temperature=0.3
    )


# ── Step 5: Main chat entry point ─────────────────────────────────────────────

async def generate_chat_response(session_id: str, user_message: str) -> str:
    """
    Send user_message to the LLM with full conversation history.
    Saves the exchange to Redis (or in-memory fallback) afterwards.
    """
    try:
        llm = get_chatbot_chain(session_id)

        # Load previous messages + system prompt
        messages, redis_history = _get_history(session_id)

        # Append the new user turn
        messages.append(HumanMessage(content=user_message))

        # Call the LLM
        response = await llm.ainvoke(messages)
        ai_text = response.content

        # Persist the exchange
        _save_to_history(session_id, user_message, ai_text, redis_history)

        return ai_text

    except Exception as e:
        print(f"LangChain Error: {e}")
        return f"I'm sorry, I encountered an error connecting to my AI brain. (Error: {e})"


# ── Step 6: Intent classifier ─────────────────────────────────────────────────

def classify_intent(message: str, role: str = 'Student') -> str:
    """
    Map a user message to a named intent string.
    Used by main.py to decide which ERP endpoint to call before LLM.
    """
    msg = message.lower()

    # ── Student intents ──
    if any(w in msg for w in ['attendance', 'absent', 'present']):
        return 'attendance'
    if any(w in msg for w in ['result', 'marks', 'grade', 'gpa', 'cgpa']):
        return 'results'
    if any(w in msg for w in ['course', 'registered', 'enrolled']):
        return 'courses'
    if any(w in msg for w in ['timetable', 'schedule', 'class time']):
        return 'timetable'
    if any(w in msg for w in ['fee', 'dues', 'payment', 'tuition']):
        return 'fees'
    if any(w in msg for w in ['assignment', 'homework', 'pending', 'due']):
        return 'assignments'
    if any(w in msg for w in ['study plan', 'prepare', 'how to study', 'weak']):
        return 'study_plan'
    if any(w in msg for w in ['exam', 'test', 'quiz', 'when is']):
        return 'exams'
    if any(w in msg for w in ['policy', 'rule', 'regulation', 'calendar']):
        return 'policy'

    # ── Faculty intents ──
    if role == 'Faculty':
        if any(w in msg for w in ['low attendance', 'absent']):
            return 'faculty_attendance'
        if any(w in msg for w in ['ungraded', 'not graded']):
            return 'faculty_ungraded'
        if any(w in msg for w in ['at risk', 'failing', 'weak']):
            return 'faculty_at_risk'
        if any(w in msg for w in ['performance', 'stats']):
            return 'faculty_stats'

    # ── Admin intents ──
    if role == 'Admin':
        if any(w in msg for w in ['total student', 'enrollment']):
            return 'admin_students'
        if any(w in msg for w in ['admission', 'intake']):
            return 'admin_admissions'
        if any(w in msg for w in ['fee', 'collection', 'revenue']):
            return 'admin_fees'
        if any(w in msg for w in ['department', 'performance']):
            return 'admin_departments'

    return 'general'


# ── Step 7: Contextual response with ERP data ─────────────────────────────────

async def generate_contextual_response(sid: str, msg: str, data: str, intent: str) -> str:
    """
    Format a structured prompt using live ERP data and send it to the LLM.
    Called by main.py after fetching data from the Mock ERP API.
    """
    if intent == 'attendance':
        prompt = ATTENDANCE_PROMPT.format(
            student_id=sid, attendance_data=data, question=msg)
    elif intent == 'results':
        prompt = RESULTS_PROMPT.format(
            student_id=sid, results_data=data, question=msg)
    elif intent in ('courses', 'timetable'):
        prompt = COURSE_PROMPT.format(
            student_id=sid, course_data=data, question=msg)
    else:
        prompt = f'Data: {data}\nQuestion: {msg}'

    return await generate_chat_response(sid, prompt)