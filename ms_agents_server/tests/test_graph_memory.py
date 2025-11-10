"""
Teste para verificar o funcionamento do reducer de mensagens limitado.
"""
import asyncio
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from ms_agents_server.src.workflow_agentic.graph import GraphSupervisor


async def test_graph_creation():
    """Testa a criação do grafo com estado limitado."""
    try:
        print("=" * 60)
        print("Teste: Criação do Grafo com Estado Limitado")
        print("=" * 60)
        
        client_id = "test_client_001"
        max_messages = 6
        
        print(f"\n1. Criando grafo para client_id: {client_id}")
        print(f"   Limite de mensagens: {max_messages}")
        
        graph = await GraphSupervisor.analysis_supervisor_graph(
            client_id=client_id,
            max_messages=max_messages
        )
        
        print("\n✅ Grafo criado com sucesso!")
        print(f"   Tipo do grafo: {type(graph)}")
        
        # Testar invocação básica
        print("\n2. Testando invocação com mensagem simples...")
        
        config = {
            "configurable": {
                "thread_id": "test_thread_001"
            }
        }
        
        test_message = "Olá, este é um teste básico."
        
        result = await graph.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": test_message
                    }
                ]
            },
            config=config
        )
        
        print("\n✅ Invocação bem-sucedida!")
        print(f"   Número de mensagens no resultado: {len(result.get('messages', []))}")
        
        return True
        
    except Exception as e:
        print("\n❌ Erro durante o teste:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {str(e)}")
        import traceback
        print("\n📋 Traceback completo:")
        traceback.print_exc()
        return False


async def test_message_limit():
    """Testa o limite de mensagens."""
    try:
        print("\n" + "=" * 60)
        print("Teste: Verificação do Limite de Mensagens")
        print("=" * 60)
        
        client_id = "test_client_002"
        max_messages = 6
        
        graph = await GraphSupervisor.analysis_supervisor_graph(
            client_id=client_id,
            max_messages=max_messages
        )
        
        config = {
            "configurable": {
                "thread_id": "test_thread_002"
            }
        }
        
        # Enviar múltiplas mensagens
        print(f"\n1. Enviando 10 mensagens sequenciais...")
        
        for i in range(1, 11):
            print(f"   Enviando mensagem {i}/10...")
            
            try:
                result = await graph.ainvoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Mensagem de teste número {i}"
                            }
                        ]
                    },
                    config=config
                )
                
                msg_count = len(result.get('messages', []))
                print(f"      ➜ Mensagens no estado: {msg_count}")
                
            except Exception as e:
                print(f"      ❌ Erro na mensagem {i}: {str(e)}")
                raise
        
        print(f"\n✅ Teste de limite concluído!")
        print(f"   Mensagens finais no estado: {msg_count}")
        print(f"   Limite configurado: {max_messages}")
        
        if msg_count <= max_messages:
            print(f"   ✅ Limite respeitado!")
        else:
            print(f"   ⚠️  Limite excedido!")
        
        return True
        
    except Exception as e:
        print("\n❌ Erro durante o teste de limite:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Executa todos os testes."""
    print("\n🧪 Iniciando testes do sistema de memória limitada\n")
    
    # Teste 1: Criação do grafo
    test1_ok = await test_graph_creation()
    
    # Teste 2: Limite de mensagens
    test2_ok = await test_message_limit()
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Teste 1 - Criação do Grafo: {'✅ PASSOU' if test1_ok else '❌ FALHOU'}")
    print(f"Teste 2 - Limite de Mensagens: {'✅ PASSOU' if test2_ok else '❌ FALHOU'}")
    print("=" * 60)
    
    if test1_ok and test2_ok:
        print("\n🎉 Todos os testes passaram!")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
