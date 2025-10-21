import os
from dotenv import load_dotenv
import streamlit as st
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
MODEL_NAME = "gemini-2.5-flash"

# Parâmetros de geração (opcional)
GEN_CFG = {
    "temperature": 0.8,     # criatividade
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1200,
}

# --- Função segura para extrair texto da resposta ---
def _safe_extract_text_from_response(resp):
    """
    Extrai texto de resp de forma segura. Retorna string com diagnóstico
    se não encontrar texto (evita o erro do .text quando não há Part).
    """
    try:
        # 1) Tenta a forma robusta: candidates -> content -> parts -> text
        if getattr(resp, "candidates", None):
            cand = resp.candidates[0]
            content = getattr(cand, "content", None)
            if content and getattr(content, "parts", None):
                part = content.parts[0]
                if getattr(part, "text", None):
                    return part.text

        # 2) Fallback para o atalho .text (se disponível)
        if getattr(resp, "text", None):
            return resp.text

    except Exception:
        # qualquer erro ao navegar na estrutura, cai no fallback abaixo
        pass

    # 3) Se nada deu certo, retorna mensagem amigável com diagnóstico resumido
    finish = None
    try:
        finish = resp.candidates[0].finish_reason
    except Exception:
        finish = "unknown"

    diag = (
        "⚠️ O modelo retornou sem partes de texto válidas.\n"
        f"finish_reason: {finish}\n"
        "Tente novamente (ou escolha outro modelo)."
    )
    return diag


# --- Função generate_content (mínima alteração) ---
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

    resp = model.generate_content(
        prompt,
        generation_config=GEN_CFG,
    )

    # Substitui o uso direto de resp.text por extração segura
    return _safe_extract_text_from_response(resp)

# -------------- UI Streamlit --------------
st.title("AI Content Booster I")
st.write("Uma ferramenta simples para afiliados gerarem posts personalizados com IA (Gemini).")
st.markdown(
    """
    **Protótipo criado por João de Oliveira Neto**  
    [🌐 LinkedIn](https://www.linkedin.com/in/joao-neto-0962b0247) | [💻 GitHub](https://github.com/Joliverto)
    """
)

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

#for m in genai.list_models():
    #print(m.name)
