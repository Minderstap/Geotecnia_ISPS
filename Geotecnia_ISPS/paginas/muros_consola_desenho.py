"""Desenhos SVG do Muro em Consola (Picture3, slides 99/100) — V5 FINAL."""
import math


def _defs():
    return (
        '<defs>'
        '<marker id="cB" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
        '<polygon points="0,0 10,3 0,6" fill="#1f77b4"/></marker>'
        '<marker id="cR" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
        '<polygon points="0,0 10,3 0,6" fill="#c0392b"/></marker>'
        '<marker id="cG" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
        '<polygon points="0,0 10,3 0,6" fill="#27ae60"/></marker>'
        '<pattern id="hcHatch" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)">'
        '<line x1="0" y1="0" x2="0" y2="10" stroke="#8b6f47" stroke-width="1.2"/></pattern>'
        '</defs>'
    )


def _dim(x1, y1, x2, y2, label, cor="#1f77b4", dy=-5, font=10):
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{cor}" '
            f'stroke-width="1.2" marker-start="url(#cB)" marker-end="url(#cB)"/>'
            f'<text x="{mx}" y="{my + dy}" text-anchor="middle" font-size="{font}" '
            f'fill="{cor}" font-weight="bold">{label}</text>')


# ============================================================
# 1. ESTRUTURA PURA (Picture3) — SEM SOLO ESQUERDO, SEM D
# ============================================================
def svg_estrutura_consola(H, HR, B, bt, bh, ts, tb, i, lang="pt"):
    """HR = H - tb (altura do stem acima da base). Sem D. Sem solo à esquerda."""
    W, Hh = 780, 560
    esc = min(400.0 / max(H, 0.1), 400.0 / max(B, 0.1))
    x0 = 170.0
    yb = 460.0
    ytop = yb - H * esc
    ytb = yb - tb * esc          # topo da base = fundo do stem
    xs0 = x0 + bt * esc
    xs1 = xs0 + ts * esc
    xr = x0 + B * esc
    tan_i = math.tan(math.radians(i))

    s = [f'<svg width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" '
         f'style="background:#fdfefe;border:1px solid #bbb;border-radius:8px;">']
    s.append(_defs())
    t = "ESTRUTURA DO MURO EM CONSOLA (Picture3)" if lang == "pt" else "CANTILEVER WALL STRUCTURE (Picture3)"
    s.append(f'<text x="{W/2}" y="22" text-anchor="middle" font-size="13" font-weight="bold">{t}</text>')

    # Solo retido (direita) — apenas acima do topo da base
    s.append(f'<polygon points="{xs1},{ytop} {xr+140},{ytop - 140*tan_i:.1f} {xr+140},{ytb} {xs1},{ytb}" '
             f'fill="#d2b48c" stroke="#8b6f47"/>')
    s.append(f'<polygon points="{xs1},{ytop} {xr+140},{ytop - 140*tan_i:.1f} {xr+140},{ytb} {xs1},{ytb}" '
             f'fill="url(#hcHatch)" opacity="0.35"/>')
    # Fundação
    s.append(f'<rect x="40" y="{yb}" width="{W-80}" height="60" fill="#8a6a4f" stroke="#6b4a2f"/>')
    s.append(f'<text x="50" y="{yb+35}" font-size="11" fill="#fff" font-weight="bold">SOLO DE FUNDAÇÃO</text>')

    # Betão
    s.append(f'<polygon points="{x0},{yb} {x0},{ytb} {xs0},{ytb} {xs0},{ytop} {xs1},{ytop} '
             f'{xs1},{ytb} {xr},{ytb} {xr},{yb}" fill="#b8b8b8" stroke="#333" stroke-width="2"/>')

    s.append(f'<text x="{(xs0+xs1)/2-18}" y="{(ytop+ytb)/2}" font-size="11" font-weight="bold" fill="#333" '
             f'transform="rotate(90 {(xs0+xs1)/2-18} {(ytop+ytb)/2})">STEM</text>')
    s.append(f'<text x="{(xr+x0)/2-20}" y="{yb+20}" font-size="11" font-weight="bold" fill="#333">BASE</text>')

    # N.F. (frente da biqueira, nível do topo da base)
    y_nf = ytb
    s.append(f'<line x1="{x0-100}" y1="{y_nf}" x2="{xs0}" y2="{y_nf}" stroke="#2980b9" '
             f'stroke-width="2" stroke-dasharray="7,4"/>')
    s.append(f'<text x="{x0-105}" y="{y_nf-6}" text-anchor="end" font-size="10" fill="#2980b9" '
             f'font-weight="bold">N.F.</text>')

    # COTAS
    s.append(_dim(x0-40, ytop, x0-40, yb, f"H = {H:.2f} m"))
    s.append(_dim(x0-70, ytop, x0-70, ytb, f"HR = {HR:.2f} m"))
    s.append(_dim(x0, yb+80, xr, yb+80, f"B = {B:.2f} m"))
    s.append(_dim(x0, yb+58, xs0, yb+58, f"bt = {bt:.2f}", dy=14))
    s.append(_dim(xs0, yb+58, xs1, yb+58, f"ts = {ts*100:.0f}cm", dy=14))
    s.append(_dim(xs1, yb+58, xr, yb+58, f"bh = {bh:.2f}", dy=14))
    s.append(_dim(xr+30, ytb, xr+30, yb, f"tb = {tb*100:.0f}cm"))
    if i > 0:
        s.append(f'<text x="{xr+90}" y="{ytop - 90*tan_i}" font-size="10" fill="#1f77b4" '
                 f'font-weight="bold">i = {i:.1f}°</text>')

    s.append('</svg>')
    return "".join(s)


