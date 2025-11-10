# 🔍 AgentSight

> **TCC - Escola Politécnica da USP**  
> Sistema Multi-Agente de IA para analytics

AgentSight combina **"Agent"** e **"Insight"**, proporcionando uma plataforma inteligente para obtenção de insights analíticos através de conversação natural com agentes especializados.

![AgentSight Architecture](image.png)

## 📋 Sumário

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Base de Dados](#-base-de-dados)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral

O **AgentSight** é um sistema de análise de dados baseado em IA que utiliza múltiplos agentes especializados para fornecer insights sobre dados de vendas. O sistema permite que usuários façam perguntas em linguagem natural e recebam análises descritivas, diagnósticas, preditivas e prescritivas.

### Principais Funcionalidades

- 🤖 **Sistema Multi-Agente**: Agentes especializados em diferentes tipos de análise
- 💬 **Conversação Natural**: Interface de chat intuitiva para interação com os agentes
- 🧠 **Memória Contextual**: Mantém o contexto da conversa por cliente e thread
- 📊 **Análises Avançadas**: Suporte a 4 tipos de análise (descritiva, diagnóstica, preditiva, prescritiva)
- 🔄 **Streaming em Tempo Real**: Respostas exibidas progressivamente
- 🗄️ **Integração com PostgreSQL**: Consultas SQL dinâmicas sobre dados reais

## 🏗️ Arquitetura

O projeto segue uma arquitetura de microsserviços com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                    MS Front End                         │
│              (Streamlit Interface)                      │
│  - Interface conversacional                            │
│  - Gerenciamento de sessões                           │
│  - Streaming de respostas                             │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────┐
│                MS Agents Server                         │
│                (FastAPI Backend)                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Supervisor Agent                      │   │
│  │     (Coordenador de Agentes)                    │   │
│  └──────────┬──────────────────────────────────────┘   │
│             │                                           │
│  ┌──────────┴──────────────────────────────────────┐   │
│  │                                                  │   │
│  ▼              ▼              ▼              ▼     │   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │Descritivo│  │Diagnóstico││Preditivo││Prescritivo│  │
│  │ Agent   │  │  Agent   │  │ Agent   ││  Agent   │  │
│  └────┬────┘  └────┬─────┘  └────┬────┘└────┬─────┘  │
│       └────────────┼─────────────┼──────────┘         │
│                    │ SQL Queries │                     │
└────────────────────┼─────────────┼─────────────────────┘
                     ▼             ▼
              ┌──────────────────────────┐
              │   PostgreSQL Database    │
              │  - Invoices              │
              │  - Order Leads           │
              │  - Sales Team            │
              └──────────────────────────┘
```

### Fluxo de Funcionamento

1. **Usuário** faz uma pergunta na interface Streamlit
2. **MS Front End** envia a mensagem para o MS Agents Server
3. **Supervisor Agent** analisa a pergunta e roteia para o agente especializado adequado
4. **Agente Especializado** processa a pergunta, executa consultas SQL se necessário
5. **Resposta** é retornada via streaming para o usuário

## 🛠️ Tecnologias

### Backend (MS Agents Server)
- **FastAPI** - Framework web moderno e de alta performance
- **LangGraph** - Orquestração de agentes e workflows
- **LangChain** - Framework para aplicações com LLMs
- **Azure OpenAI** - Modelos de linguagem GPT-4
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python

### Frontend (MS Front End)
- **Streamlit** - Framework para criação de aplicações web interativas
- **Python Requests** - Cliente HTTP para comunicação com API

### DevOps
- **Docker** - Containerização dos microsserviços
- **Python 3.12** - Linguagem de programação

## 📁 Estrutura do Projeto

```
AgentSight-tcc-poli-usp/
├── README.md                          # Este arquivo
├── dataset/                           # Dados CSV para importação
│   ├── Invoices.csv
│   ├── OrderLeads.csv
│   └── SalesTeam.csv
├── ms_agents_server/                  # Backend - Sistema de Agentes
│   ├── dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── main.py                   # Entrada da aplicação
│   │   ├── controller/               # Rotas HTTP
│   │   ├── data_models/              # Modelos Pydantic
│   │   ├── infrastructure/           # Conexões (OpenAI, PostgreSQL)
│   │   ├── prompts/                  # Prompts dos agentes
│   │   ├── service/                  # Lógica de negócio
│   │   ├── usecase/                  # Casos de uso
│   │   ├── utils/                    # Utilitários
│   │   └── workflow_agentic/         # Agentes, Graph, Tools
│   └── tests/
├── ms_front_end/                      # Frontend - Interface Web
│   ├── dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── app.py                    # Aplicação Streamlit
│   │   ├── infrastructure/           # Cliente API
│   │   ├── modules/                  # Handlers de conversa
│   │   └── utils/                    # Utilitários
│   └── tests/
└── env/                              # Ambiente virtual Python
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.12+
- PostgreSQL 12+
- Azure OpenAI API Key
- Docker (opcional)

### 1. Clone o Repositório

```bash
git clone https://github.com/Leonardojdss/AgentSight-tcc-poli-usp.git
cd AgentSight-tcc-poli-usp
```

### 2. Configure o Ambiente Virtual

```bash
python -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate
```

### 3. Instale as Dependências

**Backend:**
```bash
cd ms_agents_server
pip install -r requirements.txt
```

**Frontend:**
```bash
cd ../ms_front_end
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

Crie arquivos `.env` em cada microsserviço com as seguintes variáveis:

**ms_agents_server/.env:**
```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=agentsight
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
```

**ms_front_end/.env:**
```env
AGENTS_SERVER_URL=http://localhost:8000
```

### 5. Prepare o Banco de Dados

Execute os scripts SQL abaixo para criar as tabelas necessárias:

#### Tabela INVOICES
```sql
CREATE TABLE IF NOT EXISTS public.invoices (
    order_id VARCHAR(256) PRIMARY KEY,
    date_order DATE,
    meal_id VARCHAR(256),
    company_id VARCHAR(256),
    date_of_meal TIMESTAMPTZ,
    participants TEXT,
    meal_price NUMERIC(10, 2),
    type_of_meal VARCHAR(256)
);
```

#### Tabela ORDER_LEADS
```sql
CREATE TABLE IF NOT EXISTS public.order_leads (
    order_id VARCHAR(256),
    company_id VARCHAR(256),
    company_name VARCHAR(256),
    date DATE,
    order_value NUMERIC(10, 2),
    converted BOOLEAN
);
```

#### Tabela SALES_TEAM
```sql
CREATE TABLE IF NOT EXISTS public.sales_team (
    sales_resp VARCHAR(200),
    sales_resp_id VARCHAR(50),
    company_name VARCHAR(200),
    company_id VARCHAR(50)
);
```

### 6. Importe os Dados

Utilize os arquivos CSV da pasta `dataset/` para popular as tabelas.

## 💻 Uso

### Iniciando o Backend

```bash
cd ms_agents_server
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

O servidor estará disponível em: `http://localhost:8000`

### Iniciando o Frontend

```bash
cd ms_front_end
streamlit run src/app.py
```

A interface web estará disponível em: `http://localhost:8501`

### Usando o Sistema

1. Acesse a interface web em `http://localhost:8501`
2. Insira um **Client ID** na barra lateral (ou use o padrão `default_client`)
3. Digite sua pergunta sobre os dados de vendas
4. Aguarde a resposta do agente especializado

### Exemplos de Perguntas

- **Análise Descritiva**: "Qual foi o total de vendas no último mês?"
- **Análise Diagnóstica**: "Por que as vendas caíram em março?"
- **Análise Preditiva**: "Qual será o faturamento esperado para o próximo trimestre?"
- **Análise Prescritiva**: "O que devemos fazer para aumentar as conversões?"

## 🗄️ Base de Dados

### Modelo de Dados

O sistema utiliza três tabelas principais:

#### 📋 INVOICES
Armazena informações sobre pedidos e refeições.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `order_id` | VARCHAR(256) | ID único do pedido (PK) |
| `date_order` | DATE | Data do pedido |
| `meal_id` | VARCHAR(256) | ID da refeição |
| `company_id` | VARCHAR(256) | ID da empresa |
| `date_of_meal` | TIMESTAMPTZ | Data/hora da refeição |
| `participants` | TEXT | Participantes |
| `meal_price` | NUMERIC(10,2) | Preço da refeição |
| `type_of_meal` | VARCHAR(256) | Tipo de refeição |

#### 📊 ORDER_LEADS
Rastreia leads e conversões de vendas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `order_id` | VARCHAR(256) | ID do pedido |
| `company_id` | VARCHAR(256) | ID da empresa |
| `company_name` | VARCHAR(256) | Nome da empresa |
| `date` | DATE | Data do lead |
| `order_value` | NUMERIC(10,2) | Valor do pedido |
| `converted` | BOOLEAN | Lead convertido? |

#### 👥 SALES_TEAM
Informações sobre a equipe de vendas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `sales_resp` | VARCHAR(200) | Nome do responsável |
| `sales_resp_id` | VARCHAR(50) | ID do responsável |
| `company_name` | VARCHAR(200) | Nome da empresa |
| `company_id` | VARCHAR(50) | ID da empresa |

## 🤝 Contribuição

Este é um projeto de TCC da Escola Politécnica da USP. Contribuições são bem-vindas!

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é desenvolvido como Trabalho de Conclusão de Curso (TCC) na Escola Politécnica da USP.

## 👨‍💻 Autor

**Leonardo Santos**
- GitHub: [@Leonardojdss](https://github.com/Leonardojdss)

## 📚 Documentação Adicional

Para informações detalhadas sobre cada microsserviço:

- [MS Agents Server - README](./ms_agents_server/README.MD)
- [MS Front End - README](./ms_front_end/README.MD)

---

**AgentSight** - Transformando dados em insights através de agentes inteligentes 🚀