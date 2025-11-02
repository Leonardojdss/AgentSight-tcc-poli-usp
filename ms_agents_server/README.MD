# Arquitetura de Memória - Diagrama

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

## Fluxo de Dados

```
1. Request
   ├─> client_id: "user_123"
   ├─> thread_id: "conv_001"
   └─> message: "Qual empresa teve mais vendas?"

2. MemoryManager.get_memory("user_123")
   └─> Retorna InMemorySaver específico

3. GraphSupervisor.compile(checkpointer=memory)
   └─> Grafo vinculado à memória do cliente

4. graph.astream(messages, config={"thread_id": "conv_001"})
   └─> Executa com contexto da thread

5. InMemorySaver
   ├─> Carrega estado anterior (se existir)
   ├─> Agentes processam com contexto
   └─> Salva novo estado

6. Response
   └─> "A empresa X teve mais vendas..."
```

## Isolamento de Memória

```
┌─────────────────────────────────────────────────────────────────┐
│                        MemoryManager                             │
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

## Estrutura de Estado

```python
Estado armazenado no InMemorySaver:

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
                "content": "A empresa X teve mais vendas..."
            },
            {
                "role": "user",
                "content": "E qual foi o valor total?"
            },
            {
                "role": "assistant",
                "content": "O valor total foi R$ 10 milhões..."
            }
        ]
    }
}
```

## Comparação: Com vs Sem Memória

### Sem Memória (Antes)
```
User: "Qual empresa teve mais vendas?"
Agent: "Empresa X"

User: "E qual foi o valor?" 
Agent: "Qual valor? Precisa especificar." ❌
```

### Com Memória (Agora)
```
User: "Qual empresa teve mais vendas?"
Agent: "Empresa X"

User: "E qual foi o valor?"
Agent: "O valor de vendas da Empresa X foi..." ✅
      (Lembra do contexto!)
```

## Escalabilidade

### Desenvolvimento (InMemorySaver)
```
┌──────────────┐
│   App        │
│  ┌────────┐  │
│  │ Memory │  │
│  └────────┘  │
└──────────────┘
     RAM
```

### Produção (PostgresSaver)
```
┌──────────────┐      ┌──────────────┐
│   App 1      │ ───▶ │              │
│              │      │              │
├──────────────┤      │  PostgreSQL  │
│   App 2      │ ───▶ │   Database   │
│              │      │              │
├──────────────┤      │              │
│   App 3      │ ───▶ │              │
└──────────────┘      └──────────────┘
   Cluster           Memória Compartilhada
```
