"""
Relatório HTML (PT/EN) para Muros de Gravidade — com MathJax e esquema SVG.
"""
from datetime import datetime


TXT = {
    "pt": {
        "titulo": "RELATÓRIO TÉCNICO — MURO DE GRAVIDADE",
        "instituto": "INSTITUTO SUPERIOR POLITÉCNICO DE SONGO",
        "grupo": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
        "disciplina": "Muros de Contenção e Fundações Superficiais",
        "indice": "ÍNDICE",
        "senhor": "Senhor", "senhora": "Senhora",
        "curso": "Curso", "data": "Data", "combo": "Combinação EC7",
        "i1": "Dados de Entrada", "i2": "Parâmetros de Cálculo (EC7)",
        "i3": "Coeficientes de Impulso", "i4": "Impulsos e Componentes",
        "i5": "Subpressão", "i6": "Peso da Estrutura", "i7": "Momentos",
        "i8": "Resultante e Excentricidade", "i9": "Verificações de Segurança",
        "i10": "Observações e Conclusões", "i11": "Esquema Final",
        "h1_geo": "1.1 Geometria do Muro",
        "h1_solo": "1.2 Propriedades do Solo",
        "h1_fund": "1.3 Solo de Fundação",
        "h1_met": "1.4 Método e Atrito",
        "h2_parc": "2.1 Coeficientes Parciais Aplicados",
        "h2_val": "2.2 Valores de Cálculo (Minorados)",
        "h9_derr": "9.1 Derrubamento (EQU)",
        "h9_desl": "9.2 Deslizamento (STR/GEO)",
        "h9_cap": "9.3 Capacidade de Carga (STR/GEO)",
        "h9_detc": "9.4 Detalhe da Capacidade de Carga",
        "p_param": "Parâmetro", "p_simb": "Símbolo", "p_val": "Valor", "p_uni": "Unidade",
        "p_desc": "Descrição",
        "ok_all": "✅ MURO SATISFAZ TODAS AS VERIFICAÇÕES",
        "no_all": "❌ MURO NÃO SATISFAZ — REDIMENSIONAR",
        "btn": "Imprimir / PDF",
        "footer1": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
        "footer2": "EC7 (EN 1997-1) | REBAP (DL 349-C/83) | RSA",
    },
    "en": {
        "titulo": "TECHNICAL REPORT — GRAVITY WALL",
        "instituto": "SONGO POLYTECHNIC INSTITUTE",
        "grupo": "HYDRAULIC-GEOSTRUCT (GROUP III)",
        "disciplina": "Retaining Walls and Shallow Foundations",
        "indice": "CONTENTS",
        "senhor": "Mr.", "senhora": "Mrs.",
        "curso": "Course", "data": "Date", "combo": "EC7 Combination",
        "i1": "Input Data", "i2": "Calculation Parameters (EC7)",
        "i3": "Earth Pressure Coefficients", "i4": "Thrusts and Components",
        "i5": "Uplift Pressure", "i6": "Structure Weight", "i7": "Moments",
        "i8": "Resultant and Eccentricity", "i9": "Safety Checks",
        "i10": "Observations and Conclusions", "i11": "Final Schematic",
        "h1_geo": "1.1 Wall Geometry",
        "h1_solo": "1.2 Soil Properties",
        "h1_fund": "1.3 Foundation Soil",
        "h1_met": "1.4 Method and Friction",
        "h2_parc": "2.1 Applied Partial Factors",
        "h2_val": "2.2 Design Values (Factored)",
        "h9_derr": "9.1 Overturning (EQU)",
        "h9_desl": "9.2 Sliding (STR/GEO)",
        "h9_cap": "9.3 Bearing Capacity (STR/GEO)",
        "h9_detc": "9.4 Bearing Capacity Detail",
        "p_param": "Parameter", "p_simb": "Symbol", "p_val": "Value", "p_uni": "Unit",
        "p_desc": "Description",
        "ok_all": "✅ WALL SATISFIES ALL CHECKS",
        "no_all": "❌ WALL DOES NOT SATISFY — RESIZE",
        "btn": "Print / PDF",
        "footer1": "HYDRAULIC-GEOSTRUCT (GROUP III)",
        "footer2": "EC7 (EN 1997-1) | REBAP (DL 349-C/83) | RSA",
    },
}