# ============================================================
# 2. RANKINE (slide 100) — TRIÂNGULO PREENCHIDO
# ============================================================
def svg_esquema_rankine(H, HR, B, bt, bh, ts, tb, i, Ka, h_uso, IaH_d,
                        W_total_d, U_d, z_w_at, q_ativo, lang="pt"):
    W, Hh = 900, 620
    esc = min(380.0 / max(H, 0.1), 380.0 / max(B, 0.1))
    x0 = 170.0
    yb = 490.0
    ytop = yb - H * esc
    ytb = yb - tb * esc
    xs0 = x0 + bt * esc
    xs1 = xs0 + ts * esc
    xr = x0 + B * esc
    tan_i = math.tan(math.radians(i))

    s = [f'<svg width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" '
         f'style="background:#fdfefe;border:1px solid #bbb;border-radius:8px;">']
    s.append(_defs())
    tit = "RANKINE (slide 100) — Impulso activo ∥ ao talude" if lang == "pt" \
          else "RANKINE (slide 100) — Active thrust ∥ backfill"
    s.append(f'<text x="{W/2}" y="22" text-anchor="middle" font-size="13" font-weight="bold">{tit}</text>')

    # Solo retido
    s.append(f'<polygon points="{xs1},{ytop} {xr+200},{ytop - 200*tan_i:.1f} {xr+200},{ytb} {xs1},{ytb}" '
             f'fill="#d2b48c" stroke="#8b6f47"/>')
    s.append(f'<polygon points="{xs1},{ytop} {xr+200},{ytop - 200*tan_i:.1f} {xr+200},{ytb} {xs1},{ytb}" '
             f'fill="url(#hcHatch)" opacity="0.28"/>')
    # Fundação
    s.append(f'<rect x="40" y="{yb}" width="{W-80}" height="50" fill="#8a6a4f" stroke="#6b4a2f"/>')

    # ============================================================
    # TRIÂNGULO DE IMPULSO (Rankine) — bem visível
    # Apex no topo do paramento (pressão=0)
    # Base no fundo (pressão máxima), estendendo-se para a direita
    # ============================================================
    p_max = 200
    apex = (xs1, ytop)
    base_l = (xs1, ytb)
    base_r = (xs1 + p_max, ytb)

    s.append(f'<polygon points="{apex[0]},{apex[1]} {base_l[0]},{base_l[1]} '
             f'{base_r[0]},{base_r[1]}" '
             f'fill="rgba(192,57,43,0.38)" stroke="#c0392b" stroke-width="2.5"/>')

    # Setas DENTRO do triângulo (paralelas ao talude, apontando para a parede)
    n = 12
    for k in range(1, n):
        t = k / float(n)
        y = apex[1] + (base_l[1] - apex[1]) * t
        w = p_max * t
        # Direcção paralela ao talude (i = ângulo do terrapleno)
        dx = w * math.cos(math.radians(i))
        dy = -w * math.sin(math.radians(i))
        x_start = xs1 + dx
        y_start = y + dy
        s.append(f'<line x1="{x_start:.1f}" y1="{y_start:.1f}" x2="{xs1+4}" y2="{y:.1f}" '
                 f'stroke="#c0392b" stroke-width="1.6" marker-end="url(#cR)"/>')

    # Etiquetas
    s.append(f'<text x="{xs1+p_max+15}" y="{ytop+20}" font-size="12" fill="#c0392b" font-weight="bold">'
             f'IaH,d = {IaH_d:.1f} kN/m</text>')
    s.append(f'<text x="{xs1+p_max+15}" y="{ytop+36}" font-size="10" fill="#c0392b">'
             f'∥ talude (i = {i:.1f}°) | Ka = {Ka:.4f}</text>')
    s.append(f'<text x="{xs1+p_max+15}" y="{ytop+52}" font-size="10" fill="#c0392b">'
             f'h\'\' = {h_uso:.2f} m</text>')

    # Betão
    s.append(f'<polygon points="{x0},{yb} {x0},{ytb} {xs0},{ytb} {xs0},{ytop} {xs1},{ytop} '
             f'{xs1},{ytb} {xr},{ytb} {xr},{yb}" fill="#b8b8b8" stroke="#333" stroke-width="2.2"/>')

    # Sobrecarga q
    if q_ativo > 0:
        xx = xs1 + 20
        while xx < xr + 160:
            yg = ytop - (xx - xs1) * tan_i
            s.append(f'<line x1="{xx}" y1="{yg-28}" x2="{xx}" y2="{yg-5}" stroke="#1f77b4" stroke-width="1.5"/>')
            s.append(f'<polygon points="{xx},{yg-3} {xx-3},{yg-11} {xx+3},{yg-11}" fill="#1f77b4"/>')
            xx += 60
        s.append(f'<text x="{xs1+15}" y="{ytop - 40}" font-size="10" fill="#1f77b4" '
                 f'font-weight="bold">q = {q_ativo:.1f} kPa</text>')

    # N.F.
    if z_w_at > 0:
        yw = yb - z_w_at * esc
        s.append(f'<line x1="{xs1}" y1="{yw}" x2="{xr+200}" y2="{yw}" stroke="#2980b9" '
                 f'stroke-width="2" stroke-dasharray="7,4"/>')
        s.append(f'<text x="{xr+160}" y="{yw-6}" font-size="10" fill="#2980b9" font-weight="bold">N.F.</text>')

    # Cotas
    s.append(_dim(x0-40, ytop, x0-40, yb, f"H = {H:.2f} m"))
    s.append(_dim(x0-70, ytop, x0-70, ytb, f"HR = {HR:.2f} m"))
    s.append(_dim(x0, yb+70, xr, yb+70, f"B = {B:.2f} m"))

    # W
    s.append(f'<line x1="{(x0+xr)/2}" y1="{ytb-40}" x2="{(x0+xr)/2}" y2="{ytb-8}" '
             f'stroke="#2c3e50" stroke-width="2"/>')
    s.append(f'<polygon points="{(x0+xr)/2},{ytb-5} {(x0+xr)/2-4},{ytb-14} {(x0+xr)/2+4},{ytb-14}" '
             f'fill="#2c3e50"/>')
    s.append(f'<text x="{(x0+xr)/2+8}" y="{ytb-24}" font-size="10" fill="#2c3e50" '
             f'font-weight="bold">W = {W_total_d:.0f} kN/m</text>')

    s.append('</svg>')
    return "".join(s)


