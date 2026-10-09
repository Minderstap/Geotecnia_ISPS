import streamlit as st
import math
from calculos import relatorios
from utils.traducoes import get_text
from utils.latex_helper import show_labeled_formula, show_formula, campo_latex


def carregar_imagem_local(caminho, width=None):
    from utils.imagens import img_base64_html
    return img_base64_html(caminho, width=width)


def calcular_phi_d(phi_graus, gamma_phi):
    if gamma_phi == 0:
        return phi_graus
    phi_rad = math.radians(phi_graus)
    return math.degrees(math.atan(math.tan(phi_rad) / gamma_phi))


def calcular_delta_d(delta_graus, gamma_phi):
    if delta_graus == 0 or gamma_phi == 0:
        return 0.0
    delta_rad = math.radians(delta_graus)
    return math.degrees(math.atan(math.tan(delta_rad) / gamma_phi))


def calcular_Ka_Rankine(phi_d_rad, i_rad):
    if i_rad == 0:
        return (1 - math.sin(phi_d_rad)) / (1 + math.sin(phi_d_rad))
    cos_i = math.cos(i_rad)
    cos_phi = math.cos(phi_d_rad)
    disc = max(0, cos_i ** 2 - cos_phi ** 2)
    num = cos_i * (cos_i - math.sqrt(disc))
    den = cos_i * (cos_i + math.sqrt(disc))
    return num / den if den > 0 else 0


def calcular_Ka_Coulomb_slide48(phi_d_rad, delta_d_rad, i_rad, alpha_rad=0):
    """Coulomb / Müller-Breslau (CAP2.0 pág. 48) com paramento VERTICAL: β = 90°."""
    beta = math.radians(90.0)
    num = math.sin(beta + phi_d_rad) ** 2
    raiz = math.sqrt(max(0.0,
                         (math.sin(phi_d_rad + delta_d_rad) * math.sin(phi_d_rad - i_rad)) /
                         (math.sin(beta - delta_d_rad) * math.sin(beta + i_rad))))
    den = (math.sin(beta) ** 2) * math.sin(beta - delta_d_rad) * (1 + raiz) ** 2
    return num / den if den > 0 else 0


def calcular_componentes_impulso(Ia_d, delta_d_rad, i_rad, metodo, alpha_rad=0):
    if metodo == "Rankine":
        angulo_impulso = i_rad
    else:
        angulo_impulso = delta_d_rad + alpha_rad
    IaH_d = Ia_d * math.cos(angulo_impulso)
    IaV_d = Ia_d * math.sin(angulo_impulso)
    return IaH_d, IaV_d


def detalhar_capacidade_carga(phi_fund_d_rad, c_fund_d, gamma_fund, B_linha, q_solo_fund, g_Rv):
    """Capacidade de carga de Meyerhof (1963) com tabela + interpolacao."""
    from calculos.meyerhof_tabela import meyerhof_N
    phi_deg = math.degrees(phi_fund_d_rad)
    Nc, Nq, Ngamma = meyerhof_N(phi_deg)
    termo_c = c_fund_d * Nc
    termo_q = q_solo_fund * Nq
    termo_gamma = 0.5 * gamma_fund * B_linha * Ngamma
    q_ult = termo_c + termo_q + termo_gamma
    q_Rd = q_ult / g_Rv
    return q_Rd, Nc, Nq, Ngamma, termo_c, termo_q, termo_gamma, q_ult


