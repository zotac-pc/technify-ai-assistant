import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from app.prompts.templates import SYSTEM_PERSONA

# Store memories in memory by session_id
_memories = {}

def get_memory(session_id: str) -> ConversationBufferMemory:
    if session_id not in _memories:
        _memories[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return _memories[session_id]

def get_chatbot_chain(session_id: str) -> LLMChain:
    """Build a conversational chain using ChatOpenAI and ConversationBufferMemory."""
    
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

    # Set up the prompt template with Memory Injection
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_PERSONA),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{user_message}")
    ])

    memory = get_memory(session_id)

    # Build the Chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    return chain

async def generate_chat_response(session_id: str, user_message: str) -> str:
    """Entry point to invoke the chain with the user message."""
    try:
        chain = get_chatbot_chain(session_id)
        
        # NOTE: For Week 1 Task, we simply pass the message to the memory chain.
        # In Week 3, we will use the templates from `app.prompts.templates`
        # and ERP data to inject dynamic context.
        
        response = await chain.ainvoke({"user_message": user_message})
        return response["text"]
    except Exception as e:
        print(f"LangChain Error: {e}")
        return f"I'm sorry, I encountered an error connecting to my AI brain. (Error: {e})"
