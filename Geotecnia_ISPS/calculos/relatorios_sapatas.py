"""
Relatório HTML (PT/EN) para Sapatas Rígidas — 100% bilingue com MathJax
"""
from datetime import datetime


def gerar_relatorio_html_sapatas(
    nome, curso, genero, lang,
    tipo_sapata, bx, by, P_kN, Mx_kNm, My_kNm,
    sigma_adm_kPa, classe_betao, tipo_aco, recobrimento_mm,
    gamma_solo, gamma_sat, phi_solo, c_solo, cu_solo, Df, WT,
    Bx, By, h, Nr,
    ex, ey, eta_x, eta_y,
    sigma1, sigma2, sigma3, sigma4,
    sigma_max, sigma_min, sigma_ref, zona,
    phi_d, c_d, delta_d, q_d,
    qr_ec7, Nc, Nq, Ngamma, termo_c, termo_q, termo_g,
    ok_carga, ok_desliz, ok_derr,
    Vd_kN, Hd_kN, Rd_kN, Mest_kNm, Mderr_kNm,
    ok_punco, ok_corte, Vsd_punco, Vrd_punco, tau_sd, tau_rd,
    Vsd_corte, Vrd_corte,
    armadura_x, armadura_y, As_x, As_y,
    armadura_dist_x, armadura_dist_y,
    combo_ec7, metodo_carga="Meyerhof (1963)",
    svg_convencao="", svg_resultante="", svg_planta="", svg_perfil="",
    svg_punco="", svg_disposicoes="", svg_final="",
    fbd_MPa=0.0, lb_net_x=0.0, lb_net_y=0.0, d_mm=0.0,
    As_min_x=0.0, As_min_y=0.0,
    As_max_x=0.0, As_max_y=0.0,
    As_f_x=0.0, As_f_y=0.0,
    As_dist_x=0.0, As_dist_y=0.0,
    **kwargs
):
    # ----------------------------------------------------------
    # DICIONÁRIO COMPLETO
    # ----------------------------------------------------------
    T = {
        "pt": {
            "titulo": "RELATÓRIO TÉCNICO — SAPATA RÍGIDA",
            "instituto": "INSTITUTO SUPERIOR POLITÉCNICO DE SONGO",
            "grupo": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
            "disciplina": "Fundações e Obras de Terra",
            "indice": "ÍNDICE",
            "senhor": "Senhor", "senhora": "Senhora",
            "curso": "Curso", "data": "Data", "combo": "Combinação EC7",
            # Índice
            "i1": "Dados de Entrada", "i2": "Pré-dimensionamento",
            "i3": "Tensões Instaladas", "i4": "Verificação Geotécnica (EC7)",
            "i5": "Dimensionamento Estrutural (REBAP)", "i6": "Armaduras de Flexão",
            "i7": "Comprimentos de Amarração", "i8": "Desenho Final",
            "i9": "Conclusão",
            # Secção 1
            "h1_geo": "1.1 Geometria do Pilar e Acções",
            "h1_solo": "1.2 Solo e Materiais",
            "p_param": "Parâmetro", "p_simb": "Símbolo", "p_val": "Valor", "p_uni": "Unidade",
            "p_tipo_sap": "Tipo de sapata", "p_bx": "Comprimento pilar", "p_by": "Largura pilar",
            "p_N": "Carga vertical", "p_Mx": "Momento em x", "p_My": "Momento em y",
            "p_sig": "Tensão admissível",
            "p_gama": "Peso específico natural", "p_gama_sat": "Peso específico saturado",
            "p_phi": "Ângulo de atrito", "p_c": "Coesão efetiva",
            "p_cu": "Coesão não drenada", "p_Df": "Profundidade de fundação",
            "p_WT": "Nível freático", "p_bet": "Classe do betão",
            "p_aco": "Tipo de aço", "p_rec": "Recobrimento",
            # Secção 2
            "h2_form": "Fórmula mestre (Cap3.1, pág. 129)",
            "p_Nr": "Carga majorada", "p_Bx": "Dimensão em x",
            "p_By": "Dimensão em y", "p_h": "Altura total",
            "h2_conv": "2.1 Convenção de Sinais dos Momentos",
            "h2_kern": "2.2 Ponto de Passagem da Resultante (Núcleo Central)",
            # Secção 3
            "h3_exc": "3.1 Excentricidades",
            "h3_tens": "3.2 Tensões nas Quatro Quinas",
            "p_zona": "Zona", "p_zm": "Resultante",
            "dentro": "dentro", "fora": "fora",
            "p_canto1": "Canto 1", "p_canto2": "Canto 2",
            "p_canto3": "Canto 3", "p_canto4": "Canto 4",
            "p_smax": "σ_max", "p_smin": "σ_min", "p_sref": "σ_ref",
            "h3_plan": "3.3 Planta da Sapata com Excentricidades",
            "h3_perf": "3.4 Perfil com Diagrama de Tensões",
            # Secção 4
            "h4_cap": "4.1 Capacidade de Carga",
            "p_termo_c": "Termo coesão", "p_termo_q": "Termo sobrecarga",
            "p_termo_g": "Termo peso próprio",
            "h4_desl": "4.2 Deslizamento",
            "p_Hd": "Componente horizontal", "p_Rd": "Resistência",
            "p_Vd": "Componente vertical",
            "h4_derr": "4.3 Derrubamento",
            "p_Mest": "Momento estabilizador", "p_Mderr": "Momento derrubador",
            # Secção 5
            "h5_punc": "5.1 Punçoamento (REBAP Art. 55)",
            "p_Vsdef": "Esforço efetivo", "p_tau_sd": "Tensão atuante",
            "p_tau_rd": "Tensão resistente", "p_d": "Altura útil",
            "h5_cont": "5.2 Contorno Crítico de Punçoamento",
            "h5_corte": "5.3 Esforço Transverso (REBAP Art. 53)",
            "p_Vsd": "Esforço atuante", "p_Vrd": "Esforço resistente",
            # Secção 6
            "h6_dim": "6.1 Dimensionamento das Armaduras",
            "p_dir": "Direção", "p_ascalc": "As calculada (cm²/m)",
            "p_armad": "Armadura adoptada", "p_x": "X-X (principal)",
            "p_y": "Y-Y (principal)", "p_dx": "Distribuição X (20%)",
            "p_dy": "Distribuição Y (20%)",
            "h6_disp": "6.2 Disposições Construtivas",
            # Secção 7
            "p_lbnet": "lb,net (mm)", "p_fbd": "fbd (MPa)",
            "nota_amar": "Comprimentos de amarração segundo REBAP Art. 80, boa aderência.",
            # Secção 8
            "txt_final": "Desenho de pormenorização com a planta das armaduras e corte A-A.",
            # Secção 9
            "ok_all": "✅ SAPATA SATISFAZ TODAS AS VERIFICAÇÕES",
            "no_all": "❌ SAPATA NÃO SATISFAZ — REDIMENSIONAR",
            "footer1": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
            "footer2": "Regulamentos: EC7 (EN 1997-1) | REBAP (DL 349-C/83) | RSA",
            "btn": "Imprimir / PDF",
            "fig_conv": "Figura 2.1 — Convenção dos momentos Mx e My",
            "fig_kern": "Figura 2.2 — Verificação do núcleo central (kern)",
            "fig_plan": "Figura 3.1 — Planta com pilar, excentricidades e resultante",
            "fig_perf": "Figura 3.2 — Corte vertical com Df, N.F. e diagrama de tensões",
            "fig_punc": "Figura 5.1 — Contorno crítico a d/2 da face do pilar",
            "fig_disp": "Figura 6.1 — Consolas, secção crítica e diagrama de tensões",
            "fig_final": "Figura 8.1 — Pormenorização final das armaduras",
        },
        "en": {
            "titulo": "TECHNICAL REPORT — RIGID FOOTING",
            "instituto": "SONGO POLYTECHNIC INSTITUTE",
            "grupo": "HYDRAULIC-GEOSTRUCT (GROUP III)",
            "disciplina": "Foundations and Earthworks",
            "indice": "CONTENTS",
            "senhor": "Mr.", "senhora": "Mrs.",
            "curso": "Course", "data": "Date", "combo": "EC7 Combination",
            "i1": "Input Data", "i2": "Pre-sizing",
            "i3": "Soil Stresses", "i4": "Geotechnical Check (EC7)",
            "i5": "Structural Design (REBAP)", "i6": "Flexural Reinforcement",
            "i7": "Anchorage Lengths", "i8": "Final Drawing",
            "i9": "Conclusion",
            "h1_geo": "1.1 Column Geometry and Actions",
            "h1_solo": "1.2 Soil and Materials",
            "p_param": "Parameter", "p_simb": "Symbol", "p_val": "Value", "p_uni": "Unit",
            "p_tipo_sap": "Footing type", "p_bx": "Column length", "p_by": "Column width",
            "p_N": "Vertical load", "p_Mx": "Moment in x", "p_My": "Moment in y",
            "p_sig": "Allowable stress",
            "p_gama": "Natural unit weight", "p_gama_sat": "Saturated unit weight",
            "p_phi": "Friction angle", "p_c": "Effective cohesion",
            "p_cu": "Undrained cohesion", "p_Df": "Foundation depth",
            "p_WT": "Water table", "p_bet": "Concrete class",
            "p_aco": "Steel type", "p_rec": "Cover",
            "h2_form": "Master formula (Chap. 3.1, p. 129)",
            "p_Nr": "Factored load", "p_Bx": "Dimension in x",
            "p_By": "Dimension in y", "p_h": "Total height",
            "h2_conv": "2.1 Sign Convention for Moments",
            "h2_kern": "2.2 Resultant Location (Central Kern)",
            "h3_exc": "3.1 Eccentricities",
            "h3_tens": "3.2 Corner Stresses",
            "p_zona": "Zone", "p_zm": "Resultant",
            "dentro": "inside", "fora": "outside",
            "p_canto1": "Corner 1", "p_canto2": "Corner 2",
            "p_canto3": "Corner 3", "p_canto4": "Corner 4",
            "p_smax": "σ_max", "p_smin": "σ_min", "p_sref": "σ_ref",
            "h3_plan": "3.3 Footing Plan with Eccentricities",
            "h3_perf": "3.4 Section with Stress Diagram",
            "h4_cap": "4.1 Bearing Capacity",
            "p_termo_c": "Cohesion term", "p_termo_q": "Surcharge term",
            "p_termo_g": "Self-weight term",
            "h4_desl": "4.2 Sliding",
            "p_Hd": "Horizontal component", "p_Rd": "Resistance",
            "p_Vd": "Vertical component",
            "h4_derr": "4.3 Overturning",
            "p_Mest": "Stabilizing moment", "p_Mderr": "Overturning moment",
            "h5_punc": "5.1 Punching Shear (REBAP Art. 55)",
            "p_Vsdef": "Effective force", "p_tau_sd": "Acting stress",
            "p_tau_rd": "Resisting stress", "p_d": "Effective depth",
            "h5_cont": "5.2 Punching Shear Critical Contour",
            "h5_corte": "5.3 Shear Force (REBAP Art. 53)",
            "p_Vsd": "Acting force", "p_Vrd": "Resisting force",
            "h6_dim": "6.1 Reinforcement Design",
            "p_dir": "Direction", "p_ascalc": "As calculated (cm²/m)",
            "p_armad": "Adopted reinforcement", "p_x": "X-X (main)",
            "p_y": "Y-Y (main)", "p_dx": "Distribution X (20%)",
            "p_dy": "Distribution Y (20%)",
            "h6_disp": "6.2 Constructive Detailing",
            "p_lbnet": "lb,net (mm)", "p_fbd": "fbd (MPa)",
            "nota_amar": "Anchorage lengths per REBAP Art. 80, good bond conditions.",
            "txt_final": "Detailing drawing with reinforcement plan and section A-A.",
            "ok_all": "✅ FOOTING SATISFIES ALL CHECKS",
            "no_all": "❌ FOOTING DOES NOT SATISFY — RESIZE",
            "footer1": "HYDRAULIC-GEOSTRUCT (GROUP III)",
            "footer2": "Codes: EC7 (EN 1997-1) | REBAP (DL 349-C/83) | RSA",
            "btn": "Print / PDF",
            "fig_conv": "Figure 2.1 — Sign convention for Mx and My",
            "fig_kern": "Figure 2.2 — Central kern check",
            "fig_plan": "Figure 3.1 — Plan with column, eccentricities and resultant",
            "fig_perf": "Figure 3.2 — Vertical section with Df, W.T. and stress diagram",
            "fig_punc": "Figure 5.1 — Critical contour at d/2 from column face",
            "fig_disp": "Figure 6.1 — Cantilevers, critical section and stress diagram",
            "fig_final": "Figure 8.1 — Final reinforcement detailing",
        },
    }[lang]

    titulo_gen = T["senhor"] if genero == "Masculino" else T["senhora"]
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    ok_geral = ok_carga and ok_desliz and ok_derr and ok_punco
    status_txt = T["ok_all"] if ok_geral else T["no_all"]
    status_cor = "#28a745" if ok_geral else "#dc3545"

    def box(ok, txt_ok, txt_nok):
        cor = "#28a745" if ok else "#dc3545"
        bg = "#d4edda" if ok else "#f8d7da"
        txt = txt_ok if ok else txt_nok
        return (f'<div style="background:{bg};border-left:6px solid {cor};'
                f'padding:12px;margin:12px 0;border-radius:6px;font-weight:bold;'
                f'color:{cor};">{txt}</div>')

    def fig(titulo, svg):
        if not svg:
            return ""
        return (f'<div style="text-align:center;margin:20px 0;page-break-inside:avoid;">'
                f'<h3 style="color:#2c3e50;margin-bottom:8px;">{titulo}</h3>{svg}</div>')

    zona_txt = T["dentro"] if zona == "A" else T["fora"]
    tipo_txt = {"homotetica": "Homothetic" if lang == "en" else "Homotética",
                "bordos_equidistantes": "Equal edges" if lang == "en" else "Bordos Equidistantes",
                "quadrada": "Square" if lang == "en" else "Quadrada",
                "proporcionada": "Proportioned" if lang == "en" else "Proporcionada"}.get(tipo_sapata, tipo_sapata)

    p = []
    p.append(f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">')
    p.append(f'<title>{T["titulo"]}</title>')
    p.append('<script>window.MathJax={tex:{inlineMath:[["$","$"]],displayMath:[["$$","$$"]]},svg:{fontCache:"global"}};</script>')
    p.append('<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>')
    p.append('<style>')
    p.append('@media print{.no-print{display:none}.page-break{page-break-before:always}}')
    p.append('body{font-family:"Segoe UI",sans-serif;line-height:1.6;color:#222;max-width:960px;margin:0 auto;padding:20px;background:#f5f5f5}')
    p.append('.container{background:#fff;padding:40px;box-shadow:0 2px 10px rgba(0,0,0,.1)}')
    p.append('.capa{text-align:center;padding:40px 20px;border-bottom:3px solid #1f77b4;margin-bottom:30px}')
    p.append('.capa h1{color:#1f77b4;font-size:24px}.capa h2{color:#2c3e50;font-size:18px}')
    p.append('h1{color:#1f77b4;border-bottom:3px solid #1f77b4;padding-bottom:8px;margin-top:35px}')
    p.append('h2{color:#2c3e50;border-bottom:2px solid #2c3e50;padding-bottom:6px;margin-top:25px}')
    p.append('table{width:100%;border-collapse:collapse;margin:15px 0;font-size:13px}')
    p.append('th{background:#34495e;color:#fff;padding:8px;border:1px solid #2c3e50;text-align:left}')
    p.append('td{padding:7px 8px;border:1px solid #ddd}tr:nth-child(even){background:#f8f9fa}')
    p.append('.formula-box{background:#f0f8ff;border-left:4px solid #1f77b4;padding:12px 18px;margin:10px 0;border-radius:4px}')
    p.append(f'.status-final{{background:{status_cor};color:#fff;padding:18px;border-radius:8px;text-align:center;font-size:17px;font-weight:bold;margin:25px 0}}')
    p.append('.btn-imp{position:fixed;top:15px;right:15px;background:#1f77b4;color:#fff;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;z-index:1000}')
    p.append('.footer{text-align:center;margin-top:30px;padding-top:15px;border-top:2px solid #ddd;color:#666;font-size:11px}')
    p.append('.indice{background:#f8f9fa;padding:15px;border-radius:8px}')
    p.append('</style></head><body>')
    p.append(f'<button class="btn-imp no-print" onclick="window.print()">🖨️ {T["btn"]}</button>')
    p.append('<div class="container">')

    # CAPA
    p.append('<div class="capa">')
    p.append(f'<h1>{T["instituto"]}</h1><h2>{T["grupo"]}</h2><h3>{T["disciplina"]}</h3>')
    p.append(f'<h2 style="margin-top:30px;">{T["titulo"]}</h2>')
    p.append(f'<p><strong>{titulo_gen}:</strong> {nome} | <strong>{T["curso"]}:</strong> {curso}</p>')
    p.append(f'<p><strong>{T["data"]}:</strong> {data_atual}</p>')
    p.append(f'<p><strong>{T["combo"]}:</strong> {combo_ec7}</p></div>')

    # ÍNDICE
    p.append(f'<h1>{T["indice"]}</h1><div class="indice"><ol>')
    for k in ["i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9"]:
        p.append(f'<li>{T[k]}</li>')
    p.append('</ol></div>')

    # 1. DADOS
    p.append(f'<div class="page-break"></div><h1>1. {T["i1"].upper()}</h1>')
    p.append(f'<h2>{T["h1_geo"]}</h2><table>')
    p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>{T["p_tipo_sap"]}</td><td>-</td><td>{tipo_txt}</td><td>-</td></tr>')
    p.append(f'<tr><td>{T["p_bx"]}</td><td>$b_x$</td><td>{bx:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>{T["p_by"]}</td><td>$b_y$</td><td>{by:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>{T["p_N"]}</td><td>$N$</td><td>{P_kN:.2f}</td><td>kN</td></tr>')
    p.append(f'<tr><td>{T["p_Mx"]}</td><td>$M_x$</td><td>{Mx_kNm:.2f}</td><td>kN·m</td></tr>')
    p.append(f'<tr><td>{T["p_My"]}</td><td>$M_y$</td><td>{My_kNm:.2f}</td><td>kN·m</td></tr>')
    p.append(f'<tr><td>{T["p_sig"]}</td><td>$\\sigma_{{adm}}$</td><td>{sigma_adm_kPa:.2f}</td><td>kPa</td></tr></table>')

    p.append(f'<h2>{T["h1_solo"]}</h2><table>')
    p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>{T["p_gama"]}</td><td>$\\gamma$</td><td>{gamma_solo:.2f}</td><td>kN/m³</td></tr>')
    p.append(f'<tr><td>{T["p_gama_sat"]}</td><td>$\\gamma_{{sat}}$</td><td>{gamma_sat:.2f}</td><td>kN/m³</td></tr>')
    p.append(f'<tr><td>{T["p_phi"]}</td><td>$\\phi\'$</td><td>{phi_solo:.1f}</td><td>°</td></tr>')
    p.append(f'<tr><td>{T["p_c"]}</td><td>$c\'$</td><td>{c_solo:.2f}</td><td>kPa</td></tr>')
    p.append(f'<tr><td>{T["p_cu"]}</td><td>$c_u$</td><td>{cu_solo:.2f}</td><td>kPa</td></tr>')
    p.append(f'<tr><td>{T["p_Df"]}</td><td>$D_f$</td><td>{Df:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>{T["p_WT"]}</td><td>$W_T$</td><td>{WT:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>{T["p_bet"]}</td><td>-</td><td>{classe_betao}</td><td>-</td></tr>')
    p.append(f'<tr><td>{T["p_aco"]}</td><td>-</td><td>{tipo_aco}</td><td>-</td></tr>')
    p.append(f'<tr><td>{T["p_rec"]}</td><td>$c$</td><td>{recobrimento_mm}</td><td>mm</td></tr></table>')

    # 2. PRÉ-DIM
    p.append(f'<div class="page-break"></div><h1>2. {T["i2"].upper()}</h1>')
    p.append(f'<div class="formula-box"><strong>{T["h2_form"]}:</strong>')
    p.append('$$B_y = \\frac{1}{b}\\left[-a + e_y b + e_x + \\sqrt{(a + e_y b - e_x)^2 + b\\frac{N+P}{\\sigma_{adm}}}\\right]$$')
    p.append('$$B_x = 2a + b \\cdot B_y$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>{T["p_Nr"]}</td><td>$N_r$</td><td>{Nr:.2f}</td><td>kN</td></tr>')
    p.append(f'<tr><td>{T["p_Bx"]}</td><td>$B_x$</td><td><strong>{Bx:.2f}</strong></td><td>m</td></tr>')
    p.append(f'<tr><td>{T["p_By"]}</td><td>$B_y$</td><td><strong>{By:.2f}</strong></td><td>m</td></tr>')
    p.append(f'<tr><td>{T["p_h"]}</td><td>$h$</td><td><strong>{h:.2f}</strong></td><td>m</td></tr></table>')

    p.append(f'<h2>{T["h2_conv"]}</h2>')
    p.append(fig(T["fig_conv"], svg_convencao))
    p.append(f'<h2>{T["h2_kern"]}</h2>')
    p.append(fig(T["fig_kern"], svg_resultante))

    # 3. TENSÕES
    p.append(f'<div class="page-break"></div><h1>3. {T["i3"].upper()}</h1>')
    p.append(f'<h2>{T["h3_exc"]}</h2><div class="formula-box">')
    p.append(f'$$e_x = \\frac{{M_x}}{{N_r}} = {ex:.4f}\\text{{ m}} \\quad e_y = \\frac{{M_y}}{{N_r}} = {ey:.4f}\\text{{ m}}$$')
    p.append(f'$$\\eta_x + \\eta_y = {eta_x + eta_y:.4f} \\quad \\text{{vs}} \\quad \\frac{{1}}{{6}} = 0.1667$$</div>')
    p.append(f'<p><strong>{T["p_zona"]}:</strong> {zona} — {T["p_zm"]} {zona_txt}</p>')

    p.append(f'<h2>{T["h3_tens"]}</h2><div class="formula-box">')
    p.append('$$\\sigma_i = \\frac{N_r}{B_x B_y}\\left(1 \\pm 6\\eta_x \\pm 6\\eta_y\\right)$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_canto1"]}</th><th>σ₁ (kPa)</th><th>{T["p_canto2"]}</th><th>σ₂ (kPa)</th></tr>')
    p.append(f'<tr><td>{T["p_canto1"]}</td><td>{sigma1:.2f}</td><td>{T["p_canto2"]}</td><td>{sigma2:.2f}</td></tr>')
    p.append(f'<tr><td>{T["p_canto3"]}</td><td>{sigma3:.2f}</td><td>{T["p_canto4"]}</td><td>{sigma4:.2f}</td></tr>')
    p.append(f'<tr style="background:#fff3cd;"><td colspan="2"><strong>{T["p_smax"]}</strong></td><td colspan="2"><strong>{sigma_max:.2f}</strong></td></tr>')
    p.append(f'<tr style="background:#fff3cd;"><td colspan="2"><strong>{T["p_smin"]}</strong></td><td colspan="2"><strong>{sigma_min:.2f}</strong></td></tr>')
    p.append(f'<tr style="background:#d4edda;"><td colspan="2"><strong>{T["p_sref"]}</strong></td><td colspan="2"><strong>{sigma_ref:.2f}</strong></td></tr></table>')
    p.append(box(sigma_ref <= sigma_adm_kPa,
                 f'✅ σ_ref = {sigma_ref:.2f} ≤ σ_adm = {sigma_adm_kPa:.2f} kPa',
                 f'❌ σ_ref = {sigma_ref:.2f} > σ_adm = {sigma_adm_kPa:.2f} kPa'))

    p.append(f'<h2>{T["h3_plan"]}</h2>')
    p.append(fig(T["fig_plan"], svg_planta))
    p.append(f'<h2>{T["h3_perf"]}</h2>')
    p.append(fig(T["fig_perf"], svg_perfil))

    # 4. EC7
    p.append(f'<div class="page-break"></div><h1>4. {T["i4"].upper()}</h1>')
    p.append(f'<h2>{T["h4_cap"]} — {metodo_carga}</h2><div class="formula-box">')
    p.append('$$q_u = c\' N_c F_{cs} F_{cd} F_{ci} + q N_q F_{qs} F_{qd} F_{qi} + \\frac{1}{2}\\gamma B N_\\gamma F_{\\gamma s} F_{\\gamma d} F_{\\gamma i}$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>$N_c$</th><td>{Nc:.3f}</td><th>$N_q$</th><td>{Nq:.3f}</td></tr>')
    p.append(f'<tr><th>$N_\\gamma$</th><td>{Ngamma:.3f}</td><th>{T["p_termo_c"]}</th><td>{termo_c:.2f} kPa</td></tr>')
    p.append(f'<tr><th>{T["p_termo_q"]}</th><td>{termo_q:.2f} kPa</td><th>{T["p_termo_g"]}</th><td>{termo_g:.2f} kPa</td></tr>')
    p.append(f'<tr style="background:#d4edda;"><td colspan="2"><strong>$q_{{R,d}}$</strong></td><td colspan="2"><strong>{qr_ec7:.2f} kPa</strong></td></tr></table>')
    p.append(box(ok_carga, f'✅ q_R,d = {qr_ec7:.2f} ≥ σ_max = {sigma_max:.2f} kPa',
                 f'❌ q_R,d = {qr_ec7:.2f} < σ_max = {sigma_max:.2f} kPa'))

    p.append(f'<h2>{T["h4_desl"]}</h2><div class="formula-box">')
    p.append('$$H_d \\leq R_d = \\frac{V_d \\tan\\delta_b}{\\gamma_{R;h}}$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_Hd"]}</th><td>{Hd_kN:.2f} kN</td><th>{T["p_Rd"]}</th><td>{Rd_kN:.2f} kN</td></tr>')
    p.append(f'<tr><th>{T["p_Vd"]}</th><td>{Vd_kN:.2f} kN</td><td colspan="2"></td></tr></table>')
    p.append(box(ok_desliz, "✅ R_d ≥ H_d", "❌ R_d < H_d"))

    p.append(f'<h2>{T["h4_derr"]}</h2><div class="formula-box">')
    p.append('$$M_{stb,d} \\geq M_{dst,d}$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_Mest"]}</th><td>{Mest_kNm:.2f} kNm</td><th>{T["p_Mderr"]}</th><td>{Mderr_kNm:.2f} kNm</td></tr></table>')
    p.append(box(ok_derr, "✅ M_est ≥ M_derr", "❌ M_est < M_derr"))

    # 5. REBAP
    p.append(f'<div class="page-break"></div><h1>5. {T["i5"].upper()}</h1>')
    p.append(f'<h2>{T["h5_punc"]}</h2><div class="formula-box">')
    p.append('$$u = 2(b_x + b_y) + \\pi d \\quad ; \\quad A_u = (b_x+d)(b_y+d) - \\frac{4-\\pi}{4}d^2$$')
    p.append('$$V_{sd,ef} = V_{sd,red}\\left(1 + 1.5\\frac{|e_x|+|e_y|}{\\sqrt{b\'_x b\'_y}}\\right) \\quad ; \\quad \\tau_{sd} = \\frac{V_{sd,ef}}{u \\cdot d} \\leq (1.6-d)\\tau_1$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_Vsdef"]}</th><td>{Vsd_punco:.2f} kN</td></tr>')
    p.append(f'<tr><th>{T["p_tau_sd"]}</th><td>{tau_sd:.4f} MPa</td></tr>')
    p.append(f'<tr><th>{T["p_tau_rd"]}</th><td>{tau_rd:.4f} MPa</td></tr>')
    p.append(f'<tr><th>{T["p_d"]}</th><td>{d_mm/1000:.3f} m</td></tr></table>')
    p.append(box(ok_punco, "✅ τ_sd ≤ τ_rd", "❌ τ_sd > τ_rd"))
    p.append(f'<h2>{T["h5_cont"]}</h2>')
    p.append(fig(T["fig_punc"], svg_punco))



        # 6. ARMADURAS
    p.append(f'<div class="page-break"></div><h1>6. {T["i6"].upper()}</h1>')

    # 6.1 Dimensionamento das Armaduras — principal + mín/máx
    p.append(f'<h2>{T["h6_dim"]}</h2><div class="formula-box">')
    p.append('$$\\mu = \\frac{M_{Ed}}{b \\cdot d^2 \\cdot f_{cd}} \\quad ; \\quad \\omega = \\mu(1+\\mu) \\quad ; \\quad A_s = \\frac{\\omega \\cdot b \\cdot d \\cdot f_{cd}}{f_{syd}}$$')
    p.append('$$A_{s,\\min} = \\rho \\cdot b \\cdot d \\quad ; \\quad A_{s,\\max} = 0{,}04 \\cdot b \\cdot h \\quad ; \\quad A_{s,dist} = 0{,}20 \\, A_s$$')
    p.append('</div>')
    p.append('<table>')
    p.append('<tr>'
             f'<th>{T["p_dir"]}</th>'
             '<th>$A_{s,calc}$<br>(cm²/m)</th>'
             '<th>$A_{s,\\min}$<br>(cm²/m)</th>'
             '<th>$A_{s,\\max}$<br>(cm²/m)</th>'
             '<th>$A_s$ adoptado<br>(cm²/m)</th>'
             f'<th>{T["p_armad"]}</th></tr>')
    p.append(f'<tr><td>{T["p_x"]}</td>'
             f'<td>{As_x:.2f}</td><td>{As_min_x:.2f}</td>'
             f'<td>{As_max_x:.2f}</td><td><strong>{As_f_x:.2f}</strong></td>'
             f'<td><strong>{armadura_x}</strong></td></tr>')
    p.append(f'<tr><td>{T["p_y"]}</td>'
             f'<td>{As_y:.2f}</td><td>{As_min_y:.2f}</td>'
             f'<td>{As_max_y:.2f}</td><td><strong>{As_f_y:.2f}</strong></td>'
             f'<td><strong>{armadura_y}</strong></td></tr>')
    p.append('</table>')

    # 6.2 Armadura de Distribuição
    p.append('<h2>6.2 Armadura de Distribuição (Art. 108 REBAP — 20% da principal)</h2>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_dir"]}</th>'
             '<th>$A_{s,dist}$<br>(cm²/m)</th>'
             f'<th>{T["p_armad"]}</th></tr>')
    p.append(f'<tr><td>{T["p_x"]}</td><td>{As_dist_x:.2f}</td>'
             f'<td><strong>{armadura_dist_x}</strong></td></tr>')
    p.append(f'<tr><td>{T["p_y"]}</td><td>{As_dist_y:.2f}</td>'
             f'<td><strong>{armadura_dist_y}</strong></td></tr>')
    p.append('</table>')

    # 6.3 Disposições construtivas (figura)
    p.append(f'<h2>{T["h6_disp"]}</h2>')
    p.append(fig(T["fig_disp"], svg_disposicoes))

    # 7. AMARRAÇÃO
    p.append(f'<div class="page-break"></div><h1>7. {T["i7"].upper()}</h1><div class="formula-box">')
    p.append('$$l_b = \\frac{\\phi}{4} \\cdot \\frac{f_{syd}}{f_{bd}} \\quad ; \\quad l_{b,net} = l_b \\cdot \\frac{A_{s,cal}}{A_{s,ef}} \\cdot \\alpha_1 \\geq l_{b,min}$$</div>')
    p.append('<table>')
    p.append(f'<tr><th>{T["p_dir"]}</th><th>{T["p_fbd"]}</th><th>{T["p_lbnet"]}</th></tr>')
    p.append(f'<tr><td>X-X</td><td>{fbd_MPa:.3f}</td><td><strong>{lb_net_x:.0f}</strong></td></tr>')
    p.append(f'<tr><td>Y-Y</td><td>{fbd_MPa:.3f}</td><td><strong>{lb_net_y:.0f}</strong></td></tr></table>')
    p.append(f'<p><em>{T["nota_amar"]}</em></p>')

    # 8. DESENHO FINAL
    p.append(f'<div class="page-break"></div><h1>8. {T["i8"].upper()}</h1>')
    p.append(f'<p>{T["txt_final"]}</p>')
    p.append(fig(T["fig_final"], svg_final))

    # 9. CONCLUSÃO
    p.append(f'<div class="page-break"></div><h1>9. {T["i9"].upper()}</h1>')
    p.append(f'<div class="status-final">{status_txt}</div>')
    p.append(f'<div class="footer"><p>{T["footer1"]} — {T["instituto"]}</p>')
    p.append(f'<p>{T["footer2"]}</p><p>{data_atual}</p></div>')
    p.append('</div></body></html>')

    return "\n".join(p).encode("utf-8")