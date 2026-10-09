"""Carregamento robusto de imagens — funciona local e no Streamlit Cloud."""
import os
import base64


# Raiz do projeto = pasta acima de `utils/`
_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def caminho_asset(caminho_relativo):
    """Devolve o caminho absoluto para um ficheiro dentro do projeto."""
    # Aceita tanto "assets/Picture1.png" como "Picture1.png"
    candidatos = [
        os.path.join(_RAIZ, caminho_relativo),
        os.path.join(_RAIZ, "assets", os.path.basename(caminho_relativo)),
        os.path.join(_RAIZ, "assets", caminho_relativo),
    ]
    for c in candidatos:
        if os.path.isfile(c):
            return c
    return None


def img_base64_html(caminho_relativo, width=None, estilo_extra=""):
    """Devolve HTML <img> com a imagem embutida em base64.

    Uso:
        st.markdown(img_base64_html("assets/Picture1.png", width=200),
                    unsafe_allow_html=True)
    """
    caminho = caminho_asset(caminho_relativo)
    if not caminho:
        return (f'<p style="color:red;text-align:center;">'
                f'⚠️ Imagem não encontrada: {caminho_relativo}</p>')

    with open(caminho, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    ext = caminho.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png",
            "svg": "svg+xml", "gif": "gif", "webp": "webp"}.get(ext, ext)

    w_attr = f' width="{width}"' if width else ""
    return (f'<div style="text-align:center;margin:20px 0;">'
            f'<img src="data:image/{mime};base64,{encoded}"{w_attr} '
            f'style="max-width:100%;border-radius:8px;display:inline-block;'
            f'box-shadow:0 2px 8px rgba(0,0,0,0.1);{estilo_extra}">'
            f'</div>')