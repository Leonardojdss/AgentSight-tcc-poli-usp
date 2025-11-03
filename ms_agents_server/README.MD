# MS Agents Server - Servidor de Agentes Analíticos

## 📋 Visão Geral

O **MS Agents Server** é um microsserviço backend desenvolvido em FastAPI que implementa um sistema multi-agente para análise de dados de vendas. Utilizando a arquitetura LangGraph e agentes especializados, o sistema fornece análises descritivas, diagnósticas, preditivas e prescritivas através de uma API RESTful.

## 🎯 Objetivo

Fornecer uma infraestrutura robusta e escalável para processamento de consultas analíticas sobre dados de vendas, utilizando:
- **Múltiplos agentes especializados** com diferentes expertise analítica
- **Memória conversacional isolada** por cliente e thread
- **Integração com Azure OpenAI** para processamento de linguagem natural
- **Acesso direto a banco de dados PostgreSQL** para consultas SQL dinâmicas

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios

```
ms_agents_server/
├── src/
│   ├── main.py                          # Entrada da aplicação FastAPI
│   ├── controller/
│   │   └── routes.py                    # Rotas HTTP da API
│   ├── data_models/
│   │   └── text_input_conversation.py   # Modelos Pydantic de entrada
│   ├── infrastructure/
│   │   ├── connection_openai.py         # Cliente Azure OpenAI
│   │   └── connection_postgresql.py     # Cliente PostgreSQL
│   ├── prompts/
│   │   ├── supervisor_prompt.txt        # Prompt do agente supervisor
│   │   ├── analise_descritiva_prompt.txt
│   │   ├── analise_diagnostica_prompt.txt
│   │   ├── analise_preditiva_prompt.txt
│   │   └── analise_prescritiva_prompt.txt
│   ├── service/
│   │   └── messages_service.py          # Lógica de negócio
│   ├── usecase/
│   │   └── analysis_usecase.py          # Orquestração de casos de uso
│   ├── utils/
│   │   ├── default_messages.py          # Mensagens padrão
│   │   ├── image_graph.py               # Geração de gráficos
│   │   └── memory_manager.py            # Gerenciamento de memória
│   └── workflow_agentic/
│       ├── agents.py                    # Definição dos agentes
│       ├── graph.py                     # Construção do grafo LangGraph
│       └── tools.py                     # Ferramentas SQL dos agentes
├── tests/
│   └── test_memory.py
└── requirements.txt
```

## 🤖 Arquitetura de Agentes

### Sistema Multi-Agente Supervisor

O sistema utiliza um padrão de **supervisor hierárquico** onde um agente coordenador delega tarefas para agentes especializados:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Supervisor Agent                              │
│  - Analisa a pergunta do usuário                                │
│  - Classifica o tipo de análise necessária                      │
│  - Delega para o agente especializado apropriado                │
│  - Agrega respostas e finaliza                                  │
└────────────┬────────────────────────────────────────────────────┘
             │
    ┌────────┴────────┬────────────┬────────────┐
    │                 │            │            │
    ▼                 ▼            ▼            ▼
┌─────────┐  ┌──────────────┐  ┌─────────┐  ┌──────────────┐
│Descritiva│  │ Diagnóstica  │  │Preditiva│  │ Prescritiva  │
│ Agent   │  │    Agent     │  │ Agent   │  │    Agent     │
└─────────┘  └──────────────┘  └─────────┘  └──────────────┘
     │              │                │              │
     └──────────────┴────────────────┴──────────────┘
                        │
                        ▼
                ┌──────────────┐
                │ SQL Database │
                │   Tool       │
                └──────────────┘