# ============================================================
# 3. COULOMB (slide 99) — CUNHA MORTA + DIAGRAMA
# ============================================================
def svg_esquema_coulomb(H, HR, B, bt, bh, ts, tb, i, alpha, beta, Ka, Kaq,
                        h_uso, IaH_d, W_total_d, U_d, z_w_at, q_ativo, lang="pt",
                        phi_d=30.0):
    """
    Slide 99:
    - Cunha morta = triângulo ABC (grande) do lado do solo retido
    - A = base do stem (topo da base)
    - B = topo do stem
    - C = ponto onde a superfície de deslizamento encontra o terreno
    - Superfície de deslizamento AC faz ângulo ξ = 45 + φ'/2 com a horizontal
    - Diagrama de impulso: triângulo com apex no topo, base no fundo
    """
    W, Hh = 940, 660
    esc = min(360.0 / max(H, 0.1), 340.0 / max(B, 0.1))
    x0 = 170.0
    yb = 520.0
    ytop = yb - H * esc
    ytb = yb - tb * esc
    xs0 = x0 + bt * esc
    xs1 = xs0 + ts * esc
    xr = x0 + B * esc
    tan_i = math.tan(math.radians(i))

    s = [f'<svg width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" '
         f'style="background:#fdfefe;border:1px solid #bbb;border-radius:8px;">']
    s.append(_defs())
    tit = "COULOMB (slide 99) — cunha morta ABC + diagrama de impulso" if lang == "pt" \
          else "COULOMB (slide 99) — dead wedge ABC + thrust diagram"
    s.append(f'<text x="{W/2}" y="22" text-anchor="middle" font-size="13" font-weight="bold">{tit}</text>')

    # Solo retido grande
    s.append(f'<polygon points="{xs1},{ytop} {xr+340},{ytop - 340*tan_i:.1f} {xr+340},{ytb} {xs1},{ytb}" '
             f'fill="#d2b48c" stroke="#8b6f47"/>')
    s.append(f'<polygon points="{xs1},{ytop} {xr+340},{ytop - 340*tan_i:.1f} {xr+340},{ytb} {xs1},{ytb}" '
             f'fill="url(#hcHatch)" opacity="0.22"/>')

    # Fundação
    s.append(f'<rect x="40" y="{yb}" width="{W-80}" height="50" fill="#8a6a4f" stroke="#6b4a2f"/>')

    # ============================================================
    # CUNHA MORTA (triângulo ABC grande)
    # ============================================================
    # A = base do stem (retained side) → topo da base
    xA, yA = xs1, ytb
    # B = topo do stem
    xB, yB = xs1, ytop
    # Ângulo da superfície de deslizamento com a horizontal: ξ = 45 + φ_d/2
    xi_deg = 45.0 + phi_d / 2.0
    xi_rad = math.radians(xi_deg)

    # C = intersecção da linha de A (subindo a ξ) com o topo do terreno
    dy_vert = yA - yB  # altura do stem em pixels (positivo)
    dx_horiz = dy_vert / math.tan(xi_rad) if math.tan(xi_rad) > 1e-6 else 200
    xC = xA + dx_horiz
    yC = yB - (xC - xs1) * tan_i

    # Preenchimento da cunha morta
    s.append(f'<polygon points="{xA:.1f},{yA:.1f} {xB:.1f},{yB:.1f} {xC:.1f},{yC:.1f}" '
             f'fill="rgba(139,90,43,0.40)" stroke="#5d3a1f" stroke-width="2"/>')

    # Superfície de deslizamento (tracejada vermelha)
    s.append(f'<line x1="{xA:.1f}" y1="{yA:.1f}" x2="{xC:.1f}" y2="{yC:.1f}" '
             f'stroke="#c0392b" stroke-width="2.5" stroke-dasharray="8,4"/>')

    # Rótulos A, B, C
    s.append(f'<circle cx="{xA}" cy="{yA}" r="5" fill="#3d2a1f"/>')
    s.append(f'<text x="{xA-18}" y="{yA+5}" font-size="13" font-weight="bold" fill="#3d2a1f">A</text>')
    s.append(f'<circle cx="{xB}" cy="{yB}" r="5" fill="#3d2a1f"/>')
    s.append(f'<text x="{xB-18}" y="{yB-4}" font-size="13" font-weight="bold" fill="#3d2a1f">B</text>')
    s.append(f'<circle cx="{xC:.1f}" cy="{yC:.1f}" r="5" fill="#3d2a1f"/>')
    s.append(f'<text x="{xC+10:.1f}" y="{yC-8:.1f}" font-size="13" font-weight="bold" fill="#3d2a1f">C</text>')

    # Rótulo "CUNHA MORTA" (centro do triângulo)
    cx_m = (xA + xB + xC) / 3
    cy_m = (yA + yB + yC) / 3
    s.append(f'<text x="{cx_m:.1f}" y="{cy_m:.1f}" font-size="14" font-weight="bold" '
             f'fill="#3d2a1f" text-anchor="middle">CUNHA MORTA</text>')
    s.append(f'<text x="{cx_m:.1f}" y="{cy_m+18:.1f}" font-size="10" fill="#3d2a1f" '
             f'text-anchor="middle">ξ = {xi_deg:.1f}°</text>')

    # ============================================================
    # DIAGRAMA DE IMPULSO (triângulo com apex no topo do stem)
    # ============================================================
    p_max = 130
    apex_d = (xs1, ytop)
    base_l_d = (xs1, ytb)
    base_r_d = (xs1 + p_max, ytb)

    s.append(f'<polygon points="{apex_d[0]},{apex_d[1]} {base_l_d[0]},{base_l_d[1]} '
             f'{base_r_d[0]},{base_r_d[1]}" '
             f'fill="rgba(192,57,43,0.45)" stroke="#c0392b" stroke-width="2.5"/>')

    # Setas dentro do diagrama
    n = 10
    for k in range(1, n):
        t = k / float(n)
        y = apex_d[1] + (base_l_d[1] - apex_d[1]) * t
        w = p_max * t
        s.append(f'<line x1="{xs1+w:.1f}" y1="{y:.1f}" x2="{xs1+4}" y2="{y:.1f}" '
                 f'stroke="#c0392b" stroke-width="1.6" marker-end="url(#cR)"/>')

    # Etiquetas
    s.append(f'<text x="{xs1+p_max+20}" y="{ytop+20}" font-size="12" fill="#c0392b" font-weight="bold">'
             f'IaH,d = {IaH_d:.1f} kN/m</text>')
    s.append(f'<text x="{xs1+p_max+20}" y="{ytop+36}" font-size="10" fill="#c0392b">'
             f'α = {alpha:.1f}° | β = {beta:.1f}° | Ka = {Ka:.4f}</text>')
    s.append(f'<text x="{xs1+p_max+20}" y="{ytop+52}" font-size="10" fill="#c0392b">'
             f'Kaq = {Kaq:.4f} | h\' = {h_uso:.2f} m</text>')

    # Betão (por cima)
    s.append(f'<polygon points="{x0},{yb} {x0},{ytb} {xs0},{ytb} {xs0},{ytop} {xs1},{ytop} '
             f'{xs1},{ytb} {xr},{ytb} {xr},{yb}" fill="#b8b8b8" stroke="#333" stroke-width="2.2"/>')

    # Sobrecarga q
    if q_ativo > 0:
        xx = xs1 + 20
        while xx < xr + 300:
            yg = ytop - (xx - xs1) * tan_i
            s.append(f'<line x1="{xx}" y1="{yg-28}" x2="{xx}" y2="{yg-5}" stroke="#1f77b4" stroke-width="1.5"/>')
            s.append(f'<polygon points="{xx},{yg-3} {xx-3},{yg-11} {xx+3},{yg-11}" fill="#1f77b4"/>')
            xx += 60
        s.append(f'<text x="{xs1+15}" y="{ytop - 40}" font-size="10" fill="#1f77b4" '
                 f'font-weight="bold">q = {q_ativo:.1f} kPa</text>')

    # N.F.
    if z_w_at > 0:
        yw = yb - z_w_at * esc
        s.append(f'<line x1="{xs1}" y1="{yw}" x2="{xr+340}" y2="{yw}" stroke="#2980b9" '
                 f'stroke-width="2" stroke-dasharray="7,4"/>')
        s.append(f'<text x="{xr+300}" y="{yw-6}" font-size="10" fill="#2980b9" font-weight="bold">N.F.</text>')

    # Cotas
    s.append(_dim(x0-40, ytop, x0-40, yb, f"H = {H:.2f} m"))
    s.append(_dim(x0-70, ytop, x0-70, ytb, f"HR = {HR:.2f} m"))
    s.append(_dim(x0, yb+70, xr, yb+70, f"B = {B:.2f} m"))

    # W
    s.append(f'<line x1="{(x0+xr)/2}" y1="{ytb-40}" x2="{(x0+xr)/2}" y2="{ytb-8}" '
             f'stroke="#2c3e50" stroke-width="2"/>')
    s.append(f'<polygon points="{(x0+xr)/2},{ytb-5} {(x0+xr)/2-4},{ytb-14} {(x0+xr)/2+4},{ytb-14}" '
             f'fill="#2c3e50"/>')
    s.append(f'<text x="{(x0+xr)/2+8}" y="{ytb-24}" font-size="10" fill="#2c3e50" '
             f'font-weight="bold">W = {W_total_d:.0f} kN/m</text>')

    s.append('</svg>')
    return "".join(s)


