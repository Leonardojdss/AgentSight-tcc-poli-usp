# MS Front End - Interface Conversacional AgentSight

## 📋 Visão Geral

O **MS Front End** é a interface web do sistema AgentSight, desenvolvida com Streamlit. Fornece uma experiência de chat intuitiva e interativa para que usuários possam conversar com agentes analíticos e obter insights sobre dados de vendas em linguagem natural.

## 🎯 Objetivo

Criar uma interface de usuário amigável e responsiva que:
- **Permita conversas naturais** com agentes analíticos especializados
- **Mantenha contexto conversacional** através de múltiplas interações
- **Exiba respostas em tempo real** com efeito de streaming
- **Identifique usuários únicos** através de Client IDs
- **Gerencie múltiplas threads** de conversa simultaneamente

## 🏗️ Arquitetura da Aplicação

### Estrutura de Diretórios

```
ms_front_end/
├── src/
│   ├── app.py                        # Aplicação principal Streamlit
│   ├── infrastructure/
│   │   └── interface_agents.py       # Cliente HTTP para MS Agents Server
│   ├── modules/
│   │   └── conversation/
│   │       └── agent_conversation.py # Handler de conversação
│   └── utils/
│       ├── default_messages.py       # Mensagens padrão da UI
│       └── message_stream.py         # Comportamento de streaming
├── tests/
└── requirements.txt
```

## 🎨 Componentes da Interface

### 1. Sidebar (Barra Lateral)
```python
┌─────────────────────────┐
│    AgentSight           │
│                         │
│  Bem-vindo ao           │
│  AgentSight!            │
│                         │
│  ┌──────────────────┐   │
│  │ Client ID Input  │   │
│  │ default_client   │   │
│  └──────────────────┘   │
│                         │
└─────────────────────────┘
```

**Funcionalidades:**
- Título da aplicação
- Mensagem de boas-vindas
- Campo de entrada para Client ID
- Instruções de uso

### 2. Área de Chat Principal
```python
┌─────────────────────────────────────────────┐
│                                             │
│  👤 User                                    │
│  ┌───────────────────────────────────────┐ │
│  │ Qual foi o total de vendas?           │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  🤖 Assistant                               │
│  ┌───────────────────────────────────────┐ │
│  │ Com base na análise dos dados...      │ │
│  │ O total de vendas foi R$ 10M          │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  👤 User                                    │
│  ┌───────────────────────────────────────┐ │
│  │ E qual empresa vendeu mais?           │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  🤖 Assistant                               │
│  ┌───────────────────────────────────────┐ │
│  │ A empresa X teve mais vendas...▌      │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

**Funcionalidades:**
- Histórico completo de mensagens
- Diferenciação visual entre usuário e assistente
- Efeito de streaming em tempo real (cursor piscante)
- Scroll automático para última mensagem

### 3. Input de Chat
```python
┌─────────────────────────────────────────────┐
│ Pergunte ao agente análitico qualquer      │
│ coisa sobre os dados de vendas...          │
└─────────────────────────────────────────────┘
```

**Funcionalidades:**
- Placeholder descritivo
- Submit com Enter
- Validação de Client ID antes do envio
- Desabilitado até que Client ID seja fornecido

## 🔄 Fluxo de Interação

### Fluxo Completo de uma Conversa

```
1. Usuário Acessa a Aplicação
   └─> Streamlit inicializa session_state.messages = []

2. Usuário Insere Client ID na Sidebar
   ├─> Exemplo: "leonardo_client"
   └─> Armazenado na variável client_id

3. Usuário Digite Mensagem no Chat Input
   └─> Exemplo: "Qual foi o total de vendas?"

4. Mensagem Adicionada ao Histórico Local
   └─> st.session_state.messages.append({
         "role": "user",
         "content": "Qual foi o total de vendas?"
       })

5. ConversationHandler Envia para Backend
   ├─> POST http://localhost:8000/ms_agent_server/conversation
   ├─> Headers: { "client_id": "leonardo_client" }
   └─> Body: { "message": "Qual foi o total de vendas?" }

6. Backend Processa com Agentes
   ├─> Supervisor classifica a pergunta
   ├─> Delega para agente descritivo
   ├─> Agente consulta banco de dados
   └─> Retorna resposta estruturada

7. MessageStreamComportment Exibe Streaming
   ├─> Recebe resposta do backend
   ├─> Divide texto em chunks
   └─> Exibe palavra por palavra com cursor "▌"

