from html import escape
import math


# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------
def _fmt(v, nd=2):
    try:
        return f"{float(v):.{nd}f}"
    except Exception:
        return "-"
def _t(lang, pt, en):
    """Devolve o texto no idioma pedido (pt ou en)."""
    return pt if lang == "pt" else en

def _text(x, y, txt, size=12, fill="#1f2937", weight="400", anchor="start",
          italic=False, family="Arial, Helvetica, sans-serif"):
    style = "font-style:italic;" if italic else ""
    return (
        f'<text x="{float(x):.2f}" y="{float(y):.2f}" font-size="{size}" '
        f'font-family="{family}" fill="{fill}" font-weight="{weight}" '
        f'text-anchor="{anchor}" style="{style}">{escape(str(txt))}</text>'
    )


def _defs(prefix="sap"):
    return f"""
    <defs>
      <marker id="{prefix}-dim" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <path d="M 0 4 L 8 0 L 8 8 Z" fill="#2563eb"/>
      </marker>
      <marker id="{prefix}-load" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto">
        <path d="M 0 0 L 8 4 L 0 8 Z" fill="#111827"/>
      </marker>
      <marker id="{prefix}-soil" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
        <path d="M 0 0 L 7 4 L 0 8 Z" fill="#a16207"/>
      </marker>
      <marker id="{prefix}-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
        <path d="M 0 0 L 7 4 L 0 8 Z" fill="#dc2626"/>
      </marker>
      <marker id="{prefix}-green" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
        <path d="M 0 0 L 7 4 L 0 8 Z" fill="#15803d"/>
      </marker>
      <marker id="{prefix}-orange" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
        <path d="M 0 0 L 7 4 L 0 8 Z" fill="#ea580c"/>
      </marker>
      <pattern id="{prefix}-soil-hatch" width="10" height="10" patternUnits="userSpaceOnUse">
        <path d="M -2 10 L 10 -2 M 2 12 L 12 2" stroke="#9a6b37" stroke-width="0.85"/>
      </pattern>
      <pattern id="{prefix}-conc-hatch" width="8" height="8" patternUnits="userSpaceOnUse">
        <path d="M -1 8 L 8 -1 M 3 11 L 11 3" stroke="#7b7b7b" stroke-width="0.65"/>
      </pattern>
      <filter id="{prefix}-shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.18"/>
      </filter>
    </defs>
    """


def _svg_start(w, h, title, prefix="sap", subtitle=None):
    s = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        'xmlns="http://www.w3.org/2000/svg" '
        'style="background:#ffffff;border:1px solid #d1d5db;border-radius:10px;display:block;max-width:100%;">',
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>',
        _defs(prefix),
        _text(w / 2, 28, title, 17, "#111827", "700", "middle"),
    ]
    if subtitle:
        s.append(_text(w / 2, 47, subtitle, 10, "#64748b", "400", "middle", italic=True))
    return s


def _dim_h(x1, x2, y, label, prefix="sap", color="#2563eb", ext1=None, ext2=None, dy=-7, font=11):
    out = []
    if ext1 is not None:
        out.append(f'<line x1="{x1:.2f}" y1="{ext1:.2f}" x2="{x1:.2f}" y2="{y:.2f}" stroke="{color}" stroke-width="1"/>')
    if ext2 is not None:
        out.append(f'<line x1="{x2:.2f}" y1="{ext2:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{color}" stroke-width="1"/>')
    out.append(
        f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" '
        f'stroke="{color}" stroke-width="1.4" marker-start="url(#{prefix}-dim)" marker-end="url(#{prefix}-dim)"/>'
    )
    out.append(_text((x1+x2)/2, y+dy, label, font, color, "700", "middle"))
    return out


def _dim_v(y1, y2, x, label, prefix="sap", color="#2563eb", ext1=None, ext2=None, dx=-8, font=11):
    out = []
    if ext1 is not None:
        out.append(f'<line x1="{ext1:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y1:.2f}" stroke="{color}" stroke-width="1"/>')
    if ext2 is not None:
        out.append(f'<line x1="{ext2:.2f}" y1="{y2:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="1"/>')
    out.append(
        f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="1.4" marker-start="url(#{prefix}-dim)" marker-end="url(#{prefix}-dim)"/>'
    )
    out.append(_text(x+dx, (y1+y2)/2, label, font, color, "700", "middle"))
    return out


def _box(x, y, w, h, title, stroke="#cbd5e1", fill="#f8fafc"):
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}"/>',
        _text(x+14, y+24, title, 12, "#0f172a", "700"),
    ]


def _legend(x, y, w, items, lang="pt"):
    h = 24 + 24*len(items)
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>',
         _text(x+12, y+18, _t(lang, "LEGENDA", "LEGEND"), 11, "#0f172a", "700")]
    yy = y+41
    for kind, label in items:
        if kind == "red":
            s.append(f'<line x1="{x+12}" y1="{yy-5}" x2="{x+42}" y2="{yy-5}" stroke="#dc2626" stroke-width="3"/>')
        elif kind == "blue":
            s.append(f'<line x1="{x+12}" y1="{yy-5}" x2="{x+42}" y2="{yy-5}" stroke="#2563eb" stroke-width="3"/>')
        elif kind == "green":
            s.append(f'<rect x="{x+12}" y="{yy-13}" width="30" height="16" fill="#dcfce7" stroke="#15803d"/>')
        elif kind == "dash-red":
            s.append(f'<line x1="{x+12}" y1="{yy-5}" x2="{x+42}" y2="{yy-5}" stroke="#dc2626" stroke-width="2" stroke-dasharray="7,4"/>')
        elif kind == "dot-red":
            s.append(f'<circle cx="{x+27}" cy="{yy-5}" r="5" fill="#dc2626" stroke="#fff" stroke-width="2"/>')
        elif kind == "gray":
            s.append(f'<rect x="{x+12}" y="{yy-13}" width="30" height="16" fill="#d1d5db" stroke="#334155"/>')
        s.append(_text(x+50, yy, label, 10, "#334155"))
        yy += 24
    return s


