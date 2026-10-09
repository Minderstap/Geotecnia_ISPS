"""Muro em Consola - V12 (LaTeX + i18n PT/EN) - VERSÃO CORRIGIDA"""
import streamlit as st
import math

from calculos import relatorios_consola
from utils.traducoes import get_text
from utils.latex_helper import campo_latex, show_formula

def prosseguir_para_armaduras():
    st.session_state.fase_consola = "armaduras"

def voltar_para_geotecnica():
    st.session_state.fase_consola = "geotecnica"

def carregar_imagem_local(caminho, width=None):
    from utils.imagens import img_base64_html
    return img_base64_html(caminho, width=width or 700)

def calcular_phi_d(phi, g):
    if g == 0:
        return phi
    return math.degrees(math.atan(math.tan(math.radians(phi)) / g))

def Ka_rankine_slide100(phi_d_rad, i_rad):
    ci, cp = math.cos(i_rad), math.cos(phi_d_rad)
    disc = max(0.0, ci ** 2 - cp ** 2)
    return (ci - math.sqrt(disc)) / (ci + math.sqrt(disc)) * ci

def coulomb_alpha(phi_d_deg, i_deg):
    phi_r = math.radians(max(phi_d_deg, 1e-6))
    i_r = math.radians(i_deg)
    sin_arg = min(1.0, math.sin(i_r) / math.sin(phi_r))
    arcsin_deg = math.degrees(math.asin(sin_arg))
    return 45.0 + phi_d_deg / 2.0 + 0.5 * (arcsin_deg - i_deg)

def coulomb_K(phi_d_deg, i_deg, alpha_deg):
    beta_deg = 180.0 - alpha_deg
    phi_r = math.radians(phi_d_deg)
    i_r = math.radians(i_deg)
    beta_r = math.radians(beta_deg)
    delta_r = math.radians(phi_d_deg)
    num = math.sin(beta_r - phi_r) / math.sin(beta_r)
    den_inside = math.sin(beta_r - i_r)
    if abs(den_inside) < 1e-9:
        inner = 0.0
    else:
        inner = (math.sin(phi_r + delta_r) * math.sin(phi_r - i_r)) / den_inside
        inner = max(0.0, inner)
    den = math.sqrt(max(0.0, math.sin(beta_r + delta_r))) + math.sqrt(inner)
    if den < 1e-9:
        return 0.0
    return (num / den) ** 2

def coulomb_Kaq(Ka_gamma, beta_deg, i_deg):
    b = math.radians(beta_deg)
    ii = math.radians(i_deg)
    denom = math.sin(b - ii)
    if abs(denom) < 1e-9:
        return Ka_gamma
    return Ka_gamma * math.sin(b) / denom

def _defs():
    return (
        '<defs>'
        '<marker id="cB" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
        '<polygon points="0,0 10,3 0,6" fill="#1f77b4"/></marker>'
        '<marker id="cR" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
        '<polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker>'
        '<pattern id="hcHatch" patternUnits="userSpaceOnUse" width="10" height="10" '
        'patternTransform="rotate(45)">'
        '<line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.2"/>'
        '</pattern>'
        '</defs>'
    )

def _dim(x1, y1, x2, y2, label, cor="#1f77b4", dy=-5, font=10):
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{cor}" '
            f'stroke-width="1.2" marker-start="url(#cB)" marker-end="url(#cB)"/>'
            f'<text x="{mx}" y="{my + dy}" text-anchor="middle" font-size="{font}" '
            f'fill="{cor}" font-weight="bold">{label}</text>')

def _svg_estrutura_consola(H, HR, B, bt, bh, ts, tb, i, lang="pt"):
    """Estrutura do muro em consola com cotas técnicas correctas:
    linhas de extensão tracejadas + setas bem orientadas."""
    def _t(pt, en): return pt if lang == "pt" else en
    esc = min(330.0 / max(H, 0.1), 400.0 / max(B, 0.1))
    x0, yb = 165.0, 505.0
    ybt = yb - tb * esc
    ytop = yb - H * esc
    xs0 = x0 + bt * esc
    xs1 = xs0 + ts * esc
    xR = x0 + B * esc
    tan_i = math.tan(math.radians(i))
    x_soil_max = xR + 175.0
    max_rise = (ytop - 46.0)
    dx_soil = (x_soil_max - xs1)
    if tan_i > 1e-9 and dx_soil * tan_i > max_rise:
        dx_soil = max_rise / tan_i
    x_soil = max(xs1 + max(90.0, dx_soil), xR + 40.0)
    y_soil = ytop - (x_soil - xs1) * tan_i
    W, Hh = int(x_soil + 70), 660

    # Marcadores de seta (orientação automática, ponta na extremidade da linha)
    defs = (
        '<defs>'
        '<marker id="arrB" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto" markerUnits="strokeWidth">'
        '<polygon points="0,0 9,3.5 0,7" fill="#1f77b4"/>'
        '</marker>'
        '<marker id="arrG" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto" markerUnits="strokeWidth">'
        '<polygon points="0,0 9,3.5 0,7" fill="#27ae60"/>'
        '</marker>'
        '<pattern id="hcHatch" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)">'
        '<line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.2"/>'
        '</pattern>'
        '</defs>'
    )

    s = [f'<svg width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'style="background:#fdfefe;border:1px solid #bbb;border-radius:8px;'
         f'font-family:Segoe UI,Arial,sans-serif;">']
    s.append(defs)
    s.append(f'<text x="{W/2}" y="24" text-anchor="middle" font-size="14" '
             f'font-weight="bold">{_t("MURO EM CONSOLA", "CANTILEVER WALL")}</text>')

    # --- SOLO RETIDO ---
    poly_solo = (f'{xs1},{ytop} {x_soil},{y_soil:.1f} {x_soil},{yb} '
                 f'{xR},{yb} {xR},{ybt} {xs1},{ybt}')
    s.append(f'<polygon points="{poly_solo}" fill="#e8dcc0" stroke="#8b6f47"/>')
    s.append(f'<polygon points="{poly_solo}" fill="url(#hcHatch)" opacity="0.30"/>')
    s.append(f'<text x="{(xs1+x_soil)/2+30:.1f}" y="{(ytop+ybt)/2+4:.1f}" text-anchor="middle" '
             f'font-size="10" fill="#5d4a2f" font-weight="bold">{_t("SOLO RETIDO", "RETAINED SOIL")}</text>')

    # --- SOLO DE FUNDAÇÃO ---
    s.append(f'<rect x="40" y="{yb:.1f}" width="{W-80}" height="46" fill="#8a6a4f" stroke="#6b4a2f"/>')
    s.append(f'<rect x="40" y="{yb:.1f}" width="{W-80}" height="46" fill="url(#hcHatch)" opacity="0.25"/>')
    s.append(f'<text x="52" y="{yb+28:.1f}" font-size="10" fill="#fff" font-weight="bold">'
             f'{_t("SOLO DE FUNDACAO", "FOUNDATION SOIL")}</text>')

    # --- BETÃO ---
    poly_betao = (f'{x0},{yb} {x0},{ybt} {xs0},{ybt} {xs0},{ytop} '
                  f'{xs1},{ytop} {xs1},{ybt} {xR},{ybt} {xR},{yb}')
    s.append(f'<polygon points="{poly_betao}" fill="#b8b8b8" stroke="#333" stroke-width="2"/>')
    s.append(f'<text x="{(x0+xs0)/2:.1f}" y="{(yb+ybt)/2:.1f}" text-anchor="middle" font-size="10" '
             f'fill="#fff" font-weight="bold">{_t("BETÃO", "CONCRETE")}</text>')

    # --- ETIQUETAS INTERNAS ---
    s.append(f'<line x1="{xs0-52}" y1="{(ytop+ybt)/2:.1f}" x2="{xs0-2}" y2="{(ytop+ybt)/2:.1f}" '
             f'stroke="#555" stroke-width="1" stroke-dasharray="4,3"/>')
    s.append(f'<text x="{xs0-56}" y="{(ytop+ybt)/2+4:.1f}" text-anchor="end" font-size="10" '
             f'fill="#222" font-weight="bold">{_t("PARAMENTO", "STEM")}</text>')
    s.append(f'<text x="{(x0+xs0)/2:.1f}" y="{ybt-8:.1f}" text-anchor="middle" font-size="10" '
             f'fill="#c0392b" font-weight="bold">{_t("BIQUEIRA", "TOE")}</text>')
    s.append(f'<text x="{(xs1+xR)/2:.1f}" y="{ybt-8:.1f}" text-anchor="middle" font-size="10" '
             f'fill="#c0392b" font-weight="bold">{_t("TALAO", "HEEL")}</text>')

    # ============================================================
    # COTAS TÉCNICAS (linhas de extensão tracejadas + setas)
    # ============================================================
    # Helper: cota vertical (x fixo, varia em y)
    def cota_v(x_cota, y1, y2, x_ext1, x_ext2, label, cor="#1f77b4", marker="arrB", font=10):
        """Cota vertical com linhas de extensão tracejadas."""
        return (
            # Linhas de extensão (tracejadas, finas)
            f'<line x1="{x_ext1:.1f}" y1="{y1:.1f}" x2="{x_cota+5:.1f}" y2="{y1:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            f'<line x1="{x_ext2:.1f}" y1="{y2:.1f}" x2="{x_cota+5:.1f}" y2="{y2:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            # Linha de cota com setas
            f'<line x1="{x_cota:.1f}" y1="{y1:.1f}" x2="{x_cota:.1f}" y2="{y2:.1f}" '
            f'stroke="{cor}" stroke-width="1.1" marker-start="url(#{marker})" marker-end="url(#{marker})"/>'
            # Rótulo (rotacionado 90° para leitura vertical)
            f'<text x="{x_cota-6:.1f}" y="{(y1+y2)/2:.1f}" text-anchor="middle" '
            f'font-size="{font}" fill="{cor}" font-weight="bold" '
            f'transform="rotate(-90 {x_cota-6:.1f} {(y1+y2)/2:.1f})">{label}</text>'
        )

    # Helper: cota horizontal (y fixo, varia em x)
    def cota_h(y_cota, x1, x2, y_ext1, y_ext2, label, cor="#1f77b4", marker="arrB", font=10):
        """Cota horizontal com linhas de extensão tracejadas."""
        return (
            # Linhas de extensão (tracejadas, finas)
            f'<line x1="{x1:.1f}" y1="{y_ext1:.1f}" x2="{x1:.1f}" y2="{y_cota-5:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            f'<line x1="{x2:.1f}" y1="{y_ext2:.1f}" x2="{x2:.1f}" y2="{y_cota-5:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            # Linha de cota com setas
            f'<line x1="{x1:.1f}" y1="{y_cota:.1f}" x2="{x2:.1f}" y2="{y_cota:.1f}" '
            f'stroke="{cor}" stroke-width="1.1" marker-start="url(#{marker})" marker-end="url(#{marker})"/>'
            # Rótulo
            f'<text x="{(x1+x2)/2:.1f}" y="{y_cota-7:.1f}" text-anchor="middle" '
            f'font-size="{font}" fill="{cor}" font-weight="bold">{label}</text>'
        )

    # --- COTAS VERTICAIS (lado esquerdo) ---
    # HR (do topo da base até ao topo do stem)
    s.append(cota_v(x0 - 130, ytop, ybt, xs0, xs0, f"HR={HR:.2f} m", cor="#27ae60", marker="arrG", font=10))
    # H (do fundo da base até ao topo do stem)
    s.append(cota_v(x0 - 85, ytop, yb, xs0, x0, f"H={H:.2f} m", cor="#1f77b4", marker="arrB", font=11))
    # tb (espessura da base, lado direito)
    s.append(cota_v(xR + 35, ybt, yb, xR, xR, f"tb={tb*100:.0f} cm", cor="#1f77b4", marker="arrB", font=10))

    # --- COTAS HORIZONTAIS (em baixo) ---
    # bt, ts, bh (logo abaixo da base)
    y_cota1 = yb + 55
    s.append(cota_h(y_cota1, x0, xs0, ybt, ybt, f"bt={bt:.2f}", font=10))
    s.append(cota_h(y_cota1, xs0, xs1, ybt, ybt, f"ts={ts*100:.0f} cm", font=10))
    s.append(cota_h(y_cota1, xs1, xR, ybt, ybt, f"bh={bh:.2f}", font=10))
    # B (total, mais abaixo)
    y_cota2 = yb + 85
    s.append(cota_h(y_cota2, x0, xR, yb, yb, f"B={B:.2f} m (=bt+ts+bh)", font=11))

    # --- Inclinação do terrapleno ---
    if i > 0:
        s.append(f'<text x="{x_soil-14:.1f}" y="{y_soil+16:.1f}" text-anchor="end" font-size="10" '
                 f'fill="#1f77b4" font-weight="bold">i={i:.1f}°</text>')

    s.append('</svg>')
    return "".join(s)

