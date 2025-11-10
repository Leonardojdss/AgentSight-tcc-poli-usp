from fastapi import APIRouter, HTTPException, status
from ms_agents_server.src.usecase.analysis_usecase import ConversationAnalysisHandler
from ms_agents_server.src.data_models.text_input_conversation import TextInput
from ms_agents_server.src.utils.default_messages import FALLBACK_MESSAGE
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/V1/agent_conversation/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Conversa processada com sucesso"},
        400: {"description": "Dados de entrada inválidos"},
        500: {"description": "Erro interno do servidor"},
        503: {"description": "Serviço temporariamente indisponível"}
    }
)
async def agent_conversation_endpoint(data: TextInput) -> Dict[str, str]:
    """
    Endpoint para processar conversas com agentes de IA.
    
    Args:
        data: Dados de entrada contendo message_input e client_id
        
    Returns:
        Dict com a mensagem de resposta do agente
        
    Raises:
        HTTPException: Em caso de erro na validação ou processamento
    """
    
    message = data.message_input
    client_id = data.client_id
    
    # Validação de entrada
    if not message or not message.strip():
        logger.warning(f"Cliente {client_id}: Mensagem vazia recebida")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A mensagem não pode estar vazia"
        )
    
    if not client_id or not client_id.strip():
        logger.warning("Client ID não fornecido")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client ID é obrigatório"
        )
    
    logger.info(f"Cliente {client_id}: Processando mensagem de entrada")
    
    try:
        result = await ConversationAnalysisHandler.conversation_analysis_usecase(
            input_message=message,
            client_id=client_id
        )
        
        if not result:
            logger.error(f"Cliente {client_id}: Resultado vazio do handler")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar a conversa: resposta vazia"
            )
        
        logger.info(f"Cliente {client_id}: Conversa processada com sucesso")
        return {"message": result}
        
    except ValueError as value_error:
        logger.error(f"Cliente {client_id}: Erro de validação - {str(value_error)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de validação: {str(value_error)}"
        )
        
    except ConnectionError as ce:
        # Erros de conexão com serviços externos (OpenAI, PostgreSQL, etc)
        logger.error(f"Cliente {client_id}: Erro de conexão - {str(ce)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço temporariamente indisponível. Tente novamente em alguns instantes."
        )
        
    except TimeoutError as te:
        # Timeout em operações
        logger.error(f"Cliente {client_id}: Timeout - {str(te)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Tempo limite excedido ao processar a requisição"
        )
        
    except Exception as error:
        # Erros gerais
        logger.exception(
            f"Cliente {client_id}: Erro inesperado ao processar conversa",
            exc_info=error
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=FALLBACK_MESSAGE
        )