8. Resposta Adicionada ao Histórico Local
   └─> st.session_state.messages.append({
         "role": "assistant",
         "content": "O total de vendas foi R$ 10M..."
       })

9. Interface Atualizada
   └─> Histórico completo visível no chat
```

### Diagrama de Comunicação

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Streamlit     │         │ Conversation     │         │  MS Agents      │
│   Frontend      │         │    Handler       │         │    Server       │
└────────┬────────┘         └────────┬─────────┘         └────────┬────────┘
         │                           │                            │
         │  1. User Input            │                            │
         │  "Qual total vendas?"     │                            │
         │                           │                            │
         │  2. send_message()        │                            │
         ├──────────────────────────>│                            │
         │                           │                            │
         │                           │  3. POST /conversation     │
         │                           │  + client_id header        │
         │                           ├───────────────────────────>│
         │                           │                            │
         │                           │                            │  4. Agents
         │                           │                            │  Processing
         │                           │                            │     ...
         │                           │                            │
         │                           │  5. Response JSON          │
         │                           │<───────────────────────────┤
         │                           │                            │
         │  6. stream_data()         │                            │
         │<──────────────────────────┤                            │
         │                           │                            │
         │  7. Display with ▌        │                            │
         │     cursor effect         │                            │
         │                           │                            │
```

**Características:**
- Persiste durante toda a sessão do navegador
- Reinicia ao recarregar a página
- Armazena histórico completo de mensagens
- Mantém contexto visual (não confundir com memória dos agentes)

### 2. ConversationHandler (agent_conversation.py)

```python
class ConversationHandler:
    def __init__(self, client_id: str, message: str):
        self.client_id = client_id
        self.message = message
        self.interface = InterfaceAgents()
    
    def send_message(self) -> dict:
        return self.interface.send_message(
            client_id=self.client_id,
            message=self.message
        )
```

**Responsabilidades:**
- Encapsula lógica de envio de mensagens
- Valida parâmetros antes do envio
- Gerencia timeout e retry (futuro)
- Interface com camada de infraestrutura

### 3. InterfaceAgents (interface_agents.py)

```python
class InterfaceAgents:
    BASE_URL = "http://localhost:8000"
    
    def send_message(self, client_id: str, message: str) -> dict:
        response = requests.post(
            f"{self.BASE_URL}/ms_agent_server/conversation",
            headers={"client_id": client_id},
            json={"message": message}
        )
        return response.json()
```

**Responsabilidades:**
- Cliente HTTP para MS Agents Server
- Serialização de requests/responses
- Tratamento de erros de conexão
- Configuração de timeouts

### 4. MessageStreamComportment (message_stream.py)

```python
class MessageStreamComportment:
    @staticmethod
    def stream_data(response: dict, delay: float = 0.02):
        text = response.get("response", "")
        for word in text.split():
            yield word + " "
            time.sleep(delay)
```

**Responsabilidades:**
- Simula streaming de texto
- Adiciona cursor piscante durante digitação
- Controla velocidade de exibição
- Melhora experiência do usuário

## 🔧 Tecnologias Utilizadas

### Framework UI
- **Streamlit 1.51.0**: Framework para criação de interfaces web interativas
  - Session state para gerenciamento de estado
  - Chat components para UI de conversação
  - Hot reload para desenvolvimento rápido

### Bibliotecas Python
- **requests**: Cliente HTTP para comunicação com backend
- **typing**: Type hints para código mais robusto
- **time**: Controle de delays no streaming

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.12+
- MS Agents Server rodando em http://localhost:8000

### Instalação

1. **Navegue até o diretório do frontend:**
```bash
cd ms_front_end
```

2. **Crie e ative o ambiente virtual (opcional, mas recomendado):**
```bash
python -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

### Configuração

**Edite `interface_agents.py` se necessário:**
```python
class InterfaceAgents:
    BASE_URL = "http://localhost:8000"  # Altere para URL do seu backend
