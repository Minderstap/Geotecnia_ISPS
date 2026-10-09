"""Helpers de LaTeX e campos de entrada com rótulo matemático (PT/EN)."""
import streamlit as st


def get_text(key, lang="pt", **kw):
    from utils.traducoes import get_text as _gt
    return _gt(key, lang, **kw)


def show_formula(key, lang="pt"):
    """Mostra uma fórmula LaTeX (bloco)."""
    st.latex(get_text(key, lang))


def show_labeled_formula(label_key, formula_key, lang="pt"):
    """Mostra um título em negrito seguido da fórmula LaTeX."""
    st.markdown(f"**{get_text(label_key, lang)}**")
    st.latex(get_text(formula_key, lang))


# ---- Fallbacks de rótulos (usados se a chave não existir nas traduções) ----
_ROTULOS = {
    "altura_muro_lbl": ("Altura do muro", "Wall height"),
    "altura_total": ("Altura total", "Total height"),
    "lbl_largura_base": ("Largura da base", "Base width"),
    "lbl_largura_topo": ("Largura do topo", "Top width"),
    "lbl_inclinacao": ("Inclinação do terrapleno", "Backfill slope"),
    "lbl_gamma": ("Peso específico natural", "Natural unit weight"),
    "lbl_gamma_sat": ("Peso específico saturado", "Saturated unit weight"),
    "lbl_phi": ("Ângulo de atrito interno", "Internal friction angle"),
    "lbl_c": ("Coesão efetiva", "Effective cohesion"),
    "lbl_q": ("Sobrecarga no terrapleno", "Backfill surcharge"),
    "lbl_cu": ("Coesão não drenada", "Undrained cohesion"),
    "lbl_delta_b": ("Ângulo de atrito solo-base", "Soil-base friction angle"),
    "nivel_freatico_lbl": ("Altura do Nível Freático a partir da base",
                           "Water table height above base"),
    "lbl_altura_camada": ("Altura da camada", "Layer height"),
}
_UNIDADES = {
    "unidade_m": ("m", "m"),
    "unidade_graus": ("°", "°"),
    "unidade_knm3": ("kN/m³", "kN/m³"),
    "unidade_kpa": ("kPa", "kPa"),
}


def campo_latex(key_lbl, simbolo_latex, key_unidade, key_widget, valor,
                minimo=None, maximo=None, passo=None, lang="pt", sufixo=""):
    """Campo numérico com rótulo visível em LaTeX:
       **Nome** — $simbolo$ [unidade]
    """
    idx = 0 if lang == "pt" else 1
    txt = get_text(key_lbl, lang)
    if txt == key_lbl:                      # chave inexistente -> fallback
        txt = _ROTULOS.get(key_lbl, (key_lbl, key_lbl))[idx]
    uni = get_text(key_unidade, lang)
    if uni == key_unidade:
        uni = _UNIDADES.get(key_unidade, (key_unidade, key_unidade))[idx]
    suf = f" {sufixo}" if sufixo else ""
    # Rótulo visível com matemática inline
    st.markdown(f"**{txt}**{suf} &nbsp;—&nbsp; ${simbolo_latex}$ &nbsp;[{uni}]")
    kwargs = {"value": float(valor), "key": key_widget,
              "label_visibility": "collapsed"}
    if passo is not None:
        kwargs["step"] = float(passo)
    if minimo is not None:
        kwargs["min_value"] = float(minimo)
    if maximo is not None:
        kwargs["max_value"] = float(maximo)
    lbl_plain = f"{txt}{suf} [{uni}]"
    try:
        return st.number_input(lbl_plain, **kwargs)
    except TypeError:                        # Streamlit antigo sem label_visibility
        kwargs.pop("label_visibility", None)
        return st.number_input(lbl_plain, **kwargs)