"""Muro com Contrafortes - Versão Corrigida"""
import streamlit as st
import math
from calculos import relatorios_consola
from calculos.meyerhof_tabela import meyerhof_N
from utils.traducoes import get_text
from paginas.muros_consola import (
    calcular_phi_d, Ka_rankine_slide100, _escolher_armadura, _cm2, _fmt,
    _svg_laje_horizontal, _svg_laje_vertical, carregar_imagem_local
)

def prosseguir_cf():
    st.session_state.fase_cf = "armaduras"

def voltar_cf():
    st.session_state.fase_cf = "geotecnica"

# ============================================================
# DESENHO DA ESTRUTURA — com solo preenchido + inclinação
# ============================================================
def _svg_estrutura_cf(b1, b2, b3, t_, H, hc, hb, B, i, lang="pt"):
    """Esquema do muro com contrafortes com cotas técnicas correctas:
    linhas de extensão tracejadas + setas bem orientadas + solo de fundação visível."""
    lbl = lambda pt, en: pt if lang == "pt" else en
    titulo = lbl("MURO COM CONTRAFORTES — ESQUEMA", "COUNTERFORT WALL — SCHEMATIC")
    lbl_solo_fund = lbl("SOLO DE FUNDACAO", "FOUNDATION SOIL")
    lbl_solo_ret = lbl("SOLO RETIDO", "RETAINED SOIL")
    lbl_cf = lbl("CONTRAFORTE", "COUNTERFORT")
    lbl_par = lbl("PARAMENTO", "STEM")
    lbl_c2 = lbl("Consola 2 (frente)", "Cantilever 2 (front)")
    lbl_c1 = lbl("Consola 1 (talão)", "Cantilever 1 (heel)")
    lbl_bet = lbl("Betão", "Concrete")
    lbl_solo = lbl("Solo", "Soil")
    lbl_fund = lbl("Solo de fundação", "Foundation soil")
    
    esc = min(340.0 / max(H, 0.1), 420.0 / max(B, 0.1))
    x0, yb = 220.0, 580.0
    ybt = yb - hb * esc
    ytop = yb - H * esc
    ycf = ybt - hc * esc
    x1s = x0 + b1 * esc
    x2s = x1s + t_ * esc
    xR = x0 + B * esc
    tan_i = math.tan(math.radians(i))
    
    dx_soil = 200.0
    x_soil = xR + dx_soil
    y_soil_top = ytop - (x_soil - x2s) * tan_i
    max_rise = ytop - 60.0
    if tan_i > 1e-9 and (x_soil - x2s) * tan_i > max_rise:
        x_soil = x2s + max_rise / tan_i
        y_soil_top = 60.0
    if y_soil_top < 60.0:
        y_soil_top = 60.0
    
    W, Hh = int(x_soil + 90), 730
    s = [f'<svg width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'style="background:#fdfefe;border:1px solid #bbb;border-radius:8px;">']
    s.append('<defs>'
             '<pattern id="cfHatch" patternUnits="userSpaceOnUse" width="10" height="10" '
             'patternTransform="rotate(45)">'
             '<line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.2"/>'
             '</pattern>'
             '<marker id="cfB" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
             '<polygon points="0,0 10,3 0,6" fill="#1f77b4"/></marker>'
             '<marker id="cfG" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
             '<polygon points="0,0 10,3 0,6" fill="#27ae60"/></marker>'
             '</defs>')
    
    # ============================================================
    # ORDEM DE DESENHO (de trás para a frente):
    # 1) Solo de fundação
    # 2) Solo retido
    # 3) Betão (por cima do solo de fundação)
    # ============================================================

    # --- 1. SOLO DE FUNDAÇÃO ---
    s.append(f'<rect x="30" y="{yb:.1f}" width="{W-60}" height="50" fill="#8a6a4f" stroke="#6b4a2f"/>')
    s.append(f'<rect x="30" y="{yb:.1f}" width="{W-60}" height="50" fill="url(#cfHatch)" opacity="0.45"/>')
    s.append(f'<text x="38" y="{yb+30:.1f}" font-size="10" fill="#fff" font-weight="bold">{lbl_solo_fund}</text>')

    # --- 2. SOLO RETIDO ---
    poly_soil = (f'{x2s:.1f},{ytop:.1f} {x_soil:.1f},{y_soil_top:.1f} '
                 f'{x_soil:.1f},{yb:.1f} {xR:.1f},{yb:.1f} '
                 f'{xR:.1f},{ybt:.1f} {x2s:.1f},{ybt:.1f}')
    s.append(f'<polygon points="{poly_soil}" fill="#d2b48c" stroke="#8b6f47" stroke-width="1.2"/>')
    s.append(f'<polygon points="{poly_soil}" fill="url(#cfHatch)" opacity="0.30"/>')
    s.append(f'<text x="{(x2s+x_soil)/2:.1f}" y="{(ytop+ybt)/2:.1f}" text-anchor="middle" '
             f'font-size="11" fill="#5d4a2f" font-weight="bold">{lbl_solo_ret}</text>')
    
    # --- 3. BETÃO ---
    # 3.1 Preenchimentos (sem contorno) — aspeto monolítico sapata+paramento
    s.append(f'<rect x="{x0:.1f}" y="{ybt:.1f}" width="{xR-x0:.1f}" height="{yb-ybt:.1f}" '
             f'fill="#b8b8b8"/>')
    s.append(f'<rect x="{x1s:.1f}" y="{ytop:.1f}" width="{x2s-x1s:.1f}" height="{ybt-ytop:.1f}" '
             f'fill="#b8b8b8"/>')
    s.append(f'<polygon points="{x0:.1f},{ybt:.1f} {x1s:.1f},{ybt:.1f} {x1s:.1f},{ycf:.1f}" '
             f'fill="#9c9c9c"/>')
    
    # 3.2 Contorno exterior monolítico
    #     (o topo da sapata NÃO é traçado entre x1s e x2s → paramento ENCASTRA na sapata)
    outline = (f'M {x0:.1f},{ybt:.1f} '                 # canto sup. esq. da sapata
               f'L {x1s:.1f},{ybt:.1f} '                # topo esq. da sapata (até à face esq. do paramento)
               f'L {x1s:.1f},{ytop:.1f} '               # sobe pela face esquerda do paramento
               f'L {x2s:.1f},{ytop:.1f} '               # topo do paramento
               f'L {x2s:.1f},{ybt:.1f} '                # desce pela face direita do paramento
               f'L {xR:.1f},{ybt:.1f} '                 # topo dir. da sapata
               f'L {xR:.1f},{yb:.1f} '                  # face direita da sapata
               f'L {x0:.1f},{yb:.1f} Z')                # base + fecha
    s.append(f'<path d="{outline}" fill="none" stroke="#333" stroke-width="2"/>')
    
    # 3.3 Contraforte: só a hipotenusa fica visível
    #     (arestas em contacto com sapata/paramento não se traçam — monolítico)
    s.append(f'<line x1="{x0:.1f}" y1="{ybt:.1f}" x2="{x1s:.1f}" y2="{ycf:.1f}" '
             f'stroke="#333" stroke-width="2"/>')
    
    # --- RÓTULOS INTERNOS ---
    s.append(f'<text x="{(x0+x1s)/2-12:.1f}" y="{(ybt+ycf)/2+8:.1f}" font-size="9" '
             f'font-weight="bold" fill="#222" '
             f'transform="rotate(-52 {(x0+x1s)/2-12:.1f} {(ybt+ycf)/2+8:.1f})">{lbl_cf}</text>')
    s.append(f'<text x="{(x1s+x2s)/2-4:.1f}" y="{(ytop+ybt)/2:.1f}" font-size="10" '
             f'font-weight="bold" fill="#222" '
             f'transform="rotate(90 {(x1s+x2s)/2-4:.1f} {(ytop+ybt)/2:.1f})">{lbl_par}</text>')
    s.append(f'<text x="{(x0+x1s)/2-24:.1f}" y="{ybt-6:.1f}" font-size="10" fill="#c0392b" '
             f'font-weight="bold">{lbl_c2}</text>')
    s.append(f'<text x="{(x2s+xR)/2-24:.1f}" y="{ybt-6:.1f}" font-size="10" fill="#c0392b" '
             f'font-weight="bold">{lbl_c1}</text>')


    # ============================================================
    # COTAS TÉCNICAS
    # ============================================================
    def cota_v(x_cota, y1, y2, x_ext1, x_ext2, label, cor="#1f77b4", marker="cfB", font=10):
        return (
            f'<line x1="{x_ext1:.1f}" y1="{y1:.1f}" x2="{x_cota+5:.1f}" y2="{y1:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            f'<line x1="{x_ext2:.1f}" y1="{y2:.1f}" x2="{x_cota+5:.1f}" y2="{y2:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            f'<line x1="{x_cota:.1f}" y1="{y1:.1f}" x2="{x_cota:.1f}" y2="{y2:.1f}" '
            f'stroke="{cor}" stroke-width="1.1" marker-start="url(#{marker})" marker-end="url(#{marker})"/>'
            f'<text x="{x_cota-6:.1f}" y="{(y1+y2)/2:.1f}" text-anchor="middle" '
            f'font-size="{font}" fill="{cor}" font-weight="bold" '
            f'transform="rotate(-90 {x_cota-6:.1f} {(y1+y2)/2:.1f})">{label}</text>'
        )
    
    def cota_h(y_cota, x1, x2, y_ext1, y_ext2, label, cor="#1f77b4", marker="cfB", font=10):
        return (
            f'<line x1="{x1:.1f}" y1="{y_ext1:.1f}" x2="{x1:.1f}" y2="{y_cota-5:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            f'<line x1="{x2:.1f}" y1="{y_ext2:.1f}" x2="{x2:.1f}" y2="{y_cota-5:.1f}" '
            f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>'
            f'<line x1="{x1:.1f}" y1="{y_cota:.1f}" x2="{x2:.1f}" y2="{y_cota:.1f}" '
            f'stroke="{cor}" stroke-width="1.1" marker-start="url(#{marker})" marker-end="url(#{marker})"/>'
            f'<text x="{(x1+x2)/2:.1f}" y="{y_cota-7:.1f}" text-anchor="middle" '
            f'font-size="{font}" fill="{cor}" font-weight="bold">{label}</text>'
        )
    
    # --- COTAS VERTICAIS ---
    s.append(cota_v(x0-32, ytop, yb, x0, x0, f"H={H:.2f} m", cor="#1f77b4", marker="cfB", font=11))
    s.append(cota_v(x0-58, ycf, ybt, x1s, x1s, f"hc={hc:.2f} m", cor="#27ae60", marker="cfG", font=10))
    s.append(cota_v(xR+32, ybt, yb, xR, xR, f"hb={hb*100:.0f} cm", cor="#1f77b4", marker="cfB", font=10))
    
    # --- COTAS HORIZONTAIS (b1, b2, b3) com linhas de extensão tracejadas ---
    yd = yb + 72
    x_xl = x0 + b1 * esc
    x_xr = x0 + (b1 + b2) * esc
    # Linhas de extensão tracejadas (da base do muro até à linha de cota)
    for x_ext in (x0, x_xl, x_xr, xR):
        s.append(f'<line x1="{x_ext:.1f}" y1="{yb:.1f}" x2="{x_ext:.1f}" y2="{yd+5:.1f}" '
                 f'stroke="#888" stroke-width="0.7" stroke-dasharray="3,2"/>')
    # Linhas de cota com setas + etiquetas
    for xa, xb_, lab in ((x0, x_xl, f"b1={b1:.2f}"),
                         (x_xl, x_xr, f"b2={b2:.2f}"),
                         (x_xr, xR, f"b3={b3:.2f}")):
        s.append(f'<line x1="{xa:.1f}" y1="{yd}" x2="{xb_:.1f}" y2="{yd}" stroke="#1f77b4" '
                 f'stroke-width="1.2" marker-start="url(#cfB)" marker-end="url(#cfB)"/>')
        s.append(f'<text x="{(xa+xb_)/2:.1f}" y="{yd+14}" text-anchor="middle" '
                 f'font-size="10" fill="#1f77b4" font-weight="bold">{lab}</text>')
    
    # --- Inclinacao do terrapleno ---
    if i > 0.05:
        s.append(f'<text x="{x_soil-24:.1f}" y="{y_soil_top+22:.1f}" text-anchor="end" '
                 f'font-size="11" fill="#1f77b4" font-weight="bold">i = {i:.1f}°</text>')
        s.append(f'<line x1="{x2s:.1f}" y1="{ytop:.1f}" x2="{x2s+75:.1f}" y2="{ytop:.1f}" '
                 f'stroke="#1f77b4" stroke-width="1" stroke-dasharray="4,3"/>')
        r_arc = 60.0
        xa_ = x2s + r_arc * math.cos(math.radians(i))
        ya_ = ytop - r_arc * math.sin(math.radians(i))
        s.append(f'<path d="M {x2s+r_arc:.1f},{ytop:.1f} A {r_arc},{r_arc} 0 0 0 '
                 f'{xa_:.1f},{ya_:.1f}" fill="none" stroke="#1f77b4" stroke-width="1.3"/>')
        
    
    # --- Legenda ---
    yl = Hh - 16
    s.append(f'<rect x="30" y="{yl-12}" width="12" height="12" fill="#b8b8b8" stroke="#333"/>')
    s.append(f'<text x="48" y="{yl-2}" font-size="10">{lbl_bet}</text>')
    s.append(f'<rect x="115" y="{yl-12}" width="12" height="12" fill="#d2b48c" stroke="#8b6f47"/>')
    s.append(f'<text x="133" y="{yl-2}" font-size="10">{lbl_solo}</text>')
    s.append(f'<rect x="185" y="{yl-12}" width="12" height="12" fill="#8a6a4f" stroke="#6b4a2f"/>')
    s.append(f'<text x="203" y="{yl-2}" font-size="10">{lbl_fund}</text>')
    s.append('</svg>')
    return "".join(s)

# ============================================================
# ESQUEMA FINAL — RANKINE (adaptado dos muros em consola)
# ============================================================
def _svg_esquema_rankine_cf(b1, b2, b3, t_, H, hc, hb, B, i,
                             Ka, h_uso, IaH_d, W_total_d, q_ativo,
                             lang="pt", phi_d=None):
    """Esquema Final — Rankine para muro com contrafortes.

    Adaptação directa de `_svg_esquema_rankine` (muros em consola).
    - Sistema local: X = 0 na aresta do talão (lado retido, direita);
                     X = -b3 na face de trás do paramento;
                     X = -(b2+b3) na face da frente do paramento;
                     X = -B na aresta da biqueira (esquerda).
    - Cunha morta E-D-A + cunha activa D-C-A (se φ' > 0) ou D-x-x-A.
    - Plano vertical AD → impulso Iₐ paralelo ao talude (ângulo i).
    - h'' = AD = H + b3·tan(i) — altura do plano vertical no talão.
    """
    t = lambda pt, en: pt if lang == "pt" else en
    i_r = math.radians(i)
    tan_i = math.tan(i_r)
    Y_D = H + b3 * tan_i                       # altura no plano AD (aresta do talão)

    # Ângulo ξ da cunha activa (se φ' > 0)
    have_C = (phi_d is not None) and (float(phi_d) > 1e-6)
    phi = float(phi_d) if have_C else 0.0
    if have_C:
        arg = min(1.0, math.sin(i_r) / math.sin(math.radians(phi)))
        xi = 45.0 + phi / 2.0 - 0.5 * (math.degrees(math.asin(arg)) - i)
        xi_r = math.radians(xi)
        den_C = math.sin(xi_r) - math.cos(xi_r) * tan_i
        X_C = (Y_D / den_C) * math.cos(xi_r) if den_C > 0.05 else 1e9
        C_cap = False
        if X_C > 3.0 * Y_D:
            C_cap, X_C = True, 3.0 * Y_D
        Y_C = X_C * math.tan(xi_r) if C_cap else Y_D + X_C * tan_i
    else:
        X_C = 0.9 * Y_D
        Y_C = Y_D + X_C * tan_i

    # Faces do paramento no sistema local
    xs0 = -(b2 + b3)      # frente do paramento (esquerda)
    xs1 = -b3             # tardoz do paramento (retido, direita)

    # --------- Helpers gráficos (iguais aos dos muros em consola) ---------
    def mapper(ox, oy, esc):
        return lambda X, Y: (ox + X * esc, oy - Y * esc)

    def pts(lst):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in lst)

    def line(p, q, stroke, w=1.2, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" '
                f'x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
                f'stroke="{stroke}" stroke-width="{w}"{d}{extra}/>')

    def text(x, y, s_, size=11, fill="#222", anchor="middle",
             weight="bold", extra="", halo=True):
        base = (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
                f'text-anchor="{anchor}" font-weight="{weight}"{extra}')
        halo_t = (base + ' fill="#fdfefe" stroke="#fdfefe" stroke-width="3.5" '
                  'stroke-linejoin="round">' + s_ + '</text>')
        return (halo_t if halo else '') + base + f' fill="{fill}">' + s_ + '</text>'

    def arc(c, r, ang0, ang1, stroke, w=1.5):
        a0, a1 = math.radians(ang0), math.radians(ang1)
        p0 = (c[0] + r * math.cos(a0), c[1] - r * math.sin(a0))
        p1 = (c[0] + r * math.cos(a1), c[1] - r * math.sin(a1))
        sweep = 0 if ang1 > ang0 else 1
        large = 1 if abs(ang1 - ang0) > 180 else 0
        return (f'<path d="M {p0[0]:.1f},{p0[1]:.1f} A {r:.1f},{r:.1f} '
                f'0 {large} {sweep} {p1[0]:.1f},{p1[1]:.1f}" fill="none" '
                f'stroke="{stroke}" stroke-width="{w}"/>')

    def arc_label(c, r, ang0, ang1, s_, color, size=12):
        am = math.radians((ang0 + ang1) / 2.0)
        return text(c[0] + (r + 13) * math.cos(am),
                    c[1] - (r + 13) * math.sin(am) + 4,
                    s_, size, color)

    def dot(p, r=3.2):
        return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="#111"/>'

    def dim_v(xpx, y0, y1, label, cor="#1f77b4"):
        return (f'<line x1="{xpx:.1f}" y1="{y0:.1f}" x2="{xpx:.1f}" y2="{y1:.1f}" '
                f'stroke="{cor}" stroke-width="1.2" '
                f'marker-start="url(#rkD)" marker-end="url(#rkD)"/>'
                + text(xpx + 6, (y0 + y1) / 2.0 + 4, label, 11, cor, "start"))

    def wall(P):
        """Secção transversal do muro (sapata + paramento). O contraforte é
        longitudinal e não aparece na secção transversal do esquema Rankine."""
        poly = [(-B, 0), (-B, hb), (xs0, hb), (xs0, H),
                (xs1, H), (xs1, hb), (0, hb), (0, 0)]
        return (f'<polygon points="{pts([P(x, y) for x, y in poly])}" '
                f'fill="#b8b8b8" stroke="#333" stroke-width="2"/>'
                f'<polygon points="{pts([P(x, y) for x, y in poly])}" '
                f'fill="url(#rkC)" opacity="0.5"/>')

    def surcharge(P, x_from, x_to, gy):
        out, n = [], 0
        xx = x_from
        while xx <= x_to and n < 12:
            g = gy(xx)
            p0, p1 = P(xx, g), P(xx, g)
            out.append(
                f'<line x1="{p0[0]:.1f}" y1="{p0[1]-30:.1f}" '
                f'x2="{p1[0]:.1f}" y2="{p1[1]-7:.1f}" '
                f'stroke="#1f77b4" stroke-width="1.5"/>'
                f'<polygon points="{p1[0]:.1f},{p1[1]-4:.1f} '
                f'{p1[0]-3.5:.1f},{p1[1]-12:.1f} {p1[0]+3.5:.1f},{p1[1]-12:.1f}" '
                f'fill="#1f77b4"/>')
            xx += 0.45 * max(Y_D, 1.0) / 2.0
            n += 1
        return "".join(out)

    # --------- Dimensões do canvas ---------
    W_svg, H_svg = 1060, 660
    oy = 540.0

    # Painel ① — Geometria
    esc1 = min((600.0 - 30.0 - 150.0) / max(B + X_C, 0.1),
               470.0 / max(Y_C, 0.5))
    ox1 = 30.0 + B * esc1
    P1 = mapper(ox1, oy, esc1)

    # Painel ② — Cunha morta + impulso
    esc2 = min((400.0 - 20.0 - 150.0) / max(B + 0.45 * Y_D, 0.1),
               470.0 / max(Y_D + 0.1, 0.5))
    ox2 = 660.0 + B * esc2
    P2 = mapper(ox2, oy, esc2)

    # --------- Abertura do SVG ---------
    s = [f'<svg width="100%" viewBox="0 0 {W_svg} {H_svg}" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'style="max-width:{W_svg}px;background:#fdfefe;border:1px solid #bbb;'
         f'border-radius:8px;font-family:Segoe UI,Arial,sans-serif;">']
    s.append('<defs>'
             '<marker id="rkD" markerWidth="10" markerHeight="10" refX="9" refY="3" '
             'orient="auto-start-reverse"><polygon points="0,0 10,3 0,6" '
             'fill="#1f77b4"/></marker>'
             '<marker id="rkR" markerWidth="10" markerHeight="10" refX="9" refY="3" '
             'orient="auto"><polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker>'
             '<pattern id="rkH" patternUnits="userSpaceOnUse" width="10" height="10" '
             'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" '
             'stroke="#8b6f47" stroke-width="1.1"/></pattern>'
             '<pattern id="rkC" patternUnits="userSpaceOnUse" width="8" height="8" '
             'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" '
             'stroke="#888" stroke-width="0.8"/></pattern>'
             '</defs>')
    titulo_txt = ("RANKINE (slide 100) — MURO COM CONTRAFORTES — cunha morta E-D-A "
                  "e plano vertical AD" if lang == "pt" else
                  "RANKINE (slide 100) — COUNTERFORT WALL — dead wedge E-D-A "
                  "and vertical plane AD")
    s.append(text(W_svg / 2, 24, titulo_txt, 14))
    s.append(f'<line x1="640" y1="40" x2="640" y2="{H_svg-70}" '
             f'stroke="#ddd" stroke-width="1"/>')

    # --------- Painel ① ---------
    A, E, Dp = P1(0, 0), P1(xs1, H), P1(0, Y_D)
    Cp = P1(X_C, Y_C)
    titulo1 = ("① Geometria: pontos A, D, E" +
               (", C" if have_C else "") if lang == "pt" else
               "① Geometry: points A, D, E" +
               (", C" if have_C else ""))
    s.append(text(320, 56, titulo1, 12, "#1f4e79"))
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" '
             f'fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" '
             f'fill="url(#rkH)" opacity="0.5"/>')

    # Cunha morta E-D-A
    dead = [P1(xs1, hb), E, Dp, A]
    s.append(f'<polygon points="{pts(dead)}" fill="#8f8f8f" stroke="none"/>')

    # Cunha activa D-C-A (ou D-x-x-A sem φ')
    if have_C:
        act = [Dp, Cp, A]
    else:
        xe = X_C
        act = [Dp, P1(xe, Y_D + xe * tan_i), P1(xe, 0), A]
    s.append(f'<polygon points="{pts(act)}" fill="#f1ebdf" stroke="none"/>')
    s.append(f'<polygon points="{pts(act)}" fill="url(#rkH)" opacity="0.18"/>')

    # Muro (sapata + paramento)
    s.append(wall(P1))

    # Linha do talude
    ext = 0.12 * X_C
    G_end = P1(X_C + ext, Y_D + (X_C + ext) * tan_i)
    s.append(line(E, G_end, "#6b4a2f", 2.4))

    # Linhas de extensão + plano AD
    xd = [A[0] + 52, A[0] + 82]
    for pnt, xx in ((E, xd[0]), (Dp, xd[1])):
        s.append(line(pnt, (xx + 8, pnt[1]), "#555", 1, "2,3"))
    s.append(line(A, (xd[1] + 8, A[1]), "#555", 1, "2,3"))
    s.append(line(A, Dp, "#5d3a1f", 2.4, "7,4"))     # plano vertical AD
    if have_C:
        s.append(line(A, Cp, "#222", 1.8, "10,3,2,3"))
        s.append(arc(A, 56.0, 0.0, xi, "#27ae60"))
        s.append(arc_label(A, 56.0, 0.0, xi, "ξ", "#27ae60"))
    if i > 0.05:
        s.append(arc(Dp, 62.0, 0.0, i, "#1f77b4"))
        s.append(arc_label(Dp, 62.0, 0.0, max(i, 8.0), "i", "#1f77b4", 11))

    # Rótulo "cunha morta"
    cx = sum(p[0] for p in dead) / 4.0
    cy = sum(p[1] for p in dead) / 4.0
    s.append(text(cx, cy, t("cunha morta", "dead wedge"), 12, "#fff",
                  "middle", extra=f' transform="rotate(-90 {cx:.1f} {cy:.1f})"',
                  halo=False))

    # Sobrecarga
    if q_ativo > 0:
        s.append(surcharge(P1, xs1 + 0.1, X_C,
                           lambda x: Y_D + x * tan_i))
        qp = P1(xs1 + 0.1, H + 0.1 * tan_i)
        s.append(text(qp[0] + 4, qp[1] - 38, f"q = {q_ativo:.1f} kPa",
                      10, "#1f77b4", "start"))

    # Cotas
    s.append(dim_v(xd[0], A[1], E[1], "h"))
    s.append(dim_v(xd[1], A[1], Dp[1], "h''"))

    # Rótulos A, D, E, C
    pontos = [(A, "A", 6, 20), (Dp, "D", 4, -10), (E, "E", -14, -8)]
    if have_C:
        pontos.append((Cp, "C", 8, -9))
    for pnt, nm, dx, dy in pontos:
        s.append(dot(pnt))
        s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))

    # Rodapé informativo
    s.append(text(30, 578,
                  f"h = H = {H:.2f} m  |  h'' = AD = {Y_D:.2f} m  |  "
                  f"h_uso = {h_uso:.2f} m", 11, "#1f77b4", "start"))
    s.append(text(30, 596,
                  t(f"Plano vertical AD; Iₐ paralelo ao talude (i = {i:.1f}°)",
                    f"Vertical plane AD; Iₐ parallel to slope (i = {i:.1f}°)"),
                  11, "#c0392b", "start"))
    if have_C:
        s.append(text(30, 614,
                      f"ξ = 45° + φ'/2 − ½(arcsen(sen i / sen φ') − i) = "
                      f"{xi:.2f}°   (φ' = {phi:.1f}°)",
                      11, "#27ae60", "start"))

    # --------- Painel ② — Cunha morta e impulso ---------
    A2, E2, D2 = P2(0, 0), P2(xs1, H), P2(0, Y_D)
    titulo2 = ("② Cunha morta E-D-A e impulso Iₐ em AD" if lang == "pt" else
               "② Dead wedge E-D-A and thrust Iₐ on AD")
    s.append(text(850, 56, titulo2, 12, "#1f4e79"))
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" '
             f'fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" '
             f'fill="url(#rkH)" opacity="0.5"/>')

    dead2 = [P2(xs1, hb), E2, D2, A2]
    s.append(f'<polygon points="{pts(dead2)}" fill="#d9d9d9" stroke="none"/>')
    s.append(wall(P2))
    x_gr = 0.30 * Y_D
    s.append(line(E2, P2(x_gr, Y_D + x_gr * tan_i), "#6b4a2f", 2.4))
    s.append(line(A2, D2, "#5d3a1f", 2.4, "7,4"))
    cx2 = sum(p[0] for p in dead2) / 4.0
    cy2 = sum(p[1] for p in dead2) / 4.0
    s.append(text(cx2, cy2, t("cunha morta", "dead wedge"), 12, "#1f4e79",
                  "middle", extra=f' transform="rotate(-90 {cx2:.1f} {cy2:.1f})"'))

    # Setas do impulso Iₐ (paralelas ao talude, apontando para o plano AD)
    Lmax = 92.0
    ci, si = math.cos(i_r), math.sin(i_r)
    tail_A = (A2[0] + Lmax * ci, A2[1] - Lmax * si)
    s.append(f'<polygon points="{pts([D2, A2, tail_A])}" '
             f'fill="rgba(192,57,43,0.14)" stroke="#c0392b" stroke-width="1.5"/>')
    for f in (0.12, 0.22, 0.45, 0.56, 0.67, 0.78, 0.89):
        head = (A2[0], A2[1] + (D2[1] - A2[1]) * f)
        L = Lmax * (1.0 - f)
        tl = (head[0] + L * ci, head[1] - L * si)
        s.append(line(tl, (head[0] + 2, head[1]), "#c0392b", 1.3, None,
                      ' marker-end="url(#rkR)"'))

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

    s.append(text(660, 578,
                  f"h'' = {h_uso:.2f} m  |  Ka = {Ka:.4f}  |  i = {i:.1f}°",
                  11, "#1f77b4", "start"))
    s.append(text(660, 596, f"IaH,d = {IaH_d:.1f} kN/m", 11, "#c0392b", "start"))
    s.append('</svg>')
    return "".join(s)

