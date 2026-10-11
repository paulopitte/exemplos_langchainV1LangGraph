from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage, AIMessage

print("=========== exemplo 1 ============")

## Criando um ChatModel (
model = init_chat_model(
    model = 'ollama:llama3.2', # opcional "openai:gpt-4.1-mini", "anthropic:claude-sonnet-4-5-20250929"
    temperature = 0.1
)

## Imprimindo a resposta da chamada ao modelo:

resposta = model.invoke([HumanMessage(content="O que é python?")])
print(resposta)
print(resposta.content)

print("=========== exemplo 2 ============")

## Exemplo com uma "conversa" (lista de mensagens):

conversation = [
    SystemMessage("Você é um assistente de programação especialista em python e sua habilidade é responder e explicar de forma didática duvidas de um desenvolvedor iniciante."),
    HumanMessage("Oi tudo bem?"),
    AIMessage("Olá, tudo bem comigo. No que posso te ajudar?"),
    HumanMessage("O que é python?"),
]

response = model.invoke(conversation)

print(response)
print(response.content)

print("=========== exemplo 3 ============")
## Exemplo com stream de tokens:

for chunk in model.stream(conversation):
    print(chunk.text, end ="", flush=True)