def _svg_esquema_coulomb(H, HR, B, bt, bh, ts, tb, i, alpha, beta, Ka, Kaq, h_uso, IaH_d, W_total_d, q_ativo, lang="pt", phi_d=30.0):
    t = lambda pt, en: pt if lang == "pt" else en
    i_r = math.radians(i)
    tan_i = math.tan(i_r)
    phi = max(float(phi_d), 0.0)
    if phi > 1e-6:
        arg = min(1.0, math.sin(i_r) / math.sin(math.radians(phi)))
        dif = 0.5 * (math.degrees(math.asin(arg)) - i)
        xi = 45.0 + phi / 2.0 - dif
    else:
        xi = 45.0
    xi_r = math.radians(xi)
    alpha_use = float(alpha)
    a_r = math.radians(alpha_use)
    Y_D = H + bh * tan_i
    alpha_E = math.degrees(math.atan2(H, bh)) if bh > 1e-9 else 90.0
    tol = 0.05
    B_on_stem = alpha_use < alpha_E - tol
    B_eq_E = abs(alpha_use - alpha_E) <= tol
    if B_on_stem:
        X_B, Y_B = -bh, bh * math.tan(a_r)
    elif B_eq_E:
        X_B, Y_B = -bh, H
    else:
        den_B = math.sin(a_r) + math.cos(a_r) * tan_i
        t_B0 = Y_D / den_B if den_B > 1e-9 else 0.0
        X_B, Y_B = -t_B0 * math.cos(a_r), t_B0 * math.sin(a_r)
    t_B = math.hypot(X_B, Y_B)
    den_C = math.sin(xi_r) - math.cos(xi_r) * tan_i
    C_cap = False
    X_C = (Y_D / den_C) * math.cos(xi_r) if den_C > 0.05 else 1e9
    if X_C > 3.0 * Y_D:
        C_cap, X_C = True, 3.0 * Y_D
    Y_C = X_C * math.tan(xi_r) if C_cap else Y_D + X_C * tan_i
    xs0 = -B + bt
    xs1 = -bh
    D_front = max(H - HR, 0.0)
    
    def mapper(ox, oy, esc): return lambda X, Y: (ox + X * esc, oy - Y * esc)
    def pts(lst): return " ".join(f"{x:.1f},{y:.1f}" for x, y in lst)
    def line(p, q, stroke, w=1.2, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{stroke}" stroke-width="{w}"{d}{extra}/>'
    def text(x, y, s, size=11, fill="#222", anchor="middle", weight="bold", extra="", halo=True):
        base = f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}"{extra}'
        halo_t = base + ' fill="#fdfefe" stroke="#fdfefe" stroke-width="3.5" stroke-linejoin="round">' + s + '</text>'
        return (halo_t if halo else '') + base + f' fill="{fill}">' + s + '</text>'
    def arc(c, r, ang0, ang1, stroke, w=1.5):
        a0, a1 = math.radians(ang0), math.radians(ang1)
        p0 = (c[0] + r * math.cos(a0), c[1] - r * math.sin(a0))
        p1 = (c[0] + r * math.cos(a1), c[1] - r * math.sin(a1))
        sweep = 0 if ang1 > ang0 else 1
        large = 1 if abs(ang1 - ang0) > 180 else 0
        return f'<path d="M {p0[0]:.1f},{p0[1]:.1f} A {r:.1f},{r:.1f} 0 {large} {sweep} {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{stroke}" stroke-width="{w}"/>'
    def arc_label(c, r, ang0, ang1, s, color, size=12):
        am = math.radians((ang0 + ang1) / 2.0)
        return text(c[0] + (r + 13) * math.cos(am), c[1] - (r + 13) * math.sin(am) + 4, s, size, color)
    def dot(p, r=3.2): return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="#111"/>'
    def dim_v(xpx, y0, y1, label, cor="#1f77b4"):
        return f'<line x1="{xpx:.1f}" y1="{y0:.1f}" x2="{xpx:.1f}" y2="{y1:.1f}" stroke="{cor}" stroke-width="1.2" marker-start="url(#cqD)" marker-end="url(#cqD)"/>' + text(xpx + 6, (y0 + y1) / 2.0 + 4, label, 11, cor, "start")
    def wall(P):
        poly = [(-B, 0), (-B, tb), (xs0, tb), (xs0, H), (xs1, H), (xs1, tb), (0, tb), (0, 0)]
        return f'<polygon points="{pts([P(x, y) for x, y in poly])}" fill="#b8b8b8" stroke="#333" stroke-width="2"/><polygon points="{pts([P(x, y) for x, y in poly])}" fill="url(#cqC)" opacity="0.5"/>'

    W_svg, H_svg = 1060, 660
    oy = 540.0
    esc1 = min((600.0 - 30.0 - 150.0) / max(B + X_C, 0.1), 470.0 / max(Y_C, 0.5))
    ox1 = 30.0 + B * esc1
    P1 = mapper(ox1, oy, esc1)
    esc2 = min((400.0 - 20.0 - 120.0) / max(B + 0.45 * Y_D, 0.1), 470.0 / max(Y_D + 0.1, 0.5))
    ox2 = 660.0 + B * esc2
    P2 = mapper(ox2, oy, esc2)
    
    s = [f'<svg width="100%" viewBox="0 0 {W_svg} {H_svg}" xmlns="http://www.w3.org/2000/svg" style="max-width:{W_svg}px;background:#fdfefe;border:1px solid #bbb;border-radius:8px;font-family:Segoe UI,Arial,sans-serif;">']
    s.append('<defs><marker id="cqD" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto-start-reverse"><polygon points="0,0 10,3 0,6" fill="#1f77b4"/></marker><marker id="cqR" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker><pattern id="cqH" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.1"/></pattern><pattern id="cqC" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#888" stroke-width="0.8"/></pattern></defs>')
    s.append(text(W_svg / 2, 24, t("COULOMB (slide 99) — cunha morta, superfície AB e plano AC", "COULOMB (slide 99) — dead wedge, surface AB and plane AC"), 14))
    s.append(f'<line x1="640" y1="40" x2="640" y2="{H_svg-70}" stroke="#ddd" stroke-width="1"/>')
    
    A, E = P1(0, 0), P1(-bh, H)
    Bp, Dp, Cp = P1(X_B, Y_B), P1(0, Y_D), P1(X_C, Y_C)
    s.append(text(320, 56, t("① Geometria: pontos A, B, C, D, E", "① Geometry: points A, B, C, D, E"), 12, "#1f4e79"))
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" fill="url(#cqH)" opacity="0.5"/>')
    if D_front > tb:
        fr = [P1(-B - 0.6, 0), P1(-B - 0.6, D_front), P1(xs0, D_front), P1(xs0, 0)]
        s.append(f'<polygon points="{pts(fr)}" fill="#d2b48c" stroke="#8b6f47"/>')
        s.append(f'<polygon points="{pts(fr)}" fill="url(#cqH)" opacity="0.35"/>')
    
    if B_on_stem:
        dead = [P1(xs1, 0), Bp, A]
        wedge1 = [Bp, E, Dp, A]
    else:
        dead = [P1(xs1, 0), E, Bp, A]
        wedge1 = [Bp, Dp, A]
    
    s.append(f'<polygon points="{pts(dead)}" fill="#d9d9d9" stroke="none"/>')
    s.append(f'<polygon points="{pts(wedge1)}" fill="#8f8f8f" stroke="none"/>')
    s.append(f'<polygon points="{pts([Dp, Cp, A])}" fill="#f1ebdf" stroke="none"/>')
    s.append(f'<polygon points="{pts([Dp, Cp, A])}" fill="url(#cqH)" opacity="0.18"/>')
    s.append(wall(P1))
    
    ext = 0.12 * X_C
    G_end = P1(X_C + ext, Y_C + ext * tan_i)
    s.append(line(E, G_end, "#6b4a2f", 2.4))
    xd = [A[0] + 52, A[0] + 82, A[0] + 112]
    for pnt, xx in ((E, xd[0]), (Bp, xd[1]), (Dp, xd[2])):
        s.append(line(pnt, (xx + 8, pnt[1]), "#555", 1, "2,3"))
    s.append(line(A, (xd[2] + 8, A[1]), "#555", 1, "2,3"))
    s.append(line(A, Dp, "#555", 1.2, "2,3"))
    s.append(line(A, Bp, "#5d3a1f", 2.2, "7,4"))
    s.append(line(A, Cp, "#222", 1.8, "10,3,2,3"))
    
    ra = 44.0
    s.append(arc(A, ra, 180.0, 180.0 - alpha_use, "#c0392b"))
    s.append(arc_label(A, ra, 180.0, 180.0 - alpha_use, "α", "#c0392b"))
    rx = 56.0
    s.append(arc(A, rx, 0.0, xi, "#27ae60"))
    s.append(arc_label(A, rx, 0.0, xi, "ξ", "#27ae60"))
    if i > 0.05:
        ri = 62.0
        s.append(arc(Dp, ri, 0.0, i, "#1f77b4"))
        s.append(arc_label(Dp, ri, 0.0, max(i, 8.0) if i < 8 else i, "i", "#1f77b4", 11))
    
    c1 = (sum(p[0] for p in wedge1) / len(wedge1), sum(p[1] for p in wedge1) / len(wedge1))
    c2 = ((Dp[0] + Cp[0] + A[0]) / 3.0, (Dp[1] + Cp[1] + A[1]) / 3.0)
    s.append(text(c1[0], c1[1], "1", 15, "#fff", halo=False))
    s.append(text(c2[0], c2[1], "2", 15, "#333"))
    s.append(dim_v(xd[0], A[1], E[1], "h"))
    s.append(dim_v(xd[1], A[1], Bp[1], "h'"))
    s.append(dim_v(xd[2], A[1], Dp[1], "h''"))
    
    lblB = "B ≡ E" if B_eq_E else "B"
    bdx, bdy = (14, 4) if B_on_stem else (-8, -9)
    edx = -14 if not B_eq_E else -22
    for pnt, nm, dx, dy in ((A, "A", 6, 20), (Bp, lblB, bdx, bdy), (Cp, "C", 8, -9), (Dp, "D", 4, -10), (E, "E" if not B_eq_E else "", edx, -8)):
        s.append(dot(pnt))
        if nm:
            s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))
    
    s.append(text(30, 578, f"h = H = {H:.2f} m  |  h' = {Y_B:.2f} m (B)  |  h'' = {Y_D:.2f} m (D)", 11, "#1f77b4", "start"))
    s.append(text(30, 596, f"α = {alpha_use:.2f}°  |  φ' = {phi:.1f}°", 11, "#c0392b", "start"))
    s.append(text(30, 614, f"ξ = {xi:.2f}°   (φ' = {phi:.1f}°, i = {i:.1f}°)", 11, "#27ae60", "start"))
    
    A2, E2, B2 = P2(0, 0), P2(-bh, H), P2(X_B, Y_B)
    s.append(text(850, 56, t("② Cunha morta e impulso Iₐᶜ", "② Dead wedge and thrust Iₐᶜ"), 12, "#1f4e79"))
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" fill="url(#cqH)" opacity="0.5"/>')
    dead2 = [P2(xs1, 0), B2, A2] if B_on_stem else [P2(xs1, 0), E2, B2, A2]
    s.append(f'<polygon points="{pts(dead2)}" fill="#d9d9d9" stroke="none"/>')
    s.append(wall(P2))
    
    x_gr = 0.30 * Y_D
    s.append(line(E2, P2(x_gr, Y_D + x_gr * tan_i), "#6b4a2f", 2.4))
    s.append(line(B2, A2, "#5d3a1f", 2.4, "10,3,2,3"))
    
    ux, uy = -math.cos(a_r), math.sin(a_r)
    nx, ny = -math.sin(a_r), -math.cos(a_r)
    mp = (0.52 * t_B * ux, 0.52 * t_B * uy)
    tp = P2(mp[0], mp[1])
    tx, ty = tp[0] + 15 * nx, tp[1] - 15 * ny
    s.append(text(tx, ty, t("cunha morta", "dead wedge"), 12, "#1f4e79", "middle", extra=f' transform="rotate({alpha_use:.1f} {tx:.1f} {ty:.1f})"'))
    
    s.append(arc(A2, 44.0, 180.0, 180.0 - alpha_use, "#c0392b"))
    s.append(arc_label(A2, 44.0, 180.0, 180.0 - alpha_use, "α", "#c0392b"))
    s.append(line(A2, (A2[0] - 70, A2[1]), "#555", 1, "2,3"))
    
    t3 = t_B / 3.0
    Pm = P2(t3 * ux, t3 * uy)
    L_arrow = 78.0
    ang_f = alpha_use - phi
    tail = (Pm[0] + L_arrow * math.sin(math.radians(ang_f)), Pm[1] - L_arrow * math.cos(math.radians(ang_f)))
    s.append(line(tail, Pm, "#c0392b", 2.6, None, ' marker-end="url(#cqR)"'))
    
    th_n = 90.0 - alpha_use
    nrm_end = (Pm[0] + 62 * math.cos(math.radians(th_n)), Pm[1] - 62 * math.sin(math.radians(th_n)))
    s.append(line(Pm, nrm_end, "#555", 1, "2,3"))
    s.append(arc(Pm, 44.0, th_n, th_n + phi, "#c0392b"))
    s.append(arc_label(Pm, 44.0, th_n, th_n + phi, "φ'", "#c0392b", 12))
    
    xh = A2[0] + 40
    s.append(line(B2, (xh + 8, B2[1]), "#555", 1, "2,3"))
    s.append(dim_v(xh, A2[1], B2[1], "h'"))
    for pnt, nm, dx, dy in ((A2, "A", 6, 20), (B2, lblB, bdx, bdy), (E2, "E" if not B_eq_E else "", edx, -8)):
        s.append(dot(pnt))
        if nm:
            s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))
    
    s.append('</svg>')
    return "".join(s)