# ============================================================
# ESQUEMA FINAL — RANKINE (adaptado dos muros em consola)
# ============================================================
def _svg_esquema_rankine_cf(b1, b2, b3, t_, H, hc, hb, B, i,
                             Ka, h_uso, IaH_d, W_total_d, q_ativo,
                             lang="pt", phi_d=None):
    """Esquema Final — Rankine para muro com contrafortes.

    Adaptação directa de `_svg_esquema_rankine` (muros em consola).
    - Sistema local: X = 0 na aresta do talão (lado retido, direita);
                     X = -b3 na face de trás do paramento;
                     X = -(b2+b3) na face da frente do paramento;
                     X = -B na aresta da biqueira (esquerda).
    - Cunha morta E-D-A + cunha activa D-C-A (se φ' > 0) ou D-x-x-A.
    - Plano vertical AD → impulso Iₐ paralelo ao talude (ângulo i).
    - h'' = AD = H + b3·tan(i) — altura do plano vertical no talão.
    """
    t = lambda pt, en: pt if lang == "pt" else en
    i_r = math.radians(i)
    tan_i = math.tan(i_r)
    Y_D = H + b3 * tan_i                       # altura no plano AD (aresta do talão)

    # Ângulo ξ da cunha activa (se φ' > 0)
    have_C = (phi_d is not None) and (float(phi_d) > 1e-6)
    phi = float(phi_d) if have_C else 0.0
    if have_C:
        arg = min(1.0, math.sin(i_r) / math.sin(math.radians(phi)))
        xi = 45.0 + phi / 2.0 - 0.5 * (math.degrees(math.asin(arg)) - i)
        xi_r = math.radians(xi)
        den_C = math.sin(xi_r) - math.cos(xi_r) * tan_i
        X_C = (Y_D / den_C) * math.cos(xi_r) if den_C > 0.05 else 1e9
        C_cap = False
        if X_C > 3.0 * Y_D:
            C_cap, X_C = True, 3.0 * Y_D
        Y_C = X_C * math.tan(xi_r) if C_cap else Y_D + X_C * tan_i
    else:
        X_C = 0.9 * Y_D
        Y_C = Y_D + X_C * tan_i

    # Faces do paramento no sistema local
    xs0 = -(b2 + b3)      # frente do paramento (esquerda)
    xs1 = -b3             # tardoz do paramento (retido, direita)

    # --------- Helpers gráficos (iguais aos dos muros em consola) ---------
    def mapper(ox, oy, esc):
        return lambda X, Y: (ox + X * esc, oy - Y * esc)

    def pts(lst):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in lst)

    def line(p, q, stroke, w=1.2, dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" '
                f'x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
                f'stroke="{stroke}" stroke-width="{w}"{d}{extra}/>')

    def text(x, y, s_, size=11, fill="#222", anchor="middle",
             weight="bold", extra="", halo=True):
        base = (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
                f'text-anchor="{anchor}" font-weight="{weight}"{extra}')
        halo_t = (base + ' fill="#fdfefe" stroke="#fdfefe" stroke-width="3.5" '
                  'stroke-linejoin="round">' + s_ + '</text>')
        return (halo_t if halo else '') + base + f' fill="{fill}">' + s_ + '</text>'

    def arc(c, r, ang0, ang1, stroke, w=1.5):
        a0, a1 = math.radians(ang0), math.radians(ang1)
        p0 = (c[0] + r * math.cos(a0), c[1] - r * math.sin(a0))
        p1 = (c[0] + r * math.cos(a1), c[1] - r * math.sin(a1))
        sweep = 0 if ang1 > ang0 else 1
        large = 1 if abs(ang1 - ang0) > 180 else 0
        return (f'<path d="M {p0[0]:.1f},{p0[1]:.1f} A {r:.1f},{r:.1f} '
                f'0 {large} {sweep} {p1[0]:.1f},{p1[1]:.1f}" fill="none" '
                f'stroke="{stroke}" stroke-width="{w}"/>')

    def arc_label(c, r, ang0, ang1, s_, color, size=12):
        am = math.radians((ang0 + ang1) / 2.0)
        return text(c[0] + (r + 13) * math.cos(am),
                    c[1] - (r + 13) * math.sin(am) + 4,
                    s_, size, color)

    def dot(p, r=3.2):
        return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="#111"/>'

    def dim_v(xpx, y0, y1, label, cor="#1f77b4"):
        return (f'<line x1="{xpx:.1f}" y1="{y0:.1f}" x2="{xpx:.1f}" y2="{y1:.1f}" '
                f'stroke="{cor}" stroke-width="1.2" '
                f'marker-start="url(#rkD)" marker-end="url(#rkD)"/>'
                + text(xpx + 6, (y0 + y1) / 2.0 + 4, label, 11, cor, "start"))

    def wall(P):
        """Secção transversal do muro (sapata + paramento). O contraforte é
        longitudinal e não aparece na secção transversal do esquema Rankine."""
        poly = [(-B, 0), (-B, hb), (xs0, hb), (xs0, H),
                (xs1, H), (xs1, hb), (0, hb), (0, 0)]
        return (f'<polygon points="{pts([P(x, y) for x, y in poly])}" '
                f'fill="#b8b8b8" stroke="#333" stroke-width="2"/>'
                f'<polygon points="{pts([P(x, y) for x, y in poly])}" '
                f'fill="url(#rkC)" opacity="0.5"/>')

    def surcharge(P, x_from, x_to, gy):
        out, n = [], 0
        xx = x_from
        while xx <= x_to and n < 12:
            g = gy(xx)
            p0, p1 = P(xx, g), P(xx, g)
            out.append(
                f'<line x1="{p0[0]:.1f}" y1="{p0[1]-30:.1f}" '
                f'x2="{p1[0]:.1f}" y2="{p1[1]-7:.1f}" '
                f'stroke="#1f77b4" stroke-width="1.5"/>'
                f'<polygon points="{p1[0]:.1f},{p1[1]-4:.1f} '
                f'{p1[0]-3.5:.1f},{p1[1]-12:.1f} {p1[0]+3.5:.1f},{p1[1]-12:.1f}" '
                f'fill="#1f77b4"/>')
            xx += 0.45 * max(Y_D, 1.0) / 2.0
            n += 1
        return "".join(out)

    # --------- Dimensões do canvas ---------
    W_svg, H_svg = 1060, 660
    oy = 540.0

    # Painel ① — Geometria
    esc1 = min((600.0 - 30.0 - 150.0) / max(B + X_C, 0.1),
               470.0 / max(Y_C, 0.5))
    ox1 = 30.0 + B * esc1
    P1 = mapper(ox1, oy, esc1)

    # Painel ② — Cunha morta + impulso
    esc2 = min((400.0 - 20.0 - 150.0) / max(B + 0.45 * Y_D, 0.1),
               470.0 / max(Y_D + 0.1, 0.5))
    ox2 = 660.0 + B * esc2
    P2 = mapper(ox2, oy, esc2)

    # --------- Abertura do SVG ---------
    s = [f'<svg width="100%" viewBox="0 0 {W_svg} {H_svg}" '
         f'xmlns="http://www.w3.org/2000/svg" '
         f'style="max-width:{W_svg}px;background:#fdfefe;border:1px solid #bbb;'
         f'border-radius:8px;font-family:Segoe UI,Arial,sans-serif;">']
    s.append('<defs>'
             '<marker id="rkD" markerWidth="10" markerHeight="10" refX="9" refY="3" '
             'orient="auto-start-reverse"><polygon points="0,0 10,3 0,6" '
             'fill="#1f77b4"/></marker>'
             '<marker id="rkR" markerWidth="10" markerHeight="10" refX="9" refY="3" '
             'orient="auto"><polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker>'
             '<pattern id="rkH" patternUnits="userSpaceOnUse" width="10" height="10" '
             'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" '
             'stroke="#8b6f47" stroke-width="1.1"/></pattern>'
             '<pattern id="rkC" patternUnits="userSpaceOnUse" width="8" height="8" '
             'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" '
             'stroke="#888" stroke-width="0.8"/></pattern>'
             '</defs>')
    titulo_txt = ("RANKINE (slide 100) — MURO COM CONTRAFORTES — cunha morta E-D-A "
                  "e plano vertical AD" if lang == "pt" else
                  "RANKINE (slide 100) — COUNTERFORT WALL — dead wedge E-D-A "
                  "and vertical plane AD")
    s.append(text(W_svg / 2, 24, titulo_txt, 14))
    s.append(f'<line x1="640" y1="40" x2="640" y2="{H_svg-70}" '
             f'stroke="#ddd" stroke-width="1"/>')

    # --------- Painel ① ---------
    A, E, Dp = P1(0, 0), P1(xs1, H), P1(0, Y_D)
    Cp = P1(X_C, Y_C)
    titulo1 = ("① Geometria: pontos A, D, E" +
               (", C" if have_C else "") if lang == "pt" else
               "① Geometry: points A, D, E" +
               (", C" if have_C else ""))
    s.append(text(320, 56, titulo1, 12, "#1f4e79"))
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" '
             f'fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" '
             f'fill="url(#rkH)" opacity="0.5"/>')

    # Cunha morta E-D-A
    dead = [P1(xs1, hb), E, Dp, A]
    s.append(f'<polygon points="{pts(dead)}" fill="#8f8f8f" stroke="none"/>')

    # Cunha activa D-C-A (ou D-x-x-A sem φ')
    if have_C:
        act = [Dp, Cp, A]
    else:
        xe = X_C
        act = [Dp, P1(xe, Y_D + xe * tan_i), P1(xe, 0), A]
    s.append(f'<polygon points="{pts(act)}" fill="#f1ebdf" stroke="none"/>')
    s.append(f'<polygon points="{pts(act)}" fill="url(#rkH)" opacity="0.18"/>')

    # Muro (sapata + paramento)
    s.append(wall(P1))

    # Linha do talude
    ext = 0.12 * X_C
    G_end = P1(X_C + ext, Y_D + (X_C + ext) * tan_i)
    s.append(line(E, G_end, "#6b4a2f", 2.4))

    # Linhas de extensão + plano AD
    xd = [A[0] + 52, A[0] + 82]
    for pnt, xx in ((E, xd[0]), (Dp, xd[1])):
        s.append(line(pnt, (xx + 8, pnt[1]), "#555", 1, "2,3"))
    s.append(line(A, (xd[1] + 8, A[1]), "#555", 1, "2,3"))
    s.append(line(A, Dp, "#5d3a1f", 2.4, "7,4"))     # plano vertical AD
    if have_C:
        s.append(line(A, Cp, "#222", 1.8, "10,3,2,3"))
        s.append(arc(A, 56.0, 0.0, xi, "#27ae60"))
        s.append(arc_label(A, 56.0, 0.0, xi, "ξ", "#27ae60"))
    if i > 0.05:
        s.append(arc(Dp, 62.0, 0.0, i, "#1f77b4"))
        s.append(arc_label(Dp, 62.0, 0.0, max(i, 8.0), "i", "#1f77b4", 11))

    # Rótulo "cunha morta"
    cx = sum(p[0] for p in dead) / 4.0
    cy = sum(p[1] for p in dead) / 4.0
    s.append(text(cx, cy, t("cunha morta", "dead wedge"), 12, "#fff",
                  "middle", extra=f' transform="rotate(-90 {cx:.1f} {cy:.1f})"',
                  halo=False))

    # Sobrecarga
    if q_ativo > 0:
        s.append(surcharge(P1, xs1 + 0.1, X_C,
                           lambda x: Y_D + x * tan_i))
        qp = P1(xs1 + 0.1, H + 0.1 * tan_i)
        s.append(text(qp[0] + 4, qp[1] - 38, f"q = {q_ativo:.1f} kPa",
                      10, "#1f77b4", "start"))

    # Cotas
    s.append(dim_v(xd[0], A[1], E[1], "h"))
    s.append(dim_v(xd[1], A[1], Dp[1], "h''"))

    # Rótulos A, D, E, C
    pontos = [(A, "A", 6, 20), (Dp, "D", 4, -10), (E, "E", -14, -8)]
    if have_C:
        pontos.append((Cp, "C", 8, -9))
    for pnt, nm, dx, dy in pontos:
        s.append(dot(pnt))
        s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))

    # Rodapé informativo
    s.append(text(30, 578,
                  f"h = H = {H:.2f} m  |  h'' = AD = {Y_D:.2f} m  |  "
                  f"h_uso = {h_uso:.2f} m", 11, "#1f77b4", "start"))
    s.append(text(30, 596,
                  t(f"Plano vertical AD; Iₐ paralelo ao talude (i = {i:.1f}°)",
                    f"Vertical plane AD; Iₐ parallel to slope (i = {i:.1f}°)"),
                  11, "#c0392b", "start"))
    if have_C:
        s.append(text(30, 614,
                      f"ξ = 45° + φ'/2 − ½(arcsen(sen i / sen φ') − i) = "
                      f"{xi:.2f}°   (φ' = {phi:.1f}°)",
                      11, "#27ae60", "start"))

    # --------- Painel ② — Cunha morta e impulso ---------
    A2, E2, D2 = P2(0, 0), P2(xs1, H), P2(0, Y_D)
    titulo2 = ("② Cunha morta E-D-A e impulso Iₐ em AD" if lang == "pt" else
               "② Dead wedge E-D-A and thrust Iₐ on AD")
    s.append(text(850, 56, titulo2, 12, "#1f4e79"))
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" '
             f'fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" '
             f'fill="url(#rkH)" opacity="0.5"/>')

    dead2 = [P2(xs1, hb), E2, D2, A2]
    s.append(f'<polygon points="{pts(dead2)}" fill="#d9d9d9" stroke="none"/>')
    s.append(wall(P2))
    x_gr = 0.30 * Y_D
    s.append(line(E2, P2(x_gr, Y_D + x_gr * tan_i), "#6b4a2f", 2.4))
    s.append(line(A2, D2, "#5d3a1f", 2.4, "7,4"))
    cx2 = sum(p[0] for p in dead2) / 4.0
    cy2 = sum(p[1] for p in dead2) / 4.0
    s.append(text(cx2, cy2, t("cunha morta", "dead wedge"), 12, "#1f4e79",
                  "middle", extra=f' transform="rotate(-90 {cx2:.1f} {cy2:.1f})"'))

    # Setas do impulso Iₐ (paralelas ao talude, apontando para o plano AD)
    Lmax = 92.0
    ci, si = math.cos(i_r), math.sin(i_r)
    tail_A = (A2[0] + Lmax * ci, A2[1] - Lmax * si)
    s.append(f'<polygon points="{pts([D2, A2, tail_A])}" '
             f'fill="rgba(192,57,43,0.14)" stroke="#c0392b" stroke-width="1.5"/>')
    for f in (0.12, 0.22, 0.45, 0.56, 0.67, 0.78, 0.89):
        head = (A2[0], A2[1] + (D2[1] - A2[1]) * f)
        L = Lmax * (1.0 - f)
        tl = (head[0] + L * ci, head[1] - L * si)
        s.append(line(tl, (head[0] + 2, head[1]), "#c0392b", 1.3, None,
                      ' marker-end="url(#rkR)"'))

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

    s.append(text(660, 578,
                  f"h'' = {h_uso:.2f} m  |  Ka = {Ka:.4f}  |  i = {i:.1f}°",
                  11, "#1f77b4", "start"))
    s.append(text(660, 596, f"IaH,d = {IaH_d:.1f} kN/m", 11, "#c0392b", "start"))
    s.append('</svg>')
    return "".join(s)