```

### Agentes Especializados

#### 1. **Agente de Análise Descritiva**
- **Responsabilidade**: Responder "O que aconteceu?"
- **Capacidades**:
  - Sumarização de dados
  - Cálculo de métricas agregadas (total, média, contagem)
  - Identificação de valores máximos e mínimos
  - Listagem e classificação de registros
- **Exemplos**: 
  - "Qual foi o total de vendas no último mês?"
  - "Quantos pedidos foram realizados?"

#### 2. **Agente de Análise Diagnóstica**
- **Responsabilidade**: Responder "Por que aconteceu?"
- **Capacidades**:
  - Análise de causas e correlações
  - Comparação entre períodos
  - Identificação de anomalias
  - Drill-down em dimensões específicas
- **Exemplos**:
  - "Por que as vendas caíram em janeiro?"
  - "Qual categoria teve pior desempenho?"

#### 3. **Agente de Análise Preditiva**
- **Responsabilidade**: Responder "O que pode acontecer?"
- **Capacidades**:
  - Projeção de tendências
  - Análise de padrões históricos
  - Previsão baseada em dados passados
- **Exemplos**:
  - "Qual será a tendência de vendas no próximo trimestre?"
  - "Quais produtos devem ter maior demanda?"

#### 4. **Agente de Análise Prescritiva**
- **Responsabilidade**: Responder "O que devemos fazer?"
- **Capacidades**:
  - Recomendações acionáveis
  - Otimização de estratégias
  - Sugestões baseadas em análises anteriores
- **Exemplos**:
  - "Como podemos aumentar as vendas do produto X?"
  - "Quais ações tomar para melhorar o desempenho?"

## 🧠 Arquitetura de Memória

### Sistema de Memória Isolada por Cliente

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  POST /conversation                                              │
│  Headers: { client_id: "user_123" }                             │
│  Body: { message: "...", thread_id: "conv_001" }                │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ConversationAnalysisHandler                         │
│                   (analysis_usecase.py)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  • Recebe: input_message, client_id, thread_id                  │
│  • Valida client_id                                              │
│  • Gera thread_id se necessário                                 │
│  • Chama GraphSupervisor                                         │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GraphSupervisor                               │
│                      (graph.py)                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  • Recebe client_id                                              │
│  • Solicita memória ao MemoryManager                            │
│  • Compila grafo com checkpointer específico                    │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MemoryManager                                 │
│                  (memory_manager.py)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  _memories: Dict[client_id, InMemorySaver]           │      │
│  │                                                        │      │
│  │  "user_123" ──> InMemorySaver (thread_1, thread_2)   │      │
│  │  "user_456" ──> InMemorySaver (thread_1)             │      │
│  │  "user_789" ──> InMemorySaver (thread_1, thread_2)   │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    InMemorySaver                                 │
│            (langgraph.checkpoint.memory)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  • Armazena estados por thread_id                               │
│  • Mantém histórico de mensagens                                │
│  • Permite recuperação de contexto                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```


### Fluxo de Dados Conversacional

```
1. Request Inicial
   ├─> client_id: "user_123"
   ├─> thread_id: "conv_001"
   └─> message: "Qual empresa teve mais vendas?"

2. MemoryManager.get_memory("user_123")
   └─> Retorna InMemorySaver específico do cliente

3. GraphSupervisor.compile(checkpointer=memory)
   └─> Grafo vinculado à memória isolada do cliente

4. graph.astream(messages, config={"thread_id": "conv_001"})
   ├─> Carrega histórico da thread (se existir)
   ├─> Supervisor classifica pergunta
   ├─> Delega para agente especializado
   └─> Agente executa SQL e retorna resposta

5. InMemorySaver
   ├─> Carrega estado anterior da conversa
   ├─> Agentes processam com contexto completo
   └─> Salva novo estado com mensagens atualizadas

6. Response
   └─> "A empresa X teve mais vendas com R$ 10M..."
```

### Isolamento e Multitenancy

```
┌─────────────────────────────────────────────────────────────────┐
│                        MemoryManager                             │
│                   (Singleton Pattern)                            │
└─────────────────────────────────────────────────────────────────┘
           │
           ├─────────────────────────────────────────────┐
           │                                              │
           ▼                                              ▼
    ┌──────────────┐                              ┌──────────────┐
    │  Client A    │                              │  Client B    │
    │  InMemorySaver│                             │  InMemorySaver│
    └──────────────┘                              └──────────────┘
           │                                              │
           ├────────┬────────┐                           ├────────┐
           ▼        ▼        ▼                           ▼        ▼
      thread_1  thread_2  thread_3                  thread_1  thread_2
       │         │         │                          │         │
       ▼         ▼         ▼                          ▼         ▼
    [msgs]    [msgs]    [msgs]                     [msgs]    [msgs]

    ✅ Isolados                                    ✅ Isolados
```