def _svg_esquema_rankine(H, HR, B, bt, bh, ts, tb, i, Ka, h_uso, IaH_d, W_total_d, q_ativo, lang="pt", phi_d=None):
    t = lambda pt, en: pt if lang == "pt" else en
    i_r = math.radians(i)
    tan_i = math.tan(i_r)
    Y_D = H + bh * tan_i
    have_C = (phi_d is not None) and (float(phi_d) > 1e-6)
    phi = float(phi_d) if have_C else 0.0
    C_cap = False
    xi = 0.0
    if have_C:
        arg = min(1.0, math.sin(i_r) / math.sin(math.radians(phi)))
        xi = 45.0 + phi / 2.0 - 0.5 * (math.degrees(math.asin(arg)) - i)
        xi_r = math.radians(xi)
        den_C = math.sin(xi_r) - math.cos(xi_r) * tan_i
        X_C = (Y_D / den_C) * math.cos(xi_r) if den_C > 0.05 else 1e9
        if X_C > 3.0 * Y_D:
            C_cap, X_C = True, 3.0 * Y_D
        Y_C = X_C * math.tan(xi_r) if C_cap else Y_D + X_C * tan_i
    else:
        X_C = 0.9 * Y_D
        Y_C = Y_D + X_C * tan_i
    
    xs0 = -B + bt
    xs1 = -bh
    D_front = max(H - HR, 0.0)
    
    def mapper(ox, oy, esc): return lambda X, Y: (ox + X * esc, oy - Y * esc)
    def pts(lst): return " ".join(f"{x:.1f},{y:.1f}" for x, y in lst)
    def line(p, q, stroke, w=1.2, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{stroke}" stroke-width="{w}"{d}{extra}/>'
    def text(x, y, s_, size=11, fill="#222", anchor="middle", weight="bold", extra="", halo=True):
        base = f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}"{extra}'
        halo_t = base + ' fill="#fdfefe" stroke="#fdfefe" stroke-width="3.5" stroke-linejoin="round">' + s_ + '</text>'
        return (halo_t if halo else '') + base + f' fill="{fill}">' + s_ + '</text>'
    def arc(c, r, ang0, ang1, stroke, w=1.5):
        a0, a1 = math.radians(ang0), math.radians(ang1)
        p0 = (c[0] + r * math.cos(a0), c[1] - r * math.sin(a0))
        p1 = (c[0] + r * math.cos(a1), c[1] - r * math.sin(a1))
        sweep = 0 if ang1 > ang0 else 1
        large = 1 if abs(ang1 - ang0) > 180 else 0
        return f'<path d="M {p0[0]:.1f},{p0[1]:.1f} A {r:.1f},{r:.1f} 0 {large} {sweep} {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{stroke}" stroke-width="{w}"/>'
    def arc_label(c, r, ang0, ang1, s_, color, size=12):
        am = math.radians((ang0 + ang1) / 2.0)
        return text(c[0] + (r + 13) * math.cos(am), c[1] - (r + 13) * math.sin(am) + 4, s_, size, color)
    def dot(p, r=3.2): return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="#111"/>'
    def dim_v(xpx, y0, y1, label, cor="#1f77b4"):
        return f'<line x1="{xpx:.1f}" y1="{y0:.1f}" x2="{xpx:.1f}" y2="{y1:.1f}" stroke="{cor}" stroke-width="1.2" marker-start="url(#rkD)" marker-end="url(#rkD)"/>' + text(xpx + 6, (y0 + y1) / 2.0 + 4, label, 11, cor, "start")
    def wall(P):
        poly = [(-B, 0), (-B, tb), (xs0, tb), (xs0, H), (xs1, H), (xs1, tb), (0, tb), (0, 0)]
        return f'<polygon points="{pts([P(x, y) for x, y in poly])}" fill="#b8b8b8" stroke="#333" stroke-width="2"/><polygon points="{pts([P(x, y) for x, y in poly])}" fill="url(#rkC)" opacity="0.5"/>'
    def surcharge(P, x_from, x_to, gy):
        out, n = [], 0
        xx = x_from
        while xx <= x_to and n < 12:
            g = gy(xx)
            p0, p1 = P(xx, g), P(xx, g)
            out.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]-30:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]-7:.1f}" stroke="#1f77b4" stroke-width="1.5"/><polygon points="{p1[0]:.1f},{p1[1]-4:.1f} {p1[0]-3.5:.1f},{p1[1]-12:.1f} {p1[0]+3.5:.1f},{p1[1]-12:.1f}" fill="#1f77b4"/>')
            xx += 0.45 * max(Y_D, 1.0) / 2.0
            n += 1
        return "".join(out)

    W_svg, H_svg = 1060, 660
    oy = 540.0
    esc1 = min((600.0 - 30.0 - 150.0) / max(B + X_C, 0.1), 470.0 / max(Y_C, 0.5))
    ox1 = 30.0 + B * esc1
    P1 = mapper(ox1, oy, esc1)
    esc2 = min((400.0 - 20.0 - 150.0) / max(B + 0.45 * Y_D, 0.1), 470.0 / max(Y_D + 0.1, 0.5))
    ox2 = 660.0 + B * esc2
    P2 = mapper(ox2, oy, esc2)
    
    s = [f'<svg width="100%" viewBox="0 0 {W_svg} {H_svg}" xmlns="http://www.w3.org/2000/svg" style="max-width:{W_svg}px;background:#fdfefe;border:1px solid #bbb;border-radius:8px;font-family:Segoe UI,Arial,sans-serif;">']
    s.append('<defs><marker id="rkD" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto-start-reverse"><polygon points="0,0 10,3 0,6" fill="#1f77b4"/></marker><marker id="rkR" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker><pattern id="rkH" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.1"/></pattern><pattern id="rkC" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#888" stroke-width="0.8"/></pattern></defs>')
    s.append(text(W_svg / 2, 24, t("RANKINE (slide 100) — cunha morta E-D-A e plano vertical AD", "RANKINE (slide 100) — dead wedge E-D-A and vertical plane AD"), 14))
    s.append(f'<line x1="640" y1="40" x2="640" y2="{H_svg-70}" stroke="#ddd" stroke-width="1"/>')
    
    A, E, Dp = P1(0, 0), P1(-bh, H), P1(0, Y_D)
    Cp = P1(X_C, Y_C)
    s.append(text(320, 56, t("① Geometria: pontos A, D, E" + (", C" if have_C else ""), "① Geometry: points A, D, E" + (", C" if have_C else "")), 12, "#1f4e79"))
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" fill="url(#rkH)" opacity="0.5"/>')
    if D_front > tb:
        fr = [P1(-B - 0.6, 0), P1(-B - 0.6, D_front), P1(xs0, D_front), P1(xs0, 0)]
        s.append(f'<polygon points="{pts(fr)}" fill="#d2b48c" stroke="#8b6f47"/>')
        s.append(f'<polygon points="{pts(fr)}" fill="url(#rkH)" opacity="0.35"/>')
    
    dead = [P1(xs1, 0), E, Dp, A]
    s.append(f'<polygon points="{pts(dead)}" fill="#8f8f8f" stroke="none"/>')
    if have_C:
        act = [Dp, Cp, A]
    else:
        xe = X_C
        act = [Dp, P1(xe, Y_D + xe * tan_i), P1(xe, 0), A]
    s.append(f'<polygon points="{pts(act)}" fill="#f1ebdf" stroke="none"/>')
    s.append(f'<polygon points="{pts(act)}" fill="url(#rkH)" opacity="0.18"/>')
    s.append(wall(P1))
    
    ext = 0.12 * X_C
    G_end = P1(X_C + ext, Y_D + (X_C + ext) * tan_i)
    s.append(line(E, G_end, "#6b4a2f", 2.4))
    xd = [A[0] + 52, A[0] + 82]
    for pnt, xx in ((E, xd[0]), (Dp, xd[1])):
        s.append(line(pnt, (xx + 8, pnt[1]), "#555", 1, "2,3"))
    s.append(line(A, (xd[1] + 8, A[1]), "#555", 1, "2,3"))
    s.append(line(A, Dp, "#5d3a1f", 2.4, "7,4"))
    if have_C:
        s.append(line(A, Cp, "#222", 1.8, "10,3,2,3"))
        s.append(arc(A, 56.0, 0.0, xi, "#27ae60"))
        s.append(arc_label(A, 56.0, 0.0, xi, "ξ", "#27ae60"))
    if i > 0.05:
        s.append(arc(Dp, 62.0, 0.0, i, "#1f77b4"))
        s.append(arc_label(Dp, 62.0, 0.0, max(i, 8.0), "i", "#1f77b4", 11))
    
    cx = (sum(p[0] for p in dead) / 4.0)
    cy = (sum(p[1] for p in dead) / 4.0)
    s.append(text(cx, cy, t("cunha morta", "dead wedge"), 12, "#fff", "middle", extra=f' transform="rotate(-90 {cx:.1f} {cy:.1f})"', halo=False))
    if q_ativo > 0:
        s.append(surcharge(P1, -bh + 0.1, X_C, lambda x: Y_D + x * tan_i))
        qp = P1(-bh + 0.1, H + 0.1 * tan_i)
        s.append(text(qp[0] + 4, qp[1] - 38, f"q = {q_ativo:.1f} kPa", 10, "#1f77b4", "start"))
    
    s.append(dim_v(xd[0], A[1], E[1], "h"))
    s.append(dim_v(xd[1], A[1], Dp[1], "h''"))
    pontos = [(A, "A", 6, 20), (Dp, "D", 4, -10), (E, "E", -14, -8)]
    if have_C:
        pontos.append((Cp, "C", 8, -9))
    for pnt, nm, dx, dy in pontos:
        s.append(dot(pnt))
        s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))
    
    s.append(text(30, 578, f"h = H = {H:.2f} m  |  h'' = AD = {Y_D:.2f} m", 11, "#1f77b4", "start"))
    s.append(text(30, 596, t(f"Plano vertical AD; Iₐ paralelo ao talude (i = {i:.1f}°)", f"Vertical plane AD; Iₐ parallel to slope (i = {i:.1f}°)"), 11, "#c0392b", "start"))
    if have_C:
        s.append(text(30, 614, f"ξ = 45° + φ'/2 − ½(arcsen(sen i / sen φ') − i) = {xi:.2f}°   (φ' = {phi:.1f}°)", 11, "#27ae60", "start"))
    
    A2, E2, D2 = P2(0, 0), P2(-bh, H), P2(0, Y_D)
    s.append(text(850, 56, t("② Cunha morta E-D-A e impulso Iₐ em AD", "② Dead wedge E-D-A and thrust Iₐ on AD"), 12, "#1f4e79"))
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" fill="url(#rkH)" opacity="0.5"/>')
    if D_front > tb:
        fr2 = [P2(-B - 0.4, 0), P2(-B - 0.4, D_front), P2(xs0, D_front), P2(xs0, 0)]
        s.append(f'<polygon points="{pts(fr2)}" fill="#d2b48c" stroke="#8b6f47"/>')
        s.append(f'<polygon points="{pts(fr2)}" fill="url(#rkH)" opacity="0.35"/>')
    
    dead2 = [P2(xs1, 0), E2, D2, A2]
    s.append(f'<polygon points="{pts(dead2)}" fill="#d9d9d9" stroke="none"/>')
    s.append(wall(P2))
    x_gr = 0.30 * Y_D
    s.append(line(E2, P2(x_gr, Y_D + x_gr * tan_i), "#6b4a2f", 2.4))
    s.append(line(A2, D2, "#5d3a1f", 2.4, "7,4"))
    cx2 = (sum(p[0] for p in dead2) / 4.0)
    cy2 = (sum(p[1] for p in dead2) / 4.0)
    s.append(text(cx2, cy2, t("cunha morta", "dead wedge"), 12, "#1f4e79", "middle", extra=f' transform="rotate(-90 {cx2:.1f} {cy2:.1f})"'))
    
    Lmax = 92.0
    ci, si = math.cos(i_r), math.sin(i_r)
    tail_A = (A2[0] + Lmax * ci, A2[1] - Lmax * si)
    s.append(f'<polygon points="{pts([D2, A2, tail_A])}" fill="rgba(192,57,43,0.14)" stroke="#c0392b" stroke-width="1.5"/>')
    for f in (0.12, 0.22, 0.45, 0.56, 0.67, 0.78, 0.89):
        head = (A2[0], A2[1] + (D2[1] - A2[1]) * f)
        L = Lmax * (1.0 - f)
        tl = (head[0] + L * ci, head[1] - L * si)
        s.append(line(tl, (head[0] + 2, head[1]), "#c0392b", 1.3, None, ' marker-end="url(#rkR)"'))
    
    Pm = (A2[0], A2[1] + (D2[1] - A2[1]) / 3.0)
    Lr = Lmax * 1.05
    tl = (Pm[0] + Lr * ci, Pm[1] - Lr * si)
    s.append(line(tl, Pm, "#c0392b", 3.0, None, ' marker-end="url(#rkR)"'))
    s.append(line(Pm, (Pm[0] + 70, Pm[1]), "#555", 1, "2,3"))
    if i > 0.05:
        s.append(arc(Pm, 50.0, 0.0, i, "#1f77b4"))
        s.append(arc_label(Pm, 50.0, 0.0, max(i, 8.0), "i", "#1f77b4", 11))
    
    xh = A2[0] + Lmax * ci + 28
    s.append(line(D2, (xh + 8, D2[1]), "#555", 1, "2,3"))
    s.append(line(A2, (xh + 8, A2[1]), "#555", 1, "2,3"))
    s.append(dim_v(xh, A2[1], D2[1], "h''"))
    s.append(text(Pm[0] - 8, Pm[1] + 4, "h''/3", 10, "#c0392b", "end"))
    for pnt, nm, dx, dy in ((A2, "A", 6, 20), (D2, "D", 4, -10), (E2, "E", -14, -8)):
        s.append(dot(pnt))
        s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))
    
    s.append(text(660, 578, f"h'' = {h_uso:.2f} m  |  Ka = {Ka:.4f}  |  i = {i:.1f}°", 11, "#1f77b4", "start"))
    s.append(text(660, 596, f"IaH,d = {IaH_d:.1f} kN/m", 11, "#c0392b", "start"))
    s.append('</svg>')
    return "".join(s)