# Alias para compatibilidade
svg_estrutura_cf = _svg_estrutura_cf

# ============================================================
# ESQUEMA FINAL — RANKINE (slide 100) PARA MURO COM CONTRAFORTES
# Mesma lógica do muro em consola: cunha morta E-D-A, plano vertical AD,
# h'' = H + y'' (y'' = b3·tan i). Funciona com i = 0 (cunha rectangular) e i > 0.
# ============================================================
def _svg_esquema_rankine_cf(b1, b2, b3, H, hc, hb, B, i, Ka, h_uso, IaH_d, W_tot, q_ativo, lang="pt", phi_d=None):
    t = lambda pt, en: pt if lang == "pt" else en
    i_r = math.radians(i)
    tan_i = math.tan(i_r)
    Y_D = H + b3 * tan_i                      # h'' (geometria)
    y2 = b3 * tan_i                           # y''
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

    # Coordenadas (m): origem em A = canto inferior do talão; X para a direita (solo), Y para cima
    xs1 = -b3                 # face de trás do paramento (lado do solo)
    xs0 = -(b3 + b2)          # face da frente do paramento (lado do contraforte)

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
        return f'<line x1="{xpx:.1f}" y1="{y0:.1f}" x2="{xpx:.1f}" y2="{y1:.1f}" stroke="{cor}" stroke-width="1.2" marker-start="url(#rcD)" marker-end="url(#rcD)"/>' + text(xpx + 6, (y0 + y1) / 2.0 + 4, label, 11, cor, "start")
    def dim_h(ypx, x0, x1, label, cor="#1f77b4"):
        return f'<line x1="{x0:.1f}" y1="{ypx:.1f}" x2="{x1:.1f}" y2="{ypx:.1f}" stroke="{cor}" stroke-width="1.2" marker-start="url(#rcD)" marker-end="url(#rcD)"/>' + text((x0 + x1) / 2.0, ypx - 5, label, 11, cor, "middle")

    def wall(P):
        # base + paramento + contraforte (frente), monolítico
        poly = [(-B, 0), (-B, hb), (xs0, hb + hc), (xs0, H), (xs1, H), (xs1, hb), (0, hb), (0, 0)]
        tri = [(-B, hb), (xs0, hb + hc), (xs0, hb)]
        return (f'<polygon points="{pts([P(x, y) for x, y in poly])}" fill="#b8b8b8" stroke="#333" stroke-width="2"/>'
                f'<polygon points="{pts([P(x, y) for x, y in poly])}" fill="url(#rcC)" opacity="0.5"/>'
                f'<polygon points="{pts([P(x, y) for x, y in tri])}" fill="#9c9c9c" stroke="none"/>'
                f'<line x1="{P(-B, hb)[0]:.1f}" y1="{P(-B, hb)[1]:.1f}" x2="{P(xs0, hb + hc)[0]:.1f}" y2="{P(xs0, hb + hc)[1]:.1f}" stroke="#333" stroke-width="2"/>')
    def cf_label(P, esc):
        # rótulo CONTRAFORTE ao longo da hipotenusa (só se houver espaço)
        pa, pb = P(-B, hb), P(xs0, hb + hc)
        if (pb[0] - pa[0]) < 46 or (pa[1] - pb[1]) < 46:
            return ""
        ang = math.degrees(math.atan2(pb[1] - pa[1], pb[0] - pa[0]))
        mx_, my_ = (pa[0] + pb[0]) / 2.0 + 3, (pa[1] + pb[1]) / 2.0 + 14
        return text(mx_, my_, t("CONTRAFORTE", "COUNTERFORT"), 8, "#222", "middle", extra=f' transform="rotate({ang:.1f} {mx_:.1f} {my_:.1f})"', halo=False)
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
    s.append('<defs><marker id="rcD" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto-start-reverse"><polygon points="0,0 10,3 0,6" fill="#1f77b4"/></marker><marker id="rcR" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker><pattern id="rcH" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.1"/></pattern><pattern id="rcC" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#888" stroke-width="0.8"/></pattern></defs>')
    s.append(text(W_svg / 2, 24, t("RANKINE (slide 100) — muro com contrafortes: cunha morta E-D-A e plano vertical AD", "RANKINE (slide 100) — counterfort wall: dead wedge E-D-A and vertical plane AD"), 14))
    s.append(f'<line x1="640" y1="40" x2="640" y2="{H_svg-70}" stroke="#ddd" stroke-width="1"/>')

    # ======================= ① GEOMETRIA =======================
    A, E, Dp = P1(0, 0), P1(xs1, H), P1(0, Y_D)
    Cp = P1(X_C, Y_C)
    s.append(text(320, 56, t("① Geometria: pontos A, D, E" + (", C" if have_C else ""), "① Geometry: points A, D, E" + (", C" if have_C else "")), 12, "#1f4e79"))
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="20" y="{oy:.1f}" width="600" height="26" fill="url(#rcH)" opacity="0.5"/>')

    dead = [P1(xs1, 0), E, Dp, A]
    s.append(f'<polygon points="{pts(dead)}" fill="#8f8f8f" stroke="none"/>')
    if have_C:
        act = [Dp, Cp, A]
    else:
        xe = X_C
        act = [Dp, P1(xe, Y_D + xe * tan_i), P1(xe, 0), A]
    s.append(f'<polygon points="{pts(act)}" fill="#f1ebdf" stroke="none"/>')
    s.append(f'<polygon points="{pts(act)}" fill="url(#rcH)" opacity="0.18"/>')
    s.append(wall(P1))
    s.append(cf_label(P1, esc1))

    ext = 0.12 * X_C
    G_end = P1(X_C + ext, Y_D + (X_C + ext) * tan_i)
    s.append(line(E, G_end, "#6b4a2f", 2.4))                      # superfície do terrapleno
    xd = [A[0] + 52, A[0] + 82, A[0] + 112]
    xlast = xd[2] if i > 0.05 else xd[1]
    s.append(line(E, (xd[0] + 8, E[1]), "#555", 1, "2,3"))
    s.append(line(A, (xd[1] + 8, A[1]), "#555", 1, "2,3"))
    s.append(line(Dp, (xlast + 8, Dp[1]), "#555", 1, "2,3"))
    s.append(line(A, Dp, "#5d3a1f", 2.4, "7,4"))                  # plano vertical AD
    if have_C:
        s.append(line(A, Cp, "#222", 1.8, "10,3,2,3"))
        s.append(arc(A, 56.0, 0.0, xi, "#27ae60"))
        s.append(arc_label(A, 56.0, 0.0, xi, "ξ", "#27ae60"))
    if i > 0.05:
        s.append(arc(Dp, 62.0, 0.0, i, "#1f77b4"))
        s.append(arc_label(Dp, 62.0, 0.0, max(i, 8.0), "i", "#1f77b4", 11))
        # y'' = b3·tan i : prolongamento horizontal de E até ao plano AD
        Eh = P1(0, H)
        s.append(line(E, Eh, "#1f77b4", 1.2, "4,3"))
        s.append(line(Eh, (xd[2] + 8, Eh[1]), "#555", 1, "2,3"))
        s.append(dim_v(xd[2], Eh[1], Dp[1], "y''", "#8e44ad"))

    cx = (sum(p[0] for p in dead) / 4.0)
    cy = (sum(p[1] for p in dead) / 4.0)
    s.append(text(cx, cy, t("cunha morta", "dead wedge"), 12, "#fff", "middle", extra=f' transform="rotate(-90 {cx:.1f} {cy:.1f})"', halo=False))
    if q_ativo > 0:
        s.append(surcharge(P1, xs1 + 0.1, X_C, lambda x: Y_D + x * tan_i))
        qp = P1(xs1 + 0.1, H + 0.1 * tan_i)
        s.append(text(qp[0] + 4, qp[1] - 38, f"q = {q_ativo:.1f} kPa", 10, "#1f77b4", "start"))

    s.append(dim_h(E[1] + 18, E[0], A[0], "b3"))
    s.append(dim_v(xd[0], A[1], E[1], "h"))
    s.append(dim_v(xd[1], A[1], Dp[1], "h''"))
    pontos = [(A, "A", 6, 20), (Dp, "D", 4, -10), (E, "E", -14, -8)]
    if have_C:
        pontos.append((Cp, "C", 8, -9))
    for pnt, nm, dx, dy in pontos:
        s.append(dot(pnt))
        s.append(text(pnt[0] + dx, pnt[1] + dy, nm, 14, "#111"))

    s.append(text(30, 578, f"h = H = {H:.2f} m  |  h'' = AD = {Y_D:.2f} m  |  hc = {hc:.2f} m  |  hb = {hb*100:.0f} cm", 11, "#1f77b4", "start"))
    s.append(text(30, 596, t(f"Plano vertical AD; Iₐ paralelo ao talude (i = {i:.1f}°)", f"Vertical plane AD; Iₐ parallel to slope (i = {i:.1f}°)"), 11, "#c0392b", "start"))
    if have_C:
        s.append(text(30, 614, f"ξ = 45° + φ'/2 − ½(arcsen(sen i / sen φ') − i) = {xi:.2f}°   (φ' = {phi:.1f}°)", 11, "#27ae60", "start"))
    if i > 0.05:
        s.append(text(30, 632, f"y'' = b3·tan i = {b3:.2f}·tan({i:.1f}°) = {y2:.3f} m   →   h'' = H + y'' = {H:.2f} + {y2:.3f} = {Y_D:.3f} m", 11, "#8e44ad", "start"))
    else:
        s.append(text(30, 632, t("Sem inclinação (i = 0°): y'' = 0  →  h'' = h = H  (cunha morta rectangular)", "No slope (i = 0°): y'' = 0  →  h'' = h = H  (rectangular dead wedge)"), 11, "#8e44ad", "start"))

    # ======================= ② CUNHA MORTA + IMPULSO =======================
    A2, E2, D2 = P2(0, 0), P2(xs1, H), P2(0, Y_D)
    s.append(text(850, 56, t("② Cunha morta E-D-A e impulso Iₐ em AD", "② Dead wedge E-D-A and thrust Iₐ on AD"), 12, "#1f4e79"))
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" fill="#8a6a4f" opacity="0.55"/>')
    s.append(f'<rect x="650" y="{oy:.1f}" width="390" height="26" fill="url(#rcH)" opacity="0.5"/>')

    dead2 = [P2(xs1, 0), E2, D2, A2]
    s.append(f'<polygon points="{pts(dead2)}" fill="#d9d9d9" stroke="none"/>')
    s.append(wall(P2))
    s.append(cf_label(P2, esc2))
    x_gr = 0.30 * Y_D
    s.append(line(E2, P2(x_gr, Y_D + x_gr * tan_i), "#6b4a2f", 2.4))
    s.append(line(A2, D2, "#5d3a1f", 2.4, "7,4"))
    cx2 = (sum(p[0] for p in dead2) / 4.0)
    cy2 = (sum(p[1] for p in dead2) / 4.0)
    s.append(text(cx2, cy2, t("cunha morta", "dead wedge"), 12, "#1f4e79", "middle", extra=f' transform="rotate(-90 {cx2:.1f} {cy2:.1f})"'))
    if i > 0.05:
        Eh2 = P2(0, H)
        s.append(line(E2, Eh2, "#1f77b4", 1.2, "4,3"))

    Lmax = 92.0
    ci, si = math.cos(i_r), math.sin(i_r)
    tail_A = (A2[0] + Lmax * ci, A2[1] - Lmax * si)
    s.append(f'<polygon points="{pts([D2, A2, tail_A])}" fill="rgba(192,57,43,0.14)" stroke="#c0392b" stroke-width="1.5"/>')
    for f in (0.12, 0.22, 0.45, 0.56, 0.67, 0.78, 0.89):
        head = (A2[0], A2[1] + (D2[1] - A2[1]) * f)
        L = Lmax * (1.0 - f)
        tl = (head[0] + L * ci, head[1] - L * si)
        s.append(line(tl, (head[0] + 2, head[1]), "#c0392b", 1.3, None, ' marker-end="url(#rcR)"'))

    Pm = (A2[0], A2[1] + (D2[1] - A2[1]) / 3.0)
    Lr = Lmax * 1.05
    tl = (Pm[0] + Lr * ci, Pm[1] - Lr * si)
    s.append(line(tl, Pm, "#c0392b", 3.0, None, ' marker-end="url(#rcR)"'))
    s.append(text(tl[0] + 8, tl[1] - 4, "Iₐ", 13, "#c0392b", "start"))
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
    s.append(text(660, 614, t("h'' = H + y''  (y'' = b3·tan i)", "h'' = H + y''  (y'' = b3·tan i)"), 11, "#8e44ad", "start"))
    s.append('</svg>')
    return "".join(s)

