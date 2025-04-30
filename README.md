# 📹 YouTube Video Summarizer

Uma base de um sistema que extrai transcrições de vídeos do YouTube e gera resumos concisos usando a API do Gemini AI.

## 🚀 Funcionalidades

* 📝 Extrai o conteúdo de vídeos no YouTube gerando transcrições automáticas (legendas) em português ou inglês 
* ✨ Gera resumos inteligentes usando o modelo Gemini Pro
* 🎯 Interface simples e intuitiva com Streamlit

## ⚙️ Pré-requisitos

* Python 3.10+
* Conta no Google AI Studio (para obter a API key do Gemini)
* Conexão com internet

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/yyhago/gemini-chatbot.git
cd gemini-chatbot
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com sua API key:
```env
GEMINI_API_KEY=sua_chave_aqui
```

## 🖥️ Como Usar

1. Execute o aplicativo:
```bash
streamlit run src/main.py
```

2. No navegador, cole a URL de um vídeo do YouTube
3. Clique em "Processar" para obter a transcrição
4. Clique em "Gerar Resumo" para criar um resumo com IA

## 🧩 Estrutura do Projeto

```
gemini-chatbot/
├── src/
│   ├── main.py            # Aplicativo principal (Streamlit)
│   ├── youtube_utils.py   # Funções para processar vídeos
│   └── gemini_utils.py    # Integração com a API Gemini
├── .env                   # Configurações sensíveis
├── requirements.txt       # Dependências
└── README.md              # Documentação
```

**Dica:** Para obter uma API key do Gemini, acesse: [Google AI Studio](https://aistudio.google.com/)