def _svg_pormenorizacao_consola(B, bt, bh, ts, tb, HR, arma, lang="pt"):
    t = lambda pt, en: pt if lang == "pt" else en
    esc = min(58.0, 540.0 / B)
    cov = 9.0
    x0, ytop = 170.0, 40.0
    Hs = HR
    ytb = ytop + Hs * esc
    yb = ytb + tb * esc
    xs0 = x0 + bt * esc
    xs1 = xs0 + ts * esc
    xr = x0 + B * esc
    W_svg, H_svg = int(xr + 220), int(yb + 120)
    faceHeel = arma.get('face_bh', 'Superior')
    faceToe = arma.get('face_bt', 'Inferior')
    yH = ytb + cov + 2 if faceHeel == "Superior" else yb - cov - 2
    yHd = yH + 8 if faceHeel == "Superior" else yH - 8
    yT = yb - cov - 2 if faceToe == "Inferior" else ytb + cov + 2
    yTd = yT - 8 if faceToe == "Inferior" else yT + 8
    
    s = [f'<svg width="{W_svg}" height="{H_svg}" viewBox="0 0 {W_svg} {H_svg}" xmlns="http://www.w3.org/2000/svg" style="background:#fdfefe;border:1px solid #bbb;border-radius:6px;">']
    s.append(_defs())
    s.append(f'<text x="{W_svg/2}" y="20" text-anchor="middle" font-size="13" font-weight="bold">{t("PORMENORIZACAO — CORTE TRANSVERSAL","DETAILING — CROSS SECTION")}</text>')
    s.append(f'<polygon points="{x0},{yb} {x0},{ytb} {xs0},{ytb} {xs0},{ytop} {xs1},{ytop} {xs1},{ytb} {xr},{ytb} {xr},{yb}" fill="#eaecee" stroke="#333" stroke-width="2"/>')
    s.append(f'<polygon points="{x0+cov},{yb-cov} {x0+cov},{ytb+cov} {xs0+cov},{ytb+cov} {xs0+cov},{ytop+cov} {xs1-cov},{ytop+cov} {xs1-cov},{ytb+cov} {xr-cov},{ytb+cov} {xr-cov},{yb-cov}" fill="none" stroke="#922b21" stroke-width="1.3"/>')
    s.append(f'<line x1="{xs1-cov-2}" y1="{ytop+cov+4}" x2="{xs1-cov-2}" y2="{ytb+cov}" stroke="#c0392b" stroke-width="3"/>')
    s.append(f'<line x1="{xs1+2}" y1="{yH}" x2="{xr-cov-4}" y2="{yH}" stroke="#c0392b" stroke-width="3"/>')
    s.append(f'<line x1="{x0+cov+4}" y1="{yT}" x2="{xs0-2}" y2="{yT}" stroke="#c0392b" stroke-width="3"/>')
    
    def dots(xs, ys, r=3.0):
        return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2471a3"/>' for x, y in zip(xs, ys))
    
    n = 6
    ys_stem = [ytop + cov + 8 + (ytb - ytop - 2 * cov - 16) * k / n for k in range(n + 1)]
    s.append(dots([xs0 + cov + 2] * (n + 1), ys_stem))
    s.append(dots([xs1 + 12 + (xr - xs1 - 2 * cov - 24) * k / 4 for k in range(5)], [yHd] * 5))
    s.append(dots([x0 + cov + 12 + (xs0 - x0 - 2 * cov - 24) * k / 4 for k in range(5)], [yTd] * 5))
    
    R, Az = "#c0392b", "#2471a3"
    P_lbl = t("P", "M")
    D_lbl = t("D", "S")
    
    def leader(x1, y1, x2, y2, txt, tx, ty, cor):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{cor}" stroke-width="1"/><text x="{tx}" y="{ty}" font-size="12" fill="{cor}" font-weight="bold">{txt}</text>'
    
    s.append(leader(xs1 - cov - 2, ytop + 45, xs1 + 60, ytop + 35, f"1 {arma['m1']} ({P_lbl})", xs1 + 66, ytop + 39, R))
    s.append(leader(xs0 + cov + 2, ytop + 65, xs0 - 60, ytop + 55, f"2 {arma['m2']} ({D_lbl})", xs0 - 165, ytop + 59, Az))
    s.append(leader((xs1 + xr) / 2, yH, (xs1 + xr) / 2 + 40, ytb - 30, f"3 {arma['m3']} ({P_lbl})", xr + 15, ytb - 26, R))
    s.append(leader((xs1 + xr) / 2 - 20, yHd, (xs1 + xr) / 2 - 60, ytb + 45, f"4 {arma['m4']} ({D_lbl})", xr + 15, ytb + 49, Az))
    s.append(leader((x0 + xs0) / 2, yT, (x0 + xs0) / 2 - 40, yb - 30, f"5 {arma['m5']} ({P_lbl})", x0 - 165, yb - 26, R))
    s.append(leader((x0 + xs0) / 2 + 20, yTd, (x0 + xs0) / 2 + 60, yb + 20, f"6 {arma['m6']} ({D_lbl})", x0 - 165, yb + 24, Az))
    
    s.append(f'<text x="{x0}" y="{yb+58}" font-size="11">bt = {bt:.2f} m</text>')
    s.append(f'<text x="{xs0}" y="{yb+58}" font-size="11">ts = {ts*100:.0f} cm</text>')
    s.append(f'<text x="{xs1}" y="{yb+58}" font-size="11">bh = {bh:.2f} m</text>')
    s.append(f'<text x="{x0}" y="{yb+76}" font-size="11" font-weight="bold">B = {B:.2f} m | tb = {tb*100:.0f} cm | HR = {HR:.2f} m</text>')
    s.append('</svg>')
    return "".join(s)

def _svg_laje_vertical(Hs, q_top, q_base, M, V, titulo):
    top, bot = 40, 380
    xe = 190
    setas = ""
    for k in range(8):
        y = top + (bot - top) * k / 7
        qq = q_top + (q_base - q_top) * k / 7
        comp = 20 + 90 * (qq / max(q_base, 1e-6))
        setas += f'<line x1="{xe+comp}" y1="{y}" x2="{xe+2}" y2="{y}" stroke="red" stroke-width="1.5"/><polygon points="{xe+2},{y} {xe+10},{y-3} {xe+10},{y+3}" fill="red"/>'
    hach = " ".join([f'<line x1="{120+i*12}" y1="{bot+18}" x2="{112+i*12}" y2="{bot+28}" stroke="black" stroke-width="1.5"/>' for i in range(8)])
    return (f'<svg width="380" height="460" style="background:#f8f9fa;border:1px solid #ddd;border-radius:8px;">'
            f'<text x="190" y="20" text-anchor="middle" font-size="13" font-weight="bold">{titulo}</text>'
            f'<rect x="150" y="{top}" width="40" height="{bot-top}" fill="#d3d3d3" stroke="#333" stroke-width="2"/>'
            f'<line x1="120" y1="{bot}" x2="220" y2="{bot}" stroke="#333" stroke-width="4"/>{hach}{setas}'
            f'<text x="{xe+115}" y="{top+12}" fill="red" font-size="11">q={q_top:.1f} kPa</text>'
            f'<text x="{xe+115}" y="{bot-4}" fill="red" font-size="11">q={q_base:.1f} kPa</text>'
            f'<text x="60" y="210" fill="blue" font-size="12" font-weight="bold">Hs={Hs:.2f} m</text>'
            f'<text x="90" y="{bot+45}" fill="green" font-size="11" font-weight="bold">Msd={M:.1f} kNm/m | Vsd={V:.1f} kN/m</text></svg>')

