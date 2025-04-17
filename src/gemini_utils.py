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
            raise ValueError("Chave da API não encontrada")
            
        genai.configure(api_key=api_key)
        genai.GenerativeModel('gemini-pro')  # Testa conexão
        return True
        
    except Exception as e:
        logger.error(f"Erro na configuração: {e}")
        return False

def generate_summary(text: str, prompt: str = None) -> str:
    """Gera resumo do texto usando Gemini."""
    try:
        prompt = prompt or "Resuma em português os pontos principais:"
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{prompt}\n{text}")
        return response.text or ""
        
    except Exception as e:
        logger.error(f"Erro ao gerar resumo: {e}")
        return ""