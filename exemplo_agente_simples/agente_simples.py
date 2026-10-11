from dotenv import load_dotenv
load_dotenv()

import requests
from typing import Annotated

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage


@tool
def get_weather(city: Annotated[str, "nome de uma cidade sem acentos e sem espaços."]):
    """Ferramenta responsável por retornar o clima de uma cidade.
    Atenção cidades com espaço substituir por underline. Exemplo: Para São Paulo, usar sao_paulo.
    """
    response = requests.get(f'https://wttr.in/{city}?format=j1')
    return response.json()


agent = create_agent(
    model = 'ollama:llama3.2',   # colocar a OPENAI_API_KEY no .env e instalar o pacote langchain[openai],
    #model_provider = 'ollama',      
    tools = [get_weather],
    system_prompt = 'Você é um assistente meteorológico muito prestativo sempre!'
)

response = agent.invoke({'messages': [HumanMessage(content="Qual é o clima da cidade de mogi_das_cruzes?")]})

print(response)
print(response['messages'][-1].content)