# ============================================================
# ESQUEMA FINAL (SVG) — água RECTA/VERTICAL, símbolos matemáticos,
# rótulos sem sobreposição
# ============================================================
def _svg_esquema_muro_gravidade(H, B, a, i, gamma_sol, gamma_sat, phi, c_linha, q, z_w,
                                tipo_solo, H1=None, H2=None, gamma1=None, gamma2=None,
                                gamma1_sat=None, gamma2_sat=None, phi1=None, phi2=None,
                                Ka=None, Ka1=None, Ka2=None, IaH_d=None, U_d=None, W_d=None,
                                lang="pt", gamma_fund=None, phi_fund=None, c_fund=None):
    gamma_w = 9.81
    t = lambda pt, en: pt if lang == "pt" else en
    W_svg, y_base = 980, 470
    esc = min(340.0 / max(H, 0.1), 300.0 / max(B, 0.1))
    tan_i = math.tan(math.radians(i))
    x_esq = 150.0
    x_dir = x_esq + B * esc
    x_topo_esq = x_dir - a * esc
    y_topo = y_base - H * esc
    x_solo_dir = W_svg - 25.0
    y_g_dir = max(40.0, y_topo - (x_solo_dir - x_dir) * tan_i)
    zt = (H - z_w) if z_w > 0 else None
    y_nf = (y_base - z_w * esc) if z_w > 0 else None
    cor_betao, cor_agua = "#b0b0b0", "#2980b9"
    cor_solo, cor_solo2 = "#d2b48c", "#a0826d"
    cor_eff, cor_sub = "#c0392b", "#2471a3"
    fund_dif = (gamma_fund is not None) and (
        abs(gamma_fund - gamma_sol) > 0.01 or abs((phi_fund or phi) - phi) > 0.01)
    cor_fund = "#8a6a4f" if fund_dif else "#c9a876"

    def lbl(x, y, txt, size=10, cor="#222", anchor="start", bold=True, halo="#fdfefe"):
        w = ' font-weight="bold"' if bold else ''
        h = (f' stroke="{halo}" stroke-width="3" stroke-linejoin="round" paint-order="stroke"'
             if halo else '')
        return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
                f'fill="{cor}"{w}{h} font-family="Georgia, Times New Roman, serif">{txt}</text>')

    def dim_h(x1, x2, y, label, cor="#1f77b4", size=10):
        return (f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{cor}" '
                f'stroke-width="1.1" marker-start="url(#gHB)" marker-end="url(#gHB)"/>'
                + lbl((x1 + x2) / 2.0, y - 5, label, size, cor, "middle"))

    def dim_v(y1, y2, x, label, cor="#1f77b4", size=10, side=-1):
        return (f'<line x1="{x}" y1="{y1:.1f}" x2="{x}" y2="{y2:.1f}" stroke="{cor}" '
                f'stroke-width="1.1" marker-start="url(#gVB)" marker-end="url(#gVB)"/>'
                + lbl(x - 6, (y1 + y2) / 2.0 + 4, label, size, cor, "end"))

    # ---- tensões verticais EFECTIVAS (corrigido p/ estratificados com N.A.) ----
    def sigma_v(z):
        if tipo_solo == "unico":
            if zt is None or z <= zt:
                return gamma_sol * z
            return gamma_sol * zt + (gamma_sat - gamma_w) * (z - zt)
        g1, g1s, g2, g2s = gamma1, gamma1_sat, gamma2, gamma2_sat
        if z <= H1:
            if zt is None or z <= zt:
                return g1 * z
            return g1 * zt + (g1s - gamma_w) * (z - zt)
        if zt is None:
            return g1 * H1 + g2 * (z - H1)
        if zt <= H1:
            sv1 = g1 * zt + (g1s - gamma_w) * (H1 - zt)
            return sv1 + (g2s - gamma_w) * (z - H1)
        sv1 = g1 * H1
        return sv1 + g2 * (zt - H1) + (g2s - gamma_w) * (z - zt)

    def ka_de(z):
        if tipo_solo == "unico":
            return Ka
        return Ka1 if z <= H1 else Ka2

    def p_eff(z):
        return ka_de(z) * (q + sigma_v(z))

    def p_agua(z):
        return gamma_w * max(0.0, z - zt) if zt is not None else 0.0

    p_sc = 130.0 / max(p_eff(H) + p_agua(H), 1e-6)

    svg = []
    svg.append(f'<svg width="{W_svg}" height="600" viewBox="0 0 {W_svg} 600" '
               f'xmlns="http://www.w3.org/2000/svg" '
               f'style="background:#fdfefe;border:1px solid #bbb;border-radius:8px;">')
    svg.append('<defs>'
               '<marker id="gHB" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto-start-reverse"><polygon points="7,0 7,6 0,3" fill="#1f77b4"/></marker>'
               '<marker id="gVB" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto-start-reverse"><polygon points="7,0 7,6 0,3" fill="#1f77b4"/></marker>'
               '</defs>')
    svg.append(f'<text x="{W_svg/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">'
               f'ESQUEMA FINAL — MURO DE GRAVIDADE '
               f'({t("Solo Único","Single Soil") if tipo_solo=="unico" else t("Solos Estratificados","Stratified Soils")})</text>')
    svg.append(f'<rect x="25" y="{y_base}" width="{W_svg-50}" height="58" fill="{cor_fund}" stroke="#6b4a2f"/>')
    svg.append(lbl(32, y_base + 35, t("SOLO DE FUNDAÇÃO", "FOUNDATION SOIL") +
                   (f': γ = {gamma_fund:.1f} | φ′ = {phi_fund:.0f}°' if gamma_fund else ''),
                   10, "#ffffff", halo=cor_fund))
    if tipo_solo == "unico":
        poly = f'{x_dir},{y_topo} {x_solo_dir},{y_g_dir} {x_solo_dir},{y_base} {x_dir},{y_base}'
        svg.append(f'<polygon points="{poly}" fill="{cor_solo}" stroke="#8b6f47"/>')
    else:
        y_int = y_topo + H1 * esc
        svg.append(f'<polygon points="{x_dir},{y_topo} {x_solo_dir},{y_g_dir} {x_solo_dir},{y_int} {x_dir},{y_int}" fill="{cor_solo}" stroke="#8b6f47"/>')
        svg.append(f'<polygon points="{x_dir},{y_int} {x_solo_dir},{y_int} {x_solo_dir},{y_base} {x_dir},{y_base}" fill="{cor_solo2}" stroke="#6b4a2f"/>')
    if y_nf is not None:
        svg.append(f'<polygon points="{x_dir},{y_nf} {x_solo_dir},{y_nf} {x_solo_dir},{y_base} {x_dir},{y_base}" fill="rgba(41,128,185,0.22)"/>')
        svg.append(f'<line x1="{x_dir}" y1="{y_nf}" x2="{x_solo_dir}" y2="{y_nf}" stroke="{cor_agua}" stroke-width="2" stroke-dasharray="7,4"/>')
    svg.append(f'<polygon points="{x_esq},{y_base} {x_topo_esq},{y_topo} {x_dir},{y_topo} {x_dir},{y_base}" fill="{cor_betao}" stroke="#333" stroke-width="2"/>')
    svg.append(lbl((x_esq + x_dir) / 2.0, (y_base + y_topo) / 2.0, "BETÃO", 11, "#333", "middle", halo="#d0d0d0"))
    # ---- rótulos de solo / γ′ ----
    if tipo_solo == "unico":
        y_mc = (y_topo + (y_nf if y_nf else y_base)) / 2.0
        svg.append(lbl(x_solo_dir - 8, y_mc, f'γ = {gamma_sol:.1f} kN/m³ · φ′ = {phi:.0f}° · c′ = {c_linha:.1f} kPa', 10, "#5d4a2f", "end"))
        if y_nf is not None:
            svg.append(lbl(x_solo_dir - 8, (y_nf + y_base) / 2.0,
                           f'γ′ = γ_sat − γ_w = {gamma_sat - gamma_w:.2f} kN/m³', 10, "#1a5276", "end"))
            svg.append(lbl(x_solo_dir - 8, y_nf - 6, f'N.F. (z_w = {z_w:.2f} m)', 10, cor_agua, "end"))
    else:
        y_int = y_topo + H1 * esc
        svg.append(lbl(x_solo_dir - 8, (y_topo + y_int) / 2.0,
                       f'Camada 1: γ₁ = {gamma1:.1f} | φ′₁ = {phi1:.0f}°', 10, "#5d4a2f", "end"))
        svg.append(lbl(x_solo_dir - 8, (y_int + (y_nf if y_nf else y_base)) / 2.0,
                       f'Camada 2: γ₂ = {gamma2:.1f} | φ′₂ = {phi2:.0f}°', 10, "#3d2a1f", "end"))
        if y_nf is not None:
            gsub = (gamma1_sat if y_nf < y_int else gamma2_sat) - gamma_w
            svg.append(lbl(x_solo_dir - 8, (y_nf + y_base) / 2.0,
                           f'γ′ = γ_sat − γ_w = {gsub:.2f} kN/m³', 10, "#1a5276", "end"))
            svg.append(lbl(x_solo_dir - 8, y_nf - 6, f'N.F. (z_w = {z_w:.2f} m)', 10, cor_agua, "end"))
    # ---- sobrecarga ----
    if q > 0:
        x = x_dir + 20
        while x < x_solo_dir - 10:
            yg = max(40.0, y_topo - (x - x_dir) * tan_i)
            svg.append(f'<line x1="{x}" y1="{yg-30}" x2="{x}" y2="{yg-6}" stroke="#1f77b4" stroke-width="1.6"/>')
            svg.append(f'<polygon points="{x},{yg-4} {x-3.5},{yg-12} {x+3.5},{yg-12}" fill="#1f77b4"/>')
            x += 55
        svg.append(lbl(x_dir + 20, y_topo - 38, f'q = {q:.1f} kPa', 10, "#1f77b4"))
    # ---- amostras do diagrama de terras (com salto em H1 se estratificado) ----
    pts = []
    if tipo_solo == "estratificado" and H1 is not None and 0 < H1 < H:
        for k in range(17):
            pts.append((H1 * k / 16, Ka1))
        pts.append((H1, Ka2))
        for k in range(1, 21):
            pts.append((H1 + (H - H1) * k / 20, Ka2))
    else:
        for k in range(37):
            pts.append((H * k / 36, Ka))
    pts_eff = []
    for z, ka in pts:
        y = y_topo + (y_base - y_topo) * (z / H)
        pts_eff.append((x_dir + ka * (q + sigma_v(z)) * p_sc, y))
    # ---- BANDA 1: diagrama de TERRAS (efectivo), a partir da face ----
    poly_eff = " ".join(f"{xx:.1f},{yy:.1f}" for xx, yy in [(x_dir, y_topo)] + pts_eff + [(x_dir, y_base)])
    svg.append(f'<polygon points="{poly_eff}" fill="rgba(192,57,43,0.18)" stroke="{cor_eff}" stroke-width="1.5"/>')
    for k in range(1, 8):
        z = H * k / 8
        y = y_topo + (y_base - y_topo) * k / 8
        e = p_eff(z) * p_sc
        svg.append(f'<line x1="{x_dir+e:.1f}" y1="{y:.1f}" x2="{x_dir+3:.1f}" y2="{y:.1f}" stroke="{cor_eff}" stroke-width="1.4"/>')
        svg.append(f'<polygon points="{x_dir+2:.1f},{y:.1f} {x_dir+10:.1f},{y-3:.1f} {x_dir+10:.1f},{y+3:.1f}" fill="{cor_eff}"/>')
    svg.append(lbl(x_dir + 16, y_topo + 16, t("Impulso activo (efectivo)", "Active pressure (effective)"), 10, cor_eff))
    if IaH_d is not None:
        svg.append(lbl(x_dir + 16, y_topo + 30, f'I_aH,d = {IaH_d:.2f} kN/m', 10, cor_eff))
    # ---- BANDA 2: diagrama da ÁGUA, empilhado À DIREITA da banda de terras ----
    if y_nf is not None and z_w > 0:
        u_base = gamma_w * z_w
        u_px = u_base * p_sc
        e_max = max(p_eff(H), p_eff(zt) if zt is not None else 0.0) * p_sc
        x_w0 = x_dir + e_max + 26.0     # referência própria, sem tocar no diagrama de terras
        # triângulo rectângulo: cateto vertical (N.A -> base), cateto horizontal (base), hipotenusa
        svg.append(f'<polygon points="{x_w0:.1f},{y_nf:.1f} {x_w0:.1f},{y_base:.1f} '
                   f'{x_w0 + u_px:.1f},{y_base:.1f}" fill="rgba(41,128,185,0.30)" '
                   f'stroke="{cor_agua}" stroke-width="1.6"/>')
        # cateto vertical tracejado (linha de referência do diagrama)
        svg.append(f'<line x1="{x_w0:.1f}" y1="{y_nf:.1f}" x2="{x_w0:.1f}" y2="{y_base:.1f}" '
                   f'stroke="{cor_agua}" stroke-width="1.8" stroke-dasharray="6,3"/>')
        # setas horizontais: u cresce linearmente com a profundidade
        n_w = 6
        for k in range(1, n_w + 1):
            frac = k / float(n_w)
            yy = y_nf + (y_base - y_nf) * frac
            uu = u_px * frac
            if uu > 3:
                svg.append(f'<line x1="{x_w0 + uu:.1f}" y1="{yy:.1f}" x2="{x_w0 + 3:.1f}" y2="{yy:.1f}" '
                           f'stroke="{cor_agua}" stroke-width="1.3"/>')
                svg.append(f'<polygon points="{x_w0 + 2:.1f},{yy:.1f} {x_w0 + 10:.1f},{yy - 3.2:.1f} '
                           f'{x_w0 + 10:.1f},{yy + 3.2:.1f}" fill="{cor_agua}"/>')
        # rótulos
        svg.append(lbl(x_w0 + u_px / 2.0, y_nf - 24,
                       t("Diagrama da água (isolado)", "Water diagram (isolated)"),
                       9, cor_agua, "middle"))
        svg.append(lbl(x_w0 - 4, y_nf - 8, t("N.A (u = 0)", "W.L. (u = 0)"), 10, cor_agua, "end"))
        svg.append(lbl(x_w0 + u_px + 10, y_base - 6,
                       f"u = γw·zw = {u_base:.1f} kPa", 10, cor_agua))
        u_base = gamma_w * z_w
        e_b = p_eff(H) * p_sc
        u_b = p_agua(H) * p_sc
        svg.append(lbl(x_dir + e_b + u_b + 12, (y_nf + y_base) / 2.0,
                       f"{t('Pressão da água', 'Water pressure')}: u = {u_base:.1f} kPa", 10, cor_agua))
    # ---- peso W ----
    if W_d is not None:
        A1, x1 = a * H, x_dir - a * esc / 2
        A2, x2 = (B - a) * H / 2, (x_esq + 2 * (x_dir - a * esc)) / 3
        x_cg = (A1 * x1 + A2 * x2) / max(A1 + A2, 1e-9)
        svg.append(f'<line x1="{x_cg:.1f}" y1="{y_base-52}" x2="{x_cg:.1f}" y2="{y_base-18}" stroke="#2c3e50" stroke-width="2.2"/>')
        svg.append(f'<polygon points="{x_cg:.1f},{y_base-14} {x_cg-4.5:.1f},{y_base-24} {x_cg+4.5:.1f},{y_base-24}" fill="#2c3e50"/>')
        svg.append(lbl(x_cg + 8, y_base - 34, f'W = {W_d:.1f} kN/m', 10, "#2c3e50"))
    # ---- subpressão ----
    if U_d is not None and U_d > 0:
        up = 46.0
        svg.append(f'<polygon points="{x_esq},{y_base} {x_dir},{y_base} {x_dir},{y_base+up}" fill="rgba(36,113,163,0.35)" stroke="{cor_sub}" stroke-width="1.5"/>')
        for k in range(1, 7):
            xx = x_esq + (x_dir - x_esq) * k / 6
            hh = up * k / 6
            svg.append(f'<line x1="{xx:.1f}" y1="{y_base+hh:.1f}" x2="{xx:.1f}" y2="{y_base+3}" stroke="{cor_sub}" stroke-width="1.4"/>')
            svg.append(f'<polygon points="{xx:.1f},{y_base+2} {xx-3:.1f},{y_base+10} {xx+3:.1f},{y_base+10}" fill="{cor_sub}"/>')
        svg.append(lbl((x_esq + x_dir) / 2.0, y_base + up + 16,
                       f"{t('Subpressão (triangular)', 'Uplift (triangular)')}: U_d = {U_d:.2f} kN/m",
                       10, cor_sub, "middle"))
    # ---- cotas ----
    svg.append(dim_v(y_topo, y_base, x_esq - 30, f'H = {H:.2f} m', size=11))
    if y_nf is not None:
        svg.append(dim_v(y_nf, y_base, x_esq - 62, f'z_w = {z_w:.2f} m', cor=cor_agua))
    svg.append(dim_h(x_topo_esq, x_dir, y_topo - 14, f"{t('Topo','Top')}: a = {a:.2f} m"))
    svg.append(dim_h(x_esq, x_dir, y_base + 88, f"{t('Base','Base')}: B = {B:.2f} m", size=11))
    if i > 0:
        svg.append(lbl(x_solo_dir - 60, y_g_dir - 8, f'i = {i:.1f}°', 10, "#1f77b4"))
    yl = 588
    svg.append(f'<rect x="25" y="{yl-12}" width="12" height="12" fill="{cor_betao}"/><text x="42" y="{yl-2}" font-size="10">{t("Betão","Concrete")}</text>')
    svg.append(f'<rect x="105" y="{yl-12}" width="12" height="12" fill="{cor_solo}"/><text x="122" y="{yl-2}" font-size="10">{t("Solo retido","Retained soil")}</text>')
    svg.append(f'<rect x="215" y="{yl-12}" width="12" height="12" fill="{cor_fund}"/><text x="232" y="{yl-2}" font-size="10">{t("Solo fundação","Foundation soil")}</text>')
    svg.append(f'<rect x="335" y="{yl-12}" width="12" height="12" fill="rgba(41,128,185,0.3)"/><text x="352" y="{yl-2}" font-size="10">{t("Solo submerso (γ′)","Submerged soil (γ′)")}</text>')
    svg.append(f'<line x1="470" y1="{yl-6}" x2="495" y2="{yl-6}" stroke="{cor_eff}" stroke-width="2.5"/><text x="501" y="{yl-2}" font-size="10">{t("Impulso activo","Active pressure")}</text>')
    svg.append(f'<line x1="610" y1="{yl-6}" x2="635" y2="{yl-6}" stroke="{cor_agua}" stroke-width="2.5"/><text x="641" y="{yl-2}" font-size="10">{t("Pressão da água","Water pressure")}</text>')
    svg.append('</svg>')
    return "".join(svg)


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================
def mostrar():
    lang = st.session_state.language
    if "tipo_muro" not in st.session_state:
        st.session_state.tipo_muro = "gravidade"
    if "tipo_solo" not in st.session_state:
        st.session_state.tipo_solo = "unico"
    if "fase_consola" not in st.session_state:
        st.session_state.fase_consola = "geotecnica"
    st.markdown(f"### {get_text('modulo_muros', lang)}")
    st.divider()
    if st.session_state.tipo_muro == "gravidade":
        st.markdown(carregar_imagem_local("assets/Picture2.png", width=600), unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><p style="color: #555; font-size: 14px;"><b>{get_text('legenda', lang)}:</b> H = {get_text('altura', lang)} | B = {get_text('largura_base', lang).split(' [')[0]} | a = {get_text('largura_topo', lang).split(' [')[0]} | i = {get_text('inclinacao_terrapleno', lang).split(' [')[0]} | N.F. = {get_text('nivel_freatico', lang).split(' [')[0]}</p></div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"#### {get_text('selecione_tipo', lang)}")
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_gravidade = st.session_state.tipo_muro == "gravidade"
        if st.button(f"🧱 {get_text('muros_contencao', lang)} - {get_text('gravidade', lang)}", use_container_width=True, type="primary" if tipo_gravidade else "secondary"):
            st.session_state.tipo_muro = "gravidade"
            st.session_state.fase_consola = None
            st.rerun()
    with col2:
        tipo_consola = st.session_state.tipo_muro == "consola"
        if st.button(f"🏗️ {get_text('muros_contencao', lang)} - {get_text('consola', lang)}", use_container_width=True, type="primary" if tipo_consola else "secondary"):
            st.session_state.tipo_muro = "consola"
            st.session_state.fase_consola = "geotecnica"
            if "dados_consola" in st.session_state:
                del st.session_state.dados_consola
            st.rerun()
    with col3:
        tipo_contrafortes = st.session_state.tipo_muro == "contrafortes"
        if st.button(f"🏛️ {get_text('muros_contencao', lang)} - {get_text('contrafortes', lang)}", use_container_width=True, type="primary" if tipo_contrafortes else "secondary"):
            st.session_state.tipo_muro = "contrafortes"
            st.session_state.fase_consola = None
            st.session_state.fase_cf = "geotecnica"
            st.rerun()
    if st.session_state.tipo_muro == "gravidade":
        st.divider()
        st.markdown(f"### 🧱 {get_text('muros_contencao', lang)} - {get_text('gravidade', lang)}")
        st.markdown(f"{get_text('selecione_solo', lang)}")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            tipo_unico = st.session_state.tipo_solo == "unico"
            if st.button(get_text("solo_unico", lang), use_container_width=True, type="primary" if tipo_unico else "secondary"):
                st.session_state.tipo_solo = "unico"
                st.rerun()
        with col_s2:
            tipo_estrat = st.session_state.tipo_solo == "estratificado"
            if st.button(get_text("solos_estratificados", lang), use_container_width=True, type="primary" if tipo_estrat else "secondary"):
                st.session_state.tipo_solo = "estratificado"
                st.rerun()
        st.divider()
        if st.session_state.tipo_solo == "unico":
            formulario_gravidade_solo_unico()
        else:
            formulario_gravidade_solo_estratificado()
    elif st.session_state.tipo_muro == "consola":
        from paginas import muros_consola
        st.divider()
        muros_consola.formulario_muro_consola()
    elif st.session_state.tipo_muro == "contrafortes":
        from paginas import muros_contrafortes
        st.divider()
        muros_contrafortes.formulario_muro_contrafortes()
    st.divider()
    if st.button(get_text("voltar_menu", lang)):
        st.session_state.pagina_atual = "menu_escolha"
        st.session_state.tipo_muro = None
        st.session_state.tipo_solo = None
        st.session_state.fase_consola = None
        if "dados_consola" in st.session_state:
            del st.session_state.dados_consola
        st.rerun()


