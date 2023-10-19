import streamlit as st
import agente as tools
import openai
import os
import layout as ly
from langchain.agents.tools import Tool
from langchain.llms import AzureOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from streamlit_chat import message

main_page = st.empty()
st.title("Iniciar conversación")
user_message = st.text_input("Escriba tu mensaje aquí", key="user_input")

if user_message != "":
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    
    COMPLETION_MODEL_NAME = os.getenv("OPENAI_COMPLETIONS_MODEL")
    COMPLETION_ENGINE_NAME = os.getenv("OPENAI_COMPLETIONS_ENGINE")
    
    toolkit = [
            Tool(
                name=tool.name,
                func=tool.func,
                description=tool.description
            ) for tool in tools.tools
        ]
    
    agentellm = AzureOpenAI(model_name=COMPLETION_MODEL_NAME, engine=COMPLETION_ENGINE_NAME,temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(toolkit, agentellm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    agent.agent.llm_chain.prompt.template = ly.prompt
    
    response = agent.run(user_message)
    
    finalResponse = response.split("|||")[0]
    
    message(
        finalResponse,
        avatar_style='bottts-neutral',
        seed='George'
    )