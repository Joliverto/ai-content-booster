import os
from dotenv import load_dotenv
import streamlit as st

# --- NOVO: Google Gemini ---
import google.generativeai as genai

# Carrega variáveis do .env
load_dotenv()

# Configura a API do Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY não encontrada. Defina no seu .env (GOOGLE_API_KEY=...)."
    )
genai.configure(api_key=GOOGLE_API_KEY)

# Escolha do modelo (gratuito/rápido)
MODEL_NAME = "gemini-1.5-flash"

# Parâmetros de geração (opcional)
GEN_CFG = {
    "temperature": 0.8,     # criatividade
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1200,
}

# Função para gerar conteúdo com IA (usando Gemini)
def generate_content(product_name, niche, target_audience, benefits):
    prompt = (
        f"Gere 5 posts criativos para redes sociais promovendo o produto '{product_name}' "
        f"no nicho '{niche}', para o público '{target_audience}'. "
        f"Inclua benefícios como '{benefits}', gatilhos mentais, emojis, hashtags e um call-to-action. "
        f"Torne-os variados para Instagram, TikTok e X. "
        f"Adicione um disclaimer: 'Gerado por IA'. "
        f"Formate como lista numerada clara, separando cada post com uma linha em branco."
    )

    model = genai.GenerativeModel(MODEL_NAME)

    # Você pode usar safety_settings se quiser relaxar/bloquear categorias — default já é ok.
    # Exemplo: safety_settings=[{"category": "HARM_CATEGORY_UNSPECIFIED", "threshold": "BLOCK_NONE"}]

    resp = model.generate_content(
        prompt,
        generation_config=GEN_CFG,
    )

    # A resposta de texto fica em .text
    return resp.text

# -------------- UI Streamlit --------------
st.title("AI Content Booster")
st.write("Uma ferramenta simples para afiliados gerarem posts personalizados com IA (Gemini).")

product_name = st.text_input("Nome do Produto (ex: Curso de Finanças Pessoais)")
niche = st.text_input("Nicho (ex: Finanças Pessoais)")
target_audience = st.text_input("Público-Alvo (ex: Iniciantes em Investimentos)")
benefits = st.text_area("Benefícios Principais (ex: Aprenda a investir sem riscos)")

if st.button("Gerar Posts"):
    if product_name and niche and target_audience and benefits:
        with st.spinner("Gerando conteúdo com IA (Gemini)..."):
            try:
                content = generate_content(product_name, niche, target_audience, benefits)
                st.success("Posts Gerados!")
                st.text_area("Conteúdo Gerado:", content, height=350)
            except Exception as e:
                st.error(f"Erro ao gerar conteúdo: {e}")
    else:
        st.error("Preencha todos os campos!")

st.write("Disclaimer: Este é um protótipo. Verifique o conteúdo gerado manualmente para evitar erros.")
