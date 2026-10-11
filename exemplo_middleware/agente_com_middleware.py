from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage


# Montando nosso middleware customizado
class MiddlewareDemonstracao(AgentMiddleware):
    def __init__(self):
        super().__init__()

    def before_agent(self, state: AgentState, runtime):
        print("Passando pelo 'before_agent'") # aqui posso criar logs, métricas, etc.

    def before_model(self, state: AgentState, runtime):
        print("Passando pelo 'before_model'") # posso criar novos prompts, alterar mensagens, etc.

    def after_model(self, state: AgentState, runtime):
        print("Passando pelo 'after_model'") # aqui posso criar ações pós-modelo, como salvar logs, métricas, etc.

    def after_agent(self, state: AgentState, runtime):
        print("Passando pelo 'after_agent'") # posso chamar o langflow, enviar mensagens para o usuário, etc.

@tool
def nome_do_usuario():
    """ Ferramenta responsável por buscar o nome do usuário."""
    print("Passando pela tool")
    return "O usuário se chama PauloPitte"


agente = create_agent(
    model="ollama:llama3.2",
    system_prompt="Seja um assistente util e responda o usuário chamando ele pelo nome!",
    middleware=[MiddlewareDemonstracao()],
    tools=[nome_do_usuario],
)

resposta = agente.invoke({"messages": HumanMessage(content="Olá tudo bem? Você sabe meu nome? O que você é capaz de fazer?")})

print(resposta["messages"][-1].content)

