import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.prompts.templates import SYSTEM_PERSONA

# Store memories in memory by session_id
_memories = {}

def get_chatbot_chain(session_id: str):
    """Build a conversational model."""
    
    # Initialize the LLM (Using OpenRouter/OpenAI via config)
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