# ============================================================
# 4. PORMENORIZAÇÃO (mantém)
# ============================================================
def svg_pormenorizacao_consola(B, bt, bh, ts, tb, HR, arma):
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

    s = [f'<svg width="{W_svg}" height="{H_svg}" viewBox="0 0 {W_svg} {H_svg}" '
         f'xmlns="http://www.w3.org/2000/svg" style="background:#fdfefe;border:1px solid #bbb;border-radius:6px;">']
    s.append(_defs())
    s.append(f'<text x="{W_svg/2}" y="20" text-anchor="middle" font-size="13" font-weight="bold">'
             f'PORMENORIZAÇÃO — CORTE TRANSVERSAL</text>')
    s.append(f'<polygon points="{x0},{yb} {x0},{ytb} {xs0},{ytb} {xs0},{ytop} {xs1},{ytop} '
             f'{xs1},{ytb} {xr},{ytb} {xr},{yb}" fill="#eaecee" stroke="#333" stroke-width="2"/>')
    s.append(f'<polygon points="{x0+cov},{yb-cov} {x0+cov},{ytb+cov} {xs0+cov},{ytb+cov} {xs0+cov},{ytop+cov} '
             f'{xs1-cov},{ytop+cov} {xs1-cov},{ytb+cov} {xr-cov},{ytb+cov} {xr-cov},{yb-cov}" '
             f'fill="none" stroke="#922b21" stroke-width="1.3"/>')
    s.append(f'<line x1="{xs1-cov-2}" y1="{ytop+cov+4}" x2="{xs1-cov-2}" y2="{ytb+cov}" '
             f'stroke="#c0392b" stroke-width="3"/>')
    s.append(f'<line x1="{xs1+2}" y1="{yH}" x2="{xr-cov-4}" y2="{yH}" stroke="#c0392b" stroke-width="3"/>')
    s.append(f'<line x1="{x0+cov+4}" y1="{yT}" x2="{xs0-2}" y2="{yT}" stroke="#c0392b" stroke-width="3"/>')

    def dots(xs, ys, r=3.0):
        return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2471a3"/>' for x, y in zip(xs, ys))
    n = 6
    s.append(dots([xs0 + cov + 2] * (n + 1),
                  [ytop + cov + 8 + (ytb - ytop - 2 * cov - 16) * k / n for k in range(n + 1)]))
    s.append(dots([xs1 + 12 + (xr - xs1 - 2 * cov - 24) * k / 4 for k in range(5)], [yHd] * 5))
    s.append(dots([x0 + cov + 12 + (xs0 - x0 - 2 * cov - 24) * k / 4 for k in range(5)], [yTd] * 5))

    R, Az = "#c0392b", "#2471a3"
    def leader(x1, y1, x2, y2, txt, tx, ty, cor):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{cor}" stroke-width="1"/>'
                f'<text x="{tx}" y="{ty}" font-size="12" fill="{cor}" font-weight="bold">{txt}</text>')

    s.append(leader(xs1 - cov - 2, ytop + 45, xs1 + 60, ytop + 35, f"1 {arma['m1']} (P)", xs1 + 66, ytop + 39, R))
    s.append(leader(xs0 + cov + 2, ytop + 65, xs0 - 60, ytop + 55, f"2 {arma['m2']} (D)", xs0 - 165, ytop + 59, Az))
    s.append(leader((xs1 + xr) / 2, yH, (xs1 + xr) / 2 + 40, ytb - 30, f"3 {arma['m3']} (P)", xr + 15, ytb - 26, R))
    s.append(leader((xs1 + xr) / 2 - 20, yHd, (xs1 + xr) / 2 - 60, ytb + 45, f"4 {arma['m4']} (D)", xr + 15, ytb + 49, Az))
    s.append(leader((x0 + xs0) / 2, yT, (x0 + xs0) / 2 - 40, yb - 30, f"5 {arma['m5']} (P)", x0 - 165, yb - 26, R))
    s.append(leader((x0 + xs0) / 2 + 20, yTd, (x0 + xs0) / 2 + 60, yb + 20, f"6 {arma['m6']} (D)", x0 - 165, yb + 24, Az))
    s.append(f'<text x="{x0}" y="{yb+58}" font-size="11">bt = {bt:.2f} m</text>')
    s.append(f'<text x="{xs0}" y="{yb+58}" font-size="11">ts = {ts*100:.0f} cm</text>')
    s.append(f'<text x="{xs1}" y="{yb+58}" font-size="11">bh = {bh:.2f} m</text>')
    s.append(f'<text x="{x0}" y="{yb+76}" font-size="11" font-weight="bold">B = {B:.2f} m | tb = {tb*100:.0f} cm | HR = {HR:.2f} m</text>')
    s.append('</svg>')
    return "".join(s)