def _svg_laje_horizontal(L, q_desce, q_sobe, q_liq, sentido, M, V, titulo, fixo):
    x0, x1, y0, y1 = 60, 400, 150, 190
    setas = ""
    for k in range(8):
        x = x0 + (x1 - x0) * k / 7
        if sentido == "baixo":
            setas += f'<line x1="{x}" y1="{y0-45}" x2="{x}" y2="{y0-3}" stroke="blue" stroke-width="1.5"/><polygon points="{x},{y0-2} {x-3},{y0-10} {x+3},{y0-10}" fill="blue"/>'
        else:
            setas += f'<line x1="{x}" y1="{y1+45}" x2="{x}" y2="{y1+3}" stroke="red" stroke-width="1.5"/><polygon points="{x},{y1+2} {x-3},{y1+10} {x+3},{y1+10}" fill="red"/>'
    hx = x1 if fixo == "dir" else x0
    hach = " ".join([f'<line x1="{hx}" y1="{100+i*14}" x2="{hx+10 if fixo=="dir" else hx-10}" y2="{92+i*14}" stroke="black" stroke-width="1.5"/>' for i in range(8)])
    return (f'<svg width="470" height="300" style="background:#f8f9fa;border:1px solid #ddd;border-radius:8px;">'
            f'<text x="235" y="20" text-anchor="middle" font-size="13" font-weight="bold">{titulo}</text>'
            f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#d3d3d3" stroke="#333" stroke-width="2"/>'
            f'<line x1="{hx}" y1="100" x2="{hx}" y2="240" stroke="#333" stroke-width="4"/>{hach}{setas}'
            f'<text x="{x0}" y="{y0-55}" fill="blue" font-size="11">q_down={q_desce:.1f} kPa</text>'
            f'<text x="{x0}" y="{y1+62}" fill="red" font-size="11">q_up={q_sobe:.1f} kPa</text>'
            f'<text x="{x0}" y="{y1+80}" font-size="11" font-weight="bold">q_net={abs(q_liq):.1f} kPa</text>'
            f'<text x="60" y="292" fill="green" font-size="11" font-weight="bold">Msd={M:.1f} kNm/m | Vsd={V:.1f} kN/m</text></svg>')

