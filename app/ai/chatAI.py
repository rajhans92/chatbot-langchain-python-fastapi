from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from app.helpers.config import OPENAI_API_KEY
from app.schemas.chatSchemas import ChatHistoryRequest,ChatRequest

model = ChatOpenAI(model="gpt-4.1")

def chatbot(message: ChatRequest, chat_history: ChatHistoryRequest) -> str:
    memory = ConversationBufferMemory(return_messages=True)
        
    for msg in chat_history:
        if msg.role == "user":
            memory.chat_memory.add_user_message(msg.message)
        else:
            memory.chat_memory.add_ai_message(msg.message)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain =  prompt | model

    ai_response = chain.invoke({
            "history": memory.load_memory_variables({})["history"],
            "input": message.message
        })

    return ai_response.content