def gerar_relatorio_html_muro_gravidade(
    nome, curso, genero, H, B, a, i, gamma_sol, gamma_sat, phi, c_linha, q, z_w,
    metodo, delta, delta_b, combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu, g_Rh, g_Rv,
    phi_d, c_d, delta_d, q_d, Ka, Ia_caract, Ia_d, IaH_d, IaV_d, U_d, W_d, Area_muro,
    M_est_total, M_derr_total, V_d, e, B_linha, Rd_h, tipo_cisalhamento, q_Rd, sigma_max_d,
    ok_derr, ok_desliz, ok_carga, tipo_solo='unico',
    H1=None, H2=None, gamma1=None, gamma1_sat=None, gamma2=None, gamma2_sat=None,
    phi1=None, phi2=None, c1=None, c2=None, Ka1=None, Ka2=None, Ia1_caract=None, Ia2_caract=None,
    gamma_fund=None, gamma_sat_fund=None, phi_fund=None, c_fund=None, cu_fund=None,
    phi_fund_d=None, c_fund_d=None, cu_fund_d=None,
    Nc=None, Nq=None, Ngamma=None, termo_c=None, termo_q=None, termo_gamma=None, q_ult=None,
    x_cg=None, braco_W=None,
    lang="pt", esquema_svg=""
):
    T = TXT.get(lang, TXT["pt"])
    titulo_gen = T["senhor"] if genero == "Masculino" else T["senhora"]
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    tipo_txt = ("Solo Único" if tipo_solo == "unico" else "Solos Estratificados") if lang == "pt" else \
               ("Single Soil" if tipo_solo == "unico" else "Stratified Soils")

    ok_geral = ok_derr and ok_desliz and ok_carga
    status_txt = T["ok_all"] if ok_geral else T["no_all"]
    status_cor = "#28a745" if ok_geral else "#dc3545"

    def box(ok, txt_ok, txt_nok):
        cor = "#28a745" if ok else "#dc3545"
        bg = "#d4edda" if ok else "#f8d7da"
        txt = txt_ok if ok else txt_nok
        return (f'<div style="background:{bg};border-left:6px solid {cor};'
                f'padding:12px;margin:12px 0;border-radius:6px;font-weight:bold;color:{cor};">{txt}</div>')

    p = []
    p.append(f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8"><title>{T["titulo"]}</title>')
    p.append('<script>window.MathJax={tex:{inlineMath:[["$","$"]],displayMath:[["$$","$$"]]},svg:{fontCache:"global"}};</script>')
    p.append('<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>')
    p.append('<style>')
    p.append('@media print{.no-print{display:none}.page-break{page-break-before:always}}')
    p.append('body{font-family:"Segoe UI",sans-serif;line-height:1.6;color:#333;max-width:950px;margin:0 auto;padding:20px;background:#f5f5f5}')
    p.append('.container{background:#fff;padding:40px;box-shadow:0 2px 10px rgba(0,0,0,.1)}')
    p.append('.capa{text-align:center;padding:50px 20px;border-bottom:3px solid #1f77b4;margin-bottom:30px}')
    p.append('.capa h1{color:#1f77b4;font-size:26px}.capa h2{color:#2c3e50;font-size:20px}')
    p.append('h1{color:#1f77b4;border-bottom:3px solid #1f77b4;padding-bottom:8px;margin-top:35px}')
    p.append('h2{color:#2c3e50;border-bottom:2px solid #2c3e50;padding-bottom:6px;margin-top:25px}')
    p.append('table{width:100%;border-collapse:collapse;margin:15px 0;font-size:13px}')
    p.append('th{background:#34495e;color:#fff;padding:10px;border:1px solid #2c3e50;text-align:left}')
    p.append('td{padding:8px 10px;border:1px solid #ddd}tr:nth-child(even){background:#f8f9fa}')
    p.append('.formula-box{background:#f0f8ff;border-left:4px solid #1f77b4;padding:12px 18px;margin:10px 0;border-radius:4px}')
    p.append(f'.resumo-final{{background:{status_cor};color:#fff;padding:18px;border-radius:8px;text-align:center;font-size:17px;font-weight:bold;margin:25px 0}}')
    p.append('.footer{text-align:center;margin-top:30px;padding-top:15px;border-top:2px solid #ddd;color:#666;font-size:11px}')
    p.append('.indice{background:#f8f9fa;padding:15px;border-radius:8px}')
    p.append('.btn-imp{position:fixed;top:15px;right:15px;background:#1f77b4;color:#fff;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;z-index:1000}')
    p.append('</style></head><body>')
    p.append(f'<button class="btn-imp no-print" onclick="window.print()">🖨️ {T["btn"]}</button>')
    p.append('<div class="container">')

    # CAPA
    p.append('<div class="capa">')
    p.append(f'<h1>{T["instituto"]}</h1><h2>{T["grupo"]}</h2><h3>{T["disciplina"]}</h3>')
    p.append(f'<h2 style="margin-top:30px;">{T["titulo"]}</h2>')
    p.append(f'<p><strong>{titulo_gen}:</strong> {nome} | <strong>{T["curso"]}:</strong> {curso}</p>')
    p.append(f'<p><strong>{T["data"]}:</strong> {data_atual} | <strong>{T["combo"]}:</strong> {combo_ec7}</p>')
    p.append(f'<p><em>{tipo_txt}</em></p></div>')

    # ÍNDICE
    p.append(f'<h1>{T["indice"]}</h1><div class="indice"><ol>')
    for k in ["i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9", "i10", "i11"]:
        p.append(f'<li>{T[k]}</li>')
    p.append('</ol></div>')

    # 1. DADOS
    p.append(f'<div class="page-break"></div><h1>1. {T["i1"].upper()}</h1>')
    p.append(f'<h2>{T["h1_geo"]}</h2><table>')
    p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Altura do muro</td><td>$H$</td><td>{H:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>Largura da base</td><td>$B$</td><td>{B:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>Largura do topo</td><td>$a$</td><td>{a:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>Inclinação do terrapleno</td><td>$i$</td><td>{i:.1f}</td><td>°</td></tr></table>')

    # Solo retido
    if tipo_solo == "unico":
        p.append(f'<h2>{T["h1_solo"]}</h2><table>')
        p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
        p.append(f'<tr><td>Peso específico natural</td><td>$\\gamma$</td><td>{gamma_sol:.1f}</td><td>kN/m³</td></tr>')
        p.append(f'<tr><td>Peso específico saturado</td><td>$\\gamma_{{sat}}$</td><td>{gamma_sat:.1f}</td><td>kN/m³</td></tr>')
        p.append(f'<tr><td>Ângulo de atrito</td><td>$\\phi\'$</td><td>{phi:.1f}</td><td>°</td></tr>')
        p.append(f'<tr><td>Coesão efetiva</td><td>$c\'$</td><td>{c_linha:.2f}</td><td>kPa</td></tr>')
        p.append(f'<tr><td>Sobrecarga</td><td>$q$</td><td>{q:.2f}</td><td>kPa</td></tr>')
        p.append(f'<tr><td>Nível freático (da base)</td><td>$z_w$</td><td>{z_w:.2f}</td><td>m</td></tr></table>')
    else:
        p.append(f'<h2>Camada 1</h2><table><tr><th>{T["p_param"]}</th><th>{T["p_val"]}</th></tr>')
        p.append(f'<tr><td>$H_1$</td><td>{H1:.2f} m</td></tr><tr><td>$\\gamma_1$</td><td>{gamma1:.1f}</td></tr>')
        p.append(f'<tr><td>$\\phi\'_1$</td><td>{phi1:.1f}°</td></tr><tr><td>$c\'_1$</td><td>{c1:.2f}</td></tr></table>')
        p.append(f'<h2>Camada 2</h2><table><tr><th>{T["p_param"]}</th><th>{T["p_val"]}</th></tr>')
        p.append(f'<tr><td>$H_2$</td><td>{H2:.2f} m</td></tr><tr><td>$\\gamma_2$</td><td>{gamma2:.1f}</td></tr>')
        p.append(f'<tr><td>$\\phi\'_2$</td><td>{phi2:.1f}°</td></tr><tr><td>$c\'_2$</td><td>{c2:.2f}</td></tr></table>')

    # Solo fundação
    p.append(f'<h2>{T["h1_fund"]}</h2><table>')
    p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Peso específico</td><td>$\\gamma_{{fund}}$</td><td>{gamma_fund:.1f}</td><td>kN/m³</td></tr>')
    p.append(f'<tr><td>Ângulo de atrito</td><td>$\\phi\'_{{fund}}$</td><td>{phi_fund:.1f}</td><td>°</td></tr>')
    p.append(f'<tr><td>Coesão efetiva</td><td>$c\'_{{fund}}$</td><td>{c_fund:.2f}</td><td>kPa</td></tr>')
    p.append(f'<tr><td>Coesão não drenada</td><td>$c_{{u,fund}}$</td><td>{cu_fund:.2f}</td><td>kPa</td></tr>')
    p.append(f'<tr><td>Ângulo de atrito solo-base</td><td>$\\delta_b$</td><td>{delta_b:.1f}</td><td>°</td></tr></table>')

    # Método
    p.append(f'<h2>{T["h1_met"]}</h2><table>')
    p.append(f'<tr><td>Método de cálculo</td><td>{metodo}</td></tr>')
    p.append(f'<tr><td>Ângulo de atrito solo-estrutura</td><td>$\\delta = {delta:.1f}°$</td></tr>')
    p.append(f'<tr><td>Combinação EC7</td><td>{combo_ec7}</td></tr></table>')

    # 2. PARÂMETROS
    p.append(f'<div class="page-break"></div><h1>2. {T["i2"].upper()}</h1>')
    p.append(f'<h2>{T["h2_parc"]}</h2><table>')
    p.append(f'<tr><th>{T["p_desc"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th></tr>')
    p.append(f'<tr><td>Ações permanentes desfavoráveis</td><td>$\\gamma_{{G,unfav}}$</td><td>{g_G_unfav:.2f}</td></tr>')
    p.append(f'<tr><td>Ações permanentes favoráveis</td><td>$\\gamma_{{G,fav}}$</td><td>{g_G_fav:.2f}</td></tr>')
    p.append(f'<tr><td>Ações variáveis</td><td>$\\gamma_Q$</td><td>{g_Q:.2f}</td></tr>')
    p.append(f'<tr><td>Atrito</td><td>$\\gamma_\\phi$</td><td>{g_phi:.2f}</td></tr>')
    p.append(f'<tr><td>Coesão</td><td>$\\gamma_c$</td><td>{g_c:.2f}</td></tr>')
    p.append(f'<tr><td>Coesão não drenada</td><td>$\\gamma_{{cu}}$</td><td>{g_cu:.2f}</td></tr>')
    p.append(f'<tr><td>Resistência ao deslizamento</td><td>$\\gamma_{{Rh}}$</td><td>{g_Rh:.2f}</td></tr>')
    p.append(f'<tr><td>Resistência à capacidade de carga</td><td>$\\gamma_{{Rv}}$</td><td>{g_Rv:.2f}</td></tr></table>')

    p.append(f'<h2>{T["h2_val"]}</h2><div class="formula-box">')
    p.append('$$\\phi\'_d = \\arctan\\!\\left(\\frac{\\tan\\phi\'}{\\gamma_\\phi}\\right) = ' + f"{phi_d:.2f}^\\circ$$")
    p.append('$$c\'_d = \\frac{c\'}{\\gamma_c} = ' + f"{c_d:.2f}" + '\\text{ kPa}$$')
    p.append('$$\\delta_d = \\arctan\\!\\left(\\frac{\\tan\\delta}{\\gamma_\\phi}\\right) = ' + f"{delta_d:.2f}^\\circ$$")
    p.append('$$q_d = q \\cdot \\gamma_Q = ' + f"{q_d:.2f}" + '\\text{ kPa}$$</div>')

    # 3. IMPULSOS
    p.append(f'<div class="page-break"></div><h1>3. {T["i3"].upper()}</h1>')
    if tipo_solo == "unico":
        p.append(f'<div class="formula-box"><strong>Coeficiente de impulso activo (Ka):</strong>')
        if metodo == "Rankine":
            if i > 0:
                # Terrapleno inclinado: K_{a-gamma} inclui o factor cos i
                p.append("$$K_{a\\gamma} = \\frac{\\cos i - "
                         "\\sqrt{\\cos^2 i - \\cos^2 \\phi'_d}}"
                         "{\\cos i + \\sqrt{\\cos^2 i - \\cos^2 \\phi'_d}}"
                         "\\,\\cos i \\qquad ; \\qquad K_{aq} = K_{a\\gamma}$$")
            else:
                p.append("$$K_a = \\frac{1 - \\sin\\phi'_d}{1 + \\sin\\phi'_d}"
                         "\\qquad ; \\qquad K_{aq} = K_a$$")
        else:
            p.append("$$K_{a\\gamma} = \\left[\\frac{\\text{cosec}\\,\\beta\\,"
                     "\\sin(\\beta - \\phi'_d)}{\\sqrt{\\sin(\\beta + \\delta_d)} + "
                     "\\sqrt{\\frac{\\sin(\\phi'_d + \\delta_d)\\sin(\\phi'_d - i)}"
                     "{\\sin(\\beta - i)}}}\\right]^2 \\qquad ; \\qquad "
                     "K_{aq} = K_{a\\gamma}\\cdot\\frac{\\sin\\beta}{\\sin(\\beta - i)}$$")
        p.append(f'</div><p>$$K_a = \\mathbf{{{Ka:.4f}}}$$ &nbsp;({metodo})</p>')
    else:
        p.append(f'<p>$$K_{{a,1}} = {Ka1:.4f} \\quad ; \\quad K_{{a,2}} = {Ka2:.4f}$$</p>')

    # 4. IMPULSOS E COMPONENTES
    p.append(f'<h1>4. {T["i4"].upper()}</h1>')
    p.append(f'<div class="formula-box">$$I_a = \\frac{{1}}{{2}} K_a \\gamma H^2 + K_a q H$$</div>')
    p.append(f'<table><tr><th>{T["p_desc"]}</th><th>{T["p_simb"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Impulso activo característico</td><td>$I_{{a,k}}$</td><td>{Ia_caract:.2f}</td><td>kN/m</td></tr>')
    p.append(f'<tr><td>Impulso activo de cálculo</td><td>$I_{{a,d}}$</td><td><strong>{Ia_d:.2f}</strong></td><td>kN/m</td></tr>')
    p.append(f'<tr><td>Componente horizontal</td><td>$I_{{aH,d}}$</td><td><strong>{IaH_d:.2f}</strong></td><td>kN/m</td></tr>')
    p.append(f'<tr><td>Componente vertical</td><td>$I_{{aV,d}}$</td><td><strong>{IaV_d:.2f}</strong></td><td>kN/m</td></tr></table>')

    # 5. SUBPRESSÃO
    p.append(f'<h1>5. {T["i5"].upper()}</h1>')
    p.append(f'<div class="formula-box">$$U = \\frac{{1}}{{2}} \\gamma_w z_w B$$</div>')
    p.append(f'<p>$U_d = {U_d:.2f}$ kN/m</p>')

    # 6. PESO
    p.append(f'<h1>6. {T["i6"].upper()}</h1>')
    p.append(f'<table><tr><th>{T["p_desc"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Área da secção</td><td>{Area_muro:.2f}</td><td>m²</td></tr>')
    p.append(f'<tr><td>Peso específico do betão</td><td>25.0</td><td>kN/m³</td></tr>')
    p.append(f'<tr><td>Peso de cálculo</td><td><strong>{W_d:.2f}</strong></td><td>kN/m</td></tr>')
    if x_cg is not None:
        p.append(f'<tr><td>Distância do centro de gravidade à face '
                 f'<i>toe</i> (bordo de menor largura)</td>'
                 f'<td>$x_{{cg}}$ = <strong>{x_cg:.3f}</strong></td><td>m</td></tr>')
    if braco_W is not None:
        p.append(f'<tr><td>Braço do peso da estrutura (face <i>heel</i> → '
                 f'linha de acção)</td>'
                 f'<td>$b_W = B - x_{{cg}}$ = <strong>{braco_W:.3f}</strong></td>'
                 f'<td>m</td></tr>')
        p.append(f'<tr><td>Momento do peso da estrutura</td>'
                 f'<td>$M_{{W,d}} = W_d \\cdot b_W$ = <strong>'
                 f'{W_d * braco_W:.2f}</strong></td><td>kNm/m</td></tr>')
    p.append('</table>')
    if x_cg is not None and braco_W is not None:
        p.append(f'<div class="formula-box">$$x_{{cg}} = \\frac{{B^2 + B\\,a + a^2}}'
                 f'{{3(B + a)}} \\qquad ; \\qquad '
                 f'b_W = B - x_{{cg}}$$</div>')

    # 7. MOMENTOS
    p.append(f'<div class="page-break"></div><h1>7. {T["i7"].upper()}</h1>')
    p.append(f'<table><tr><th>{T["p_desc"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Momento estabilizador</td><td><strong>{M_est_total:.2f}</strong></td><td>kNm/m</td></tr>')
    p.append(f'<tr><td>Momento derrubador</td><td><strong>{M_derr_total:.2f}</strong></td><td>kNm/m</td></tr></table>')

    # 8. RESULTANTE
    p.append(f'<h1>8. {T["i8"].upper()}</h1>')
    p.append(f'<div class="formula-box">$$e = \\frac{{B}}{{2}} - \\frac{{M_{{est}} - M_{{derr}}}}{{V_d}}$$</div>')
    p.append(f'<table><tr><th>{T["p_desc"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Força vertical total</td><td>{V_d:.2f}</td><td>kN/m</td></tr>')
    p.append(f'<tr><td>Excentricidade</td><td>{abs(e):.3f}</td><td>m</td></tr>')
    p.append(f'<tr><td>Largura efectiva</td><td>{B_linha:.3f}</td><td>m</td></tr></table>')

    # 9. VERIFICAÇÕES
    p.append(f'<div class="page-break"></div><h1>9. {T["i9"].upper()}</h1>')

    p.append(f'<h2>{T["h9_derr"]}</h2><div class="formula-box">$$M_{{stb,d}} \\geq M_{{dst,d}}$$</div>')
    p.append(f'<p>$M_{{est,d}} = {M_est_total:.2f}$ kNm/m | $M_{{derr,d}} = {M_derr_total:.2f}$ kNm/m</p>')
    p.append(box(ok_derr, "✅ SATISFAZ — M_est,d ≥ M_derr,d",
                 "❌ NÃO SATISFAZ — Redimensionar"))

    p.append(f'<h2>{T["h9_desl"]}</h2><div class="formula-box">')
    p.append('$$H_d \\leq R_d = \\frac{V_d \\tan\\delta_b}{\\gamma_{R;h}}$$</div>')
    p.append(f'<p>$H_d = {IaH_d:.2f}$ | $R_{{d,h}} = {Rd_h:.2f}$ kN/m ({tipo_cisalhamento}) | $R_{{p,d}} = 0$ (desprezado)</p>')
    p.append(box(ok_desliz, "✅ SATISFAZ — R_d,h ≥ H_d",
                 "❌ NÃO SATISFAZ — Aumentar B ou adicionar dente"))

    p.append(f'<h2>{T["h9_cap"]}</h2><div class="formula-box">')
    p.append('$$q_u = c\'N_c + q\'N_q + \\frac{1}{2}\\gamma B\' N_\\gamma \\; ; \\; q_{R,d} = q_u / \\gamma_{R,v}$$</div>')
    p.append(f'<p>$q_{{R,d}} = {q_Rd:.2f}$ kPa | $\\sigma_{{max,d}} = {sigma_max_d:.2f}$ kPa</p>')
    p.append(box(ok_carga, "✅ SATISFAZ — q_R,d ≥ σ_max,d",
                 "❌ NÃO SATISFAZ — Aumentar B ou melhorar solo"))

    # Detalhe capacidade
    if Nc is not None and termo_c is not None:
        q_ult_c = q_ult if q_ult is not None else (termo_c + termo_q + termo_gamma)
        p.append(f'<h2>{T["h9_detc"]}</h2><table>')
        p.append(f'<tr><th>{T["p_desc"]}</th><th>{T["p_val"]}</th></tr>')
        p.append(f'<tr><td>$N_c$</td><td>{Nc:.3f}</td></tr>')
        p.append(f'<tr><td>$N_q$</td><td>{Nq:.3f}</td></tr>')
        p.append(f'<tr><td>$N_\\gamma$</td><td>{Ngamma:.3f}</td></tr>')
        p.append(f'<tr><td>Termo coesão $c\'N_c$</td><td>{termo_c:.2f} kPa</td></tr>')
        p.append(f'<tr><td>Termo sobrecarga $q\'N_q$</td><td>{termo_q:.2f} kPa</td></tr>')
        p.append(f'<tr><td>Termo peso $\\frac{{1}}{{2}}\\gamma B\'N_\\gamma$</td><td>{termo_gamma:.2f} kPa</td></tr>')
        p.append(f'<tr><td><strong>$q_{{ult}}$</strong></td><td><strong>{q_ult_c:.2f} kPa</strong></td></tr>')
        p.append(f'<tr><td><strong>$q_{{R,d}}$</strong></td><td><strong>{q_Rd:.2f} kPa</strong></td></tr></table>')

    # 10. CONCLUSÃO
    p.append(f'<div class="page-break"></div><h1>10. {T["i10"].upper()}</h1>')
    p.append(f'<div class="resumo-final">{status_txt}</div>')

    # 11. ESQUEMA
    if esquema_svg:
        p.append(f'<div class="page-break"></div><h1>11. {T["i11"].upper()}</h1>')
        p.append(esquema_svg)

    p.append(f'<div class="footer"><p>{T["footer1"]} — {T["instituto"]}</p>')
    p.append(f'<p>{T["footer2"]}</p><p>{data_atual}</p></div>')
    p.append('</div></body></html>')

    return "\n".join(p).encode("utf-8")