# ============================================================
# FORMULÁRIO - SOLO ÚNICO
# ============================================================
def formulario_gravidade_solo_unico():
    lang = st.session_state.language
    st.markdown(f"#### {get_text('solo_unico', lang)}")
    st.markdown(f"#### {get_text('abordagem_ec7', lang)}")
    combo_ec7 = st.radio(get_text("combinacao", lang), [get_text("combinacao1", lang), get_text("combinacao2", lang)], index=1, horizontal=True)
    if get_text("combinacao1", lang) in combo_ec7:
        g_G_unfav, g_G_fav, g_Q = 1.35, 1.00, 1.50
        g_phi, g_c, g_cu = 1.00, 1.00, 1.00
        g_Rh, g_Rv = 1.00, 1.00
    else:
        g_G_unfav, g_G_fav, g_Q = 1.00, 1.00, 1.30
        g_phi, g_c, g_cu = 1.25, 1.25, 1.40
        g_Rh, g_Rv = 1.00, 1.00
    st.divider()
    st.markdown(f"#### {get_text('geometria', lang)}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        H = campo_latex("altura_muro_lbl", "H", "unidade_m", "H_grav", 5.0, minimo=0.5, passo=0.1, lang=lang)
    with col2:
        B = campo_latex("lbl_largura_base", "B", "unidade_m", "B_grav", 3.5, minimo=0.5, passo=0.1, lang=lang)
    with col3:
        a = campo_latex("lbl_largura_topo", "a", "unidade_m", "a_grav", 1.0, minimo=0.1, passo=0.1, lang=lang)
    with col4:
        i = campo_latex("lbl_inclinacao", "i", "unidade_graus", "i_grav", 0.0, minimo=0.0, maximo=45.0, passo=1.0, lang=lang)
    st.divider()
    st.markdown(f"#### {get_text('solo_retido', lang)}")
    st.caption(get_text("info_gamma_sat", lang))
    col1, col2 = st.columns(2)
    with col1:
        gamma_sol = campo_latex("lbl_gamma", r"\gamma", "unidade_knm3", "g_sol", 18.0, minimo=10.0, passo=0.5, lang=lang)
        gamma_sat = campo_latex("lbl_gamma_sat", r"\gamma_{sat}", "unidade_knm3", "gsat_sol", 20.0, minimo=10.0, passo=0.5, lang=lang)
        phi = campo_latex("lbl_phi", r"\phi'", "unidade_graus", "phi_sol", 30.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
        c_linha = campo_latex("lbl_c", "c'", "unidade_kpa", "c_sol", 0.0, minimo=0.0, passo=1.0, lang=lang)
    with col2:
        q = campo_latex("lbl_q", "q", "unidade_kpa", "q_sol", 0.0, minimo=0.0, passo=1.0, lang=lang)
        z_w = campo_latex("nivel_freatico_lbl", "z_w", "unidade_m", "zw_sol", 0.0, minimo=0.0, passo=0.1, lang=lang)
    st.divider()
    st.markdown(f"#### {get_text('solo_fundacao', lang)}")
    fund = get_text("sufixo_fund", lang)
    sfx = f" — {fund}"
    col1, col2 = st.columns(2)
    with col1:
        gamma_fund = campo_latex("lbl_gamma", r"\gamma", "unidade_knm3", "g_fund", 18.0, minimo=10.0, passo=0.5, lang=lang, sufixo=sfx)
        gamma_sat_fund = campo_latex("lbl_gamma_sat", r"\gamma_{sat}", "unidade_knm3", "gsat_fund", 20.0, minimo=10.0, passo=0.5, lang=lang, sufixo=sfx)
        phi_fund = campo_latex("lbl_phi", r"\phi'_{d,fund}", "unidade_graus", "phi_fund", 28.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang, sufixo=sfx)
        c_fund = campo_latex("lbl_c", "c'_{d,fund}", "unidade_kpa", "c_fund", 2.0, minimo=0.0, passo=1.0, lang=lang, sufixo=sfx)
    with col2:
        cu_fund = campo_latex("lbl_cu", r"c_{u,fund}", "unidade_kpa", "cu_fund", 0.0, minimo=0.0, passo=1.0, lang=lang, sufixo=sfx)
        delta_b = campo_latex("lbl_delta_b", r"\delta_b", "unidade_graus", "delta_b", 20.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
        st.caption(get_text("info_delta_b", lang))
    st.divider()
    st.markdown(f"#### {get_text('metodo_calculo', lang)}")
    col1, col2 = st.columns(2)
    with col1:
        metodo = st.radio(get_text("metodo", lang), [get_text("rankine", lang), get_text("coulomb", lang)], horizontal=True)
    with col2:
        if metodo == get_text("rankine", lang):
            delta = 0.0
            st.caption(get_text("info_rankine", lang))
        else:
            delta = st.number_input(get_text("angulo_atrito_estrutura", lang), min_value=0.0, max_value=45.0, value=20.0, step=1.0)
    st.divider()
    if st.button(f"🧮 {get_text('calcular_geotecnica', lang)}", type="primary", use_container_width=True):
        calcular_gravidade_solo_unico(H, B, a, i, gamma_sol, gamma_sat, phi, c_linha, q, z_w,
                                      gamma_fund, gamma_sat_fund, phi_fund, c_fund, cu_fund, delta_b,
                                      metodo, delta, combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv)


# ============================================================
# CÁLCULO - SOLO ÚNICO
# ============================================================
def calcular_gravidade_solo_unico(H, B, a, i, gamma_sol, gamma_sat, phi, c_linha, q, z_w,
                                  gamma_fund, gamma_sat_fund, phi_fund, c_fund, cu_fund, delta_b,
                                  metodo, delta, combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv):
    lang = st.session_state.language
    st.divider()
    st.markdown(f"### {get_text('resultados', lang)} - {get_text('solo_unico', lang)}")
    gamma_w = 9.81
    phi_d = calcular_phi_d(phi, g_phi)
    c_d = c_linha / g_c
    delta_d = calcular_delta_d(delta, g_phi)
    q_d = q * g_Q
    phi_fund_d = calcular_phi_d(phi_fund, g_phi)
    c_fund_d = c_fund / g_c
    cu_fund_d = cu_fund / g_cu
    with st.expander(f"📋 1. {get_text('valores_calculo', lang).strip()}", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{get_text('solo_retido', lang).split(' - ')[0]} ({get_text('parametros_minorados', lang).replace('**','')})**")
            st.latex(rf"\phi'_d = {phi_d:.2f}^\circ")
            st.latex(rf"\delta_d = {delta_d:.2f}^\circ")
            st.latex(rf"c'_d = {c_d:.2f}\ \mathrm{{kPa}}")
        with col2:
            st.markdown(f"**{get_text('solo_fundacao', lang).split(' (')[0]} ({get_text('parametros_minorados', lang).replace('**','')})**")
            st.latex(rf"\phi'_{{d,fund}} = {phi_fund_d:.2f}^\circ")
            st.latex(rf"c'_{{d,fund}} = {c_fund_d:.2f}\ \mathrm{{kPa}}")
            st.latex(rf"C_{{u,fund}} = {cu_fund_d:.2f}\ \mathrm{{kPa}}")
            st.latex(rf"\delta_b = {delta_b:.2f}^\circ")
        with col3:
            st.markdown(f"**{get_text('peso_especifico', lang).split(' γ')[0]}s**")
            st.latex(rf"\gamma = {gamma_sol:.2f}\ \mathrm{{kN/m^3}}")
            st.latex(rf"\gamma_{{sat}} = {gamma_sat:.2f}\ \mathrm{{kN/m^3}}")
            st.latex(rf"\gamma_{{sub}} = {gamma_sat - gamma_w:.2f}\ \mathrm{{kN/m^3}}")
            st.latex(rf"\gamma_{{fund}} = {gamma_fund:.2f}\ \mathrm{{kN/m^3}}")
            st.latex(rf"q_d = {q_d:.2f}\ \mathrm{{kPa}}")
    st.divider()
    i_rad = math.radians(i)
    phi_d_rad = math.radians(phi_d)
    delta_d_rad = math.radians(delta_d)
    if metodo == get_text("rankine", lang):
        Ka = calcular_Ka_Rankine(phi_d_rad, i_rad)
        if i > 0:
            show_labeled_formula("coeficiente_impulso", "formula_ka_rankine_inclinado", lang)
            st.caption("ℹ️ " + get_text("info_inclinacao", lang))
        else:
            show_labeled_formula("coeficiente_impulso", "formula_ka_rankine", lang)
    else:
        Ka = calcular_Ka_Coulomb_slide48(phi_d_rad, delta_d_rad, i_rad, alpha_rad=0)
        st.markdown("##### " + get_text('coeficiente_impulso', lang) + (" (Coulomb / Müller-Breslau, pág. 48)" if lang == "pt" else " (Coulomb / Müller-Breslau, p. 48)"))
        st.latex(r"K_a = \frac{\sin^2(\beta + \phi'_d)}{\sin^2(\beta)\,\sin(\beta - \delta_d)\left[1 + \sqrt{\frac{\sin(\phi'_d + \delta_d)\,\sin(\phi'_d - i)}{\sin(\beta - \delta_d)\,\sin(\beta + i)}}\right]^2}")
        st.markdown(r"Para paramento vertical ($\beta = 90^\circ$), a expressão reduz-se a:" if lang == "pt"
                    else r"For a vertical back face ($\beta = 90^\circ$), the expression reduces to:")
        st.latex(r"K_a = \frac{\cos^2(\phi'_d)}{\cos(\delta_d)\left[1 + \sqrt{\frac{\sin(\phi'_d + \delta_d)\,\sin(\phi'_d - i)}{\cos(\delta_d)\,\cos(i)}}\right]^2}")
    st.latex(rf"K_a = {Ka:.4f}")
    if z_w > 0 and z_w < H:
        H_acima = H - z_w
        H_abaixo = z_w
        gamma_abaixo = gamma_sat - gamma_w
        sigma_topo = Ka * q_d
        sigma_nf = Ka * (gamma_sol * H_acima + q_d)
        sigma_base_efetiva = Ka * (gamma_sol * H_acima + gamma_abaixo * H_abaixo + q_d)
        Ia_acima = 0.5 * (sigma_topo + sigma_nf) * H_acima
        Ia_abaixo = 0.5 * (sigma_nf + sigma_base_efetiva) * H_abaixo
        Ia_agua = 0.5 * gamma_w * (H_abaixo ** 2)
        Ia_caract = Ia_acima + Ia_abaixo + Ia_agua
        with st.expander(f"💪 2. {get_text('impulso_ativo', lang)} ({get_text('com_nf', lang) if 'com_nf' in get_text.__dict__ else 'com NF'})", expanded=True):
            st.markdown("**" + ("Zona acima do NF" if lang == "pt" else "Zone above W.T.") + rf"** ($H_{{acima}} = {H_acima:.2f}\ \mathrm{{m}}$):")
            st.write(rf"- $\sigma_{{topo}} = {sigma_topo:.2f}\ \mathrm{{kPa}} \quad|\quad \sigma_{{NF}} = {sigma_nf:.2f}\ \mathrm{{kPa}}$")
            st.write(rf"- $I_{{a,acima}} = \mathbf{{{Ia_acima:.2f}}}\ \mathrm{{kN/m}}$")
            st.markdown("**" + ("Zona abaixo do NF" if lang == "pt" else "Zone below W.T.") + rf"** ($H_{{abaixo}} = {H_abaixo:.2f}\ \mathrm{{m}}$):")
            st.write(rf"- $\sigma_{{base,ef}} = {sigma_base_efetiva:.2f}\ \mathrm{{kPa}}$")
            st.write(rf"- $I_{{a,abaixo}} = \mathbf{{{Ia_abaixo:.2f}}}\ \mathrm{{kN/m}} \quad|\quad I_{{a,agua}} = \mathbf{{{Ia_agua:.2f}}}\ \mathrm{{kN/m}}$")
            st.write(rf"👉 $I_a = \mathbf{{{Ia_caract:.2f}}}\ \mathrm{{kN/m}}$")
    else:
        Ia_caract = 0.5 * Ka * gamma_sol * (H ** 2) + Ka * q_d * H
        with st.expander(f"💪 2. {get_text('impulso_ativo', lang)} (sem NF)", expanded=True):
            show_formula("formula_impulso", lang)
            st.write(rf"- $I_a = \mathbf{{{Ia_caract:.2f}}}\ \mathrm{{kN/m}}$")
    Ia_d = Ia_caract * g_G_unfav
    IaH_d, IaV_d = calcular_componentes_impulso(Ia_d, delta_d_rad, i_rad, metodo, alpha_rad=0)
    col1, col2, col3 = st.columns(3)
    col1.metric("Ka", f"{Ka:.4f}")
    col2.metric("Ia,d", f"{Ia_d:.2f} kN/m")
    col3.metric("IaH,d / IaV,d", f"{IaH_d:.2f} / {IaV_d:.2f}")
    st.divider()
    if z_w > 0 and z_w < H:
        p_ativo = gamma_w * z_w
        U_d = 0.5 * p_ativo * B * g_G_unfav
    else:
        U_d = 0.0
    gamma_betao = 25.0
    Area_muro = (a + B) / 2 * H
    W_d = gamma_betao * Area_muro * g_G_fav
    x_cg = (B ** 2 + B * a + a ** 2) / (3 * (B + a))
    braco_W = B - x_cg
    M_est_W = W_d * braco_W
    M_est_IaV = IaV_d * B if IaV_d > 0 else 0.0
    M_est_total = M_est_W + M_est_IaV
    M_derr_total = IaH_d * (H / 3)
    with st.expander(f"⚖️ 3. {get_text('peso_estrutura', lang)} e {get_text('momentos', lang).lower()}", expanded=False):
        st.latex(rf"W_d = {W_d:.2f}\ \mathrm{{kN/m}} \quad|\quad U_d = {U_d:.2f}\ \mathrm{{kN/m}}")
        st.latex(rf"M_{{est,total}} = {M_est_total:.2f}\ \mathrm{{kNm/m}} \quad|\quad M_{{derr,total}} = {M_derr_total:.2f}\ \mathrm{{kNm/m}}")
    st.divider()
    V_d = W_d + IaV_d - U_d
    if V_d > 0:
        M_centro = M_est_total - M_derr_total
        e = (B / 2) - (M_centro / V_d)
    else:
        e = B
        st.error(get_text("forca_negativa", lang))
    B_linha = max(0.0, B - 2 * abs(e))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.latex(rf"V_d = {V_d:.2f}\ \mathrm{{kN/m}}")
    with col2:
        st.latex(rf"e = {abs(e):.3f}\ \mathrm{{m}}")
    with col3:
        st.latex(rf"B' = {B_linha:.3f}\ \mathrm{{m}}")
    if abs(e) <= B / 6:
        st.success(get_text("dentro_nucleo", lang, B6=B / 6, e=abs(e)))
    else:
        st.warning(get_text("fora_nucleo", lang, B6=B / 6, e=abs(e)))
    st.divider()
    st.markdown(f"### {get_text('verificacoes', lang)}")
    ok_derr = M_est_total >= M_derr_total
    st.markdown(f"**a) {get_text('derrubamento', lang)}**")
    col1, col2 = st.columns(2)
    col1.latex(rf"M_{{est,d}} = {M_est_total:.2f}\ \mathrm{{kNm/m}}")
    col2.latex(rf"M_{{derr,d}} = {M_derr_total:.2f}\ \mathrm{{kNm/m}}")
    if ok_derr:
        st.success(f"✅ **{get_text('satisfaz', lang)}**")
    else:
        st.error(f"❌ **{get_text('nao_satisfaz', lang)}**")
    st.markdown("---")
    if cu_fund_d > 0:
        Rd_h = (cu_fund_d * B_linha) / g_Rh
        tipo_cisalhamento = get_text("cis_nao_drenada", lang) + r" ($c_u$)"
        show_labeled_formula("deslizamento", "formula_deslizamento_nao_drenado", lang)
    else:
        delta_b_rad = math.radians(delta_b)
        Rd_h = (V_d * math.tan(delta_b_rad)) / g_Rh
        tipo_cisalhamento = get_text("cis_drenada", lang) + rf" ($\delta_b = {delta_b:.2f}^\circ$)"
        show_labeled_formula("deslizamento", "formula_deslizamento_drenado", lang)
    ok_desliz = (Rd_h / IaH_d >= 1.0) if IaH_d > 0 else True
    st.markdown(f"**b) {get_text('deslizamento', lang)} ({tipo_cisalhamento})**")
    col1, col2 = st.columns(2)
    col1.latex(rf"H_d = {IaH_d:.2f}\ \mathrm{{kN/m}}")
    col2.latex(rf"R_{{d,h}} = {Rd_h:.2f}\ \mathrm{{kN/m}}")
    if ok_desliz:
        st.success(f"✅ **{get_text('satisfaz', lang)}**")
    else:
        st.error(f"❌ **{get_text('nao_satisfaz', lang)}**")
    st.markdown("---")
    phi_fund_rad = math.radians(phi_fund_d)
    q_solo_fund = 0.0
    q_Rd, Nc, Nq, Ngamma, termo_c, termo_q, termo_gamma, q_ult = detalhar_capacidade_carga(
        phi_fund_rad, c_fund_d, gamma_fund, B_linha, q_solo_fund, g_Rv)
    if abs(e) <= B / 6:
        sigma_max_d = (V_d / B) * (1 + (6 * abs(e) / B))
    else:
        sigma_max_d = (2 * V_d) / (3 * (B / 2 - abs(e))) if (B / 2 - abs(e)) > 0 else float('inf')
    ok_carga = q_Rd >= sigma_max_d
    st.markdown(f"##### c) {get_text('capacidade_carga', lang)}")
    show_formula("formula_capacidade_carga", lang)
    st.markdown("**🔎 " + ("Detalhe parcela a parcela (Meyerhof — Tabela + interpolação):" if lang == "pt"
                           else "Term-by-term detail (Meyerhof — Table + interpolation):") + "**")
    st.write(rf"- $\phi'_{{d,fund}} = {phi_fund_d:.2f}^\circ \;\rightarrow\; N_c = \mathbf{{{Nc:.2f}}}\quad N_q = \mathbf{{{Nq:.2f}}}\quad N_\gamma = \mathbf{{{Ngamma:.2f}}}$")
    st.write(rf"- **{('Termo coesão' if lang=='pt' else 'Cohesion term')}**: $c'\cdot N_c = {c_fund_d:.2f} \times {Nc:.2f} = \mathbf{{{termo_c:.2f}}}\ \mathrm{{kPa}}$")
    st.write(rf"- **{('Termo sobrecarga' if lang=='pt' else 'Surcharge term')}**: $q'\cdot N_q = {q_solo_fund:.2f} \times {Nq:.2f} = \mathbf{{{termo_q:.2f}}}\ \mathrm{{kPa}}$")
    st.write(rf"- **{('Termo peso solo' if lang=='pt' else 'Soil weight term')}**: $0.5\cdot\gamma\cdot B'\cdot N_\gamma = 0.5 \times {gamma_fund:.2f} \times {B_linha:.3f} \times {Ngamma:.2f} = \mathbf{{{termo_gamma:.2f}}}\ \mathrm{{kPa}}$")
    st.write(rf"- $q_{{ult}} = {termo_c:.2f} + {termo_q:.2f} + {termo_gamma:.2f} = \mathbf{{{q_ult:.2f}}}\ \mathrm{{kPa}}$")
    st.write(rf"- $q_{{R,d}} = \frac{{{q_ult:.2f}}}{{{g_Rv:.2f}}} = \mathbf{{{q_Rd:.2f}}}\ \mathrm{{kPa}}$")
    col1, col2 = st.columns(2)
    col1.info(rf"$q_{{R,d}} = \mathbf{{{q_Rd:.2f}}}\ \mathrm{{kPa}}$")
    col2.info(rf"$\sigma_{{max,d}} = \mathbf{{{sigma_max_d:.2f}}}\ \mathrm{{kPa}}$")
    if ok_carga:
        st.success(f"✅ **{get_text('satisfaz', lang)}**")
    else:
        st.error(f"❌ **{get_text('nao_satisfaz', lang)}**")
    st.divider()
    if ok_derr and ok_desliz and ok_carga:
        st.success(get_text("muro_satisfaz", lang))
    else:
        st.error(get_text("muro_nao_satisfaz", lang))
        if not ok_derr:
            st.write(f"- ❌ {get_text('derrubamento', lang)}")
        if not ok_desliz:
            st.write(f"- ❌ {get_text('deslizamento', lang)}")
        if not ok_carga:
            st.write(f"- ❌ {get_text('capacidade_carga', lang)}")
    st.markdown("### 🎨 Esquema Final do Muro")
    svg_esquema = _svg_esquema_muro_gravidade(
        H=H, B=B, a=a, i=i, gamma_sol=gamma_sol, gamma_sat=gamma_sat, phi=phi, c_linha=c_linha,
        q=q, z_w=z_w, tipo_solo='unico', Ka=Ka, IaH_d=IaH_d, U_d=U_d, W_d=W_d, lang=lang,
        gamma_fund=gamma_fund, phi_fund=phi_fund, c_fund=c_fund)
    st.markdown(svg_esquema, unsafe_allow_html=True)
    st.divider()
    st.markdown(f"#### {get_text('exportar_relatorio', lang)}")
    st.caption(get_text("converter_pdf", lang))
    html_bytes = relatorios.gerar_relatorio_html_muro_gravidade(
        lang=lang, esquema_svg=svg_esquema,
        nome=st.session_state.nome, curso=st.session_state.curso, genero=st.session_state.genero,
        H=H, B=B, a=a, i=i, gamma_sol=gamma_sol, gamma_sat=gamma_sat, phi=phi, c_linha=c_linha, q=q, z_w=z_w,
        metodo=metodo, delta=delta, delta_b=delta_b, combo_ec7=combo_ec7,
        g_G_unfav=g_G_unfav, g_G_fav=g_G_fav, g_Q=g_Q, g_phi=g_phi, g_c=g_c, g_cu=g_cu, g_Rh=g_Rh, g_Rv=g_Rv,
        phi_d=phi_d, c_d=c_d, delta_d=delta_d, q_d=q_d, Ka=Ka, Ia_caract=Ia_caract, Ia_d=Ia_d, IaH_d=IaH_d, IaV_d=IaV_d,
        U_d=U_d, W_d=W_d, Area_muro=Area_muro, M_est_total=M_est_total, M_derr_total=M_derr_total,
        V_d=V_d, e=e, B_linha=B_linha, Rd_h=Rd_h, tipo_cisalhamento=tipo_cisalhamento, q_Rd=q_Rd, sigma_max_d=sigma_max_d,
        ok_derr=ok_derr, ok_desliz=ok_desliz, ok_carga=ok_carga, tipo_solo='unico',
        gamma_fund=gamma_fund, gamma_sat_fund=gamma_sat_fund, phi_fund=phi_fund, c_fund=c_fund, cu_fund=cu_fund,
        phi_fund_d=phi_fund_d, c_fund_d=c_fund_d, cu_fund_d=cu_fund_d,
        x_cg=x_cg, braco_W=braco_W)
    st.download_button(
        label=get_text("descarregar_relatorio", lang),
        data=html_bytes,
        file_name=f"Relatorio_Muro_Gravidade_{st.session_state.nome.replace(' ', '_')}.html",
        mime="text/html", use_container_width=True, type="primary")


# ============================================================
# FORMULÁRIO - SOLOS ESTRATIFICADOS
# ============================================================
def formulario_gravidade_solo_estratificado():
    lang = st.session_state.language
    st.markdown(f"#### {get_text('solos_estratificados', lang)}")
    st.markdown(f"#### {get_text('abordagem_ec7', lang)}")
    combo_ec7 = st.radio(get_text("combinacao", lang), [get_text("combinacao1", lang), get_text("combinacao2", lang)], index=1, horizontal=True, key="ec7_est")
    if get_text("combinacao1", lang) in combo_ec7:
        g_G_unfav, g_G_fav, g_Q = 1.35, 1.00, 1.50
        g_phi, g_c, g_cu = 1.00, 1.00, 1.00
        g_Rh, g_Rv = 1.00, 1.00
    else:
        g_G_unfav, g_G_fav, g_Q = 1.00, 1.00, 1.30
        g_phi, g_c, g_cu = 1.25, 1.25, 1.40
        g_Rh, g_Rv = 1.00, 1.00
    st.divider()
    st.markdown(f"#### {get_text('geometria', lang)}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        H = campo_latex("altura_total", "H", "unidade_m", "H_est", 6.0, minimo=0.5, passo=0.1, lang=lang)
    with col2:
        B = campo_latex("lbl_largura_base", "B", "unidade_m", "B_est", 4.0, minimo=0.5, passo=0.1, lang=lang)
    with col3:
        a = campo_latex("lbl_largura_topo", "a", "unidade_m", "a_est", 1.2, minimo=0.1, passo=0.1, lang=lang)
    with col4:
        i = campo_latex("lbl_inclinacao", "i", "unidade_graus", "i_est", 0.0, minimo=0.0, maximo=45.0, passo=1.0, lang=lang)
    st.divider()
    st.markdown("#### 🟫 " + ("Camada 1 — Solo Superior" if lang == "pt" else "Layer 1 — Upper Soil"))
    col1, col2 = st.columns(2)
    with col1:
        H1 = campo_latex("lbl_altura_camada", "H_1", "unidade_m", "H1_est", 3.0, minimo=0.1, passo=0.1, lang=lang)
        gamma1 = campo_latex("lbl_gamma", r"\gamma_1", "unidade_knm3", "g1_est", 17.0, minimo=10.0, passo=0.5, lang=lang)
        gamma1_sat = campo_latex("lbl_gamma_sat", r"\gamma_{sat,1}", "unidade_knm3", "gsat1_est", 19.0, minimo=10.0, passo=0.5, lang=lang)
        phi1 = campo_latex("lbl_phi", r"\phi'_1", "unidade_graus", "phi1_est", 28.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
    with col2:
        c1 = campo_latex("lbl_c", "c'_1", "unidade_kpa", "c1_est", 2.0, minimo=0.0, passo=1.0, lang=lang)
        q = campo_latex("lbl_q", "q", "unidade_kpa", "q_est", 0.0, minimo=0.0, passo=1.0, lang=lang)
    st.divider()
    st.markdown("#### 🟫 " + ("Camada 2 — Solo Inferior" if lang == "pt" else "Layer 2 — Lower Soil"))
    H2 = max(0.1, H - H1)
    st.latex(rf"H_2 = {H2:.2f}\ \mathrm{{m}}")
    col1, col2 = st.columns(2)
    with col1:
        gamma2 = campo_latex("lbl_gamma", r"\gamma_2", "unidade_knm3", "g2_est", 18.0, minimo=10.0, passo=0.5, lang=lang)
        gamma2_sat = campo_latex("lbl_gamma_sat", r"\gamma_{sat,2}", "unidade_knm3", "gsat2_est", 20.0, minimo=10.0, passo=0.5, lang=lang)
        phi2 = campo_latex("lbl_phi", r"\phi'_2", "unidade_graus", "phi2_est", 32.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
    with col2:
        c2 = campo_latex("lbl_c", "c'_2", "unidade_kpa", "c2_est", 5.0, minimo=0.0, passo=1.0, lang=lang)
    st.divider()
    st.markdown(f"#### {get_text('solo_fundacao', lang)}")
    fund = get_text("sufixo_fund", lang)
    sfx = f" — {fund}"
    col1, col2 = st.columns(2)
    with col1:
        gamma_fund = campo_latex("lbl_gamma", r"\gamma_{fund}", "unidade_knm3", "g_fund_est", 18.0, minimo=10.0, passo=0.5, lang=lang, sufixo=sfx)
        gamma_sat_fund = campo_latex("lbl_gamma_sat", r"\gamma_{sat,fund}", "unidade_knm3", "gsat_fund_est", 20.0, minimo=10.0, passo=0.5, lang=lang, sufixo=sfx)
        phi_fund = campo_latex("lbl_phi", r"\phi'_{d,fund}", "unidade_graus", "phi_fund_est", 30.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang, sufixo=sfx)
    with col2:
        c_fund = campo_latex("lbl_c", "c'_{d,fund}", "unidade_kpa", "c_fund_est", 3.0, minimo=0.0, passo=1.0, lang=lang, sufixo=sfx)
        cu_fund = campo_latex("lbl_cu", r"c_{u,fund}", "unidade_kpa", "cu_fund_est", 0.0, minimo=0.0, passo=1.0, lang=lang, sufixo=sfx)
        delta_b = campo_latex("lbl_delta_b", r"\delta_b", "unidade_graus", "delta_b_est", 20.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
    st.divider()
    st.markdown(f"#### 💧 {get_text('nivel_freatico', lang).split(' [')[0]}")
    z_w = campo_latex("nivel_freatico_lbl", "z_w", "unidade_m", "zw_est", 0.0, minimo=0.0, passo=0.1, lang=lang)
    st.divider()
    st.markdown(f"#### {get_text('metodo_calculo', lang)}")
    col1, col2 = st.columns(2)
    with col1:
        metodo = st.radio(get_text("metodo", lang), [get_text("rankine", lang), get_text("coulomb", lang)], horizontal=True, key="met_est")
    with col2:
        if metodo == get_text("rankine", lang):
            delta = 0.0
            st.caption(get_text("info_rankine", lang))
        else:
            delta = st.number_input(get_text("angulo_atrito_estrutura", lang), min_value=0.0, max_value=45.0, value=20.0, step=1.0, key="delta_est")
    st.divider()
    if st.button(f"🧮 {get_text('calcular_geotecnica', lang)} - {get_text('solos_estratificados', lang)}", type="primary", use_container_width=True):
        calcular_gravidade_solo_estratificado(H, B, a, i, H1, H2, gamma1, gamma1_sat, phi1, c1,
                                              gamma2, gamma2_sat, phi2, c2, gamma_fund, gamma_sat_fund,
                                              phi_fund, c_fund, cu_fund, delta_b, q, z_w, metodo, delta,
                                              combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv)


# ============================================================
# CÁLCULO - SOLOS ESTRATIFICADOS
# ============================================================
def calcular_gravidade_solo_estratificado(H, B, a, i, H1, H2, gamma1, gamma1_sat, phi1, c1,
                                          gamma2, gamma2_sat, phi2, c2, gamma_fund, gamma_sat_fund,
                                          phi_fund, c_fund, cu_fund, delta_b, q, z_w, metodo, delta,
                                          combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv):
    lang = st.session_state.language
    st.divider()
    st.markdown(f"### {get_text('resultados', lang)} - {get_text('solos_estratificados', lang)}")
    gamma_w = 9.81
    phi1_d = calcular_phi_d(phi1, g_phi)
    phi2_d = calcular_phi_d(phi2, g_phi)
    phi_fund_d = calcular_phi_d(phi_fund, g_phi)
    c1_d = c1 / g_c
    c2_d = c2 / g_c
    c_fund_d = c_fund / g_c
    cu_fund_d = cu_fund / g_cu
    delta_d = calcular_delta_d(delta, g_phi)
    q_d = q * g_Q
    with st.expander(f"📋 1. {get_text('valores_calculo', lang).strip()}", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**" + ("Camada 1" if lang == "pt" else "Layer 1") + ":**")
            st.write(rf"- $\phi'_{{d,1}} = {phi1_d:.2f}^\circ \quad|\quad c'_{{d,1}} = {c1_d:.2f}\ \mathrm{{kPa}}$")
        with col2:
            st.markdown("**" + ("Camada 2" if lang == "pt" else "Layer 2") + ":**")
            st.write(rf"- $\phi'_{{d,2}} = {phi2_d:.2f}^\circ \quad|\quad c'_{{d,2}} = {c2_d:.2f}\ \mathrm{{kPa}}$")
        with col3:
            st.markdown(f"**{get_text('solo_fundacao', lang).split(' (')[0]}:**")
            st.write(rf"- $\phi'_{{d,fund}} = {phi_fund_d:.2f}^\circ \quad|\quad c'_{{d,fund}} = {c_fund_d:.2f}\ \mathrm{{kPa}}$")
    st.divider()
    i_rad = math.radians(i)
    phi1_d_rad = math.radians(phi1_d)
    phi2_d_rad = math.radians(phi2_d)
    delta_d_rad = math.radians(delta_d)
    if metodo == get_text("rankine", lang):
        Ka1 = calcular_Ka_Rankine(phi1_d_rad, i_rad)
        Ka2 = calcular_Ka_Rankine(phi2_d_rad, i_rad)
        if i > 0:
            show_labeled_formula("coeficiente_impulso", "formula_ka_rankine_inclinado", lang)
            st.caption("ℹ️ " + get_text("info_inclinacao", lang))
        else:
            show_labeled_formula("coeficiente_impulso", "formula_ka_rankine", lang)
    else:
        Ka1 = calcular_Ka_Coulomb_slide48(phi1_d_rad, delta_d_rad, i_rad, alpha_rad=0)
        Ka2 = calcular_Ka_Coulomb_slide48(phi2_d_rad, delta_d_rad, i_rad, alpha_rad=0)
        st.markdown("##### " + get_text('coeficiente_impulso', lang) + (" (Coulomb / Müller-Breslau, pág. 48)" if lang == "pt" else " (Coulomb / Müller-Breslau, p. 48)"))
        st.latex(r"K_a = \frac{\sin^2(\beta + \phi'_d)}{\sin^2(\beta)\,\sin(\beta - \delta_d)\left[1 + \sqrt{\frac{\sin(\phi'_d + \delta_d)\,\sin(\phi'_d - i)}{\sin(\beta - \delta_d)\,\sin(\beta + i)}}\right]^2}")
        st.markdown(r"Para paramento vertical ($\beta = 90^\circ$), a expressão reduz-se a:" if lang == "pt"
                    else r"For a vertical back face ($\beta = 90^\circ$), the expression reduces to:")
        st.latex(r"K_a = \frac{\cos^2(\phi'_d)}{\cos(\delta_d)\left[1 + \sqrt{\frac{\sin(\phi'_d + \delta_d)\,\sin(\phi'_d - i)}{\cos(\delta_d)\,\cos(i)}}\right]^2}")
    st.latex(rf"K_{{a,1}} = {Ka1:.4f} \qquad K_{{a,2}} = {Ka2:.4f}")
    st.divider()

    def calcular_Ia_camada(Ka, gamma, gamma_sat, H_camada, z_w_camada_topo, z_w_camada_base, q_aplicada):
        if z_w_camada_topo >= H_camada or (z_w_camada_topo <= 0 and z_w_camada_base <= 0):
            sigma_topo = Ka * q_aplicada
            sigma_base = Ka * (gamma * H_camada + q_aplicada)
            Ia = 0.5 * (sigma_topo + sigma_base) * H_camada
            return Ia, 0.0, sigma_topo, sigma_base
        H_acima = min(z_w_camada_topo, H_camada) if z_w_camada_topo > 0 else 0.0
        H_abaixo = H_camada - H_acima
        gamma_sub = gamma_sat - gamma_w
        sigma_topo = Ka * q_aplicada
        sigma_interface = Ka * (gamma * H_acima + q_aplicada)
        sigma_base = Ka * (gamma * H_acima + gamma_sub * H_abaixo + q_aplicada)
        Ia_acima = 0.5 * (sigma_topo + sigma_interface) * H_acima
        Ia_abaixo = 0.5 * (sigma_interface + sigma_base) * H_abaixo
        Ia = Ia_acima + Ia_abaixo
        Ia_agua = 0.5 * gamma_w * (H_abaixo ** 2)
        return Ia, Ia_agua, sigma_topo, sigma_base

    z_w_c2_topo = z_w - H2
    z_w_c1_topo = z_w - H
    Ia1_efetivo, Ia1_agua, _, _ = calcular_Ia_camada(Ka1, gamma1, gamma1_sat, H1, z_w_c1_topo, z_w - H2, q_d)
    Ia1_caract = Ia1_efetivo + Ia1_agua
    if z_w >= H:
        q_sobrecarga = (gamma1_sat - gamma_w) * H1
    elif z_w <= 0:
        q_sobrecarga = gamma1 * H1
    else:
        q_sobrecarga = gamma1 * (H1 - (z_w - H2)) + (gamma1_sat - gamma_w) * (z_w - H2)
    Ia2_efetivo, Ia2_agua, _, _ = calcular_Ia_camada(Ka2, gamma2, gamma2_sat, H2, z_w_c2_topo, z_w, q_sobrecarga + q_d)
    Ia2_caract = Ia2_efetivo + Ia2_agua
    Ia_total_caract = Ia1_caract + Ia2_caract
    Ia_d = Ia_total_caract * g_G_unfav
    IaH_d, IaV_d = calcular_componentes_impulso(Ia_d, delta_d_rad, i_rad, metodo, alpha_rad=0)
    with st.expander(f"💪 2. {get_text('impulso_ativo', lang)} " + ("por Camada" if lang == "pt" else "per Layer"), expanded=True):
        st.write(rf"- $I_{{a,1}} = \mathbf{{{Ia1_caract:.2f}}}\ \mathrm{{kN/m}} \quad|\quad I_{{a,2}} = \mathbf{{{Ia2_caract:.2f}}}\ \mathrm{{kN/m}}$")
        st.write(rf"👉 $I_{{a,d}} = \mathbf{{{Ia_d:.2f}}}\ \mathrm{{kN/m}} \quad|\quad I_{{aH,d}} = {IaH_d:.2f} \quad|\quad I_{{aV,d}} = {IaV_d:.2f}$")
    st.divider()
    U_d = 0.5 * gamma_w * z_w * B * g_G_unfav if z_w > 0 else 0.0
    gamma_betao = 25.0
    Area_muro = (a + B) / 2 * H
    W_d = gamma_betao * Area_muro * g_G_fav
    x_cg = (B ** 2 + B * a + a ** 2) / (3 * (B + a))
    braco_W = B - x_cg
    M_est_total = W_d * braco_W + (IaV_d * B if IaV_d > 0 else 0.0)
    M_derr_total = IaH_d * (H / 3)
    V_d = W_d + IaV_d - U_d
    if V_d > 0:
        M_centro = M_est_total - M_derr_total
        e = (B / 2) - (M_centro / V_d)
    else:
        e = B
        st.error(get_text("forca_negativa", lang))
    B_linha = max(0.0, B - 2 * abs(e))
    col1, col2, col3 = st.columns(3)
    col1.metric("V_d", f"{V_d:.2f} kN/m")
    col2.metric("e", f"{abs(e):.3f} m")
    col3.metric("B'", f"{B_linha:.3f} m")
    if abs(e) <= B / 6:
        st.success(get_text("dentro_nucleo", lang, B6=B / 6, e=abs(e)))
    else:
        st.warning(get_text("fora_nucleo", lang, B6=B / 6, e=abs(e)))
    st.divider()
    st.markdown(f"### {get_text('verificacoes', lang)}")
    ok_derr = M_est_total >= M_derr_total
    st.markdown(f"**a) {get_text('derrubamento', lang)}**")
    if ok_derr:
        st.success(f"✅ **{get_text('satisfaz', lang)}**")
    else:
        st.error(f"❌ **{get_text('nao_satisfaz', lang)}**")
    st.markdown("---")
    if cu_fund_d > 0:
        Rd_h = (cu_fund_d * B_linha) / g_Rh
        tipo_cisalhamento = get_text("cis_nao_drenada", lang) + r" ($c_u$)"
    else:
        delta_b_rad = math.radians(delta_b)
        Rd_h = (V_d * math.tan(delta_b_rad)) / g_Rh
        tipo_cisalhamento = get_text("cis_drenada", lang) + rf" ($\delta_b = {delta_b:.2f}^\circ$)"
    ok_desliz = (Rd_h / IaH_d >= 1.0) if IaH_d > 0 else True
    st.markdown(f"**b) {get_text('deslizamento', lang)} ({tipo_cisalhamento})**")
    if ok_desliz:
        st.success(f"✅ **{get_text('satisfaz', lang)}**")
    else:
        st.error(f"❌ **{get_text('nao_satisfaz', lang)}**")
    st.markdown("---")
    phi_fund_rad = math.radians(phi_fund_d)
    q_solo_fund = 0.0
    q_Rd, Nc, Nq, Ngamma, termo_c, termo_q, termo_gamma, q_ult = detalhar_capacidade_carga(
        phi_fund_rad, c_fund_d, gamma_fund, B_linha, q_solo_fund, g_Rv)
    if abs(e) <= B / 6:
        sigma_max_d = (V_d / B) * (1 + (6 * abs(e) / B))
    else:
        sigma_max_d = (2 * V_d) / (3 * (B / 2 - abs(e))) if (B / 2 - abs(e)) > 0 else float('inf')
    ok_carga = q_Rd >= sigma_max_d
    st.markdown(f"##### c) {get_text('capacidade_carga', lang)}")
    show_formula("formula_capacidade_carga", lang)
    st.markdown("**🔎 " + ("Detalhe (Meyerhof — Tabela + interpolação):" if lang == "pt"
                           else "Detail (Meyerhof — Table + interpolation):") + "**")
    st.write(rf"- $\phi'_{{d,fund}} = {phi_fund_d:.2f}^\circ \;\rightarrow\; N_c = \mathbf{{{Nc:.2f}}}\quad N_q = \mathbf{{{Nq:.2f}}}\quad N_\gamma = \mathbf{{{Ngamma:.2f}}}$")
    st.write(rf"- $c'\cdot N_c = \mathbf{{{termo_c:.2f}}} \quad|\quad q'\cdot N_q = \mathbf{{{termo_q:.2f}}} \quad|\quad 0.5\cdot\gamma\cdot B'\cdot N_\gamma = \mathbf{{{termo_gamma:.2f}}}$")
    st.write(rf"- $q_{{ult}} = \mathbf{{{q_ult:.2f}}}\ \mathrm{{kPa}} \quad|\quad q_{{R,d}} = \mathbf{{{q_Rd:.2f}}}\ \mathrm{{kPa}}$")
    col1, col2 = st.columns(2)
    col1.info(rf"$q_{{R,d}} = \mathbf{{{q_Rd:.2f}}}\ \mathrm{{kPa}}$")
    col2.info(rf"$\sigma_{{max,d}} = \mathbf{{{sigma_max_d:.2f}}}\ \mathrm{{kPa}}$")
    if ok_carga:
        st.success(f"✅ **{get_text('satisfaz', lang)}**")
    else:
        st.error(f"❌ **{get_text('nao_satisfaz', lang)}**")
    st.divider()
    if ok_derr and ok_desliz and ok_carga:
        st.success(get_text("muro_satisfaz", lang))
    else:
        st.error(get_text("muro_nao_satisfaz", lang))
    st.markdown("### 🎨 Esquema Final do Muro")
    svg_esquema = _svg_esquema_muro_gravidade(
        H=H, B=B, a=a, i=i, gamma_sol=gamma2, gamma_sat=gamma2_sat, phi=phi2, c_linha=c2,
        q=q, z_w=z_w, tipo_solo='estratificado',
        H1=H1, H2=H2, gamma1=gamma1, gamma2=gamma2, gamma1_sat=gamma1_sat, gamma2_sat=gamma2_sat,
        phi1=phi1, phi2=phi2, Ka1=Ka1, Ka2=Ka2, IaH_d=IaH_d, U_d=U_d, W_d=W_d, lang=lang,
        gamma_fund=gamma_fund, phi_fund=phi_fund, c_fund=c_fund)
    st.markdown(svg_esquema, unsafe_allow_html=True)
    st.divider()
    st.markdown(f"#### {get_text('exportar_relatorio', lang)}")
    html_bytes = relatorios.gerar_relatorio_html_muro_gravidade(
        lang=lang, esquema_svg=svg_esquema,
        nome=st.session_state.nome, curso=st.session_state.curso, genero=st.session_state.genero,
        H=H, B=B, a=a, i=i, gamma_sol=gamma2, gamma_sat=gamma2_sat, phi=phi2, c_linha=c2, q=q, z_w=z_w,
        metodo=metodo, delta=delta, delta_b=delta_b, combo_ec7=combo_ec7,
        g_G_unfav=g_G_unfav, g_G_fav=g_G_fav, g_Q=g_Q, g_phi=g_phi, g_c=g_c, g_cu=g_cu, g_Rh=g_Rh, g_Rv=g_Rv,
        phi_d=phi2_d, c_d=c2_d, delta_d=delta_d, q_d=q_d, Ka=Ka2, Ia_caract=Ia_total_caract, Ia_d=Ia_d,
        IaH_d=IaH_d, IaV_d=IaV_d, U_d=U_d, W_d=W_d, Area_muro=Area_muro,
        M_est_total=M_est_total, M_derr_total=M_derr_total, V_d=V_d, e=e, B_linha=B_linha,
        Rd_h=Rd_h, tipo_cisalhamento=tipo_cisalhamento, q_Rd=q_Rd, sigma_max_d=sigma_max_d,
        ok_derr=ok_derr, ok_desliz=ok_desliz, ok_carga=ok_carga, tipo_solo='estratificado',
        H1=H1, H2=H2, gamma1=gamma1, gamma1_sat=gamma1_sat, gamma2=gamma2, gamma2_sat=gamma2_sat,
        phi1=phi1, phi2=phi2, c1=c1, c2=c2, Ka1=Ka1, Ka2=Ka2,
        Ia1_caract=Ia1_caract, Ia2_caract=Ia2_caract,
        gamma_fund=gamma_fund, gamma_sat_fund=gamma_sat_fund, phi_fund=phi_fund,
        c_fund=c_fund, cu_fund=cu_fund, phi_fund_d=phi_fund_d, c_fund_d=c_fund_d, cu_fund_d=cu_fund_d,
        x_cg=x_cg, braco_W=braco_W)
    st.download_button(
        label=get_text("descarregar_relatorio", lang),
        data=html_bytes,
        file_name=f"Relatorio_Muro_Gravidade_Estratificado_{st.session_state.nome.replace(' ', '_')}.html",
        mime="text/html", use_container_width=True, type="primary")