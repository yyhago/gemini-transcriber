import streamlit as st
import youtube_utils
import gemini_utils
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🎬 Resumidor Inteligente de Vídeos",
    page_icon="📹",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #FF4E50 0%, #F9D423 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .header h1 {
        margin: 0;
        font-size: 2.3rem;
        font-weight: 800;
    }
    .stTextInput>div>div>input {
        padding: 12px !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF4E50 0%, #F9D423 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 78, 80, 0.3);
    }
    .stExpander {
        border-radius: 10px !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #38a169;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class='header'>
        <h1>🎬 Resumidor Inteligente de Vídeos</h1>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("video_form"):
        url = st.text_input(
            "Cole a URL do vídeo do YouTube:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Exemplo: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        
        submitted = st.form_submit_button(
            "🔍 Analisar Vídeo",
            use_container_width=True
        )
    
    if submitted and url:
        try:
            with st.spinner("🔍 Analisando vídeo..."):
                video_id = youtube_utils.extract_video_id(url)
                if not video_id:
                    st.error("❌ URL inválida ou vídeo não encontrado")
                    return

                title = youtube_utils.get_video_title(video_id) or f"Vídeo (ID: {video_id})"
                
                st.markdown(f"""
                <div class='success-box'>
                    <h3>🎥 {title}</h3>
                    <p>ID do vídeo: <code>{video_id}</code></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Busca transcrição
                transcript, err = youtube_utils.get_video_transcript(video_id)
                if not transcript:
                    st.error(f"❌ Não foi possível obter a transcrição: {err}")
                    return

                with st.expander("📝 Ver Transcrição Completa", expanded=False):
                    st.write(transcript)
                
                # Gera resumo
                if st.button(
                    "✨ Gerar Resumo", 
                    use_container_width=True,
                    type="primary"
                ):
                    with st.spinner("🧠 Criando resumo inteligente..."):
                        if not gemini_utils.configure_gemini():
                            st.error("🔌 Erro na conexão com a API do Gemini")
                            return
                            
                        resumo = gemini_utils.generate_summary(transcript)
                        if resumo:
                            st.subheader("📌 Resumo do Vídeo")
                            st.markdown("---")
                            st.write(resumo)
                            
                            # Botão de download com timestamp
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            st.download_button(
                                label="⬇️ Baixar Resumo",
                                data=resumo,
                                file_name=f"resumo_{video_id}_{timestamp}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        else:
                            st.error("❌ Falha ao gerar o resumo")
                            
        except Exception as e:
            st.error(f"⚠️ Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()