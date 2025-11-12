import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Load .env variables
load_dotenv()

# Initialize LLM (Groq)
llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    streaming=False
)

# ✅ Memory (stores conversation history)
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# ✅ Prompt — restricts the chatbot’s topic
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "You are **WW3 ChatBot**, an expert assistant that ONLY discusses topics "
        "related to **World War 3** — including geopolitics, alliances, AI in warfare, "
        "military strategy, historical parallels, or potential outcomes.\n\n"
        "If the user asks something unrelated to WW3, politely refuse and say you "
        "can only discuss topics related to World War 3.\n\n"
        "Maintain memory of the user’s details, such as their name or anything they mention, "
        "to provide personalized, contextual responses.\n\n"
        "Conversation so far:\n{history}\n\n"
        "User: {input}\n"
        "WW3 ChatBot:"
    )
)

# ✅ Build conversational chain
conversation = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
)

def get_response(user_input: str) -> str:
    """Get response restricted to WW3 topics with memory."""
    try:
        response = conversation.run(input=user_input)
        return response.strip()
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return "Sorry, I had trouble processing that."
