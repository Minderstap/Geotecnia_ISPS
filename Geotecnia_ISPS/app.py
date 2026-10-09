import streamlit as st
import webbrowser
import os
import base64

# Importar o sistema de traduções
from utils.traducoes import get_text

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Geotecnia ISPS - HYDRAULIC-GEOSTRUCT",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://wa.me/258873846242',
        'Report a bug': "https://wa.me/258873846242",
        'About': "# HYDRAULIC-GEOSTRUCT (GRUPO III)\nInstituto Superior Politécnico de Songo"
    }
)

# --- INICIALIZAÇÃO DO ESTADO (MEMÓRIA DA APP) ---
if "logado" not in st.session_state:
    st.session_state.logado = False
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "genero" not in st.session_state:
    st.session_state.genero = ""
if "curso" not in st.session_state:
    st.session_state.curso = ""
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "capa"
if "language" not in st.session_state:
    st.session_state.language = "pt"

# --- FUNÇÕES DOS ATALHOS ---
def ir_para_home():
    st.session_state.logado = False
    st.session_state.pagina_atual = "capa"
    st.rerun()

def abrir_guia():
    lang = st.session_state.language
    st.info(get_text("guiao_uso", lang))

def abrir_suporte():
    url_whatsapp = "https://wa.me/258873846242?text=Olá!%20Preciso%20de%20suporte%20com%20a%20folha%20de%20cálculo%20do%20Grupo%20III."
    webbrowser.open(url_whatsapp)

# --- BARRA LATERAL (ATALHOS E CONFIGURAÇÕES) ---
with st.sidebar:
    # Seletor de Idioma (Melhor prática no Streamlit para mudança global)
    lang_options = {"🇵🇹 Português": "pt", "🇬🇧 English": "en"}
    lang_labels = list(lang_options.keys())
    current_lang_label = [k for k, v in lang_options.items() if v == st.session_state.language][0]
    
    selected_lang_label = st.selectbox("🌐 Language / Idioma", lang_labels, index=lang_labels.index(current_lang_label))
    st.session_state.language = lang_options[selected_lang_label]
    lang = st.session_state.language
    
    st.divider()
    st.title("⚙️ Menu")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("pag_inicial", lang), use_container_width=True):
            ir_para_home()
    with col2:
        if st.button(get_text("guiao_uso", lang), use_container_width=True):
            abrir_guia()
            
    if st.button(get_text("suporte", lang), use_container_width=True, type="primary"):
        abrir_suporte()
        
    st.divider()
    st.caption("© 2026 HYDRAULIC-GEOSTRUCT (GRUPO III)")
    st.caption("Instituto Superior Politécnico de Songo")


# --- LÓGICA DAS PÁGINAS ---
lang = st.session_state.language

# 1. PÁGINA DA CAPA E CAIXA DE ENTRADA
if st.session_state.pagina_atual == "capa":
    
    # Logo do ISPS CENTRALIZADO usando HTML
    logo_path = "assets/Picture1.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{encoded_string}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Logo não encontrado. Verifica o caminho: " + logo_path)
    
    # Títulos com Tradução
    st.markdown(f"<h1 style='text-align: center; color: #2E86AB;'>{get_text('titulo_instituto', lang)}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #A23B72;'>{get_text('titulo_grupo', lang)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #F18F01;'>{get_text('titulo_disciplina', lang)}</h3>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown(f"### {get_text('caixa_entrada', lang)}")
    
    with st.form("form_login"):
        nome = st.text_input(get_text("nome", lang))
        curso = st.text_input(get_text("curso", lang), placeholder="Ex: Engenharia Hidráulica")
        genero = st.radio(get_text("genero", lang), [get_text("masculino", lang), get_text("feminino", lang)], horizontal=True)
        
        submitted = st.form_submit_button(get_text("entrar", lang), use_container_width=True)
        
        if submitted:
            if nome and curso:
                st.session_state.nome = nome
                st.session_state.curso = curso
                st.session_state.genero = "Masculino" if genero == get_text("masculino", lang) else "Feminino"
                st.session_state.logado = True
                st.session_state.pagina_atual = "menu_escolha"
                st.rerun()
            else:
                st.error("⚠️ Por favor, preencha o Nome e o Curso para continuar. / Please fill in Name and Course.")

# 2. PAINEL DE BOAS-VINDAS E ESCOLHA DA ESTRUTURA
elif st.session_state.pagina_atual == "menu_escolha":
    titulo_genero = get_text("senhor", lang) if st.session_state.genero == "Masculino" else get_text("senhora", lang)
    
    st.markdown(f"### {get_text('bem_vindo', lang)}, {titulo_genero} {st.session_state.nome}! 👋")
    st.markdown(f"*{get_text('curso', lang)}: {st.session_state.curso}*")
    st.divider()
    
    st.markdown(f"### 🏗️ {get_text('que_estrutura', lang)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Opção 1")
        if st.button(f"🧱 {get_text('muros_contencao', lang)}", use_container_width=True, type="primary"):
            st.session_state.pagina_atual = "muros"
            st.rerun()
        st.markdown(f"*{get_text('gravidade', lang)}, {get_text('consola', lang)} e {get_text('contrafortes', lang)}*")
        
    with col2:
        st.markdown("#### Opção 2")
        if st.button(f"📐 {get_text('sapatas_rigidas', lang)}", use_container_width=True, type="primary"):
            st.session_state.pagina_atual = "sapatas"
            st.rerun()
        st.markdown(f"*{get_text('fundações_superficiais', lang)}*")

# 3. MÓDULO DE MUROS DE CONTENÇÃO (FASE 2 ATIVA)
elif st.session_state.pagina_atual == "muros":
    from paginas import muros
    muros.mostrar()

# 4. PLACEHOLDER PARA SAPATAS (FASE 3 - A DESENVOLVER)
elif st.session_state.pagina_atual == "sapatas":
    from paginas import sapatas
    sapatas.mostrar()