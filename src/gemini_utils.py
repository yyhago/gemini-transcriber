import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Configuração básica
load_dotenv()
logger = logging.getLogger(__name__)

def configure_gemini() -> bool:
    """Configura API do Gemini e valida conexão."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("Chave da API não encontrada no arquivo .env")
            return False
            
        genai.configure(api_key=api_key)
        # Testa conexão com um prompt simples
        model = genai.GenerativeModel('gemini-pro')
        model.generate_content("Teste de conexão")
        return True
        
    except Exception as e:
        logger.error(f"Erro na configuração do Gemini: {str(e)}")
        return False

def generate_summary(text: str, prompt: str = None) -> str:
    """Gera resumo do texto usando Gemini com prompt otimizado."""
    try:
        prompt = prompt or """
        Crie um resumo detalhado em português com os pontos principais do vídeo.
        Inclua tópicos importantes e conclusões quando aplicável.
        Formate a resposta em parágrafos bem estruturados.
        """
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{prompt}\n\nTexto para resumir:\n{text}")
        return response.text or ""
        
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {str(e)}")
        return ""