# -----------------------------------------------------------------------------
# 1. Convenção de momentos
# -----------------------------------------------------------------------------
def svg_convencao_momentos(lang="pt"):
    pt = lang == "pt"
    title = _t(lang, "CONVENÇÃO DE SINAIS — Mx e My",
                    "SIGN CONVENTION — Mx and My")
    W, H = 860, 460
    s = _svg_start(W, H, title, "conv",
                   _t(lang,
                      "Representação esquemática para fixar a convenção antes do cálculo",
                      "Schematic representation to fix the convention before calculation"))
    s.append('<defs><marker id="conv-axis" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
             '<path d="M 0 0 L 8 4 L 0 8 Z" fill="#2563eb"/></marker></defs>')

    cx, cy = 290, 310
    kx, ky = 0.55, 0.38

    def P(x, y, z=0.0):
        return (cx + x + kx * y, cy - ky * y - z)

    def pts(lst):
        return " ".join(f"{a:.1f},{b:.1f}" for a, b in lst)

    def path(lst):
        return "M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in lst)

    def arc(f, a0, a1, n=48):
        return [f(math.radians(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

    hx, hy, t = 200, 100, 26
    qx, qy, qh = 24, 24, 70

    s += [
        f'<polygon points="{pts([P(-hx,-hy), P(hx,-hy), P(hx,-hy,-t), P(-hx,-hy,-t)])}" fill="#d1d5db" stroke="#334155" stroke-width="2"/>',
        f'<polygon points="{pts([P(hx,-hy), P(hx,hy), P(hx,hy,-t), P(hx,-hy,-t)])}" fill="#cbd5e1" stroke="#334155" stroke-width="2"/>',
        f'<polygon points="{pts([P(-hx,hy), P(hx,hy), P(hx,-hy), P(-hx,-hy)])}" fill="#e5e7eb" stroke="#334155" stroke-width="2.2" filter="url(#conv-shadow)"/>',
        _text(*P(-hx + 70, -hy, -t / 2 - 4),
              _t(lang, "SAPATA", "FOOTING"), 11, "#334155", "700", "middle"),
    ]

    xa, xb = P(-hx - 35, 0), P(hx + 60, 0)
    ya, yb = P(0, -hy - 30), P(0, hy + 38)
    s += [
        f'<line x1="{xa[0]:.1f}" y1="{xa[1]:.1f}" x2="{xb[0]:.1f}" y2="{xb[1]:.1f}" stroke="#2563eb" stroke-width="2" stroke-dasharray="16,5,3,5" marker-end="url(#conv-axis)"/>',
        f'<line x1="{ya[0]:.1f}" y1="{ya[1]:.1f}" x2="{yb[0]:.1f}" y2="{yb[1]:.1f}" stroke="#2563eb" stroke-width="2" stroke-dasharray="16,5,3,5" marker-end="url(#conv-axis)"/>',
        _text(xb[0] + 10, xb[1] + 5, "X", 14, "#2563eb", "700"),
        _text(yb[0] + 8, yb[1] + 2, "Y", 14, "#2563eb", "700"),
    ]

    for n, (px, py, dx, dy) in {1: (hx, hy, 16, -10), 2: (hx, -hy, 16, 12),
                                3: (-hx, hy, -16, -10), 4: (-hx, -hy, -16, 12)}.items():
        a, b = P(px, py)
        s += [
            f'<circle cx="{a+dx:.1f}" cy="{b+dy:.1f}" r="10" fill="#ffffff" stroke="#334155" stroke-width="1.5"/>',
            _text(a + dx, b + dy + 4, n, 11, "#0f172a", "700", "middle"),
        ]

    Rx, Ry = 100, 140
    fx = lambda b: P(0, Rx * math.cos(b), Rx * math.sin(b))
    fy = lambda a: P(Ry * math.sin(a), 0, Ry * math.cos(a))
    s.append(f'<path d="{path(arc(fx, 52, 20))}" fill="none" stroke="#dc2626" stroke-width="3" marker-end="url(#conv-red)"/>')

    s += [
        f'<polygon points="{pts([P(-qx,-qy,0), P(qx,-qy,0), P(qx,-qy,qh), P(-qx,-qy,qh)])}" fill="#9ca3af" stroke="#1f2937" stroke-width="2"/>',
        f'<polygon points="{pts([P(qx,-qy,0), P(qx,qy,0), P(qx,qy,qh), P(qx,-qy,qh)])}" fill="#6b7280" stroke="#1f2937" stroke-width="2"/>',
        f'<polygon points="{pts([P(-qx,qy,qh), P(qx,qy,qh), P(qx,-qy,qh), P(-qx,-qy,qh)])}" fill="#d1d5db" stroke="#1f2937" stroke-width="2"/>',
        _text(*P(0, -qy, qh / 2 - 4),
              _t(lang, "PILAR", "COLUMN"), 9, "#ffffff", "700", "middle"),
    ]

    s.append(f'<path d="{path(arc(fx, 160, 52))}" fill="none" stroke="#dc2626" stroke-width="3"/>')
    ex, ey = P(0, Rx * math.cos(math.radians(160)), Rx * math.sin(math.radians(160)))
    s.append(_text(ex - 14, ey + 22, "My (+)", 13, "#dc2626", "700", "end"))

    s.append(f'<path d="{path(arc(fy, -58, 58))}" fill="none" stroke="#15803d" stroke-width="3" marker-end="url(#conv-green)"/>')
    mx_, my_ = fy(math.radians(36))
    s.append(_text(mx_ + 14, my_ - 6, "Mx (+)", 13, "#15803d", "700"))

    s += _box(625, 75, 215, 150,
              _t(lang, "REGRA DE UTILIZAÇÃO", "USAGE RULES"),
              "#cbd5e1", "#f8fafc")
    s += [
        _text(639, 114,
              _t(lang, "• Regra da mão direita.",
                      "• Right-hand rule."), 10, "#334155"),
        _text(639, 135,
              _t(lang, "• Mx (+) — seta verde, plano X-Z,",
                      "• Mx (+) — green arrow, plane X-Z,"), 10, "#334155"),
        _text(639, 150,
              _t(lang, "  sentido Z → X (arco vertical).",
                      "  direction Z → X (vertical arc)."), 10, "#334155"),
        _text(639, 171,
              _t(lang, "• My (+) — seta vermelha, plano Y-Z,",
                      "• My (+) — red arrow, plane Y-Z,"), 10, "#334155"),
        _text(639, 186,
              _t(lang, "  sentido Z → Y (arco vertical).",
                      "  direction Z → Y (vertical arc)."), 10, "#334155"),
        _text(639, 207,
              _t(lang, "• Z positivo aponta para cima.",
                      "• Positive Z points up."), 10, "#334155"),
    ]
    s.append(_text(W / 2, 438,
                   _t(lang,
                      "Base: slides 132–134 — convenção dos momentos e solicitações referidas ao centro G.",
                      "Basis: slides 132–134 — sign convention and actions about centre G."),
                   10, "#64748b", "400", "middle", True))
    s.append('</svg>')
    return "".join(s)


# -----------------------------------------------------------------------------
# 2. Planta
# -----------------------------------------------------------------------------
def svg_planta_sapata(Bx, By, bx, by, ex, ey, Mx, My, lang="pt"):
    Bx=max(float(Bx),0.1); By=max(float(By),0.1); bx=max(float(bx),0.05); by=max(float(by),0.05)
    ex=float(ex); ey=float(ey)
    W,H=980,630
    esc=min(485/Bx,390/By)
    x0,y0=90,125
    wp,hp=Bx*esc,By*esc
    xc,yc=x0+wp/2,y0+hp/2
    xr,yr=xc+ex*esc,yc-ey*esc
    kx,ky=wp/6,hp/6
    s=_svg_start(W,H,
                 _t(lang,
                    "PLANTA — PILAR, NÚCLEO CENTRAL E RESULTANTE",
                    "PLAN — COLUMN, CENTRAL KERN AND RESULTANT"),
                 "plan",
                 _t(lang,
                    "O pilar permanece na sua posição geométrica; a excentricidade desloca a resultante R",
                    "The column stays in its geometric position; the eccentricity shifts the resultant R"))

    s += [
        f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{wp:.2f}" height="{hp:.2f}" fill="#f8fafc" stroke="#111827" stroke-width="2.4"/>',
        f'<line x1="{x0-24}" y1="{yc:.2f}" x2="{x0+wp+24}" y2="{yc:.2f}" stroke="#64748b" stroke-width="1" stroke-dasharray="8,5"/>',
        f'<line x1="{xc:.2f}" y1="{y0-24}" x2="{xc:.2f}" y2="{y0+hp+24}" stroke="#64748b" stroke-width="1" stroke-dasharray="8,5"/>',
        _text(x0+wp+30,yc+5,"X",12,"#2563eb","700"),
        _text(xc+6,y0-30,"Y",12,"#2563eb","700"),
        f'<polygon points="{xc:.2f},{yc-ky:.2f} {xc+kx:.2f},{yc:.2f} {xc:.2f},{yc+ky:.2f} {xc-kx:.2f},{yc:.2f}" fill="#dcfce7" stroke="#15803d" stroke-width="1.8"/>',
        _text(xc+kx+10,yc+4,
              _t(lang, "Núcleo central", "Central kern"),
              10,"#166534","700"),
    ]

    pw,ph=bx*esc,by*esc
    xp,yp=xc-pw/2,yc-ph/2
    s += [
        f'<rect x="{xp:.2f}" y="{yp:.2f}" width="{pw:.2f}" height="{ph:.2f}" fill="#9ca3af" stroke="#111827" stroke-width="2.2"/>',
        _text(xc,yc+4, _t(lang, "PILAR", "COLUMN"),11,"#ffffff","700","middle"),
        f'<circle cx="{xc:.2f}" cy="{yc:.2f}" r="5" fill="#111827"/>',
        _text(xc+9,yc-8,"G",10,"#111827","700"),
    ]

    if abs(ex)>1e-9 or abs(ey)>1e-9:
        s += [
            f'<line x1="{xc:.2f}" y1="{yc:.2f}" x2="{xr:.2f}" y2="{yr:.2f}" stroke="#dc2626" stroke-width="2.4" stroke-dasharray="8,5" marker-end="url(#plan-red)"/>',
            f'<circle cx="{xr:.2f}" cy="{yr:.2f}" r="8" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>',
            _text(xr+11,yr-9,"R",12,"#b91c1c","700"),
        ]

    if abs(ex)>1e-9:
        ydim=y0+hp+56
        s += _dim_h(xc,xr,ydim,f"ex = {ex:+.3f} m","plan","#dc2626",yc,yr,-8,11)
    if abs(ey)>1e-9:
        xdim=x0+wp+62
        s += _dim_v(min(yc,yr),max(yc,yr),xdim,f"ey = {ey:+.3f} m","plan","#dc2626",xc,xr,30,11)

    s += _dim_h(x0,x0+wp,y0-44,f"Bx = {Bx:.2f} m","plan",ext1=y0,ext2=y0,dy=-8)
    s += _dim_v(y0,y0+hp,x0-42,f"By = {By:.2f} m","plan",ext1=x0,ext2=x0,dx=-13)
    s += _dim_h(xp,xp+pw,yp-20,f"bx = {bx:.2f} m","plan","#64748b",yp,yp,-5,10)
    s += _dim_v(yp,yp+ph,xp-18,f"by = {by:.2f} m","plan","#64748b",xp,xp,-10,10)

    eta_x=abs(ex)/Bx; eta_y=abs(ey)/By; ksum=eta_x+eta_y
    inside=ksum<=1/6+1e-12
    r_inside_footing=(abs(ex)<=Bx/2.0+1e-12 and abs(ey)<=By/2.0+1e-12)
    col="#166534" if inside else "#b91c1c"
    bg="#f0fdf4" if inside else "#fef2f2"
    s += _box(650,95,285,205,
              _t(lang, "VERIFICAÇÃO DO NÚCLEO", "KERN CHECK"), col, bg)
    s += [
        _text(668,128,f"|ex|/Bx = {eta_x:.4f}",10,"#334155"),
        _text(668,151,f"|ey|/By = {eta_y:.4f}",10,"#334155"),
        _text(668,174,
              f"{_t(lang, 'Soma', 'Sum')} = {ksum:.4f}",10,"#334155"),
        _text(792,201,
              _t(lang, "≤ 1/6 → DENTRO", "≤ 1/6 → INSIDE") if inside
              else _t(lang, "> 1/6 → FORA", "> 1/6 → OUTSIDE"),
              12,col,"700","middle"),
        _text(668,231,
              _t(lang, "A posição física do pilar NÃO é alterada:",
                      "The physical position of the column is NOT changed:"),
              9,"#475569","700"),
        _text(668,250,
              _t(lang, "G permanece no centro geométrico da sapata",
                      "G remains at the geometric centre of the footing"),
              9,"#475569"),
        _text(668,267,
              _t(lang, "e R é que se desloca devido a Mx/My.",
                      "and R moves because of Mx/My."),
              9,"#475569"),
        _text(668,286,
              _t(lang, "R dentro da sapata: ", "R inside the footing: ")
              + _t(lang, "SIM" if r_inside_footing else "NÃO — rever geometria",
                      "YES" if r_inside_footing else "NO — revise geometry"),
              9,"#475569","700"),
    ]
    s += _box(650,290,285,118,
              _t(lang, "ACÇÕES", "ACTIONS"), "#cbd5e1", "#f8fafc")
    s += [
        _text(668,321,f"Mx = {Mx:+.2f} kN·m",10,"#991b1b","700"),
        _text(668,345,f"My = {My:+.2f} kN·m",10,"#991b1b","700"),
        _text(668,371,
              _t(lang, "G = centro geométrico",
                      "G = geometric centre"),10,"#475569"),
        _text(668,393,
              _t(lang, "R = ponto de passagem da resultante",
                      "R = resultant passage point"),10,"#475569"),
    ]
    s += _legend(650, 430, 285, [
        ("green",   _t(lang, "núcleo central", "central kern")),
        ("dot-red", _t(lang, "resultante R", "resultant R")),
        ("dash-red",_t(lang, "vector G → R", "vector G → R")),
    ], lang)
    s.append('</svg>')
    return "".join(s)


# -----------------------------------------------------------------------------
# 3. Corte vertical
# -----------------------------------------------------------------------------
def svg_perfil_sapata(Bx, bx, h, Df, WT, sigma1, sigma2, sigma_max, sigma_min, lang="pt"):
    Bx=max(float(Bx),0.1); bx=max(float(bx),0.05); h=max(float(h),0.05); Df=max(float(Df),0.0)
    W,H=980,675
    esc=min(500/Bx,82/max(h,0.15))
    x0=115; y_ground=112; y_base=y_ground+Df*62
    wp=Bx*esc; hp=h*82; x1=x0+wp
    pw=bx*esc; xp=x0+(wp-pw)/2
    y_top_foot=y_base-hp
    py_top=max(58,y_top_foot-155)
    p_height=max(y_top_foot-py_top,35)

    s=_svg_start(
        W, H,
        _t(lang,
           "CORTE A–A — SAPATA, SOLO, CARGA E REACÇÃO",
           "SECTION A–A — FOOTING, SOIL, LOAD AND REACTION"),
        "perfil",
        _t(lang,
           "Cotas em metros; diagrama de tensões separado para facilitar a leitura",
           "Dimensions in metres; stress diagram shown separately for clarity"))

    # Terreno.
    s += [
        f'<rect x="45" y="{y_ground}" width="890" height="515" fill="#e8d3b2"/>',
        f'<rect x="45" y="{y_ground}" width="890" height="515" fill="url(#perfil-soil-hatch)" opacity="0.55"/>',
        f'<line x1="45" y1="{y_ground}" x2="935" y2="{y_ground}" stroke="#1f2937" stroke-width="2.4"/>',
        _text(50, y_ground-12,
              _t(lang, "NT — terreno natural", "GL — natural ground"),
              11, "#334155", "700"),
        f'<rect x="{x0-32:.2f}" y="{y_ground:.2f}" width="{wp+64:.2f}" height="{max(y_base-y_ground,0):.2f}" fill="#ffffff" fill-opacity="0.82" stroke="#cbd5e1"/>',
    ]

    # Sapata + pilar.
    s += [
        f'<rect x="{x0:.2f}" y="{y_top_foot:.2f}" width="{wp:.2f}" height="{hp:.2f}" fill="#d1d5db" stroke="#111827" stroke-width="2.3" filter="url(#perfil-shadow)"/>',
        f'<rect x="{x0:.2f}" y="{y_top_foot:.2f}" width="{wp:.2f}" height="{hp:.2f}" fill="url(#perfil-conc-hatch)" opacity="0.55"/>',
        f'<rect x="{xp:.2f}" y="{py_top:.2f}" width="{pw:.2f}" height="{p_height:.2f}" fill="#9ca3af" stroke="#111827" stroke-width="2"/>',
        _text(xp+pw/2, py_top+p_height/2+4,
              _t(lang, "PILAR", "COLUMN"),
              11, "#ffffff", "700", "middle"),
        '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#111827" stroke-width="2.3" marker-end="url(#perfil-load)"/>'.format(xp+pw/2, py_top-34, xp+pw/2, py_top+4),
        _text(xp+pw/2+12, py_top-40, "N", 12, "#111827", "700"),
    ]

    # Armadura inferior com recobrimento esquemático.
    ysteel=y_base-22
    for k in range(11):
        xx=x0+28+k*max(wp-56,20)/10
        s.append(f'<circle cx="{xx:.2f}" cy="{ysteel:.2f}" r="3.2" fill="#b91c1c" stroke="#7f1d1d" stroke-width="0.6"/>')
    s += [
        _text(x1+18, ysteel+4,
              _t(lang, "armadura inferior", "bottom reinforcement"),
              10, "#b91c1c", "700"),
        '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#15803d" stroke-width="1.3" marker-start="url(#perfil-green)" marker-end="url(#perfil-green)"/>'.format(x1+110, y_top_foot, x1+110, ysteel),
        _text(x1+120, (y_top_foot+ysteel)/2+4, "d", 10, "#166534", "700"),
        _text(x0+12, y_base-8,
              _t(lang, "base da sapata", "footing base"),
              9, "#475569"),
    ]

    # Cotas principais.
    s += _dim_h(x0, x1, y_ground-40, f"B = {Bx:.2f} m", "perfil", ext1=y_ground, ext2=y_ground)
    s += _dim_v(y_ground, y_base, x0-52, f"Df = {Df:.2f} m", "perfil", ext1=x0, ext2=x0, dx=-12)
    s += _dim_v(y_top_foot, y_base, x1+58, f"h = {h:.2f} m", "perfil", ext1=x1, ext2=x1, dx=15)

    # WT.
    if WT is not None and float(WT)>0:
        y_wt=min(max(y_ground+5, y_ground+float(WT)*62), H-110)
        s += [
            f'<line x1="45" y1="{y_wt:.2f}" x2="935" y2="{y_wt:.2f}" stroke="#0284c7" stroke-width="2" stroke-dasharray="9,5"/>',
            _text(930, y_wt-7,
                  _t(lang, "N.F.", "W.T."),
                  10, "#0369a1", "700", "end"),
        ]

    # Diagrama de contacto.
    qy=520; qh=100
    vmax=max(abs(float(sigma_max)), abs(float(sigma_min)), 1.0)
    scale=qh/vmax
    pmax=max(float(sigma_max),0)*scale
    pmin=max(float(sigma_min),0)*scale
    s += [
        f'<line x1="{x0-10}" y1="{qy}" x2="{x1+10}" y2="{qy}" stroke="#7c2d12" stroke-width="1.5"/>',
        f'<polygon points="{x0:.2f},{qy:.2f} {x0:.2f},{qy+pmin:.2f} {x1:.2f},{qy+pmax:.2f} {x1:.2f},{qy:.2f}" fill="#fecaca" fill-opacity="0.62" stroke="#dc2626" stroke-width="2"/>',
        _text(x0-10, qy+pmin+4, f"σmin = {float(sigma_min):.1f} kPa", 10, "#b91c1c", "700", "end"),
        _text(x1+10, qy+pmax+4, f"σmax = {float(sigma_max):.1f} kPa", 10, "#b91c1c", "700"),
        _text((x0+x1)/2, qy+qh+27,
              _t(lang,
                 "REACÇÃO DO TERRENO — diagrama de pressão de contacto",
                 "GROUND REACTION — contact pressure diagram"),
              10, "#7f1d1d", "700", "middle"),
    ]
    for k in range(13):
        xx=x0+(x1-x0)*k/12
        sig=float(sigma_min)+(float(sigma_max)-float(sigma_min))*k/12
        hh=max(sig,0)*scale
        if hh>1:
            s.append(f'<line x1="{xx:.2f}" y1="{qy+hh:.2f}" x2="{xx:.2f}" y2="{qy+3:.2f}" stroke="#b91c1c" stroke-width="1.1" marker-end="url(#perfil-red)"/>')

    s += _box(650, 75, 285, 122,
              _t(lang, "LEITURA DO CORTE", "SECTION NOTES"),
              "#cbd5e1", "#f8fafc")
    s += [
        _text(668, 108,
              _t(lang, "• B = dimensão da sapata",
                      "• B = footing dimension"), 10, "#334155"),
        _text(668, 130,
              _t(lang, "• Df = profundidade da fundação",
                      "• Df = foundation depth"), 10, "#334155"),
        _text(668, 152,
              _t(lang, "• h = altura total; d = altura útil",
                      "• h = total height; d = effective depth"), 10, "#334155"),
        _text(668, 174,
              _t(lang, "• N = acção vertical no pilar",
                      "• N = vertical action at the column"), 10, "#334155"),
    ]
    s += _legend(650, 218, 285, [
        ("gray",  _t(lang, "betão", "concrete")),
        ("red",   _t(lang, "armadura / tensão", "reinforcement / stress")),
        ("green", _t(lang, "altura útil d", "effective depth d")),
    ], lang)
    s.append(_text(485, 655,
                   _t(lang,
                      "Diagrama desenhado segundo a sequência do dimensionamento estrutural e as tensões de contacto da aula.",
                      "Diagram drawn following the structural design sequence and the contact stresses from the lecture."),
                   9, "#64748b", "400", "middle", True))
    s.append('</svg>')
    return "".join(s)


# -----------------------------------------------------------------------------
# 4. Ponto de resultante / núcleo central
# -----------------------------------------------------------------------------
def svg_ponto_resultante(Bx, By, ex, ey, eta_x, eta_y, dentro, lang="pt"):
    Bx=max(float(Bx),0.1); By=max(float(By),0.1); ex=float(ex); ey=float(ey)
    W,H=820,585
    esc=min(390/Bx,390/By)
    x0,y0=85,82
    wp,hp=Bx*esc,By*esc
    xc,yc=x0+wp/2,y0+hp/2
    xr,yr=xc+ex*esc,yc-ey*esc
    kx,ky=wp/6,hp/6
    s=_svg_start(W,H,
                 _t(lang,
                    "PONTO DE PASSAGEM DA RESULTANTE — NÚCLEO CENTRAL",
                    "RESULTANT PASSAGE POINT — CENTRAL KERN"),
                 "res",
                 _t(lang,
                    "Critério de localização da resultante usado nos slides 136–145",
                    "Resultant location criterion used in slides 136–145"))
    s += [
        f'<rect x="{x0}" y="{y0}" width="{wp:.2f}" height="{hp:.2f}" fill="#f8fafc" stroke="#111827" stroke-width="2.2"/>',
        f'<polygon points="{xc:.2f},{yc-ky:.2f} {xc+kx:.2f},{yc:.2f} {xc:.2f},{yc+ky:.2f} {xc-kx:.2f},{yc:.2f}" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>',
        f'<line x1="{x0-18}" y1="{yc}" x2="{x0+wp+18}" y2="{yc}" stroke="#64748b" stroke-dasharray="7,4"/>',
        f'<line x1="{xc}" y1="{y0-18}" x2="{xc}" y2="{y0+hp+18}" stroke="#64748b" stroke-dasharray="7,4"/>',
        f'<circle cx="{xc}" cy="{yc}" r="5" fill="#111827"/>',
        _text(xc+9,yc-8,"G",10,"#111827","700"),
    ]
    if abs(ex)+abs(ey)>1e-9:
        s += [
            f'<line x1="{xc}" y1="{yc}" x2="{xr}" y2="{yr}" stroke="#dc2626" stroke-width="2.3" stroke-dasharray="8,5" marker-end="url(#res-red)"/>',
            f'<circle cx="{xr}" cy="{yr}" r="8" fill="#dc2626" stroke="#fff" stroke-width="2"/>',
            _text(xr+11,yr-9,"R",12,"#b91c1c","700"),
        ]
    s += [
        _text(xc+kx+10,yc+5,"Bx/6",9,"#166534","700"),
        _text(xc+9,yc-ky-9,"By/6",9,"#166534","700"),
    ]
    col="#166534" if bool(dentro) else "#b91c1c"
    bg="#f0fdf4" if bool(dentro) else "#fef2f2"
    r_inside_footing=(abs(ex)<=Bx/2.0+1e-12 and abs(ey)<=By/2.0+1e-12)
    s += _box(530,82,250,222, _t(lang, "CRITÉRIO", "CRITERION"),col,bg)
    s += [
        _text(550,120,f"ηx = {float(eta_x):.4f}",11,"#334155"),
        _text(550,145,f"ηy = {float(eta_y):.4f}",11,"#334155"),
        _text(550,170,f"ηx + ηy = {float(eta_x)+float(eta_y):.4f}",11,"#334155"),
        _text(655,208,
              _t(lang, "≤ 1/6 → DENTRO", "≤ 1/6 → INSIDE") if bool(dentro)
              else _t(lang, "> 1/6 → FORA", "> 1/6 → OUTSIDE"),
              12,col,"700","middle"),
        _text(550,238,
              _t(lang, "Não se move o pilar por causa de e.",
                      "The column is not moved because of e."),
              10,"#334155","700"),
        _text(550,258,
              _t(lang, "O pilar continua centrado geometricamente",
                      "The column stays geometrically centred"),
              9,"#475569"),
        _text(550,276,
              _t(lang, "na sapata; a resultante R é deslocada.",
                      "on the footing; the resultant R is shifted."),
              9,"#475569"),
        _text(550,299,
              _t(lang, "R dentro da sapata: ", "R inside the footing: ")
              + _t(lang, "SIM" if r_inside_footing else "NÃO — rever geometria",
                      "YES" if r_inside_footing else "NO — revise geometry"),
              9,"#475569","700"),
    ]
    s += _dim_h(x0,x0+wp,y0-20,f"Bx = {Bx:.2f} m","res",ext1=y0,ext2=y0)
    s += _dim_v(y0,y0+hp,x0-37,f"By = {By:.2f} m","res",ext1=x0,ext2=x0,dx=-12)
    s += _box(530,325,250,120, _t(lang, "LEITURA", "NOTES"), "#cbd5e1", "#f8fafc")
    s += [
        _text(550,357,
              _t(lang, "Dentro do núcleo → tensões",
                      "Inside the kern → linear"), 10, "#334155"),
        _text(550,377,
              _t(lang, "lineares sem tracção no contacto.",
                      "stresses without uplift at contact."), 10, "#334155"),
        _text(550,403,
              _t(lang, "Fora do núcleo → seguir slides",
                      "Outside the kern → follow slides"), 10, "#334155"),
        _text(550,423,
              _t(lang, "142–146 / ábaco de Montoya quando aplicável.",
                      "142–146 / Montoya chart when applicable."),
              10, "#334155"),
    ]
    s += _legend(530, 465, 250, [
        ("green",   _t(lang, "núcleo central", "central kern")),
        ("dot-red", _t(lang, "resultante R", "resultant R")),
        ("dash-red",_t(lang, "G → R", "G → R")),
    ], lang)
    s.append('</svg>')
    return "".join(s)


# -----------------------------------------------------------------------------
# 5. Punçoamento
# -----------------------------------------------------------------------------
def svg_puncoamento(Bx, By, bx, by, d, sigma_max=None, sigma_min=None,
                    Vsd=None, Vrd=None, tau_sd=None, tau_rd=None, lang="pt"):
    Bx=float(Bx); By=float(By); bx=float(bx); by=float(by); d=max(float(d),0.01)
    esc=min(435/max(Bx,0.1), 435/max(By,0.1))
    x0,y0=65,90; wp=Bx*esc; hp=By*esc; xc,yc=x0+wp/2,y0+hp/2
    pw,ph=bx*esc,by*esc; off=d/2*esc; cw,ch=pw+2*off,ph+2*off
    cx,cy=xc-cw/2,yc-ch/2
    u=2*(bx+by)+math.pi*d
    Au=(bx+d)*(by+d)-((4-math.pi)/4.0)*d**2
    W,H=980,650
    s=_svg_start(
        W, H,
        _t(lang,
           "PUNÇOAMENTO — CONTORNO CRÍTICO A d/2",
           "PUNCHING SHEAR — CRITICAL PERIMETER AT d/2"),
        "punc",
        _t(lang,
           "REBAP — geometria do contorno conforme slides 147–148",
           "REBAP — critical perimeter geometry per slides 147–148"))

    s += [
        f'<rect x="{x0}" y="{y0}" width="{wp:.2f}" height="{hp:.2f}" fill="#f8fafc" stroke="#111827" stroke-width="2.2"/>',
        f'<rect x="{cx:.2f}" y="{cy:.2f}" width="{cw:.2f}" height="{ch:.2f}" rx="{off:.2f}" fill="#fee2e2" fill-opacity="0.28" stroke="#dc2626" stroke-width="2.8" stroke-dasharray="10,6"/>',
        f'<rect x="{xc-pw/2:.2f}" y="{yc-ph/2:.2f}" width="{pw:.2f}" height="{ph:.2f}" fill="#9ca3af" stroke="#111827" stroke-width="2.2"/>',
        _text(xc, yc+4, _t(lang, "PILAR", "COLUMN"), 11, "#ffffff", "700", "middle"),
        _text(xc, cy-12,
              _t(lang, "u — contorno crítico", "u — critical perimeter"),
              11, "#b91c1c", "700", "middle"),
    ]

    # Dimensão d/2.
    ydim=yc+ph/2+25
    s += [
        f'<line x1="{xc+pw/2:.2f}" y1="{ydim:.2f}" x2="{xc+pw/2+off:.2f}" y2="{ydim:.2f}" stroke="#dc2626" stroke-width="1.6" marker-start="url(#punc-red)" marker-end="url(#punc-red)"/>',
        _text(xc+pw/2+off/2, ydim-8, "d/2", 10, "#b91c1c", "700", "middle"),
        f'<line x1="{xc}" y1="{y0-44}" x2="{xc}" y2="{y0+3}" stroke="#111827" stroke-width="2.2" marker-end="url(#punc-load)"/>',
        _text(xc+10, y0-49, "Nsd", 11, "#111827", "700"),
    ]
    for i in range(8):
        xx=x0+35+i*max(wp-70,20)/7
        s.append(f'<line x1="{xx:.2f}" y1="{y0+hp+52}" x2="{xx:.2f}" y2="{y0+hp+10}" stroke="#a16207" stroke-width="1.5" marker-end="url(#punc-soil)"/>')
    s.append(_text(x0+12, y0+hp+78,
                   _t(lang, "reacção do terreno", "soil reaction"),
                   10, "#92400e", "700"))

    # painel.
    s += _box(555, 74, 365, 450,
              _t(lang, "CÁLCULO DO PUNÇOAMENTO", "PUNCHING SHEAR CALCULATION"),
              "#cbd5e1", "#f8fafc")
    s += [
        _text(575, 110, f"d = {d:.3f} m", 11, "#334155", "700"),
        _text(575, 136, f"u = 2(bx + by) + πd = {u:.3f} m", 11, "#334155"),
        _text(575, 162, f"Au = (bx+d)(by+d) − (4−π)d²/4", 10, "#334155"),
        _text(575, 185, f"Au = {Au:.4f} m²", 11, "#334155", "700"),
        _text(575, 219,
              _t(lang, "Verificação:", "Check:"), 12, "#0f172a", "700"),
        _text(575, 245, f"Vsd,ef = {_fmt(Vsd,2)} kN" if Vsd is not None else "Vsd,ef = —", 10, "#334155"),
        _text(575, 269, f"Vrd = {_fmt(Vrd,2)} kN" if Vrd is not None else "Vrd = —", 10, "#334155"),
        _text(575, 294, f"τsd = {_fmt(tau_sd,4)} MPa" if tau_sd is not None else "τsd = —", 10, "#334155"),
        _text(575, 318, f"τrd = {_fmt(tau_rd,4)} MPa" if tau_rd is not None else "τrd = —", 10, "#334155"),
    ]
    if Vsd is not None and Vrd is not None:
        ok=float(Vsd)<=float(Vrd)+1e-9
        col="#166534" if ok else "#b91c1c"; bg="#f0fdf4" if ok else "#fef2f2"
        s.append(f'<rect x="570" y="345" width="320" height="54" rx="8" fill="{bg}" stroke="{col}"/>')
        s.append(_text(730, 378,
                       _t(lang, "OK — Vsd,ef ≤ Vrd", "OK — Vsd,ef ≤ Vrd") if ok
                              else _t(lang, "NÃO VERIFICA — aumentar h",
                                             "DOES NOT VERIFY — increase h"),
                       11, col, "700", "middle"))
    if sigma_max is not None:
        s.append(_text(575, 426, f"σmax = {_fmt(sigma_max,1)} kPa", 10, "#991b1b", "700"))
    if sigma_min is not None:
        s.append(_text(575, 447, f"σmin = {_fmt(sigma_min,1)} kPa", 10, "#991b1b", "700"))
    s.append(_text(575, 478,
                   _t(lang,
                      "τrd = (1.6 − d) τ1  (d em metros)",
                      "τrd = (1.6 − d) τ1  (d in metres)"),
                   10, "#334155"))
    s.append(_text(575, 498, "τsd = Vsd,ef/(u·d)", 10, "#334155"))

    s += _legend(555, 545, 365, [
        ("dash-red", _t(lang, "contorno crítico a d/2", "critical perimeter at d/2")),
        ("gray",     _t(lang, "pilar", "column")),
        ("blue",     _t(lang, "cotas", "dimensions")),
    ], lang)
    s.append('</svg>')
    return "".join(s)


# -----------------------------------------------------------------------------
# 6. Método das consolas
# -----------------------------------------------------------------------------
def svg_disposicoes_construtivas(Bx, bx, h, sigma1, sigma2, As_x, As_y,
                                  diam_x, esp_x, lang="pt"):
    Bx=float(Bx); bx=float(bx); h=float(h)
    W,H=980,700
    esc=min(455/max(Bx,0.1), 105/max(h,0.1))
    x0=78; ytop=130; wp=Bx*esc; hp=h*105; ybot=ytop+hp; x1=x0+wp
    pw=bx*esc; xp=x0+(wp-pw)/2
    secL=xp+0.15*pw; secR=xp+0.85*pw
    s=_svg_start(
        W, H,
        _t(lang,
           "MÉTODO DAS CONSOLAS — SECÇÕES DE REFERÊNCIA I E II",
           "CANTILEVER METHOD — REFERENCE SECTIONS I AND II"),
        "disp",
        _t(lang,
           "A secção de referência está a 15% da largura do pilar para o interior",
           "The reference section is located 15% of the column width inwards"))

    s += [
        f'<rect x="{x0}" y="{ytop}" width="{wp:.2f}" height="{hp:.2f}" fill="#d1d5db" stroke="#111827" stroke-width="2.2"/>',
        f'<rect x="{x0}" y="{ytop}" width="{wp:.2f}" height="{hp:.2f}" fill="url(#disp-conc-hatch)" opacity="0.48"/>',
        f'<rect x="{xp}" y="35" width="{pw:.2f}" height="{ytop-35:.2f}" fill="#9ca3af" stroke="#111827" stroke-width="2"/>',
        _text(xp+pw/2, 83, _t(lang, "PILAR", "COLUMN"), 11, "#ffffff", "700", "middle"),
        f'<line x1="{secL}" y1="{ytop-12}" x2="{secL}" y2="{ybot+20}" stroke="#dc2626" stroke-width="1.7" stroke-dasharray="8,5"/>',
        f'<line x1="{secR}" y1="{ytop-12}" x2="{secR}" y2="{ybot+20}" stroke="#dc2626" stroke-width="1.7" stroke-dasharray="8,5"/>',
        _text(secL, ytop-17, "I", 11, "#b91c1c", "700", "middle"),
        _text(secR, ytop-17, "I", 11, "#b91c1c", "700", "middle"),
    ]

    # Diagrama de tensão.
    qy=ybot+38; qh=105
    vmax=max(abs(float(sigma1)), abs(float(sigma2)), 1.0); sc=qh/vmax
    h1=max(float(sigma1),0)*sc; h2=max(float(sigma2),0)*sc
    s += [
        f'<line x1="{x0-10}" y1="{qy}" x2="{x1+10}" y2="{qy}" stroke="#7c2d12" stroke-width="1.4"/>',
        f'<polygon points="{x0},{qy} {x0},{qy+h1} {x1},{qy+h2} {x1},{qy}" fill="#fecaca" fill-opacity="0.65" stroke="#dc2626" stroke-width="2"/>',
        _text(x0-8, qy+h1+4, f"σ1 = {_fmt(sigma1,1)} kPa", 9, "#b91c1c", "700", "end"),
        _text(x1+8, qy+h2+4, f"σ2 = {_fmt(sigma2,1)} kPa", 9, "#b91c1c", "700"),
    ]
    for k in range(11):
        xx=x0+(x1-x0)*k/10
        sig=float(sigma1)+(float(sigma2)-float(sigma1))*k/10
        hh=max(sig,0)*sc
        if hh>2:
            s.append(f'<line x1="{xx:.2f}" y1="{qy+hh:.2f}" x2="{xx:.2f}" y2="{qy+3:.2f}" stroke="#b91c1c" stroke-width="1.1" marker-end="url(#disp-red)"/>')
    s.append(_text((x0+x1)/2, qy+qh+25,
                   _t(lang, "reacção do terreno", "soil reaction"),
                   10, "#7f1d1d", "700", "middle"))

    # Consolas laterais e cotas l.
    l=(Bx-bx)/2+0.15*bx
    s += _dim_h(xp+0.15*pw, x1, qy+qh+52,
                f"l = (B−bx)/2 + 0.15bx = {l:.3f} m",
                "disp", "#2563eb", ytop, ybot, 10, 10)

    # Armadura inferior em corte.
    ysteel=ybot-19
    for k in range(12):
        xx=x0+24+k*max(wp-48,20)/11
        s.append(f'<circle cx="{xx:.2f}" cy="{ysteel:.2f}" r="3.2" fill="#b91c1c"/>')
    s.append(_text(x1+16, ysteel+4,
                   _t(lang,
                      f"armadura inferior — Ø{diam_x} // {esp_x} mm",
                      f"bottom reinforcement — Ø{diam_x} // {esp_x} mm"),
                   10, "#b91c1c", "700"))

    # Painel didáctico.
    s += _box(565, 78, 350, 265,
              _t(lang, "COMO O MÉTODO É APLICADO", "HOW THE METHOD IS APPLIED"),
              "#cbd5e1", "#f8fafc")
    lines_pt = [
        "1. Localizar as secções I e II a 15% da largura do pilar.",
        "2. Determinar a tensão de referência correspondente à consola.",
        "3. Calcular MEd em cada direcção pela reacção do terreno.",
        "4. Usar b = 1,00 m na tabela de flexão.",
        "5. Obter μ → ω → As e comparar com As,min.",
        "6. Pormenorizar diâmetro, espaçamento e ancoragem.",
    ]
    lines_en = [
        "1. Locate sections I and II at 15% of the column width.",
        "2. Determine the reference stress for the cantilever.",
        "3. Compute MEd in each direction from the soil reaction.",
        "4. Use b = 1.00 m in the bending table.",
        "5. Obtain μ → ω → As and compare with As,min.",
        "6. Detail diameter, spacing and anchorage.",
    ]
    lines = lines_pt if lang == "pt" else lines_en
    yy=116
    for line in lines:
        s.append(_text(583, yy, line, 10, "#334155")); yy+=33
    s += [
        _text(583, 320, f"Asx = {_fmt(As_x,2)} cm²/m", 11, "#b91c1c", "700"),
        _text(750, 320, f"Asy = {_fmt(As_y,2)} cm²/m", 11, "#1d4ed8", "700"),
    ]

    s += _box(565, 365, 350, 185,
              _t(lang, "TENSÃO DE REFERÊNCIA", "REFERENCE STRESS"),
              "#fde68a", "#fffbeb")
    s += [
        _text(583, 400,
              _t(lang, "Para a flexão longitudinal, evitar usar sempre σmax",
                      "For longitudinal bending, avoid always using σmax"),
              10, "#334155", "700"),
        _text(583, 422,
              _t(lang, "sem verificar a secção de referência.",
                      "without checking the reference section."),
              10, "#334155"),
        _text(583, 452,
              _t(lang, "A pressão na consola é linear; o código usa uma tensão",
                      "The pressure on the cantilever is linear; the code uses a"),
              10, "#475569"),
        _text(583, 472,
              _t(lang, "equivalente/representativa da zona de cálculo.",
                      "representative/equivalent stress for the design zone."),
              10, "#475569"),
        _text(583, 504,
              _t(lang, "Base: slides 156–157.", "Basis: slides 156–157."),
              10, "#7c2d12", "700"),
    ]
    s += _legend(565, 575, 350, [
        ("dash-red", _t(lang, "secções I/II", "sections I/II")),
        ("red",      _t(lang, "armadura inferior", "bottom reinforcement")),
        ("blue",     _t(lang, "cota / consola", "dimension / cantilever")),
    ], lang)
    s.append('</svg>')
    return "".join(s)


# -----------------------------------------------------------------------------
# 7. Desenho final
# -----------------------------------------------------------------------------
def svg_final_sapata(Bx, By, bx, by, h, arm_x, arm_y,
                     arm_dist_x, arm_dist_y, lang="pt"):
    Bx=float(Bx); By=float(By); bx=float(bx); by=float(by); h=float(h)
    W,H=1120,795
    esc=min(385/max(Bx,0.1), 300/max(By,0.1))
    x0,y0=58,112; wp,hp=Bx*esc,By*esc; xc,yc=x0+wp/2,y0+hp/2
    esc_c=min(410/max(Bx,0.1), 120/max(h,0.1)); x0c=575; y0c=185; wc=Bx*esc_c; hc=h*120; xcc=x0c+wc/2
    s=_svg_start(
        W, H,
        _t(lang,
           "DESENHO FINAL — SAPATA ARMADA",
           "FINAL DRAWING — REINFORCED FOOTING"),
        "final",
        _t(lang,
           "Planta + corte + quadro de armaduras + pormenor construtivo",
           "Plan + section + reinforcement schedule + detailing"))

    # PLANTA
    s.append(_text(x0+wp/2, 96,
                   _t(lang, "PLANTA", "PLAN"),
                   14, "#0f172a", "700", "middle"))
    s.append(f'<rect x="{x0}" y="{y0}" width="{wp:.2f}" height="{hp:.2f}" fill="#f8fafc" stroke="#111827" stroke-width="2.2"/>')
    # Armadura X
    nx=max(8,min(22,round(wp/22)))
    for i in range(nx):
        yy=y0+9+i*(hp-18)/max(nx-1,1)
        s.append(f'<line x1="{x0+7}" y1="{yy:.2f}" x2="{x0+wp-7}" y2="{yy:.2f}" stroke="#b91c1c" stroke-width="1.55" opacity="0.92"/>')
    # Armadura Y
    ny=max(8,min(22,round(hp/22)))
    for i in range(ny):
        xx=x0+9+i*(wp-18)/max(ny-1,1)
        s.append(f'<line x1="{xx:.2f}" y1="{y0+7}" x2="{xx:.2f}" y2="{y0+hp-7}" stroke="#1d4ed8" stroke-width="1.55" opacity="0.92"/>')
    # Pilar.
    pwp=bx*esc; php=by*esc; xp=xc-pwp/2; yp=yc-php/2
    s += [
        f'<rect x="{xp:.2f}" y="{yp:.2f}" width="{pwp:.2f}" height="{php:.2f}" fill="#9ca3af" stroke="#111827" stroke-width="2"/>',
        _text(xc, yc+4, _t(lang, "PILAR", "COLUMN"), 10, "#ffffff", "700", "middle"),
        f'<line x1="{xc}" y1="{y0-16}" x2="{xc}" y2="{y0+hp+16}" stroke="#64748b" stroke-dasharray="8,5"/>',
        f'<line x1="{x0-16}" y1="{yc}" x2="{x0+wp+16}" y2="{yc}" stroke="#64748b" stroke-dasharray="8,5"/>',
        _text(x0+wp+24, yc+5, "X", 11, "#2563eb", "700"),
        _text(xc+5, y0-20, "Y", 11, "#2563eb", "700"),
        _text(x0+wp/2, y0+hp+32,
              _t(lang, f"Armadura X: {arm_x}", f"Reinforcement X: {arm_x}"),
              10, "#b91c1c", "700", "middle"),
        _text(x0+wp/2, y0+hp+52,
              _t(lang, f"Armadura Y: {arm_y}", f"Reinforcement Y: {arm_y}"),
              10, "#1d4ed8", "700", "middle"),
    ]
    s += _dim_h(x0, x0+wp, y0-52, f"Bx = {Bx:.2f} m", "final", ext1=y0, ext2=y0)
    s += _dim_v(y0, y0+hp, x0-34, f"By = {By:.2f} m", "final", ext1=x0, ext2=x0, dx=-11)
    s += _dim_h(xp, xp+pwp, yp-18, f"bx = {bx:.2f} m", "final", "#64748b", yp, yp, -5, 10)
    s += _dim_v(yp, yp+php, xp-16, f"by = {by:.2f} m", "final", "#64748b", xp, xp, -9, 10)

    # CORTE.
    s.append(_text(x0c+wc/2, y0c-48,
                   _t(lang, "CORTE A–A", "SECTION A–A"),
                   14, "#0f172a", "700", "middle"))
    s += [
        f'<rect x="{x0c}" y="{y0c}" width="{wc:.2f}" height="{hc:.2f}" fill="#d1d5db" stroke="#111827" stroke-width="2.2"/>',
        f'<rect x="{x0c}" y="{y0c}" width="{wc:.2f}" height="{hc:.2f}" fill="url(#final-conc-hatch)" opacity="0.48"/>',
        f'<rect x="{x0c+(wc-bx*esc_c)/2:.2f}" y="{y0c-104}" width="{bx*esc_c:.2f}" height="104" fill="#9ca3af" stroke="#111827" stroke-width="2"/>',
        _text(xcc, y0c-53, _t(lang, "PILAR", "COLUMN"), 10, "#ffffff", "700", "middle"),
    ]
    ysteel=y0c+hc-21
    for i in range(10):
        xx=x0c+22+i*max(wc-44,20)/9
        s.append(f'<circle cx="{xx:.2f}" cy="{ysteel:.2f}" r="3.3" fill="#b91c1c" stroke="#7f1d1d"/>')
    s.append(_text(x0c+wc+15, ysteel+4,
                   _t(lang, "armadura inferior", "bottom reinforcement"),
                   10, "#b91c1c", "700"))
    s += _dim_v(y0c, y0c+hc, x0c+wc+50, f"h = {h:.2f} m", "final", ext1=x0c+wc, ext2=x0c+wc, dx=14)
    s.append(_text(x0c+wc+70, y0c+hc-42, "5 cm", 9, "#166534", "700"))
    s.append(_text(x0c+wc+70, y0c+hc-24,
                   _t(lang, "recobrimento", "cover"),
                   9, "#166534"))

    # QUADRO.
    s += _box(55, 500, 1035, 220,
              _t(lang, "QUADRO DE ARMADURAS", "REINFORCEMENT SCHEDULE"),
              "#cbd5e1", "#f8fafc")
    s += [
        _text(78, 536, _t(lang, "Direcção X", "Direction X"), 11, "#b91c1c", "700"),
        _text(175, 536, str(arm_x), 11, "#334155", "700"),
        _text(78, 568, _t(lang, "Distribuição X", "Distribution X"), 11, "#b91c1c", "700"),
        _text(175, 568, str(arm_dist_x), 11, "#334155", "700"),
        _text(78, 600, _t(lang, "Direcção Y", "Direction Y"), 11, "#1d4ed8", "700"),
        _text(175, 600, str(arm_y), 11, "#334155", "700"),
        _text(78, 632, _t(lang, "Distribuição Y", "Distribution Y"), 11, "#1d4ed8", "700"),
        _text(175, 632, str(arm_dist_y), 11, "#334155", "700"),
    ]
    s += _box(485, 525, 575, 155,
              _t(lang, "DETALHES CONSTRUTIVOS", "CONSTRUCTIVE DETAILS"),
              "#cbd5e1", "#ffffff")
    s += [
        _text(505, 558,
              _t(lang, "• Armaduras principais inferiores de extremidade a extremidade.",
                      "• Main bottom bars running from edge to edge."),
              10, "#334155"),
        _text(505, 581,
              _t(lang, "• Diâmetro mínimo e espaçamento máximo conforme slide 166.",
                      "• Minimum diameter and maximum spacing per slide 166."),
              10, "#334155"),
        _text(505, 604,
              _t(lang, "• Ancoragem deve satisfazer lb,net conforme slides 167–169.",
                      "• Anchorage must satisfy lb,net per slides 167–169."),
              10, "#334155"),
        _text(505, 627,
              _t(lang, "• Armadura superior só é necessária em casos particulares de tracção superior.",
                      "• Top reinforcement is only required in specific cases of top tension."),
              10, "#334155"),
        _text(505, 650,
              _t(lang, "• Conferir punçoamento, esforço transverso e pormenorização com o relatório.",
                      "• Verify punching, shear and detailing against the report."),
              10, "#7c2d12", "700"),
    ]

    s += _legend(55, 735, 220, [
        ("red",  _t(lang, "armadura X", "reinforcement X")),
        ("blue", _t(lang, "armadura Y", "reinforcement Y")),
        ("gray", _t(lang, "betão", "concrete")),
    ], lang)

    # Painel de distribuição (extra)
    s += _box(55, 435, 1035, 60,
              _t(lang, "ARMADURA DE DISTRIBUIÇÃO", "DISTRIBUTION REINFORCEMENT"),
              "#cbd5e1", "#fffbeb")
    s += [
        _text(78, 470, f"X: {arm_dist_x}", 11, "#b91c1c", "700"),
        _text(400, 470, f"Y: {arm_dist_y}", 11, "#1d4ed8", "700"),
        _text(760, 470,
              _t(lang,
                 "(20% da principal — Art. 108 REBAP)",
                 "(20% of main — Art. 108 REBAP)"),
              10, "#7c2d12", "700"),
    ]

    s.append(_text(300, 785,
                   _t(lang,
                      "Pormenorização esquemática: substituir os campos pelas designações finais do projecto e conferir ancoragens/cortes.",
                      "Schematic detailing: replace the fields with the final project designations and check anchorages/cut-offs."),
                   9, "#64748b", "400", italic=True))
    s.append('</svg>')
    return "".join(s)