# ============================================================
# FORMULÁRIO
# ============================================================
def formulario_muro_contrafortes():
    lang = st.session_state.get("language", "pt")
    if "fase_cf" not in st.session_state:
        st.session_state.fase_cf = "geotecnica"
        
    st.markdown(f"#### {get_text('cf_dados', lang)}")
    st.markdown(carregar_imagem_local("assets/Picture5.png", 650), unsafe_allow_html=True)
    st.divider()
    
    st.markdown(f"#### {get_text('consola_ec7', lang)}")
    combo = st.radio(get_text("combinacao", lang), [get_text("combinacao1", lang), get_text("combinacao2", lang)], index=1, horizontal=True, key="ec7_cf")
    if get_text("combinacao1", lang) in combo:
        gG_u, gG_f, gQ, gphi, gc, gcu, gRh, gRv = 1.35, 1.00, 1.50, 1.00, 1.00, 1.00, 1.00, 1.00
    else:
        gG_u, gG_f, gQ, gphi, gc, gcu, gRh, gRv = 1.00, 1.00, 1.30, 1.25, 1.25, 1.40, 1.00, 1.00
    st.divider()
    
        # ---------- Helper local: rótulo LaTeX por cima do campo ----------
    def _lbl(txt_pt, txt_en, simbolo, unidade=None, nota=""):
        txt = txt_pt if lang == "pt" else txt_en
        uni = f" &nbsp;[{unidade}]" if unidade else ""
        extra = f" &nbsp;<span style='color:#888;'>{nota}</span>" if nota else ""
        st.markdown(f"**{txt}**{extra} &nbsp;—&nbsp; ${simbolo}${uni}")

    # ============================================================
    # 2. GEOMETRIA
    # ============================================================
    titulo_geo = (get_text("cf_geom", lang)
                  .replace(" (Picture5)", "")
                  .replace(" (picture5)", ""))
    st.markdown(f"#### {titulo_geo}")
    st.markdown(
        "Parâmetros geométricos do muro com contrafortes: "
        r"$b_1$ (consola da frente), $b_2$ (base do paramento), $b_3$ (consola do talão), "
        r"$H$ (altura total), $h_c$ (altura do contraforte), $h_b$ (espessura da sapata) "
        r"e $i$ (inclinação do terrapleno)."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _lbl("Consola 2 (frente)", "Cantilever 2 (front)", "b_1", "m")
        b1 = st.number_input("b1", value=1.2, step=0.1,
                             key="b1_cf", label_visibility="collapsed")
        _lbl("Base do paramento", "Stem base", "b_2", "m")
        b2 = st.number_input("b2", value=0.5, step=0.05,
                             key="b2_cf", label_visibility="collapsed")
    with c2:
        _lbl("Consola 1 (talão)", "Cantilever 1 (heel)", "b_3", "m")
        b3 = st.number_input("b3", value=1.2, step=0.1,
                             key="b3_cf", label_visibility="collapsed")
        t_ = b2
    with c3:
        _lbl("Altura total", "Total height", "H", "m")
        H = st.number_input("H", value=6.0, step=0.1,
                            key="H_cf", label_visibility="collapsed")
        _lbl("Altura do contraforte", "Counterfort height", "h_c", "m")
        hc = st.number_input("hc", value=4.0, step=0.1,
                             key="hc_cf", label_visibility="collapsed")
    with c4:
        _lbl("Espessura da sapata", "Base thickness", "h_b", "m")
        hb = st.number_input("hb", value=0.5, step=0.05,
                             key="hb_cf", label_visibility="collapsed")
        _lbl("Inclinação do terrapleno", "Backfill slope", "i", "°")
        i = st.number_input("i", value=0.0, step=1.0,
                            key="i_cf", label_visibility="collapsed")

    B = b1 + b2 + b3
    st.latex(rf"B = b_1 + b_2 + b_3 = {b1:.2f} + {b2:.2f} + {b3:.2f} = "
             rf"\mathbf{{{B:.2f}}}\ \text{{m}}")
    if hc > H - hb:
        st.error(get_text("cf_erro_hc", lang)); st.stop()

    st.divider()

    # ============================================================
    # 3. SOLO RETIDO (LADO ACTIVO)
    # ============================================================
    st.markdown(f"#### {get_text('cf_solo_ativo', lang)}")
    st.markdown(
        "Características do solo retido, responsável pelo impulso activo sobre o paramento. "
        r"Considera-se $\phi'$ (ângulo de atrito efectivo), $c'$ (coesão efectiva) e "
        r"$q$ (sobrecarga uniforme no terrapleno)."
    )

    c1, c2 = st.columns(2)
    with c1:
        _lbl("Peso específico natural", "Natural unit weight", r"\gamma", "kN/m³")
        gamma = st.number_input("γ", min_value=10.0, max_value=25.0,
                                value=18.0, step=0.5, key="g_cf",
                                label_visibility="collapsed")
        _lbl("Ângulo de atrito interno", "Internal friction angle", r"\phi'", "°")
        phi = st.number_input("φ'", min_value=0.0, max_value=60.0,
                              value=30.0, step=1.0, key="phi_cf",
                              label_visibility="collapsed")
    with c2:
        _lbl("Coesão efectiva", "Effective cohesion", "c'", "kPa")
        c_ = st.number_input("c'", min_value=0.0, max_value=100.0,
                             value=0.0, step=1.0, key="c_cf",
                             label_visibility="collapsed")
        _lbl("Sobrecarga no terrapleno", "Backfill surcharge", "q", "kPa")
        q = st.number_input("q", min_value=0.0, max_value=100.0,
                            value=10.0, step=1.0, key="q_cf",
                            label_visibility="collapsed")

    st.divider()

    # ============================================================
    # 4. SOLO DE FUNDAÇÃO
    # ============================================================
    st.markdown(f"#### {get_text('cf_solo_fund', lang)}")
    st.markdown(
        "Parâmetros resistentes do solo sob a sapata, usados nas verificações de "
        r"capacidade de carga (Meyerhof) e deslizamento na base."
    )

    c1, c2 = st.columns(2)
    with c1:
        _lbl("Peso específico", "Unit weight", r"\gamma_{fund}", "kN/m³")
        gamma_f = st.number_input("γ_f", min_value=10.0, max_value=25.0,
                                  value=18.0, step=0.5, key="gf_cf",
                                  label_visibility="collapsed")
        _lbl("Ângulo de atrito", "Friction angle", r"\phi'_{fund}", "°")
        phi_f = st.number_input("φ'_f", min_value=0.0, max_value=60.0,
                                value=28.0, step=1.0, key="phif_cf",
                                label_visibility="collapsed")
        _lbl("Coesão efectiva", "Effective cohesion", "c'_{fund}", "kPa")
        c_f = st.number_input("c'_f", min_value=0.0, max_value=100.0,
                              value=2.0, step=0.5, key="cf_cf",
                              label_visibility="collapsed")
    with c2:
        _lbl("Coesão não drenada", "Undrained cohesion", "c_{u,fund}", "kPa")
        cu_f = st.number_input("c_u", min_value=0.0, max_value=200.0,
                               value=0.0, step=1.0, key="cuf_cf",
                               label_visibility="collapsed")
        _lbl("Atrito solo–base", "Soil–base friction", r"\delta_b", "°")
        delta_b = st.number_input("δ_b", min_value=0.0, max_value=60.0,
                                  value=20.0, step=1.0, key="db_cf",
                                  label_visibility="collapsed")
        st.caption(get_text("info_delta_b", lang))

    st.divider()

    # ============================================================
    # 5. MATERIAIS (REBAP)
    # ============================================================
    st.markdown(f"#### {get_text('cf_materiais', lang)}")
    st.markdown(
        r"Características dos materiais para o dimensionamento estrutural: classe do "
        r"betão ($f_{ck}$), tipo de aço ($f_{yk}$) e recobrimento nominal das armaduras "
        r"($c_{nom}$)."
    )

    c1, c2 = st.columns(2)
    with c1:
        _lbl("Classe do betão", "Concrete class", "f_{ck}")
        cb = st.selectbox("Betão", ["B20", "B25", "B30", "B35", "B40"], 1,
                          key="cb_cf", label_visibility="collapsed")
        _lbl("Tipo de aço", "Steel type", "f_{yk}")
        ta = st.selectbox("Aço", ["A235", "A400", "A500"], 1,
                          key="ta_cf", label_visibility="collapsed")
    with c2:
        _lbl("Recobrimento nominal", "Nominal cover", "c_{nom}", "mm")
        rec = st.number_input("Recobrimento", min_value=20, max_value=80,
                              value=50, step=5, key="rec_cf",
                              label_visibility="collapsed")

    st.divider()


    # ============================================================
    # BOTÃO CALCULAR / RETOMAR ARMADURAS
    # ============================================================
    if st.session_state.fase_cf == "geotecnica":
        if st.button(get_text("cf_btn", lang),
                     type="primary", use_container_width=True, key="btn_cf"):
            calcular_muro_cf(
                b1, b2, b3, t_, H, hc, hb, B, i,
                gamma, phi, c_, q,
                gamma_f, phi_f, c_f, cu_f, delta_b,
                combo, gG_u, gG_f, gQ, gphi, gc, gcu, gRh, gRv,
                cb, ta, rec,
            )
    else:
        d = st.session_state.get("dados_cf", {})
        if d:
            dimensionar_cf(**d)
        else:
            st.error("Dados não encontrados / Data not found.")
        st.divider()
        st.button(get_text("consola_btn_voltar_geo", lang),
                  use_container_width=True, on_click=voltar_cf)

# ============================================================
# CÁLCULO GEOTÉCNICO — Rankine (idêntico ao muro em consola)
# ============================================================
def calcular_muro_cf(b1, b2, b3, t_, H, hc, hb, B, i, gamma, phi, c_, q, gamma_f, phi_f, c_f, cu_f, delta_b, combo, gG_u, gG_f, gQ, gphi, gc, gcu, gRh, gRv, cb, ta, rec):
    lang = st.session_state.get("language", "pt")
    st.divider()
    st.markdown(f"### {get_text('cf_res', lang)}")
    
    phi_d = calcular_phi_d(phi, gphi)
    phi_fd = calcular_phi_d(phi_f, gphi)
    c_fd = c_f / gc
    cu_fd = cu_f / gcu
    q_d = q * gQ
    i_rad = math.radians(i)
    phi_d_rad = math.radians(phi_d)
    Hs = H - hb
    tan_i = math.tan(i_rad)
    
    Ka = Ka_rankine_slide100(phi_d_rad, i_rad)
    Kaq = Ka
    theta = i_rad
    y_linha = b3 * tan_i
    h_uso = H + y_linha
    
    st.markdown(f"**{get_text('coeficiente_impulso', lang)} — Rankine (slide 100)**")
    if i > 0:
        st.latex(r"K_{a\gamma} = \frac{\cos i - \sqrt{\cos^2 i - \cos^2\phi'_d}}{\cos i + \sqrt{\cos^2 i - \cos^2\phi'_d}}\,\cos i")
        st.latex(r"K_{aq} = K_{a\gamma}")
    else:
        st.latex(r"K_a = \frac{1 - \sin\phi'_d}{1 + \sin\phi'_d}")
        st.latex(r"K_{aq} = K_a")
        
    st.write(rf"- $\phi'_d = {phi_d:.2f}°$, $i = {i:.1f}°$ → $K_a = K_{{aq}} = \mathbf{{{Ka:.4f}}}$")
    st.write(rf"- $y'' = b_3 \tan i = {b3:.2f} \cdot \tan({i:.1f}°) = {y_linha:.3f}$ m")
    st.write(rf"- $h'' = H + y'' = {H:.2f} + {y_linha:.3f} = \mathbf{{{h_uso:.3f}}}$ m")
    
    st.markdown(f"**{get_text('impulso_ativo', lang)}**")
    st.latex(get_text("formula_impulso_consola", lang))
    Ia_solo = 0.5 * Ka * gamma * h_uso ** 2
    Ia_sob = Kaq * q_d * h_uso
    Ia_caract = Ia_solo + Ia_sob
    Ia_d = Ia_caract * gG_u
    IaH_d = Ia_d * math.cos(theta)
    IaV_d = Ia_d * math.sin(theta)
    
    st.write(rf"- $I_{{a,solo}} = {Ia_solo:.2f}$ kN/m | $I_{{a,sobr.}} = {Ia_sob:.2f}$ kN/m")
    st.write(rf"- $I_{{a,d}} = \mathbf{{{Ia_d:.2f}}}$ kN/m | $I_{{aH,d}} = \mathbf{{{IaH_d:.2f}}}$ | $I_{{aV,d}} = \mathbf{{{IaV_d:.2f}}}$")
    st.divider()
    
    W_stem_d = 25.0 * (b2 * Hs) * gG_f
    W_base_d = 25.0 * B * hb * gG_f
    W_cf_d = 25.0 * (b1 * hc / 2.0) * gG_f
    solo_b3_h = Hs + b3 * tan_i / 2.0
    W_solo_b3_d = gamma * b3 * solo_b3_h * gG_f
    W_sob_d = q * b3 * gQ
    W_tot = W_stem_d + W_base_d + W_cf_d + W_solo_b3_d + W_sob_d
    
    st.markdown(f"#### {get_text('cf_pesos', lang)}")
    st.write(rf"- $W_{{stem}} = {W_stem_d:.1f}$ | $W_{{base}} = {W_base_d:.1f}$ | $W_{{contraforte}} = {W_cf_d:.1f}$ | $W_{{solo}} = {W_solo_b3_d:.1f}$ | $W_{{q}} = {W_sob_d:.1f}$ kN/m")
    st.write(rf"- $W_{{total}} = \mathbf{{{W_tot:.2f}}}$ kN/m")
    
    x_stem = b1 + b2 / 2.0
    x_cf = 2.0 * b1 / 3.0
    x_solo_b3 = B - b3 / 2.0
    x_sob = B - b3 / 2.0
    
    M_est = (W_base_d * B / 2.0 + W_stem_d * x_stem + W_cf_d * x_cf + W_solo_b3_d * x_solo_b3 + W_sob_d * x_sob + IaV_d * B)
    M_derr = IaH_d * h_uso / 3.0
    V_d = W_tot + IaV_d
    x_R = (M_est - M_derr) / V_d if V_d > 0 else 0.0
    e_cc = x_R - B / 2.0
    e = abs(e_cc)
    Bl = max(0.0, B - 2.0 * e)
    
    st.markdown(f"#### {get_text('consola_momentos', lang)}")
    st.latex(r"e = \frac{B}{2} - \frac{M_{est} - M_{derr}}{V_d}")
    st.write(rf"- $M_{{est}} = {M_est:.2f}$ kNm/m | $M_{{derr}} = {M_derr:.2f}$ kNm/m")
    st.write(rf"- $V_d = {V_d:.2f}$ kN/m | $e = \mathbf{{{e:.3f}}}$ m | $B' = {Bl:.3f}$ m")
    
    if e <= B / 6.0:
        st.success(get_text('dentro_nucleo', lang, B6=B/6, e=e))
    else:
        st.warning(get_text('fora_nucleo', lang, B6=B/6, e=e))
    st.divider()
    
    ok_derr = M_est >= M_derr
    if cu_fd > 0:
        Rd_h = cu_fd * Bl / gRh
        cis = "Não drenada / Undrained (Cu)"
    else:
        Rd_h = V_d * math.tan(math.radians(delta_b)) / gRh
        cis = f"Drenada / Drained (δb = {delta_b:.0f}°)"
        
    ok_des = (Rd_h / IaH_d) >= 1.0 if IaH_d > 0 else True
    
    Nc, Nq, Ng = meyerhof_N(phi_fd)
    if cu_fd == 0:
        q_Rd = (c_fd * Nc + gamma_f * hb * Nq + 0.5 * gamma_f * Bl * Ng) / gRv
    else:
        q_Rd = 5.14 * cu_fd / gRv
        
    sig_r = (V_d / B) * (1 + 6 * e_cc / B)
    sig_l = (V_d / B) * (1 - 6 * e_cc / B)
    ok_carga = q_Rd >= max(sig_r, sig_l)
    
    st.markdown(f"#### {get_text('cf_verif', lang)}")
    st.write(rf"- Meyerhof: $\phi'_{{d,fund}} = {phi_fd:.2f}°$ → $N_c = {Nc:.2f}$, $N_q = {Nq:.2f}$, $N_\gamma = {Ng:.2f}$")
    st.write(rf"- **{get_text('derrubamento', lang)}**: {M_est:.1f} ≥ {M_derr:.1f} → {'✅' if ok_derr else '❌'}")
    st.write(rf"- **{get_text('deslizamento', lang)}** ({cis}): {Rd_h:.1f} ≥ {IaH_d:.1f} → {'✅' if ok_des else '❌'}")
    st.write(rf"- **{get_text('capacidade_carga', lang)}**: {q_Rd:.1f} ≥ {max(sig_r, sig_l):.1f} kPa → {'✅' if ok_carga else '❌'}")
    
    svg = _svg_estrutura_cf(b1, b2, b3, t_, H, hc, hb, B, i, lang)
    st.markdown(f"### {get_text('cf_esquema', lang)}")
    st.markdown(svg, unsafe_allow_html=True)

    svg_rk = _svg_esquema_rankine_cf(b1, b2, b3, H, hc, hb, B, i, Ka, h_uso, IaH_d, W_tot, q, lang, phi_d=phi_d)
    st.markdown(f"### {get_text('consola_esquema_final', lang)} — Rankine")
    st.markdown(svg_rk, unsafe_allow_html=True)
    
    if ok_derr and ok_des and ok_carga:
        st.success(get_text("muro_satisfaz", lang))
        st.session_state.dados_cf = dict(
            b1=b1, b2=b2, b3=b3, t_=t_, H=H, hc=hc, hb=hb, B=B, Hs=Hs, i=i, combo=combo,
            gamma=gamma, phi=phi, q=q, gamma_f=gamma_f, phi_f=phi_f, c_f=c_f, cu_f=cu_f, delta_b=delta_b,
            gG_u=gG_u, gG_f=gG_f, gQ=gQ, cb=cb, ta=ta, rec=rec, Ka=Ka, Kaq=Kaq, h_uso=h_uso,
            Ia_d=Ia_d, IaH_d=IaH_d, IaV_d=IaV_d, M_derr=M_derr, W_cf=W_cf_d, W_tot=W_tot,
            V_d=V_d, e=e_cc, Bl=Bl, sig_l=sig_l, sig_r=sig_r,
            svg=svg, svg_rankine=svg_rk,           # <-- acrescentar svg_rankine
            q_d=q_d, phi_d=phi_d
        )
        st.divider()
        st.button(get_text("consola_btn_arm", lang), type="primary", use_container_width=True, on_click=prosseguir_cf, key="btn_cf_arm")
    else:
        st.error(get_text("muro_nao_satisfaz", lang))

# ============================================================
# DIMENSIONAMENTO ESTRUTURAL
# ============================================================
def dimensionar_cf(b1, b2, b3, t_, H, hc, hb, B, Hs, i, combo, gamma, phi, q,
                   gamma_f, phi_f, c_f, cu_f, delta_b, gG_u, gG_f, gQ, cb, ta, rec,
                   Ka, Kaq, h_uso, Ia_d, IaH_d, IaV_d, M_derr, W_cf, W_tot,
                   V_d, e, Bl, sig_l, sig_r, svg, q_d, phi_d,
                   svg_rankine=None, **kw):
    lang = st.session_state.get("language", "pt")
    st.divider()
    st.markdown(f"### {get_text('cf_dim_arm', lang)}")

    # ------------------------------------------------------------------
    # 1) MATERIAIS
    # ------------------------------------------------------------------
    fck = 0.8 * {"B20": 20, "B25": 25, "B30": 30, "B35": 35, "B40": 40}[cb]
    fcd = fck / 1.5
    fctd = 0.30 * (fck ** (2 / 3)) / 1.5
    fyk = {"A235": 235, "A400": 400, "A500": 500}[ta]
    fsyd = fyk / 1.15
    fbd = 2.25 * fctd
    eta = {"A235": 1.4, "A400": 1.0, "A500": 0.8}[ta]
    rho_min = {"A235": 0.25, "A400": 0.15, "A500": 0.12}[ta] / 100.0

    st.write(rf"- $f_{{cd}} = {fcd:.2f}$ MPa | $f_{{ctd}} = {fctd:.2f}$ MPa | "
             rf"$f_{{bd}} = {fbd:.2f}$ MPa | $f_{{syd}} = {fsyd:.2f}$ MPa")

    st.markdown("**Flexão Simples (Art. 52 REBAP)**")
    st.latex(r"\mu = \frac{M_{Ed}}{b\,d^2 f_{cd}}\;;\;\omega = \mu(1+\mu)\;;\;"
             r"A_s = \frac{\omega\,b\,d\,f_{cd}}{f_{syd}}")
    st.markdown("**Armadura Mínima (Art. 90/104 REBAP)**")
    st.latex(r"A_{s,min} = \rho\,b\,d\quad;\quad \rho = " +
             ("0.25\\%" if ta == "A235" else "0.15\\%" if ta == "A400" else "0.12\\%"))
    st.markdown("**Armadura Máxima (Art. 90.2 REBAP)**")
    st.latex(r"A_{s,max} = 0.04\,A_c = 0.04\,b\,h")
    st.markdown("**Armadura de Distribuição (Art. 108 REBAP)**")
    st.latex(r"A_{s,dist} = 0.20\,A_s")
    st.markdown("**Esforço Transverso (Art. 53 REBAP)**")
    st.latex(get_text("formula_VRd_corte", lang))
    st.markdown("**Amarração (Art. 80 REBAP)**")
    st.latex(get_text("formula_amarracao", lang))

    # Espessuras mínimas
    st.markdown("##### Verificação de espessuras mínimas")
    for nm, L, h in (("Paramento", Hs, Hs), ("Consola 1", b3, hb), ("Consola 2", b1, hb)):
        hmin = max(2 * L / (30 * eta), 0.07)
        st.write(rf"- **{nm}**: $L = {L:.2f}$ m | $h_{{min}} = {hmin*100:.1f}$ cm "
                 rf"vs $h = {h*100:.0f}$ cm " + ("✅" if h >= hmin else "⚠️"))

    # ------------------------------------------------------------------
    # 2) FUNÇÃO DE SECÇÃO
    # ------------------------------------------------------------------
    def seccao(Msd, Vsd, h_mm):
        d = h_mm - rec - 5
        mu = (Msd * 1e6) / (1000 * d * d * fcd) if Msd > 0 else 0.0
        w = mu * (1 + mu)
        As = w * 1000 * d * fcd / fsyd
        As_min = rho_min * 1000 * d
        As_max = 0.04 * 1000 * h_mm
        As_f = min(max(As, As_min), As_max)
        dm, sp, Aef = _escolher_armadura(As_f)
        d_eff = h_mm - rec - dm / 2
        dd, ss, Aef_d = _escolher_armadura(0.2 * As_f, diam_min=6)
        fac = max(0.6, 0.6 * (1.6 - d_eff / 1000))
        VRd = fac * 0.6 * fctd * 1000 * d_eff / 1000
        lb = max((dm / 4) * (fsyd / fbd) * (As / Aef if Aef else 1),
                 10 * dm, 100, 0.3 * (dm / 4) * (fsyd / fbd))
        As_dist = 0.20 * As_f
        return dict(d=d, d_eff=d_eff, mu=mu, w=w, As=As,
                    As_min=As_min, As_max=As_max, As_f=As_f, As_dist=As_dist,
                    diam=dm, esp=sp, Aef=Aef, dd=dd, ee=ss, Aef_d=Aef_d,
                    VRd=VRd, ok_corte=VRd >= Vsd, ok_esp=sp <= min(1.5 * h_mm, 350),
                    lb=lb, Vsd=Vsd, Msd=Msd,
                    M=Msd, V=Vsd)          # <-- aliases usados na apresentação

    # ------------------------------------------------------------------
    # 3) CÁLCULO DOS ESFORÇOS EM CADA PEÇA
    # ------------------------------------------------------------------
    # Paramento
    p0 = Kaq * q_d
    p1 = Kaq * q_d + Ka * gamma * Hs
    M_par = Ka * gamma * gG_u * Hs ** 3 / 6 + Ka * q_d * Hs ** 2 / 2
    V_par = Ka * gamma * gG_u * Hs ** 2 / 2 + Ka * q_d * Hs

    # Consola 1 (talão)
    sig_stem_dir = sig_l + (sig_r - sig_l) * ((b1 + b2) / B)
    up1 = (sig_r + sig_stem_dir) / 2
    down1 = gQ * q + gG_u * (gamma * Hs + 25 * hb)
    net1 = up1 - down1
    M1 = abs(net1) * b3 ** 2 / 2
    V1 = abs(net1) * b3

    # Consola 2 (frente)
    sig_stem_esq = sig_l + (sig_r - sig_l) * (b1 / B)
    q_cf = W_cf / b1 if b1 > 0 else 0.0
    up2 = (sig_l + sig_stem_esq) / 2
    down2 = gG_f * (25 * hb + q_cf)
    net2 = up2 - down2
    M2 = abs(net2) * b1 ** 2 / 2
    V2 = abs(net2) * b1

    r_par = seccao(M_par, V_par, Hs * 1000)
    r_par.update(elem="Paramento", face=get_text("consola_face_dir", lang),
                 H_elem=Hs, label_H="H_s")

    r_c1 = seccao(M1, V1, hb * 1000)
    r_c1.update(elem="Consola 1",
                face=get_text("consola_face_sup", lang) if net1 < 0 else get_text("consola_face_inf", lang),
                H_elem=b3, label_H="b_3")

    r_c2 = seccao(M2, V2, hb * 1000)
    r_c2.update(elem="Consola 2",
                face=get_text("consola_face_sup", lang) if net2 < 0 else get_text("consola_face_inf", lang),
                H_elem=b1, label_H="b_1")

    res = [r_par, r_c1, r_c2]

    # ------------------------------------------------------------------
    # 4) APRESENTAÇÃO DETALHADA DE CADA PEÇA
    # ------------------------------------------------------------------
    def _bloco_peca(titulo, subtitulo, r, q_up=None, q_down=None, q_net=None):
        st.markdown(f"#### {titulo} {subtitulo}")
        if q_up is not None and q_down is not None:
            st.write(rf"- $q_{{up}} = {q_up:.1f}$ kPa | $q_{{down}} = {q_down:.1f}$ kPa"
                     + (rf" | $q_{{net}} = {q_net:.1f}$ kPa" if q_net is not None else ""))
        st.write(rf"- **$M_{{sd}} = {r['M']:.2f}$ kNm/m** | "
                 rf"**$V_{{sd}} = {r['V']:.2f}$ kN/m**")
        st.write(rf"- $\mu = {r['mu']:.4f}$ | $\omega = {r['w']:.4f}$ | $d = {r['d']:.1f}$ mm")
        st.write(rf"- $A_{{s,calc}} = {_cm2(r['As']):.2f}$ cm²/m")
        st.write(rf"- $A_{{s,min}} = {_cm2(r['As_min']):.2f}$ cm²/m  |  "
                 rf"$A_{{s,max}} = {_cm2(r['As_max']):.2f}$ cm²/m")
        st.write(rf"- **$A_s = {_cm2(r['As_f']):.2f}$ cm²/m** "
                 rf"(face {r['face']}) → **{_fmt(r['diam'], r['esp'])}**")
        st.write(rf"- $A_{{s,dist}} = 0.20\,A_s = {_cm2(r['As_dist']):.2f}$ cm²/m → "
                 rf"**{_fmt(r['dd'], r['ee'])}**")
        st.write(rf"- **Corte**: $V_{{Rd}} = {r['VRd']:.2f}$ kN ≥ "
                 rf"$V_{{sd}} = {r['Vsd']:.2f}$ kN → "
                 + ("✅ SATISFAZ" if r["ok_corte"] else "❌ NÃO SATISFAZ"))
        st.write(rf"- **Amarração**: $l_b = {r['lb']:.0f}$ mm | "
                 rf"Espaçamento {'✅' if r['ok_esp'] else '⚠️'}")
        st.success(f"✅ {_fmt(r['diam'], r['esp'])} | Dist: {_fmt(r['dd'], r['ee'])}"
                   + ("" if r["ok_corte"] else "  —  ⚠️ VERIFICAR CORTE"))

    _bloco_peca(f"🧱 {get_text('cf_paramento', lang)}",
                f"($H_s = {Hs:.2f}$ m)",
                r_par, q_up=p1, q_down=p0)
    _bloco_peca(f"🔹 {get_text('cf_consola1', lang)}",
                f"($b_3 = {b3:.2f}$ m)",
                r_c1, q_up=up1, q_down=down1, q_net=abs(net1))
    _bloco_peca(f"🔹 {get_text('cf_consola2', lang)}",
                f"($b_1 = {b1:.2f}$ m, $q_{{cf}} = {q_cf:.1f}$ kPa)",
                r_c2, q_up=up2, q_down=down2, q_net=abs(net2))

    # ------------------------------------------------------------------
    # 5) TABELA-RESUMO — duas versões (UI HTML limpa + relatório com LaTeX)
    # ------------------------------------------------------------------
    st.markdown(f"#### {get_text('cf_tabela_pecas', lang)}")

    # --- 5a) Tabela para UI: HTML puro (sem LaTeX) ---
    def _ui_head():
        return (f"<table style='border-collapse:collapse;width:100%;font-size:0.88em;'>"
                f"<tr style='background:#2c3e50;color:#fff;'>"
                f"<th style='padding:6px;border:1px solid #ddd;'>Peça</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>Face</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>M<sub>sd</sub><br>(kNm/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>V<sub>sd</sub><br>(kN/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>μ</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>A<sub>s,calc</sub><br>(cm²/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>A<sub>s,min</sub><br>(cm²/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>A<sub>s,max</sub><br>(cm²/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'><b>A<sub>s</sub></b><br>(cm²/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>A<sub>s,dist</sub><br>(cm²/m)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>Armadura<br>Principal</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>Distrib.</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>V<sub>Rd</sub><br>(kN)</th>"
                f"<th style='padding:6px;border:1px solid #ddd;'>Corte</th></tr>")

    tab_ui = _ui_head()
    for r in res:
        tab_ui += (
            f"<tr><td><strong>{r['elem']}</strong></td>"
            f"<td>{r['face']}</td>"
            f"<td>{r['M']:.2f}</td>"
            f"<td>{r['V']:.2f}</td>"
            f"<td>{r['mu']:.4f}</td>"
            f"<td>{_cm2(r['As']):.2f}</td>"
            f"<td>{_cm2(r['As_min']):.2f}</td>"
            f"<td>{_cm2(r['As_max']):.2f}</td>"
            f"<td><strong>{_cm2(r['As_f']):.2f}</strong></td>"
            f"<td>{_cm2(r['As_dist']):.2f}</td>"
            f"<td><strong>{_fmt(r['diam'], r['esp'])}</strong></td>"
            f"<td>{_fmt(r['dd'], r['ee'])}</td>"
            f"<td>{r['VRd']:.2f}</td>"
            f"<td>{'✅' if r['ok_corte'] else '❌'}</td></tr>"
        )
    tab_ui += "</table>"
    st.markdown(tab_ui, unsafe_allow_html=True)

    # --- 5b) Tabela para o RELATÓRIO: pode usar LaTeX (MathJax) ---
    tab_rel = (
        "<table><tr>"
        "<th>Peça</th><th>Face</th>"
        "<th>$M_{sd}$<br>(kNm/m)</th>"
        "<th>$V_{sd}$<br>(kN/m)</th>"
        "<th>$\\mu$</th>"
        "<th>$A_{s,calc}$<br>(cm²/m)</th>"
        "<th>$A_{s,min}$<br>(cm²/m)</th>"
        "<th>$A_{s,max}$<br>(cm²/m)</th>"
        "<th>$A_s$<br>(cm²/m)</th>"
        "<th>$A_{s,dist}$<br>(cm²/m)</th>"
        "<th>Armadura<br>Principal</th>"
        "<th>Distribuição</th>"
        "<th>$V_{Rd}$<br>(kN)</th>"
        "<th>Corte</th></tr>"
    )
    for r in res:
        tab_rel += (
            f"<tr><td><strong>{r['elem']}</strong></td>"
            f"<td>{r['face']}</td>"
            f"<td>{r['M']:.2f}</td>"
            f"<td>{r['V']:.2f}</td>"
            f"<td>{r['mu']:.4f}</td>"
            f"<td>{_cm2(r['As']):.2f}</td>"
            f"<td>{_cm2(r['As_min']):.2f}</td>"
            f"<td>{_cm2(r['As_max']):.2f}</td>"
            f"<td><strong>{_cm2(r['As_f']):.2f}</strong></td>"
            f"<td>{_cm2(r['As_dist']):.2f}</td>"
            f"<td><strong>{_fmt(r['diam'], r['esp'])}</strong></td>"
            f"<td>{_fmt(r['dd'], r['ee'])}</td>"
            f"<td>{r['VRd']:.2f}</td>"
            f"<td>{'✅' if r['ok_corte'] else '❌'}</td></tr>"
        )
    tab_rel += "</table>"

    # ------------------------------------------------------------------
    # 6) GRÁFICOS
    # ------------------------------------------------------------------
    st.markdown(f"#### {get_text('cf_graficos', lang)}")
    sv_par = _svg_laje_vertical(Hs, p0, p1, M_par, V_par, "PARAMENTO / STEM")
    sv_c1 = _svg_laje_horizontal(b3, down1, up1, net1,
                                 "cima" if net1 > 0 else "baixo",
                                 M1, V1, "CONSOLA 1", "esq")
    sv_c2 = _svg_laje_horizontal(b1, down2, up2, net2,
                                 "cima" if net2 > 0 else "baixo",
                                 M2, V2, "CONSOLA 2", "dir")
    st.markdown(sv_par, unsafe_allow_html=True)
    st.markdown(sv_c1, unsafe_allow_html=True)
    st.markdown(sv_c2, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # 7) VERIFICAÇÕES (HTML para relatório)
    # ------------------------------------------------------------------
    ver = "<ul>"
    for r in res:
        ver += (f"<li><strong>{r['elem']}</strong>: "
                f"$A_s = {_cm2(r['As_f']):.2f}$ cm²/m, "
                f"$A_{{s,min}} = {_cm2(r['As_min']):.2f}$ cm²/m, "
                f"$A_{{s,max}} = {_cm2(r['As_max']):.2f}$ cm²/m, "
                f"$A_{{s,dist}} = {_cm2(r['As_dist']):.2f}$ cm²/m, "
                f"$V_{{Rd}} = {r['VRd']:.2f}$ kN vs $V_{{sd}} = {r['Vsd']:.2f}$ kN "
                f"({'OK' if r['ok_corte'] else 'NOK'}), "
                f"espaçamento {'OK' if r['ok_esp'] else 'verificar'}</li>")
    ver += "</ul>"

    # ---- SVG combinado para o relatório -------------------------------
    diagramas_completos = (
        (svg or "") + (svg_rankine or "") + sv_par + sv_c1 + sv_c2
    )

    # ------------------------------------------------------------------
    # 8) RELATÓRIO
    # ------------------------------------------------------------------
    html = relatorios_consola.gerar_relatorio_html_muro_consola(
        nome=st.session_state.nome, curso=st.session_state.curso,
        genero=st.session_state.genero,
        H=H, HR=Hs, D=0, B=B, bt=b1, bh=b3, ts=b2, tb=hb, i=i,
        gamma_ativo=gamma, gamma_sat_ativo=gamma,
        phi_ativo=phi, c_ativo=0.0, q_ativo=q, z_w_ativo=0.0,
        gamma_passivo=gamma, gamma_sat_passivo=gamma,
        phi_passivo=phi, c_passivo=0.0, z_w_passivo=0.0,
        gamma_fund=gamma_f, gamma_sat_fund=gamma_f,
        phi_fund=phi_f, c_fund=c_f, cu_fund=cu_f, delta_b=delta_b,
        metodo=f"Rankine ({'counterfort' if lang=='en' else 'contrafortes'})",
        delta=0.0, combo_ec7=combo,
        g_G_unfav=gG_u, g_G_fav=gG_f, g_Q=gQ,
        g_phi=1.0, g_c=1.0, g_cu=1.0, g_Rh=1.0, g_Rv=1.0,
        phi_ativo_d=phi_d, phi_passivo_d=phi_d, phi_fund_d=phi_f,
        c_ativo_d=0.0, c_passivo_d=0.0, c_fund_d=c_f, cu_fund_d=cu_f,
        delta_d=0.0, q_d=q_d,
        Ka=Ka, Kp=0.0, Ia_ativo_caract=Ia_d, Ia_ativo_d=Ia_d,
        IaH_d=IaH_d, IaV_d=IaV_d,
        Ip_passivo_caract=0.0, Rpd_d=0.0,
        W_stem_d=0.0, W_base_d=0.0, W_solo_talao_d=0.0, W_solo_biqueira_d=0.0,
        W_total_d=W_tot, M_est_total=0.0, M_derr_total=M_derr,
        V_d=V_d, e=e, B_linha=Bl, Rd_h=0.0, tipo_cisalhamento="",
        q_Rd=0.0, sigma_max_d=max(sig_l, sig_r),
        ok_derr=True, ok_desliz=True, ok_carga=True,
        classe_betao=cb, tipo_aco=ta, recobrimento=rec,
        fck=fck, fcd=fcd, fctd=fctd, fyk=fyk, fsyd=fsyd,
        M_stem_d=res[0]['M'], d_stem=res[0]['d'] / 1000,
        As_stem_final=_cm2(res[0]['As_f']),
        M_talao_d=res[1]['M'], M_biqueira_d=res[2]['M'],
        d_base=res[1]['d'] / 1000,
        As_talao_final=_cm2(res[1]['As_f']),
        As_biqueira_final=_cm2(res[2]['As_f']),
        V_stem_d=res[0]['V'], VRd_stem=res[0]['VRd'],
        ok_corte_stem=res[0]['ok_corte'], D_passivo=0.0,
        V_talao_d=res[1]['V'], V_biqueira_d=res[2]['V'],
        diam_stem=res[0]['diam'], esp_stem=res[0]['esp'],
        diam_talao=res[1]['diam'], esp_talao=res[1]['esp'],
        diam_biqueira=res[2]['diam'], esp_biqueira=res[2]['esp'],
        face_talao=res[1]['face'],
        tabela_armaduras_html=tab_rel,      # <-- LaTeX OK no relatório (MathJax)
        verificacoes_html=ver,
        diagramas_html=diagramas_completos,
        lang=lang,
    )

    st.download_button(
        f"📥 {get_text('descarregar_relatorio', lang)}",
        data=html,
        file_name=f"Relatorio_Contrafortes_{st.session_state.nome.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True,
        type="primary",
        key="btn_download_relatorio_contrafortes",
    )
    
   