import streamlit as st
import youtube_utils
import gemini_utils

def main():
    st.set_page_config(page_title="Resumidor de Vídeos", page_icon="▶️")
    st.title("📹 Resumidor de Vídeos do YouTube")
    
    # Input de URL com exemplo
    url = st.text_input("Cole a URL do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Processar") and url:
        try:
            with st.spinner("Analisando vídeo..."):
                # Obtém ID e título
                video_id = youtube_utils.extract_video_id(url)
                if not video_id:
                    st.error("URL inválida")
                    return

                title = youtube_utils.get_video_title(url) or f"Vídeo (ID: {video_id})"
                st.success(f"✅ {title}")

                # Busca transcrição
                transcript, err = youtube_utils.get_video_transcript(video_id)
                if not transcript:
                    st.error(f"❌ Falha na transcrição: {err}")
                    return

                with st.expander("Ver transcrição"):
                    st.write(transcript)

                # Gera resumo
                if st.button("Gerar Resumo"):
                    with st.spinner("Criando resumo..."):
                        if not gemini_utils.configure_gemini():
                            st.error("Erro na API do Gemini")
                            return
                            
                        resumo = gemini_utils.generate_summary(transcript)
                        if resumo:
                            st.subheader("Resumo")
                            st.write(resumo)
                            st.download_button("Baixar", resumo, "resumo.txt")
                        else:
                            st.error("Falha ao gerar resumo")
                            
        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    main()