### Estrutura de Estado Persistido

```python
Estado armazenado no InMemorySaver por thread:

{
    "configurable": {
        "thread_id": "conv_001"
    },
    "values": {
        "messages": [
            {
                "role": "user",
                "content": "Qual empresa teve mais vendas?"
            },
            {
                "role": "assistant", 
                "content": "A empresa X teve mais vendas com R$ 10M"
            },
            {
                "role": "user",
                "content": "E qual foi o valor total?"
            },
            {
                "role": "assistant",
                "content": "O valor total de vendas da Empresa X foi R$ 10 milhões..."
            }
        ]
    }
}
```

### Comparação: Com vs Sem Memória

#### Sem Memória Conversacional ❌
```
User: "Qual empresa teve mais vendas?"
Agent: "Empresa X com R$ 10M"

User: "E qual foi o valor total?" 
Agent: "Qual valor? Precisa especificar a empresa." ❌
      (Perdeu o contexto!)
```

#### Com Memória Conversacional ✅
```
User: "Qual empresa teve mais vendas?"
Agent: "Empresa X com R$ 10M"

User: "E qual foi o valor total?"
Agent: "O valor total de vendas da Empresa X foi R$ 10 milhões..." ✅
      (Mantém o contexto da conversa!)
```

## 🔌 API Endpoints

### POST `/ms_agent_server/conversation`

Processa uma mensagem do usuário e retorna análise dos agentes.

**Headers:**
```json
{
  "client_id": "user_123"  // Obrigatório - Identificador único do cliente
}
```

**Request Body:**
```json
{
  "message": "Qual foi o total de vendas no último trimestre?",
  "thread_id": "conv_001"  // Opcional - ID da thread de conversa
}
```

**Response:**
```json
{
  "response": "Com base na análise dos dados...",
  "thread_id": "conv_001",
  "timestamp": "2025-11-03T10:30:00Z"
}
```

**Códigos de Status:**
- `200 OK`: Requisição processada com sucesso
- `400 Bad Request`: Parâmetros inválidos ou ausentes
- `500 Internal Server Error`: Erro no processamento

## 🛠️ Tecnologias Utilizadas

### Core Framework
- **FastAPI 0.116.1**: Framework web assíncrono de alta performance
- **Uvicorn 0.35.0**: Servidor ASGI para Python

### Agentes & LLM
- **LangGraph 0.5.3**: Orquestração de workflows multi-agente
- **LangChain OpenAI 0.3.22**: Integração com Azure OpenAI
- **LangChain Community 0.3.27**: Ferramentas e utilitários da comunidade

### Banco de Dados
- **PostgreSQL**: Banco de dados relacional
- **psycopg2-binary 2.9.10**: Driver PostgreSQL para Python
- **SQLAlchemy 2.0.41**: ORM e toolkit SQL

### Observabilidade
- **Langfuse 3.6.1**: Monitoramento e tracing de LLM

### Utilidades
- **python-dotenv 1.1.1**: Gerenciamento de variáveis de ambiente
- **aiofiles 24.1.0**: I/O assíncrono de arquivos

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.12+
- PostgreSQL 12+
- Acesso à Azure OpenAI API

### Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd ms_agents_server
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=sales_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

# Langfuse Configuration (Opcional)
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Executando o Servidor

**Modo de desenvolvimento:**
```bash
uvicorn ms_agents_server.src.main:app --reload --host 0.0.0.0 --port 8000
```

**Modo de produção:**
```bash
uvicorn ms_agents_server.src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Acesso à documentação interativa:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testes

Execute os testes com pytest:
```bash
pytest tests/
```

Teste específico de memória:
```bash
pytest tests/test_memory.py -v
```


---

**Status do Projeto**: 🚧 Em Desenvolvimento Ativo
