import openai
import os
import pandas as pd
from langchain.agents.tools import Tool
from langchain.utilities import BingSearchAPIWrapper
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage
from langchain.tools import tool
from langchain.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()

search = BingSearchAPIWrapper(k=3)

@tool
def consulta_bwd(query: str) -> str:
    """_summary_

    Args:
        query (str): _description_

    Returns:
        str: _description_
    
    Herramienta encargada de consultar información única y exclusivamente de la empresa Big Wave Data BWD
    """
    
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    
    CHAT_MODEL_NAME = os.getenv("OPENAI_CHAT_MODEL")
    
    chat_llm = AzureChatOpenAI(deployment_name=CHAT_MODEL_NAME, temperature=0)
    
    prompt = (
    """
    Eres un agente que se encarga de dar la información que contengas acerca de la empresa Big Wave Data (BWD), responde si o si solo información relacioanda a la empresa.
    Utiliza solo la información que se te proporciona a continuación, no inventes información.
    
    Datos de la empresa Big Wave Data (BWD)      
        - Empleados actuales:
            1. Nombre: John Smith, Cargo: Desarrollador Senior
            2. Nombre: Sarah Johnson, Cargo: Desarrollador Senior
            3. Nombre: Michael Williams, Cargo: Desarrollador Front-end
            4. Nombre: Emily Brown, Cargo: Desarrollador Back-end
            5. Nombre: Christopher Davis, Cargo: Ingeniero de Software
            6. Nombre: Olivia Miller, Cargo: Desarrollador Full-stack
            7. Nombre: Daniel Jones, Cargo: Diseñador UX/UI
            8. Nombre: Sophia Wilson, Cargo: Desarrollador Front-end
            9. Nombre: David Lee, Cargo: Desarrollador Back-end
            10. Nombre: Emma Martinez, Cargo: Desarrollador Junior
            11. Nombre: Matthew Taylor, Cargo: Ingeniero de Calidad
            12. Nombre: Ava White, Cargo: Diseñador de Experiencia de Usuario
            13. Nombre: James Harris, Cargo: Analista de Negocios
            14. Nombre: Mia Rodriguez, Cargo: Desarrollador Full-stack
            15. Nombre: William Moore, Cargo: Gerente de Proyecto
            16. Nombre: Sophia Clark, Cargo: Ingeniero de Pruebas
            17. Nombre: Alexander Scott, Cargo: Desarrollador Senior
            18. Nombre: Isabella Turner, Cargo: Diseñador Gráfico
            19. Nombre: Benjamin Hall, Cargo: Desarrollador Front-end
            20. Nombre: Amelia Evans, Cargo: Desarrollador Back-end
            21. Nombre: Samuel King, Cargo: Analista de Datos
            22. Nombre: Harper Allen, Cargo: Desarrollador Junior
            23. Nombre: Joseph Wright, Cargo: Desarrollador Full-stack

        - Mision:
            En Big Wave Data, nuestra misión es impulsar la innovación a través de soluciones de software de vanguardia. Nos dedicamos a ofrecer a nuestros clientes productos y servicios de calidad excepcional, diseñados para impulsar sus objetivos comerciales y tecnológicos. 
        - Vision:
            En Big Wave Data, nuestra visión es liderar la industria de desarrollo de software, siendo reconocidos globalmente por nuestra innovación y excelencia en el diseño y entrega de soluciones tecnológicas. 
        - Director General: 
            Luis Cancino Culebro
        - Objetivo:
            El objetivo de Big Wave Data (BWD) es ser el líder en innovación y excelencia en el desarrollo de software, proporcionando soluciones tecnológicas de vanguardia que transformen la forma en que las empresas operan y crecen. Buscamos brindar a nuestros clientes soluciones personalizadas de alta calidad que maximicen su eficiencia y competitividad en un mundo digital en constante evolución.
        - Ubicación:
            Limbasi Ta:Matar, Valle Oriente, 387530 N.L.
        - Telefono:
            81 1193 0694
        - Fundación:
            Diciembre 2013
                
    Siempre retorna la información como cadena, NUNCA inventes información
    
    """ + query)
    
    response = chat_llm.predict_messages(messages=[SystemMessage(content=prompt)])
    return response.__str__()

@tool
def consultar_ventas(query: str) -> str:
    """Herramientan encargada de consultar información de ventas en un archivo determinado"""
    
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    
    COMPLETION_MODEL_NAME = os.getenv("OPENAI_COMPLETIONS_MODEL")
    COMPLETION_ENGINE_NAME = os.getenv("OPENAI_COMPLETIONS_ENGINE")
    
    completions_llm = AzureOpenAI(model_name=COMPLETION_MODEL_NAME, engine = COMPLETION_ENGINE_NAME, temperature=0)

    data = pd.read_csv("Data/datasetAutos.csv")
    agent = create_pandas_dataframe_agent(completions_llm, df=data, verbose=True)
    
    prompt = ("""
              Eres un agente especializado en realizar busqueda de información en un dataset de ventas 
              Retorna toda la información como una cadena
              
              """ + query)
    
    response = agent.run(prompt)
    return response.__str__()


tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
    Tool(
        name="ConsultaBWD",
        func=consulta_bwd,
        description="Este agente es útil para realizar consultas de información de la empresa Big Wave Data BWD de Monterrey Nuevo León México"
    ),
    Tool(
        name="Ventas",
        func=consultar_ventas,
        description="Este agente es útil para realizar consultas de información de ventas"
    )
]