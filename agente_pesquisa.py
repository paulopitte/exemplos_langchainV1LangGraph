from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from dataclasses import dataclass

from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain.chat_models import init_chat_model



## Criando Um contexto runtime (exemplo pegando o nome do usuário do nosso sistema)
@dataclass
class Context:
    user_name: str


## Criando nossa Tools

"""Tool de pesquisa"""
search = DuckDuckGoSearchResults(output_format="list")

"""Tool de escrita de txt"""
@tool(parse_docstring=True)
def escreve_arquivo_txt(
    nome_arquivo: Annotated[str, "Nome do arquivo TXT onde o conteudo sera escrito, incluindo a extensao .txt"],
    conteudo: Annotated[str, "Texto completo que sera escrito no arquivo. Todo o conteudo anterior sera substituido."],
    runtime: ToolRuntime[Context]
) -> str:
    """Escreve ou sobrescreve um arquivo de texto (.txt) no diretorio atual com o conteudo fornecido. Esta ferramenta cria um novo arquivo de texto ou sobrescreve um arquivo existente com o conteudo especificado. ATENCAO: Se o arquivo ja existir, todo o seu conteudo anterior sera completamente substituido pelo novo conteudo. Para adicionar conteudo ao final de um arquivo existente, primeiro use ler_arquivo_txt para obter o conteudo atual e entao concatene com o novo conteudo.

    Args:
        nome_arquivo: O nome do arquivo onde escrever, deve incluir a extensao .txt. Se o arquivo nao existir, sera criado. Se existir, sera sobrescrito (por exemplo: 'saida.txt' ou 'resultado.txt')
        conteudo: O texto completo a ser escrito no arquivo. Pode conter multiplas linhas e caracteres especiais. Use quebras de linha quando necessario

    Returns:
        Mensagem de sucesso indicando que o arquivo foi escrito corretamente, ou mensagem de erro se algo deu errado
    """
    try:
        with open(runtime.context.user_name + "_" + nome_arquivo , 'w', encoding='utf-8') as arquivo: # acessando o contex e criando o txt com complemento do nome do usuário.
            arquivo.write(conteudo)
        return f"Sucesso: O conteudo foi escrito no arquivo '{nome_arquivo}'."
    except PermissionError:
        return f"Erro: Sem permissao para escrever no arquivo '{nome_arquivo}'."
    except Exception as e:
        return f"Erro ao escrever no arquivo '{nome_arquivo}': {str(e)}"


## Inicializando nosso chat
model = init_chat_model("ollama:llama3.2", temperature=0)

agent = create_agent(
    model=model,
    tools=[escreve_arquivo_txt, search],
    context_schema=Context,
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="ollama:llama3.2",
            trigger=("tokens", 4000),
            keep=("messages", 5)),
        HumanInTheLoopMiddleware(
            interrupt_on={
                "escreve_arquivo_txt": {
                    "allowed_decisions": ["approve", "reject"],
                },
                "duckduckgo_results_json": False,
            })
                ],
)


def print_messages(result):
    """Imprime as mensagens do resultado de forma legível."""
    if "messages" in result:
        for msg in result["messages"]:
            role = msg.__class__.__name__.replace("Message", "")
            print(f"\n[{role}]: {msg.content}")
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"  -> Tool Call: {tc['name']}({tc['args']})")


def main():
    config = {"configurable": {"thread_id": "1"}}
    context = Context(user_name="PauloPitte")  # Exemplo de contexto com o nome do usuário

    print("=" * 50)
    print("Agente de Pesquisa - Digite 'Q' para sair")
    print("=" * 50)

    while True:
        user_input = input("\nVocê: ").strip()

        if user_input.upper() == "Q":
            print("\nEncerrando o agente. Até mais!")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                context=context
            )

            print_messages(result)

            # Verifica se há interrupção humana pendente (conforme documentação)
            while "__interrupt__" in result:
                interrupts = result["__interrupt__"]

                print("\n" + "=" * 50)
                print("INTERRUPÇÃO: Aprovação necessária!")
                print("=" * 50)

                # Mostra informações sobre as ações pendentes
                for interrupt in interrupts:
                    interrupt_value = interrupt.value
                    if hasattr(interrupt_value, "action_requests"):
                        for action in interrupt_value.action_requests:
                            print(f"Tool: {action.action}")
                            print(f"Args: {action.args}")

                decision = input("\nDigite 'approve' para aprovar ou 'reject' para rejeitar: ").strip().lower()

                if decision == "approve":
                    # Continua a execução aprovando via Command (conforme documentação)
                    result = agent.invoke(
                        Command(resume={"decisions": [{"type": "approve"}]}),
                        config=config,
                        context=context
                    )
                    print_messages(result)
                elif decision == "reject":
                    # Rejeita a tool call via Command
                    result = agent.invoke(
                        Command(resume={"decisions": [{"type": "reject", "reason": "Rejeitado pelo usuário"}]}),
                        config=config,
                        context=context
                    )
                    print_messages(result)
                    break
                else:
                    print("Opção inválida. Use 'approve' ou 'reject'.")

        except Exception as e:
            print(f"\nErro: {e}")


if __name__ == "__main__":
    main()

# https://docs.langchain.com/oss/python/langchain/human-in-the-loop#%E2%9C%85-approve