# ============================================================
# 5. LAJE VERTICAL
# ============================================================
def svg_laje_vertical(Hs, q_top, q_base, M, V, titulo):
    top, bot = 40, 380
    xe = 190
    setas = ""
    for k in range(8):
        y = top + (bot - top) * k / 7
        qq = q_top + (q_base - q_top) * k / 7
        comp = 20 + 90 * (qq / max(q_base, 1e-6))
        setas += (f'<line x1="{xe+comp}" y1="{y}" x2="{xe+2}" y2="{y}" stroke="red" stroke-width="1.5"/>'
                  f'<polygon points="{xe+2},{y} {xe+10},{y-3} {xe+10},{y+3}" fill="red"/>')
    hach = "".join([f'<line x1="{120+i*12}" y1="{bot+18}" x2="{112+i*12}" y2="{bot+28}" stroke="black" stroke-width="1.5"/>' for i in range(8)])
    return (f'<svg width="380" height="460" style="background:#f8f9fa;border:1px solid #ddd;border-radius:8px;">'
            f'<text x="190" y="20" text-anchor="middle" font-size="13" font-weight="bold">{titulo}</text>'
            f'<rect x="150" y="{top}" width="40" height="{bot-top}" fill="#d3d3d3" stroke="#333" stroke-width="2"/>'
            f'<line x1="120" y1="{bot}" x2="220" y2="{bot}" stroke="#333" stroke-width="4"/>{hach}{setas}'
            f'<text x="{xe+115}" y="{top+12}" fill="red" font-size="11">q={q_top:.1f} kPa</text>'
            f'<text x="{xe+115}" y="{bot-4}" fill="red" font-size="11">q={q_base:.1f} kPa</text>'
            f'<text x="60" y="210" fill="blue" font-size="12" font-weight="bold">Hs={Hs:.2f} m</text>'
            f'<text x="90" y="{bot+45}" fill="green" font-size="11" font-weight="bold">'
            f'ENCASTRE: Msd={M:.1f} kNm/m | Vsd={V:.1f} kN/m</text></svg>')


