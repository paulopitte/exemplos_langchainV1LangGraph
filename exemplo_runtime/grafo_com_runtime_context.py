from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass


from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.runtime import Runtime
from langgraph.graph import StateGraph, START, END, MessagesState

@dataclass
class MeuContexto:
    user_name: str

model = init_chat_model(model="ollama:llama3.2", temperature=0.1)

# Criando apenas 1 nó com chamada LLM

def call_llm(state: MessagesState, runtime: Runtime[MeuContexto]):
    if runtime.context.user_name  == "PauloPitte":
        prompt_sys = [SystemMessage(content=f"O Usuário se chama {runtime.context.user_name }. Aja como um assistente comediante.")]
    else:
        prompt_sys = [SystemMessage(content=f"O Usuário se chama {runtime.context.user_name }. Aja como um assistente prestativo formal.")]

    mensagens = prompt_sys + state["messages"]

    resposta = model.invoke(mensagens)
    return {"messages": resposta.content}

## Grafo
grafo = StateGraph(MessagesState)

grafo.add_node("call_llm", call_llm)

grafo.add_edge(START, "call_llm")
grafo.add_edge("call_llm", END)

app = grafo.compile()



print("---------- Exemplo usuário PauloPitte ---------")

resposta_app = app.invoke(
    {"messages": [HumanMessage(content="Olá como está o dia Hoje?")]},
    context=MeuContexto(user_name="PauloPitte")
)
print(resposta_app["messages"][-1].content)

print("---------- Exemplo usuário Fernanda ---------")

resposta_app = app.invoke(
    {"messages": [HumanMessage(content="Olá como está o dia Hoje?")]},
    context=MeuContexto(user_name="Fernanda")
)
print(resposta_app["messages"][-1].content)