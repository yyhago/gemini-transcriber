import re
import requests
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> str | None:
    """Extrai ID do vídeo de URLs do YouTube."""
    if not url:
        return None
        
    url = url.strip()
    
    # Verifica se já é um ID válido
    if re.fullmatch(r'[\w-]{11}', url):
        return url
    
    try:
        parsed = urlparse(url)
        
        # URLs encurtadas (youtu.be)
        if 'youtu.be' in parsed.netloc:
            return parsed.path[1:] if len(parsed.path) > 1 else None
            
        # URLs padrão do YouTube
        if 'youtube.com' in parsed.netloc:
            if parsed.path == '/watch':
                return parse_qs(parsed.query).get('v', [None])[0]
            for prefix in ('/embed/', '/v/', '/live/', '/shorts/'):
                if parsed.path.startswith(prefix):
                    return parsed.path.split('/')[2]
                    
        match = re.search(r'(?:v=|youtu\.be\/|embed\/)([\w-]{11})', url)
        return match.group(1) if match else None
        
    except Exception:
        logger.exception("Falha ao extrair ID do vídeo")
        return None

def get_video_title(video_id: str) -> str | None:
    """Obtém título do vídeo usando a API oEmbed."""
    try:
        response = requests.get(
            f"https://www.youtube.com/oembed?url=https://youtube.com/watch?v={video_id}",
            timeout=10
        )
        return response.json().get('title') if response.ok else None
    except Exception:
        return None

def get_video_transcript(video_id: str) -> tuple[str | None, Exception | None]:
    """Obtém transcrição com suporte a múltiplos idiomas."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            return ' '.join(t['text'] for t in transcript), None
        except Exception as e:
            return None, e
            
    except ImportError:
        return None, ImportError("Instale youtube-transcript-api")