# ============================================================
# 6. LAJE HORIZONTAL
# ============================================================
def svg_laje_horizontal(L, q_desce, q_sobe, q_liq, sentido, M, V, titulo, fixo):
    x0, x1, y0, y1 = 60, 400, 150, 190
    setas = ""
    for k in range(8):
        x = x0 + (x1 - x0) * k / 7
        if sentido == "baixo":
            setas += (f'<line x1="{x}" y1="{y0-45}" x2="{x}" y2="{y0-3}" stroke="blue" stroke-width="1.5"/>'
                      f'<polygon points="{x},{y0-2} {x-3},{y0-10} {x+3},{y0-10}" fill="blue"/>')
        else:
            setas += (f'<line x1="{x}" y1="{y1+45}" x2="{x}" y2="{y1+3}" stroke="red" stroke-width="1.5"/>'
                      f'<polygon points="{x},{y1+2} {x-3},{y1+10} {x+3},{y1+10}" fill="red"/>')
    hx = x1 if fixo == "dir" else x0
    hach = "".join([f'<line x1="{hx}" y1="{100+i*14}" x2="{hx+10 if fixo=="dir" else hx-10}" y2="{92+i*14}" stroke="black" stroke-width="1.5"/>' for i in range(8)])
    return (f'<svg width="470" height="300" style="background:#f8f9fa;border:1px solid #ddd;border-radius:8px;">'
            f'<text x="235" y="20" text-anchor="middle" font-size="13" font-weight="bold">{titulo}</text>'
            f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#d3d3d3" stroke="#333" stroke-width="2"/>'
            f'<line x1="{hx}" y1="100" x2="{hx}" y2="240" stroke="#333" stroke-width="4"/>{hach}{setas}'
            f'<text x="{x0}" y="{y0-55}" fill="blue" font-size="11">↓ desce={q_desce:.1f} kPa</text>'
            f'<text x="{x0}" y="{y1+62}" fill="red" font-size="11">↑ sobe={q_sobe:.1f} kPa</text>'
            f'<text x="{x0}" y="{y1+80}" font-size="11" font-weight="bold">'
            f'RESULTANTE q={abs(q_liq):.1f} kPa ({"↑" if sentido=="cima" else "↓"})</text>'
            f'<text x="60" y="292" fill="green" font-size="11" font-weight="bold">'
            f'ENCASTRE: Msd={M:.1f} kNm/m | Vsd={V:.1f} kN/m</text></svg>')