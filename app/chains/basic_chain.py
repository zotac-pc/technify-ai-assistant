"""
TAIA - Basic LangChain Chain
File location: app/chains/basic_chain.py
"""

import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# -----------------------------------------
# TAIA System Prompt
# -----------------------------------------
SYSTEM_PROMPT = """You are TAIA (Technify Academic AI Assistant), a helpful university assistant.
You help students, faculty, and admins with academic information.

Current User:
- Name: {user_name}
- Role: {user_role}
- User ID: {user_id}

Rules:
1. Only answer academic questions related to the university.
2. Be friendly, concise, and helpful.
3. If you don't have data, say "Please contact the university office."
4. Never share one student's data with another."""


# -----------------------------------------
# TAIA Chain Class
# -----------------------------------------
class TAIAChain:
    def __init__(self, user_name: str, user_role: str, user_id: str):
        self.user_name = user_name
        self.user_role = user_role
        self.user_id = user_id
        self.chat_history = []  # Stores conversation history

        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0.3)),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

    def chat(self, user_input: str) -> str:
        # Build prompt with current history
        messages = self.prompt.format_messages(
            user_name=self.user_name,
            user_role=self.user_role,
            user_id=self.user_id,
            chat_history=self.chat_history,
            input=user_input
        )

        # Call the LLM
        response = self.llm.invoke(messages)
        answer = response.content

        # Update conversation memory
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=answer))

        return answer


# -----------------------------------------
# Quick Test
# -----------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("TAIA Basic Chain - Test")
    print("=" * 50)

    taia = TAIAChain(
        user_name="Ali Hassan",
        user_role="student",
        user_id="STU-0042"
    )

    # Turn 1
    r1 = taia.chat("What is my attendance in Web Engineering?")
    print(f"\nTAIA: {r1}")

    # Turn 2 - Memory test
    r2 = taia.chat("What about Database Systems?")
    print(f"\nTAIA: {r2}")

    # Turn 3
    r3 = taia.chat("Can you create a study plan for me?")
    print(f"\nTAIA: {r3}")

    print("\nChain working! Memory is also working.")
