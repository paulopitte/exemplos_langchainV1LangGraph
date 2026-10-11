# Exemplos LangChain / LangGraph v1


![LangChain v1.png](nota_aula/LangChain%20v1.png)

## Estrutura do Projeto

```
├── exemplo_chatmodels/      # Uso do init_chat_model e mensagens
├── exemplo_agente_simples/  # Agente basico com create_agent e tools
├── exemplo_middleware/      # Middleware customizado (before/after hooks)
├── exemplo_runtime/         # Runtime context em grafos LangGraph
├── agente_pesquisa.py       # Exemplo completo: agente com pesquisa, human-in-the-loop e summarization
```

## Exemplos

| Pasta | Conceito |
|-------|----------|
| `exemplo_chatmodels` | `init_chat_model`, `HumanMessage`, `SystemMessage`, streaming |
| `exemplo_agente_simples` | `create_agent`, `@tool`, system_prompt |
| `exemplo_middleware` | `AgentMiddleware`, hooks before/after |
| `exemplo_runtime` | `Runtime[Context]` em nos do StateGraph |
| `agente_pesquisa.py` | `SummarizationMiddleware`, `HumanInTheLoopMiddleware`, checkpointer |

## Como usar com UV

### Instalar o UV

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup do projeto

```bash
# Clonar/entrar no diretorio
cd tutorial_langchain_v1

# Sincronizar dependencias (cria .venv automaticamente)
uv sync

# Configurar variaveis de ambiente
cp .env.exemple .env
# Editar .env e adicionar sua OPENAI_API_KEY
```

### Executar exemplos

```bash
uv run python exemplo_chatmodels/chatmodel_premodelado.py
uv run python exemplo_agente_simples/agente_simples.py
uv run python exemplo_middleware/agente_com_middleware.py
uv run python exemplo_runtime/grafo_com_runtime_context.py
uv run python agente_pesquisa.py
```

## Requisitos

- Python >= 3.13
- OpenAI API Key