def formulario_muro_consola():
    lang = st.session_state.get("language", "pt")
    if "fase_consola" not in st.session_state:
        st.session_state.fase_consola = "geotecnica"
    
    st.markdown(f"#### {get_text('consola_dados', lang)}")
    st.markdown(carregar_imagem_local("assets/Picture3.png", 700), unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;margin:6px 0 18px 0;"><p style="color:#555;font-size:13px;">
    <b>{get_text('legenda', lang)}:</b> {get_text('consola_legenda_corpo', lang)}</p></div>""", unsafe_allow_html=True)
    st.divider()
    
    st.markdown(f"#### {get_text('consola_ec7', lang)}")
    combo_ec7 = st.radio(get_text("combinacao", lang), [get_text("combinacao1", lang), get_text("combinacao2", lang)], index=1, horizontal=True, key="ec7_consola")
    if get_text("combinacao1", lang) in combo_ec7:
        g_G_unfav, g_G_fav, g_Q = 1.35, 1.00, 1.50
        g_phi, g_c, g_cu = 1.00, 1.00, 1.00
        g_Rh, g_Rv = 1.00, 1.00
    else:
        g_G_unfav, g_G_fav, g_Q = 1.00, 1.00, 1.30
        g_phi, g_c, g_cu = 1.25, 1.25, 1.40
        g_Rh, g_Rv = 1.00, 1.00
    st.divider()
    
    st.markdown(f"#### {get_text('consola_geom', lang)}")
    c1, c2, c3, c4 = st.columns(4)
    with c1: H = campo_latex("altura_total", "H", "unidade_m", "H_consola", 5.0, minimo=1.0, passo=0.1, lang=lang)
    with c2: tb = campo_latex("espessura_base", "t_b", "unidade_m", "tb_consola", 0.50, minimo=0.10, passo=0.05, lang=lang)
    with c3: bt = campo_latex("comprimento_biqueira", "b_t", "unidade_m", "bt_consola", 1.20, minimo=0.10, passo=0.10, lang=lang)
    with c4: bh = campo_latex("comprimento_talao", "b_h", "unidade_m", "bh_consola", 1.20, minimo=0.10, passo=0.10, lang=lang)
    
    c1, c2 = st.columns(2)
    with c1: ts = campo_latex("espessura_stem", "t_s", "unidade_m", "ts_consola", 0.40, minimo=0.10, passo=0.05, lang=lang)
    with c2: i = campo_latex("lbl_inclinacao", "i", "unidade_graus", "i_consola", 0.0, minimo=0.0, passo=1.0, lang=lang)
    
    B = bt + ts + bh
    HR = H - tb
    if HR < 0.1:
        st.error(get_text("erro_d", lang, HR=HR))
        st.stop()
    st.success(get_text("verificacao_b", lang, bt=bt, bh=bh, ts=ts, B=B) + " &nbsp;|&nbsp; " + get_text("verificacao_hr", lang, H=H, D=tb, HR=HR))
    st.divider()
    
    st.markdown(f"#### {get_text('consola_solo_ativo', lang)}")
    c1, c2 = st.columns(2)
    with c1:
        gamma_ativo = campo_latex("lbl_gamma", r"\gamma", "unidade_knm3", "g_at_consola", 18.0, minimo=10.0, passo=0.5, lang=lang)
        gamma_sat_ativo = campo_latex("lbl_gamma_sat", r"\gamma_{sat}", "unidade_knm3", "gsat_at_consola", 20.0, minimo=10.0, passo=0.5, lang=lang)
        phi_ativo = campo_latex("lbl_phi", r"\phi'", "unidade_graus", "phi_at_consola", 30.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
    with c2:
        c_ativo = campo_latex("lbl_c", "c'", "unidade_kpa", "c_at_consola", 0.0, minimo=0.0, passo=1.0, lang=lang)
        q_ativo = campo_latex("lbl_q", "q", "unidade_kpa", "q_at_consola", 10.0, minimo=0.0, passo=1.0, lang=lang)
    st.divider()
    
    st.markdown(f"#### {get_text('consola_solo_fund', lang)}")
    fund = get_text("sufixo_fund", lang)
    c1, c2 = st.columns(2)
    with c1:
        gamma_fund = campo_latex("lbl_gamma", r"\gamma", "unidade_knm3", "g_fund_consola", 18.0, minimo=10.0, passo=0.5, lang=lang, sufixo=f"— {fund}")
        phi_fund = campo_latex("lbl_phi", r"\phi'_{d,fund}", "unidade_graus", "phi_fund_consola", 28.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang, sufixo=f"— {fund}")
        c_fund = campo_latex("lbl_c", "c'_{d,fund}", "unidade_kpa", "c_fund_consola", 2.0, minimo=0.0, passo=1.0, lang=lang, sufixo=f"— {fund}")
    with c2:
        cu_fund = campo_latex("lbl_cu", "c_{u,fund}", "unidade_kpa", "cu_fund_consola", 0.0, minimo=0.0, passo=1.0, lang=lang, sufixo=f"— {fund}")
        delta_b = campo_latex("lbl_delta_b", r"\delta_b", "unidade_graus", "delta_b_consola", 20.0, minimo=0.0, maximo=60.0, passo=1.0, lang=lang)
    st.caption(get_text("info_delta_b", lang))
    st.divider()
    
    st.markdown(f"#### {get_text('consola_metodo', lang)}")
    c1, c2 = st.columns(2)
    with c1: metodo = st.radio(get_text("metodo", lang), ["Rankine", "Coulomb"], horizontal=True, key="met_consola")
    with c2: st.caption("Rankine (slide 100)" if metodo == "Rankine" else "Coulomb (slide 99)")
    st.divider()
    
    st.markdown(f"#### {get_text('consola_materiais', lang)}")
    c1, c2 = st.columns(2)
    with c1:
        classe_betao = st.selectbox(get_text("classe_betao", lang), ["B20", "B25", "B30", "B35", "B40"], index=1, key="bet_consola")
        tipo_aco = st.selectbox(get_text("tipo_aco", lang), ["A235", "A400", "A500"], index=1, key="aco_consola")
    with c2: recobrimento = campo_latex("recobrimento", "c_{nom}", "unidade_mm", "rec_consola", 50, minimo=20, maximo=80, passo=5, lang=lang)
    st.divider()
    
    if st.session_state.fase_consola == "geotecnica":
        if st.button(get_text("consola_btn_geo", lang), type="primary", use_container_width=True, key="btn_calc_geo"):
            calcular_muro_consola(H, HR, B, bt, bh, ts, tb, i, gamma_ativo, gamma_sat_ativo, phi_ativo, c_ativo, q_ativo, gamma_fund, phi_fund, c_fund, cu_fund, delta_b, metodo, combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv, classe_betao, tipo_aco, recobrimento)
    else:
        dados = st.session_state.get('dados_consola', {})
        if dados:
            dimensionar_armaduras_consola(**dados)
        else:
            st.error("Dados nao encontrados / Data not found.")
        st.divider()
        st.button(get_text("consola_btn_voltar_geo", lang), use_container_width=True, on_click=voltar_para_geotecnica)

def calcular_muro_consola(H, HR, B, bt, bh, ts, tb, i, gamma_ativo, gamma_sat_ativo, phi_ativo, c_ativo, q_ativo, gamma_fund, phi_fund, c_fund, cu_fund, delta_b, metodo, combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv, classe_betao, tipo_aco, recobrimento):
    lang = st.session_state.get("language", "pt")
    st.divider()
    st.markdown(f"### {get_text('consola_res_geo', lang)}")
    
    tan_i = math.tan(math.radians(i))
    phi_ativo_d = calcular_phi_d(phi_ativo, g_phi)
    phi_fund_d = calcular_phi_d(phi_fund, g_phi)
    c_fund_d = c_fund / g_c
    cu_fund_d = cu_fund / g_cu
    q_d = q_ativo * g_Q
    i_rad = math.radians(i)
    phi_d_rad = math.radians(phi_ativo_d)
    Hs = H - tb
    h_uso = None
    
    if metodo == "Rankine":
        Ka = Ka_rankine_slide100(phi_d_rad, i_rad)
        Kaq = Ka
        alpha = 90.0
        beta = 90.0
        y_linha2 = bh * tan_i
        h_uso = H + y_linha2
        theta = i_rad
        st.markdown(f"##### {get_text('coeficiente_impulso', lang)} — Rankine (slide 100)")
        if i > 0:
            st.latex(r"K_{a\gamma} = \frac{\cos i - \sqrt{\cos^2 i - \cos^2\phi'_d}}{\cos i + \sqrt{\cos^2 i - \cos^2\phi'_d}}\,\cos i")
            st.latex(r"K_{aq} = K_{a\gamma}")
        else:
            st.latex(r"K_a = \frac{1 - \sin\phi'_d}{1 + \sin\phi'_d}")
            st.latex(r"K_{aq} = K_a")
        st.write(rf"- $\phi'_d = {phi_ativo_d:.2f}^\circ$, $i = {i:.1f}^\circ$ $\rightarrow$ $K_a = K_{{aq}} = \mathbf{{{Ka:.4f}}}$")
        st.write(rf"- $y'' = b_h \tan i = {bh:.2f} \tan({i:.1f}^\circ) = {y_linha2:.3f}\ \mathrm{{m}}$")
        st.write(rf"- $h'' = H + y'' = {H:.2f} + {y_linha2:.3f} = \mathbf{{{h_uso:.3f}}}\ \mathrm{{m}}$")
    else:
        alpha = coulomb_alpha(phi_ativo_d, i)
        beta = 180.0 - alpha
        Ka = coulomb_K(phi_ativo_d, i, alpha)
        Kaq = coulomb_Kaq(Ka, beta, i)
        Y_D = H + bh * tan_i
        alpha_E = math.degrees(math.atan2(H, bh)) if bh > 1e-9 else 90.0
        tol = 0.05
        a_r = math.radians(alpha)
        if alpha < alpha_E - tol:
            h_uso = bh * math.tan(a_r)
            caso_B = "B no tardoz do stem ($h' < H$)" if lang == "pt" else "B on the stem back face ($h' < H$)"
        elif abs(alpha - alpha_E) <= tol:
            h_uso = H
            caso_B = "$B \\equiv E$ ($h' = H$)"
        else:
            den_B = math.sin(a_r) + math.cos(a_r) * tan_i
            t_B0 = Y_D / den_B if den_B > 1e-9 else 0.0
            h_uso = t_B0 * math.sin(a_r)
            caso_B = "B no terreno ($h' > H$)" if lang == "pt" else "B on the ground surface ($h' > H$)"
        theta = math.radians(phi_ativo_d)
        st.markdown(f"##### {get_text('coeficiente_impulso', lang)} — Coulomb (slide 99)")
        st.latex(get_text("formula_alpha_coulomb", lang))
        st.latex(get_text("formula_ka_coulomb_consola", lang))
        st.latex(get_text("formula_kaq_coulomb", lang))
        st.write(rf"- $\alpha = {alpha:.2f}^\circ, \quad \beta = {beta:.2f}^\circ, \quad \delta = \phi'_d = {phi_ativo_d:.2f}^\circ$")
        st.write(rf"- $\arctan(H/b_h) = {alpha_E:.2f}^\circ \;\rightarrow\;$ {caso_B}")
        st.write(rf"- $K_a = \mathbf{{{Ka:.4f}}},\quad K_{{aq}} = \mathbf{{{Kaq:.4f}}}$")
        st.write(rf"- $h' = \mathbf{{{h_uso:.3f}}}\ \mathrm{{m}}$ " + ("(altura de B — mesmo valor do Esquema Final)" if lang == "pt" else "(height of B — same value as in the Final Scheme)"))
    
    st.markdown(f"##### {get_text('impulso_ativo', lang)}")
    st.write(rf"- $q = {q_ativo:.2f}\ \mathrm{{kPa}}\;\rightarrow\;q_d = q\cdot\gamma_Q = {q_d:.2f}\ \mathrm{{kPa}}$")
    if metodo == "Rankine":
        st.latex(r"I_a = \tfrac{1}{2} K_{a\gamma}\,\gamma\, h''^2 + K_{aq}\, q_d\, h''")
    else:
        st.latex(r"I_a = \tfrac{1}{2} K_{a\gamma}\,\gamma\, h'^2 + K_{aq}\, q_d\, h'")
    st.write(rf"- {('altura usada' if lang == 'pt' else 'height used')}: ${'h\'\'' if metodo == 'Rankine' else 'h\prime'} = {h_uso:.3f}\ \mathrm{{m}}$")
    
    Ia_solo = 0.5 * Ka * gamma_ativo * h_uso ** 2
    Ia_sob = Kaq * q_d * h_uso
    Ia_caract = Ia_solo + Ia_sob
    Ia_d = Ia_caract * g_G_unfav
    IaH_d = Ia_d * math.cos(theta)
    IaV_d = Ia_d * math.sin(theta)
    
    st.write(rf"- $I_{{a,\gamma}} = {Ia_solo:.2f}\ \mathrm{{kN/m}}\quad|\quad I_{{a,q}} = {Ia_sob:.2f}\ \mathrm{{kN/m}}$")
    st.write(rf"- $I_{{a,d}} = \mathbf{{{Ia_d:.2f}}}\ \mathrm{{kN/m}}\quad|\quad I_{{aH,d}} = \mathbf{{{IaH_d:.2f}}}\quad|\quad I_{{aV,d}} = \mathbf{{{IaV_d:.2f}}}$")
    st.divider()
    
    W_stem_d = 25.0 * ts * Hs * g_G_fav
    W_base_d = 25.0 * B * tb * g_G_fav
    arm_sob = B - bh / 2
    
    if metodo == "Coulomb":
        tan_a = math.tan(math.radians(alpha))
        alpha_E = math.degrees(math.atan2(H, bh)) if bh > 1e-9 else 90.0
        d_fora = min(bh, tb / tan_a) if tan_a > 1e-9 else bh
        x3 = max(-bh, -tb / tan_a)
        if alpha < alpha_E:
            h_linha = bh * tan_a
            pts = [(-bh, tb), (-bh, max(h_linha, tb)), (x3, tb)]
        else:
            Y_Dl = H + bh * tan_i
            den_B = math.sin(math.radians(alpha)) + math.cos(math.radians(alpha)) * tan_i
            t_B = Y_Dl / den_B if den_B > 1e-9 else 0.0
            X_B = -t_B * math.cos(math.radians(alpha))
            Y_B = t_B * math.sin(math.radians(alpha))
            h_linha = Y_B
            pts = [(-bh, tb), (-bh, H), (max(-bh, min(0.0, X_B)), Y_B), (x3, tb)]
        
        s2 = 0.0; sx = 0.0
        n = len(pts)
        for k in range(n):
            x1, y1 = pts[k]; x2, y2 = pts[(k + 1) % n]
            cr = x1 * y2 - x2 * y1
            s2 += cr; sx += cr * (x1 + x2)
        
        A_cunha = abs(s2) / 2.0
        cx = (sx / (3.0 * s2)) if abs(s2) > 1e-12 else -bh / 2.0
        A_fora = max(0.0, h_linha * bh - A_cunha)
        base_cunha = bh - d_fora
        W_solo_bh_d = gamma_ativo * A_cunha * g_G_fav
        arm_bh = B + cx
        
        st.write(rf"- {('Cunha morta' if lang == 'pt' else 'Dead wedge')}: $h' = {h_linha:.2f}\ \mathrm{{m}}\quad|\quad d_{{fora}} = {d_fora:.2f}\ \mathrm{{m}}\quad|\quad b_{{cunha}} = b_h - d_{{fora}} = {base_cunha:.2f}\ \mathrm{{m}}$")
        st.write(rf"- $A_{{cunha}} = h'\cdot b_h - A_{{fora}} = {h_linha*bh:.2f} - {A_fora:.2f} = \mathbf{{{A_cunha:.2f}}}\ \mathrm{{m^2/m}}\;\rightarrow\;W_{{solo,b_h}} = \gamma\cdot A_{{cunha}} = \mathbf{{{W_solo_bh_d/g_G_fav:.2f}}}\ \mathrm{{kN/m}}$ " + ("(característica)" if lang == "pt" else "(characteristic)"))
    else:
        solo_bh_h = Hs + bh * tan_i / 2
        W_solo_bh_d = gamma_ativo * bh * solo_bh_h * g_G_fav
        arm_bh = B - bh / 2
    
    W_sob_d = g_Q * q_ativo * bh
    W_total_d = W_stem_d + W_base_d + W_solo_bh_d + W_sob_d
    
    st.markdown(f"##### {get_text('consola_pesos', lang)}")
    st.write(rf"- $W_{{stem,d}} = \mathbf{{{W_stem_d:.1f}}}\quad|\quad W_{{base,d}} = \mathbf{{{W_base_d:.1f}}}\quad|\quad W_{{solo,b_h,d}} = \mathbf{{{W_solo_bh_d:.1f}}}\quad|\quad W_{{q,d}} = \mathbf{{{W_sob_d:.1f}}}\qquad\left[\mathrm{{kN/m}}\right]$")
    st.write(rf"- $W_{{total,d}} = \mathbf{{{W_total_d:.2f}}}\ \mathrm{{kN/m}}$")
    st.divider()
    
    M_est = (W_base_d * B / 2 + W_stem_d * (bt + ts / 2) + W_solo_bh_d * arm_bh + W_sob_d * arm_sob + IaV_d * B)
    M_derr = IaH_d * h_uso / 3
    V_d = W_total_d + IaV_d
    x_R = (M_est - M_derr) / V_d if V_d > 0 else 0
    e_cc = x_R - B / 2
    e = abs(e_cc)
    B_linha = max(0.0, B - 2 * e)
    
    st.markdown(f"##### {get_text('consola_momentos', lang)}")
    st.latex(r"e = \frac{B}{2} - \frac{M_{est} - M_{derr}}{V_d}")
    st.write(rf"- $M_{{est}} = {M_est:.2f}\ \mathrm{{kNm/m}}\quad|\quad M_{{derr}} = {M_derr:.2f}\ \mathrm{{kNm/m}}$")
    st.write(rf"- $V_d = {V_d:.2f}\ \mathrm{{kN/m}}\quad|\quad e = \mathbf{{{e:.3f}}}\ \mathrm{{m}}\quad|\quad B' = {B_linha:.3f}\ \mathrm{{m}}$")
    
    if e <= B / 6:
        st.success(get_text("dentro_nucleo", lang, B6=B / 6, e=e))
    else:
        st.warning(get_text("fora_nucleo", lang, B6=B / 6, e=e))
    st.divider()
    
    ok_derr = M_est >= M_derr
    if cu_fund_d > 0:
        Rd_h = cu_fund_d * B_linha / g_Rh
        tipo_cis = get_text("cis_nao_drenada", lang)
    else:
        Rd_h = V_d * math.tan(math.radians(delta_b)) / g_Rh
        tipo_cis = (get_text("cis_drenada", lang) + rf" ($\delta_b = {delta_b:.0f}^\circ$)")
    
    ok_desliz = (Rd_h / IaH_d) >= 1.0 if IaH_d > 0 else True
    
    from calculos.meyerhof_tabela import meyerhof_N
    if cu_fund_d == 0:
        Nc, Nq, Ng = meyerhof_N(phi_fund_d)
        q_Rd = (c_fund_d * Nc + gamma_fund * tb * Nq + 0.5 * gamma_fund * B_linha * Ng) / g_Rv
    else:
        Nc, Nq, Ng = 5.14, 1.0, 0.0
        q_Rd = 5.14 * cu_fund_d / g_Rv
    
    sigma_bh = (V_d / B) * (1 + 6 * e_cc / B)
    sigma_bt = (V_d / B) * (1 - 6 * e_cc / B)
    sigma_max_d = max(sigma_bh, sigma_bt)
    ok_carga = q_Rd >= sigma_max_d
    
    st.markdown(f"##### {get_text('consola_verif', lang)}")
    if cu_fund_d == 0:
        st.write(rf"- Meyerhof: $\phi'_{{d,fund}} = {phi_fund_d:.2f}^\circ \;\rightarrow\; N_c = {Nc:.2f},\; N_q = {Nq:.2f},\; N_\gamma = {Ng:.2f}$")
    st.latex(r"M_{stb,d} \geq M_{dst,d} \quad;\quad H_d \leq R_d \quad;\quad q_{R,d} \geq \sigma_{max,d}")
    
    st.write(rf"- **{get_text('derrubamento', lang)}**: $M_{{est}} = {M_est:.1f} \geq M_{{derr}} = {M_derr:.1f}$ " + ("✅" if ok_derr else "❌"))
    st.write(rf"- **{get_text('deslizamento', lang)}** ({tipo_cis}): $R_{{d,h}} = {Rd_h:.1f} \geq H_d = {IaH_d:.1f}$ " + ("✅" if ok_desliz else "❌"))
    st.write(rf"- **{get_text('capacidade_carga', lang)}**: $q_{{R,d}} = {q_Rd:.1f} \geq \sigma_{{max,d}} = {sigma_max_d:.1f}\ \mathrm{{kPa}}$ " + ("✅" if ok_carga else "❌"))
    st.divider()
    
    svg_estrutura = _svg_estrutura_consola(H, HR, B, bt, bh, ts, tb, i, lang)
    if metodo == "Rankine":
        svg_esquema = _svg_esquema_rankine(H, HR, B, bt, bh, ts, tb, i, Ka, h_uso, IaH_d, W_total_d, q_ativo, lang, phi_d=phi_ativo_d)
    else:
        svg_esquema = _svg_esquema_coulomb(H, HR, B, bt, bh, ts, tb, i, alpha, beta, Ka, Kaq, h_uso, IaH_d, W_total_d, q_ativo, lang, phi_d=phi_ativo_d)
    
    st.markdown(f"### {get_text('consola_estrutura', lang)}")
    st.markdown(svg_estrutura, unsafe_allow_html=True)
    st.markdown(f"### {get_text('consola_esquema_final', lang)} — {metodo}")
    st.markdown(svg_esquema, unsafe_allow_html=True)
    
    if ok_derr and ok_desliz and ok_carga:
        st.success(get_text("muro_satisfaz", lang))
        st.session_state.dados_consola = dict(
            H=H, HR=HR, B=B, bt=bt, bh=bh, ts=ts, tb=tb, i=i, Hs=Hs,
            gamma_ativo=gamma_ativo, gamma_sat_ativo=gamma_sat_ativo, phi_ativo=phi_ativo, c_ativo=c_ativo, q_ativo=q_ativo,
            gamma_passivo=gamma_ativo, gamma_sat_passivo=gamma_sat_ativo, phi_passivo=phi_ativo, c_passivo=0.0, z_w_passivo=0.0,
            gamma_fund=gamma_fund, phi_fund=phi_fund, c_fund=c_fund, cu_fund=cu_fund, delta_b=delta_b,
            metodo=metodo, delta=0.0, combo_ec7=combo_ec7, g_G_unfav=g_G_unfav, g_G_fav=g_G_fav, g_Q=g_Q,
            classe_betao=classe_betao, tipo_aco=tipo_aco, recobrimento=recobrimento,
            Ka=Ka, Kaq=Kaq, alpha=alpha, h_uso=h_uso, IaH_d=IaH_d, IaV_d=IaV_d, Ia_caract=Ia_caract, phi_ativo_d=phi_ativo_d,
            V_d=V_d, e=e_cc, B_linha=B_linha, sigma_bh=sigma_bh, sigma_bt=sigma_bt, W_total_d=W_total_d, M_est=M_est, M_derr=M_derr,
            D_passivo=0.0, q_d=q_d, svg_esquema=svg_esquema, svg_estrutura=svg_estrutura,
        )
        st.divider()
        st.button(get_text("consola_btn_arm", lang), type="primary", use_container_width=True, on_click=prosseguir_para_armaduras, key="btn_arm")
    else:
        st.error(get_text("muro_nao_satisfaz", lang))

def _escolher_armadura(As_nec, diam_min=10, esp_max=350):
    from calculos.tabela48 import AREA_VARAO, ESPACAMENTOS_COMERCIAIS
    melhor = None
    for d in AREA_VARAO:
        if d < diam_min: continue
        for spp in ESPACAMENTOS_COMERCIAIS:
            if spp > esp_max: continue
            A = AREA_VARAO[d] * 1000.0 / spp
            if A >= As_nec * 0.98 and (melhor is None or A < melhor[2]):
                melhor = (d, spp, A)
    if melhor is None:
        melhor = (25, 100, AREA_VARAO[25] * 10.0)
    return melhor

def _fmt(d, s):
    return f"Ø{d}@{s/10:g}cm"

def _cm2(mm2):
    return mm2 / 100.0

def dimensionar_armaduras_consola(
    H, HR, B, bt, bh, ts, tb, i, Hs,
    gamma_ativo, gamma_sat_ativo, phi_ativo, c_ativo, q_ativo,
    gamma_passivo, gamma_sat_passivo, phi_passivo, c_passivo, z_w_passivo,
    gamma_fund, phi_fund, c_fund, cu_fund, delta_b,
    metodo, delta, combo_ec7, g_G_unfav, g_G_fav, g_Q,
    classe_betao, tipo_aco, recobrimento,
    Ka, Kaq, alpha, h_uso, IaH_d, IaV_d, Ia_caract,
    V_d, e, B_linha, sigma_bh, sigma_bt,
    W_total_d, M_est, M_derr, D_passivo, q_d,
    svg_esquema=None, svg_estrutura=None, phi_ativo_d=None, **kw
):
    lang = st.session_state.get("language", "pt")
    st.divider()
    st.markdown(f"### {get_text('consola_dim_arm', lang)}")
    
    # Materiais
    fck = 0.8 * {"B20": 20, "B25": 25, "B30": 30, "B35": 35, "B40": 40}[classe_betao]
    fcd = fck / 1.5
    fctd = 0.30 * (fck ** (2 / 3)) / 1.5
    fyk = {"A235": 235, "A400": 400, "A500": 500}[tipo_aco]
    fsyd = fyk / 1.15
    fbd = 2.25 * fctd
    eta = {"A235": 1.4, "A400": 1.0, "A500": 0.8}[tipo_aco]
    rho = {"A235": 0.25, "A400": 0.15, "A500": 0.12}[tipo_aco] / 100.0
    tan_i = math.tan(math.radians(i))
    
    st.write(rf"- $f_{{cd}} = {fcd:.2f}$ | $f_{{ctd}} = {fctd:.2f}$ | "
             f"$f_{{bd}} = {fbd:.2f}$ | $f_{{syd}} = {fsyd:.2f}$ MPa")
    
    # Espessuras mínimas
    h_min_stem = max(2 * Hs / (30 * eta), 0.07)
    h_min_base = max(2 * max(bt, bh) / (30 * eta), 0.07)
    st.write(rf"- $h_{{min,stem}} = {h_min_stem*100:.1f}$ cm vs $t_s = {ts*100:.0f}$ cm "
             f"→ {'✅' if ts >= h_min_stem else '⚠️'}")
    st.write(rf"- $h_{{min,base}} = {h_min_base*100:.1f}$ cm vs $t_b = {tb*100:.0f}$ cm "
             f"→ {'✅' if tb >= h_min_base else '⚠️'}")
    
    # Fórmulas REBAP
    st.markdown("**Flexão Simples (Art. 52 REBAP)**")
    st.latex(r"\mu = \frac{M_{Ed}}{b\,d^2 f_{cd}}\;;\;\omega = \mu(1+\mu)\;;\;A_s = \frac{\omega\,b\,d\,f_{cd}}{f_{syd}}")
    st.markdown("**Armadura Mínima (Art. 90/104 REBAP)**")
    st.latex(r"A_{s,min} = \rho\,b\,d\quad;\quad \rho = " + 
             ("0.25\\%" if tipo_aco == "A235" else "0.15\\%" if tipo_aco == "A400" else "0.12\\%"))
    st.markdown("**Armadura Máxima (Art. 90.2 REBAP)**")
    st.latex(r"A_{s,max} = 0.04\,A_c = 0.04\,b\,h")
    st.markdown("**Armadura de Distribuição (Art. 108 REBAP)**")
    st.latex(r"A_{s,dist} = 0.20\,A_s")
    st.markdown("**Esforço Transverso (Art. 53 REBAP)**")
    st.latex(r"V_{Rd} = \eta\,\tau_1\,d\,b_1 \quad;\quad \eta = \max(1.0,\,1.6-d)")
    st.markdown("**Amarração (Art. 80 REBAP)**")
    st.latex(r"l_b = \frac{\phi}{4}\cdot\frac{f_{syd}}{f_{bd}}\;;\;l_{b,net} = l_b\cdot\frac{A_{s,cal}}{A_{s,ef}}\geq l_{b,min}")
    
    def seccao(Msd, Vsd, h_mm, elem_name):
        d = h_mm - recobrimento - 5
        mu = (Msd * 1e6) / (1000 * d * d * fcd) if Msd > 0 else 0.0
        w = mu * (1 + mu)
        As = w * 1000 * d * fcd / fsyd
        As_min = rho * 1000 * d
        As_max = 0.04 * 1000 * h_mm
        As_f = min(max(As, As_min), As_max)
        dm, sp, Aef = _escolher_armadura(As_f)
        d = h_mm - recobrimento - dm / 2
        dd, ss, Aef_d = _escolher_armadura(0.2 * As_f, diam_min=6)
        fac = max(0.6, 0.6 * (1.6 - d / 1000))
        VRd = fac * 0.6 * fctd * 1000 * d / 1000
        lb = max((dm / 4) * (fsyd / fbd) * (As / Aef if Aef else 1),
                 10 * dm, 100, 0.3 * (dm / 4) * (fsyd / fbd))
        As_dist = 0.20 * As_f
        return dict(d=d, mu=mu, w=w, As=As, As_min=As_min, As_max=As_max, As_f=As_f,
                    As_dist=As_dist, diam=dm, esp=sp, Aef=Aef, dd=dd, ee=ss, Aef_d=Aef_d,
                    VRd=VRd, ok_corte=VRd >= Vsd, ok_esp=sp <= min(1.5 * h_mm, 350), lb=lb,
                    elem=elem_name)
    
    res = []
    
    # 1) STEM
    p0 = Kaq * q_d
    p1 = Kaq * q_d + Ka * gamma_ativo * Hs
    M_stem = (Ka * gamma_ativo * Hs ** 3 / 6 + Kaq * q_d * Hs ** 2 / 2)
    V_stem = Ka * gamma_ativo * Hs ** 2 / 2 + Kaq * q_d * Hs
    r = seccao(M_stem, V_stem, ts * 1000, get_text("consola_stem", lang))
    r.update(face=get_text("consola_face_dir", lang), M=M_stem, V=V_stem, H_elem=Hs, label_H="H_s")
    res.append(r)
    st.markdown(f"#### 🧱 {get_text('consola_stem', lang)} ($H_s = {Hs:.2f}$ m)")
    st.write(rf"- $M_{{sd}} = {M_stem:.2f}$ kNm/m | $V_{{sd}} = {V_stem:.2f}$ kN/m")
    st.write(rf"- $A_{{s,calc}} = {_cm2(r['As']):.2f}$ cm²/m | "
             rf"$A_{{s,min}} = {_cm2(r['As_min']):.2f}$ cm²/m | "
             rf"$A_{{s,max}} = {_cm2(r['As_max']):.2f}$ cm²/m")
    st.write(rf"- **$A_s = {_cm2(r['As_f']):.2f}$ cm²/m** → {_fmt(r['diam'], r['esp'])}")
    st.write(rf"- $A_{{s,dist}} = 0.20\,A_s = {_cm2(r['As_dist']):.2f}$ cm²/m → {_fmt(r['dd'], r['ee'])}")
    st.success(f"✅ {_fmt(r['diam'], r['esp'])} | Dist: {_fmt(r['dd'], r['ee'])} | $l_b = {r['lb']:.0f}$ mm")
    
    # 2) TALÃO (bh)
    sig_stem_dir = sigma_bt + (sigma_bh - sigma_bt) * ((bt + ts) / B)
    q_down_bh = (g_Q * q_ativo + g_G_unfav * (gamma_ativo * (Hs + bh * tan_i / 2) + 25 * tb))
    q_up_bh = (sigma_bh + sig_stem_dir) / 2
    net_bh = q_up_bh - q_down_bh
    M_bh = abs(net_bh) * bh ** 2 / 2
    V_bh = abs(net_bh) * bh
    r = seccao(M_bh, V_bh, tb * 1000, get_text("consola_bh", lang))
    r.update(face=get_text("consola_face_sup", lang) if net_bh < 0 else get_text("consola_face_inf", lang),
             M=M_bh, V=V_bh, H_elem=bh, label_H="b_h")
    res.append(r)
    st.markdown(f"#### 🔹 {get_text('consola_bh', lang)} ($b_h = {bh:.2f}$ m)")
    st.write(rf"- $M_{{sd}} = {M_bh:.2f}$ kNm/m | $V_{{sd}} = {V_bh:.2f}$ kN/m")
    st.write(rf"- $A_{{s,calc}} = {_cm2(r['As']):.2f}$ cm²/m | "
             rf"$A_{{s,min}} = {_cm2(r['As_min']):.2f}$ cm²/m | "
             rf"$A_{{s,max}} = {_cm2(r['As_max']):.2f}$ cm²/m")
    st.write(rf"- **$A_s = {_cm2(r['As_f']):.2f}$ cm²/m** (face {r['face']}) → {_fmt(r['diam'], r['esp'])}")
    st.write(rf"- $A_{{s,dist}} = 0.20\,A_s = {_cm2(r['As_dist']):.2f}$ cm²/m → {_fmt(r['dd'], r['ee'])}")
    st.success(f"✅ {_fmt(r['diam'], r['esp'])} | Dist: {_fmt(r['dd'], r['ee'])}")
    
    # 3) BIQUEIRA (bt)
    sig_stem_esq = sigma_bt + (sigma_bh - sigma_bt) * (bt / B)
    q_down_bt = g_G_fav * 25 * tb
    q_up_bt = (sigma_bt + sig_stem_esq) / 2
    net_bt = q_up_bt - q_down_bt
    M_bt = abs(net_bt) * bt ** 2 / 2
    V_bt = abs(net_bt) * bt
    r = seccao(M_bt, V_bt, tb * 1000, get_text("consola_bt", lang))
    r.update(face=get_text("consola_face_inf", lang) if net_bt > 0 else get_text("consola_face_sup", lang),
             M=M_bt, V=V_bt, H_elem=bt, label_H="b_t")
    res.append(r)
    st.markdown(f"#### 🔹 {get_text('consola_bt', lang)} ($b_t = {bt:.2f}$ m)")
    st.write(rf"- $M_{{sd}} = {M_bt:.2f}$ kNm/m | $V_{{sd}} = {V_bt:.2f}$ kN/m")
    st.write(rf"- $A_{{s,calc}} = {_cm2(r['As']):.2f}$ cm²/m | "
             rf"$A_{{s,min}} = {_cm2(r['As_min']):.2f}$ cm²/m | "
             rf"$A_{{s,max}} = {_cm2(r['As_max']):.2f}$ cm²/m")
    st.write(rf"- **$A_s = {_cm2(r['As_f']):.2f}$ cm²/m** (face {r['face']}) → {_fmt(r['diam'], r['esp'])}")
    st.write(rf"- $A_{{s,dist}} = 0.20\,A_s = {_cm2(r['As_dist']):.2f}$ cm²/m → {_fmt(r['dd'], r['ee'])}")
    st.success(f"✅ {_fmt(r['diam'], r['esp'])} | Dist: {_fmt(r['dd'], r['ee'])}")
    
    # Tabela-resumo completa
    arma = {
        'm1': _fmt(res[0]['diam'], res[0]['esp']),
        'm2': _fmt(res[0]['dd'], res[0]['ee']),
        'm3': _fmt(res[1]['diam'], res[1]['esp']),
        'm4': _fmt(res[1]['dd'], res[1]['ee']),
        'm5': _fmt(res[2]['diam'], res[2]['esp']),
        'm6': _fmt(res[2]['dd'], res[2]['ee']),
        'face_bh': res[1]['face'], 'face_bt': res[2]['face'],
    }
    
    st.markdown(f"####  {get_text('consola_tabela_arm', lang)}")
    tab = (f"<table style='border-collapse:collapse;width:100%;font-size:0.9em;'>"
           f"<tr style='background:#2c3e50;color:#fff;'>"
           f"<th style='padding:6px;border:1px solid #ddd;'>#</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>{get_text('stem', lang)}</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>Face</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>Msd<br>(kNm/m)</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>Vsd<br>(kN/m)</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>μ</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>As,min<br>(cm²/m)</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>As,max<br>(cm²/m)</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'><b>As</b><br>(cm²/m)</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>As,dist<br>(cm²/m)</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>Armadura</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>Distrib.</th>"
           f"<th style='padding:6px;border:1px solid #ddd;'>Corte</th></tr>")
    for k, r in enumerate(res, 1):
        tab += (f"<tr><td>{k}</td><td>{r['elem']}</td><td>{r['face']}</td>"
                f"<td>{r['M']:.2f}</td><td>{r['V']:.2f}</td><td>{r['mu']:.4f}</td>"
                f"<td>{_cm2(r['As_min']):.2f}</td><td>{_cm2(r['As_max']):.2f}</td>"
                f"<td><strong>{_cm2(r['As_f']):.2f}</strong></td>"
                f"<td>{_cm2(r['As_dist']):.2f}</td>"
                f"<td><strong>{_fmt(r['diam'], r['esp'])}</strong></td>"
                f"<td>{_fmt(r['dd'], r['ee'])}</td>"
                f"<td>{'✅' if r['ok_corte'] else '❌'}</td></tr>")
    tab += "</table>"
    st.markdown(tab, unsafe_allow_html=True)
    
    # Pormenorização e diagramas
    st.markdown(f"#### 🎨 {get_text('consola_pormenor', lang)}")
    svg_porm = _svg_pormenorizacao_consola(B, bt, bh, ts, tb, HR, arma, lang)
    st.markdown(svg_porm, unsafe_allow_html=True)
    
    svg_laje_stem = _svg_laje_vertical(Hs, p0, p1, M_stem, V_stem,
                                       get_text("consola_stem", lang).upper())
    svg_laje_bh = _svg_laje_horizontal(
        bh, q_down_bh, q_up_bh, net_bh,
        "cima" if net_bh > 0 else "baixo", M_bh, V_bh,
        get_text("consola_bh", lang).upper(), "dir")
    svg_laje_bt = _svg_laje_horizontal(
        bt, q_down_bt, q_up_bt, net_bt,
        "cima" if net_bt > 0 else "baixo", M_bt, V_bt,
        get_text("consola_bt", lang).upper(), "esq")
    
    st.markdown(f"#### 📊 {get_text('consola_diagramas', lang)}")
    st.markdown(svg_laje_stem, unsafe_allow_html=True)
    st.markdown(svg_laje_bh, unsafe_allow_html=True)
    st.markdown(svg_laje_bt, unsafe_allow_html=True)
    
    # Relatório HTML
    diagramas_completos = (
        (svg_estrutura or "") + (svg_esquema or "") + svg_porm +
        svg_laje_stem + svg_laje_bh + svg_laje_bt
    )
    
    # Tabela detalhada para relatório
    tab_rel = (f"<table><tr><th>#</th><th>Elemento</th><th>Face</th>"
               f"<th>$M_{{sd}}$ (kNm/m)</th><th>$V_{{sd}}$ (kN/m)</th><th>$\\mu$</th>"
               f"<th>$A_{{s,min}}$ (cm²/m)</th><th>$A_{{s,max}}$ (cm²/m)</th>"
               f"<th>$A_s$ (cm²/m)</th><th>$A_{{s,dist}}$ (cm²/m)</th>"
               f"<th>Armadura Principal</th><th>Armadura Distribuição</th><th>Corte</th></tr>")
    for k, r in enumerate(res, 1):
        tab_rel += (f"<tr><td>{k}</td><td>{r['elem']}</td><td>{r['face']}</td>"
                    f"<td>{r['M']:.2f}</td><td>{r['V']:.2f}</td><td>{r['mu']:.4f}</td>"
                    f"<td>{_cm2(r['As_min']):.2f}</td><td>{_cm2(r['As_max']):.2f}</td>"
                    f"<td><strong>{_cm2(r['As_f']):.2f}</strong></td>"
                    f"<td>{_cm2(r['As_dist']):.2f}</td>"
                    f"<td><strong>{_fmt(r['diam'], r['esp'])}</strong></td>"
                    f"<td>{_fmt(r['dd'], r['ee'])}</td>"
                    f"<td>{'✅' if r['ok_corte'] else '❌'}</td></tr>")
    tab_rel += "</table>"
    
    verif_html = "<ul>"
    for r in res:
        verif_html += (f"<li><strong>{r['elem']}</strong>: $A_s = {_cm2(r['As_f']):.2f}$ cm²/m, "
                       f"$A_{{s,min}} = {_cm2(r['As_min']):.2f}$ cm²/m, "
                       f"$A_{{s,max}} = {_cm2(r['As_max']):.2f}$ cm²/m, "
                       f"$A_{{s,dist}} = {_cm2(r['As_dist']):.2f}$ cm²/m, "
                       f"corte {'✅' if r['ok_corte'] else '❌'}, "
                       f"espaçamento {'✅' if r['ok_esp'] else ''}</li>")
    verif_html += "</ul>"
    
    html_bytes = relatorios_consola.gerar_relatorio_html_muro_consola(
        nome=st.session_state.nome, curso=st.session_state.curso,
        genero=st.session_state.genero,
        H=H, HR=HR, D=0, B=B, bt=bt, bh=bh, ts=ts, tb=tb, i=i,
        gamma_ativo=gamma_ativo, gamma_sat_ativo=gamma_sat_ativo,
        phi_ativo=phi_ativo, c_ativo=c_ativo, q_ativo=q_ativo,
        z_w_ativo=0.0,
        gamma_passivo=gamma_passivo, gamma_sat_passivo=gamma_sat_passivo,
        phi_passivo=phi_passivo, c_passivo=c_passivo, z_w_passivo=z_w_passivo,
        gamma_fund=gamma_fund, gamma_sat_fund=gamma_fund,
        phi_fund=phi_fund, c_fund=c_fund, cu_fund=cu_fund, delta_b=delta_b,
        metodo=metodo, delta=delta, combo_ec7=combo_ec7,
        g_G_unfav=g_G_unfav, g_G_fav=g_G_fav, g_Q=g_Q,
        g_phi=1.0, g_c=1.0, g_cu=1.0, g_Rh=1.0, g_Rv=1.0,
        phi_ativo_d=phi_ativo_d or phi_ativo,
        phi_passivo_d=phi_passivo, phi_fund_d=phi_fund,
        c_ativo_d=c_ativo, c_passivo_d=c_passivo, c_fund_d=c_fund,
        cu_fund_d=cu_fund, delta_d=delta, q_d=q_d,
        Ka=Ka, Kp=0.0, Ia_ativo_caract=Ia_caract,
        Ia_ativo_d=Ia_caract * g_G_unfav,
        IaH_d=IaH_d, IaV_d=IaV_d,
        Ip_passivo_caract=0.0, Rpd_d=0.0,
        W_stem_d=0.0, W_base_d=0.0, W_solo_talao_d=0.0, W_solo_biqueira_d=0.0,
        W_total_d=W_total_d, M_est_total=M_est, M_derr_total=M_derr,
        V_d=V_d, e=e, B_linha=B_linha, Rd_h=0.0, tipo_cisalhamento="",
        q_Rd=0.0, sigma_max_d=max(sigma_bh, sigma_bt),
        ok_derr=True, ok_desliz=True, ok_carga=True,
        classe_betao=classe_betao, tipo_aco=tipo_aco,
        recobrimento=recobrimento,
        fck=fck, fcd=fcd, fctd=fctd, fyk=fyk, fsyd=fsyd,
        M_stem_d=res[0]['M'], d_stem=res[0]['d'] / 1000,
        As_stem_final=_cm2(res[0]['As_f']),
        M_talao_d=res[1]['M'], M_biqueira_d=res[2]['M'],
        d_base=res[1]['d'] / 1000,
        As_talao_final=_cm2(res[1]['As_f']),
        As_biqueira_final=_cm2(res[2]['As_f']),
        V_stem_d=res[0]['V'], VRd_stem=res[0]['VRd'],
        ok_corte_stem=res[0]['ok_corte'],
        D_passivo=0.0,
        V_talao_d=res[1]['V'], V_biqueira_d=res[2]['V'],
        diam_stem=res[0]['diam'], esp_stem=res[0]['esp'],
        diam_talao=res[1]['diam'], esp_talao=res[1]['esp'],
        diam_biqueira=res[2]['diam'], esp_biqueira=res[2]['esp'],
        face_talao=res[1]['face'],
        tabela_armaduras_html=tab_rel,
        verificacoes_html=verif_html,
        diagramas_html=diagramas_completos,
        lang=lang,
    )
    
    st.download_button(
        label=f" {get_text('descarregar_relatorio', lang)}",
        data=html_bytes,
        file_name=f"Relatorio_Consola_{st.session_state.nome.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True,
        type="primary",
        key="btn_download_relatorio_consola_arm"
    )