```

### Executando a Aplicação

**Comando básico:**
```bash
streamlit run ms_front_end/src/app.py
```

**Ou do diretório raiz do projeto:**
```bash
streamlit run src/app.py
```

**A aplicação estará disponível em:**
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Configurações Avançadas

**Porta personalizada:**
```bash
streamlit run src/app.py --server.port 8080
```

**Modo headless (sem auto-open browser):**
```bash
streamlit run src/app.py --server.headless true
```

**CORS habilitado:**
```bash
streamlit run src/app.py --server.enableCORS false
```

## 🎯 Casos de Uso

### 1. Consulta Simples
```
User: "Qual foi o total de vendas em 2024?"
Assistant: "O total de vendas em 2024 foi R$ 15,5 milhões."
```

### 2. Conversa Contextual
```
User: "Qual empresa teve mais vendas?"
Assistant: "A empresa TechCorp teve mais vendas com R$ 5M."

User: "E em que período?"
Assistant: "As vendas de R$ 5M da TechCorp foram no último trimestre."
```

### 3. Análise Comparativa
```
User: "Compare vendas de 2023 vs 2024"
Assistant: "Em 2023: R$ 12M. Em 2024: R$ 15,5M. Crescimento de 29,2%."
```

### 4. Recomendações
```
User: "Como posso aumentar vendas do produto X?"
Assistant: "Baseado nos dados, recomendo: 1) Focar em clientes enterprise..."
```

## 🎨 Personalização

### Alterar Tema
Crie `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Customizar Sidebar
Edite `app.py`:
```python
with st.sidebar:
    st.title("🤖 Seu Logo")
    st.markdown("**Seu texto customizado**")
    # Adicionar mais elementos...
```

### Adicionar Funcionalidades
```python
# Botão de limpar histórico
if st.sidebar.button("Limpar Conversa"):
    st.session_state.messages = []
    st.rerun()

# Download do histórico
import json
if st.sidebar.button("Baixar Conversa"):
    json_str = json.dumps(st.session_state.messages, indent=2)
    st.sidebar.download_button(
        label="Download JSON",
        data=json_str,
        file_name="conversa.json",
        mime="application/json"
    )
```

## 🐛 Troubleshooting

### Erro: "Connection Refused"
**Problema:** Backend não está rodando
**Solução:** Inicie o MS Agents Server primeiro:
```bash
cd ms_agents_server
uvicorn ms_agents_server.src.main:app --reload
```

### Erro: "Client ID não fornecido"
**Problema:** Campo Client ID está vazio
**Solução:** Insira um Client ID na sidebar antes de enviar mensagens

### Mensagens não aparecem
**Problema:** Session state não inicializado
**Solução:** Recarregue a página (Ctrl+R ou Cmd+R)

### Streaming muito lento/rápido
**Problema:** Delay configurado inadequadamente
**Solução:** Ajuste o parâmetro `delay` em `message_stream.py`:
```python
def stream_data(response: dict, delay: float = 0.01):  # Mais rápido
    # ou
def stream_data(response: dict, delay: float = 0.05):  # Mais lento
```

## 🔒 Segurança

### Client ID
- **Não use informações sensíveis** como CPF ou email completo
- Use identificadores únicos mas anônimos
- Exemplo: `user_12345`, `client_abc123`

### Dados em Trânsito
- Use HTTPS em produção
- Configure certificados SSL/TLS no Streamlit Cloud

### Validação
- Sempre valide Client ID antes de enviar
- Sanitize inputs do usuário
- Implemente rate limiting se necessário

## 📈 Performance

### Otimizações
- Session state é leve e eficiente
- Streaming melhora percepção de velocidade
- Cache de recursos estáticos

### Limites Conhecidos
- Histórico ilimitado pode consumir memória
- Considere limitar a N mensagens recentes
- Session state não persiste entre reloads

### Implementar Paginação
```python
MAX_MESSAGES = 50

if len(st.session_state.messages) > MAX_MESSAGES:
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]
```

## 🚀 Deploy em Produção

### Streamlit Cloud
1. Push código para GitHub
2. Conecte repositório no Streamlit Cloud
3. Configure variáveis de ambiente
4. Deploy automático

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "src/app.py", "--server.port=8501"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  frontend:
    build: ./ms_front_end
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://agents:8000
    depends_on:
      - agents
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaUI`)
3. Commit suas mudanças (`git commit -m 'Add nova interface'`)
4. Push para a branch (`git push origin feature/NovaUI`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é parte de um Trabalho de Conclusão de Curso (TCC) da Poli-USP.

## 👥 Autores

Desenvolvido como parte do TCC - Poli USP

## 📞 Suporte

Para questões e suporte, abra uma issue no repositório do projeto.

---

**Status do Projeto**: 🚧 Em Desenvolvimento Ativo