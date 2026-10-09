"""Relatório HTML bilingue (PT/EN) com MathJax — Muro em Consola / Contrafortes."""
from datetime import datetime


TXT = {
    "pt": {
        "titulo": "RELATÓRIO TÉCNICO — MURO EM CONSOLA",
        "instituto": "INSTITUTO SUPERIOR POLITÉCNICO DE SONGO",
        "grupo": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
        "disciplina": "Muros de Contenção e Fundações Superficiais",
        "indice": "ÍNDICE",
        "senhor": "Senhor", "senhora": "Senhora",
        "curso": "Curso", "data": "Data", "combo": "Combinação EC7",
        "i1": "Geometria e Dados de Entrada",
        "i2": "Acções e Impulsos (EC7)",
        "i3": "Verificações Geotécnicas (EC7)",
        "i4": "Materiais (REBAP)",
        "i5": "Dimensionamento das Armaduras (REBAP)",
        "i6": "Conclusão",
        "p_param": "Parâmetro", "p_val": "Valor", "p_uni": "Unidade",
        "ok_all": "✅ MURO SATISFAZ TODAS AS VERIFICAÇÕES",
        "no_all": "❌ MURO NÃO SATISFAZ — REDIMENSIONAR",
        "btn": "Imprimir / PDF",
        "footer1": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
        "footer2": "EC7 (EN 1997-1) | REBAP (DL 349-C/83) | RSA",
    },
    "en": {
        "titulo": "TECHNICAL REPORT — CANTILEVER WALL",
        "instituto": "SONGO POLYTECHNIC INSTITUTE",
        "grupo": "HYDRAULIC-GEOSTRUCT (GROUP III)",
        "disciplina": "Retaining Walls and Shallow Foundations",
        "indice": "CONTENTS",
        "senhor": "Mr.", "senhora": "Mrs.",
        "curso": "Course", "data": "Date", "combo": "EC7 Combination",
        "i1": "Geometry and Input Data",
        "i2": "Actions and Thrusts (EC7)",
        "i3": "Geotechnical Checks (EC7)",
        "i4": "Materials (REBAP)",
        "i5": "Reinforcement Design (REBAP)",
        "i6": "Conclusion",
        "p_param": "Parameter", "p_val": "Value", "p_uni": "Unit",
        "ok_all": "✅ WALL SATISFIES ALL CHECKS",
        "no_all": "❌ WALL DOES NOT SATISFY — RESIZE",
        "btn": "Print / PDF",
        "footer1": "HYDRAULIC-GEOSTRUCT (GROUP III)",
        "footer2": "EC7 (EN 1997-1) | REBAP (DL 349-C/83) | RSA",
    },
}


def gerar_relatorio_html_muro_consola(
    nome, curso, genero, H, HR, D, B, bt, bh, ts, tb, i,
    gamma_ativo, gamma_sat_ativo, phi_ativo, c_ativo, q_ativo, z_w_ativo,
    gamma_passivo, gamma_sat_passivo, phi_passivo, c_passivo, z_w_passivo,
    gamma_fund, gamma_sat_fund, phi_fund, c_fund, cu_fund, delta_b,
    metodo, delta, combo_ec7, g_G_unfav, g_G_fav, g_Q, g_phi, g_c, g_cu,
    g_Rh, g_Rv, phi_ativo_d, phi_passivo_d, phi_fund_d,
    c_ativo_d, c_passivo_d, c_fund_d, cu_fund_d, delta_d, q_d,
    Ka, Kp, Ia_ativo_caract, Ia_ativo_d, IaH_d, IaV_d,
    Ip_passivo_caract, Rpd_d, W_stem_d, W_base_d,
    W_solo_talao_d, W_solo_biqueira_d, W_total_d,
    M_est_total, M_derr_total, V_d, e, B_linha, Rd_h,
    tipo_cisalhamento, q_Rd, sigma_max_d,
    ok_derr, ok_desliz, ok_carga, classe_betao, tipo_aco, recobrimento,
    fck, fcd, fctd, fyk, fsyd,
    M_stem_d, d_stem, As_stem_final, M_talao_d, M_biqueira_d,
    d_base, As_talao_final, As_biqueira_final,
    V_stem_d, VRd_stem, ok_corte_stem, D_passivo,
    V_talao_d=0.0, V_biqueira_d=0.0,
    tabela_armaduras_html="", verificacoes_html="",
    diagramas_html="", lang="pt", **kwargs
):
    T = TXT.get(lang, TXT["pt"])
    titulo_gen = T["senhor"] if genero == "Masculino" else T["senhora"]
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # --- Brazos das forças verticais (medidos a partir do bordo "toe") ---
    # x_cg do conjunto betao (stem + base): x_cg = (W_stem*x_stem + W_base*x_base)/W_total
    x_stem = bt + ts / 2.0                 # centro do stem
    x_base = B / 2.0                        # centro da base
    W_conc = (W_stem_d or 0.0) + (W_base_d or 0.0)
    if W_conc > 1e-9:
        x_cg = ((W_stem_d or 0.0) * x_stem + (W_base_d or 0.0) * x_base) / W_conc
    else:
        x_cg = B / 2.0
    braco_W = B - x_cg                      # braco do peso da estrutura
    braco_stem = x_stem
    braco_base = x_base

    ok_geral = ok_derr and ok_desliz and ok_carga
    status_txt = T["ok_all"] if ok_geral else T["no_all"]
    status_cor = "#28a745" if ok_geral else "#dc3545"

    def box(ok, txt_ok, txt_nok):
        cor = "#28a745" if ok else "#dc3545"
        bg = "#d4edda" if ok else "#f8d7da"
        return (f'<div style="background:{bg};border-left:6px solid {cor};'
                f'padding:12px;margin:12px 0;border-radius:6px;'
                f'font-weight:bold;color:{cor};">{txt_ok if ok else txt_nok}</div>')

    p = []
    p.append(f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">')
    p.append(f'<title>{T["titulo"]}</title>')
    p.append('<script>window.MathJax={tex:{inlineMath:[["$","$"]],'
             'displayMath:[["$$","$$"]]},svg:{fontCache:"global"}};</script>')
    p.append('<script id="MathJax-script" async '
             'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>')
    p.append('<style>')
    p.append('@media print{.no-print{display:none}.page-break{page-break-before:always}}')
    p.append('body{font-family:"Segoe UI",sans-serif;line-height:1.6;color:#222;'
             'max-width:960px;margin:0 auto;padding:20px;background:#f5f5f5}')
    p.append('.container{background:#fff;padding:40px;box-shadow:0 2px 10px rgba(0,0,0,.1)}')
    p.append('.capa{text-align:center;padding:40px 20px;border-bottom:3px solid #1f77b4;margin-bottom:30px}')
    p.append('.capa h1{color:#1f77b4;font-size:24px}.capa h2{color:#2c3e50;font-size:18px}')
    p.append('h1{color:#1f77b4;border-bottom:3px solid #1f77b4;padding-bottom:8px;margin-top:35px}')
    p.append('h2{color:#2c3e50;border-bottom:2px solid #2c3e50;padding-bottom:6px;margin-top:25px}')
    p.append('table{width:100%;border-collapse:collapse;margin:15px 0;font-size:13px}')
    p.append('th{background:#34495e;color:#fff;padding:8px;border:1px solid #2c3e50;text-align:left}')
    p.append('td{padding:7px 8px;border:1px solid #ddd}tr:nth-child(even){background:#f8f9fa}')
    p.append('.formula-box{background:#f0f8ff;border-left:4px solid #1f77b4;'
             'padding:12px 18px;margin:10px 0;border-radius:4px;overflow-x:auto}')
    p.append(f'.status-final{{background:{status_cor};color:#fff;padding:18px;'
             'border-radius:8px;text-align:center;font-size:17px;font-weight:bold;margin:25px 0}')
    p.append('.btn-imp{position:fixed;top:15px;right:15px;background:#1f77b4;color:#fff;'
             'border:none;padding:10px 20px;border-radius:8px;cursor:pointer;z-index:1000}')
    p.append('.footer{text-align:center;margin-top:30px;padding-top:15px;'
             'border-top:2px solid #ddd;color:#666;font-size:11px}')
    p.append('.indice{background:#f8f9fa;padding:15px;border-radius:8px}')
    p.append('.artigo-ref{background:#e8f4f8;padding:8px 12px;'
             'border-left:3px solid #1f77b4;margin:10px 0;font-size:12px}')
    p.append('svg{display:block;margin:10px auto;max-width:100%}')
    p.append('</style></head><body>')
    p.append(f'<button class="btn-imp no-print" onclick="window.print()">🖨️ {T["btn"]}</button>')
    p.append('<div class="container">')

    # CAPA
    p.append('<div class="capa">')
    p.append(f'<h1>{T["instituto"]}</h1><h2>{T["grupo"]}</h2><h3>{T["disciplina"]}</h3>')
    p.append(f'<h2 style="margin-top:30px;">{T["titulo"]}</h2>')
    p.append(f'<p><strong>{titulo_gen}:</strong> {nome} | <strong>{T["curso"]}:</strong> {curso}</p>')
    p.append(f'<p><strong>{T["data"]}:</strong> {data_atual} | <strong>{T["combo"]}:</strong> {combo_ec7}</p></div>')

    # ÍNDICE
    p.append(f'<h1>{T["indice"]}</h1><div class="indice"><ol>')
    for k in ["i1", "i2", "i3", "i4", "i5", "i6"]:
        p.append(f'<li>{T[k]}</li>')
    p.append('</ol></div>')

    # 1. GEOMETRIA
    p.append(f'<div class="page-break"></div><h1>1. {T["i1"].upper()}</h1>')
    p.append(f'<table><tr><th>{T["p_param"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>H (total height)</td><td>{H:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>H_R (retained height)</td><td>{HR:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>B (base)</td><td>{B:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>b_t (toe)</td><td>{bt:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>b_h (heel)</td><td>{bh:.2f}</td><td>m</td></tr>')
    p.append(f'<tr><td>t_s (stem)</td><td>{ts*100:.0f}</td><td>cm</td></tr>')
    p.append(f'<tr><td>t_b (base)</td><td>{tb*100:.0f}</td><td>cm</td></tr>')
    p.append(f'<tr><td>i (slope)</td><td>{i:.1f}</td><td>°</td></tr>')
    p.append(f'<tr><td>$\\gamma$ / $\\phi\'$ / $c\'$ (active)</td>'
             f'<td>{gamma_ativo:.1f} / {phi_ativo:.1f} / {c_ativo:.1f}</td>'
             f'<td>kN/m³ / ° / kPa</td></tr>')
    p.append(f'<tr><td>$\\gamma$ / $\\phi\'$ / $c\'$ / $c_u$ (found.)</td>'
             f'<td>{gamma_fund:.1f} / {phi_fund:.1f} / {c_fund:.1f} / {cu_fund:.1f}</td>'
             f'<td>kN/m³ / ° / kPa / kPa</td></tr>')
    p.append(f'<tr><td>q (surcharge)</td><td>{q_ativo:.2f}</td><td>kPa</td></tr>')
    p.append(f'<tr><td>$\\delta_b$</td><td>{delta_b:.1f}</td><td>°</td></tr></table>')

    # 2. IMPULSOS
    p.append(f'<div class="page-break"></div><h1>2. {T["i2"].upper()}</h1>')
    p.append('<h2>2.1 ' + ('Coeficiente de Impulso Activo' if lang == 'pt' else 'Active Earth Pressure Coefficient') + f' — {metodo}</h2>')
    p.append('<div class="formula-box">')
    if metodo == "Rankine":
        p.append(r"$$K_{a\gamma} = \frac{\cos i - \sqrt{\cos^2 i - \cos^2 \phi'_d}}{\cos i + \sqrt{\cos^2 i - \cos^2 \phi'_d}}\cos i$$")
    else:
        p.append(r"$$K_{a\gamma} = \left[\frac{\mathrm{cosec}\,\beta\,\sin(\beta-\phi'_d)}{\sqrt{\sin(\beta+\delta_d)} + \sqrt{\frac{\sin(\phi'_d+\delta_d)\,\sin(\phi'_d-i)}{\sin(\beta-i)}}}\right]^2$$")
        p.append(r"$$K_{aq} = K_{a\gamma}\cdot\frac{\sin\beta}{\sin(\beta-i)}$$")
    p.append(f'</div><p><strong>$K_a = {Ka:.4f}$</strong></p>')

    p.append('<h2>2.2 ' + ('Impulso Activo' if lang == 'pt' else 'Active Thrust') + '</h2>')
    p.append('<div class="formula-box">')
    p.append(r'$$I_a = \tfrac{1}{2}K_a\,\gamma\,{h^{\prime\prime}}^2 + K_{aq}\,q_d\,h^{\prime\prime}$$</div>')
    p.append('<table>')
    p.append(f'<tr><td>$I_{{a,k}}$</td><td>{Ia_ativo_caract:.2f}</td><td>kN/m</td></tr>')
    p.append(f'<tr><td>$I_{{a,d}}$</td><td><strong>{Ia_ativo_d:.2f}</strong></td><td>kN/m</td></tr>')
    p.append(f'<tr><td>$I_{{aH,d}}$</td><td><strong>{IaH_d:.2f}</strong></td><td>kN/m</td></tr>')
    p.append(f'<tr><td>$I_{{aV,d}}$</td><td><strong>{IaV_d:.2f}</strong></td><td>kN/m</td></tr></table>')

    p.append('<h2>2.3 ' + ('Pesos e Momentos' if lang == 'pt' else 'Weights and Moments') + '</h2><table>')
    p.append(f'<tr><td>$W_{{total,d}}$</td><td>{W_total_d:.2f}</td><td>kN/m</td></tr>')
    if braco_W is not None:
        p.append(f'<tr><td>' + ('Braço do peso da estrutura (bordo da base → '
                                 'linha de acção)'
                                 if lang == "pt" else
                                 'Lever arm of structure weight (base edge → '
                                 'line of action)') +
                 f'</td><td>$b_W = B - x_{{cg}}$ = <strong>{braco_W:.3f}</strong></td>'
                 f'<td>m</td></tr>')
        if W_stem_d:
            p.append(f'<tr><td>' + ('Braço do peso do stem'
                                     if lang == "pt" else 'Lever arm of stem weight') +
                     f'</td><td>$b_{{stem}} = b_t + \\tfrac{{t_s}}{{2}}$ = '
                     f'<strong>{braco_stem:.3f}</strong></td><td>m</td></tr>')
            p.append(f'<tr><td>' + ('Momento do peso do stem'
                                     if lang == "pt" else 'Moment of stem weight') +
                     f'</td><td>$M_{{stem,d}} = W_{{stem,d}} \\cdot b_{{stem}}$ = '
                     f'<strong>{W_stem_d * braco_stem:.2f}</strong></td>'
                     f'<td>kNm/m</td></tr>')
        if W_base_d:
            p.append(f'<tr><td>' + ('Braço do peso da base'
                                     if lang == "pt" else 'Lever arm of base weight') +
                     f'</td><td>$b_{{base}} = \\tfrac{{B}}{{2}}$ = '
                     f'<strong>{braco_base:.3f}</strong></td><td>m</td></tr>')
            p.append(f'<tr><td>' + ('Momento do peso da base'
                                     if lang == "pt" else 'Moment of base weight') +
                     f'</td><td>$M_{{base,d}} = W_{{base,d}} \\cdot b_{{base}}$ = '
                     f'<strong>{W_base_d * braco_base:.2f}</strong></td>'
                     f'<td>kNm/m</td></tr>')
        p.append(f'<tr><td>' + ('Momento total do peso da estrutura'
                                 if lang == "pt" else
                                 'Total moment of structure weight') +
                 f'</td><td>$M_{{W,d}} = W_{{total,d}} \\cdot b_W$ = '
                 f'<strong>{W_total_d * braco_W:.2f}</strong></td>'
                 f'<td>kNm/m</td></tr>')
    p.append(f'<tr><td>$M_{{est}}$</td><td>{M_est_total:.2f}</td><td>kNm/m</td></tr>')
    p.append(f'<tr><td>$M_{{derr}}$</td><td>{M_derr_total:.2f}</td><td>kNm/m</td></tr>')
    p.append(f'<tr><td>$V_d$</td><td>{V_d:.2f}</td><td>kN/m</td></tr>')
    p.append(f'<tr><td>$e$</td><td>{abs(e):.3f}</td><td>m</td></tr>')
    p.append(f'<tr><td>$B\'$</td><td>{B_linha:.3f}</td><td>m</td></tr></table>')
    if braco_W is not None:
        p.append(f'<div class="formula-box">$$b_W = B - x_{{cg}} \\qquad ; '
                 f'\\qquad b_{{stem}} = b_t + \\frac{{t_s}}{{2}} \\qquad ; '
                 f'\\qquad b_{{base}} = \\frac{{B}}{{2}}$$</div>')

    # 3. VERIFICAÇÕES
    p.append(f'<div class="page-break"></div><h1>3. {T["i3"].upper()}</h1>')
    p.append('<h2>3.1 ' + ('Derrubamento' if lang == 'pt' else 'Overturning') + ' (EQU)</h2>')
    p.append('<div class="formula-box">$$M_{stb,d} \\geq M_{dst,d}$$</div>')
    p.append(box(ok_derr,
                 f'✅ {M_est_total:.2f} ≥ {M_derr_total:.2f} kNm/m',
                 f'❌ {M_est_total:.2f} < {M_derr_total:.2f} kNm/m'))

    p.append('<h2>3.2 ' + ('Deslizamento' if lang == 'pt' else 'Sliding') + ' (STR/GEO)</h2>')
    p.append('<div class="formula-box">$$H_d \\leq R_d = \\frac{V_d\\tan\\delta_b}{\\gamma_{R;h}}$$</div>')
    p.append(box(ok_desliz,
                 f'✅ R_d = {Rd_h:.2f} ≥ H_d = {IaH_d:.2f} kN/m',
                 f'❌ R_d = {Rd_h:.2f} < H_d = {IaH_d:.2f} kN/m'))

    p.append('<h2>3.3 ' + ('Capacidade de Carga' if lang == 'pt' else 'Bearing Capacity') + ' (STR/GEO)</h2>')
    p.append('<div class="formula-box">$$q_u = c\'N_c + q\'N_q + \\tfrac{1}{2}\\gamma B\' N_\\gamma\\;;\\;q_{R,d}=q_u/\\gamma_{R,v}$$</div>')
    p.append(box(ok_carga,
                 f'✅ q_R,d = {q_Rd:.2f} ≥ σ_max = {sigma_max_d:.2f} kPa',
                 f'❌ q_R,d = {q_Rd:.2f} < σ_max = {sigma_max_d:.2f} kPa'))

    # 4. MATERIAIS
    p.append(f'<div class="page-break"></div><h1>4. {T["i4"].upper()}</h1><table>')
    p.append(f'<tr><th>{T["p_param"]}</th><th>{T["p_val"]}</th><th>{T["p_uni"]}</th></tr>')
    p.append(f'<tr><td>Concrete {classe_betao}: $f_{{ck}}/f_{{cd}}/f_{{ctd}}$</td>'
             f'<td>{fck:.1f} / {fcd:.2f} / {fctd:.2f}</td><td>MPa</td></tr>')
    p.append(f'<tr><td>Steel {tipo_aco}: $f_{{yk}}/f_{{syd}}$</td>'
             f'<td>{fyk:.1f} / {fsyd:.2f}</td><td>MPa</td></tr>')
    p.append(f'<tr><td>Cover</td><td>{recobrimento}</td><td>mm</td></tr></table>')

    # 5. ARMADURAS
    p.append(f'<div class="page-break"></div><h1>5. {T["i5"].upper()}</h1>')
    p.append('<h2>5.1 ' + ('Flexão Simples' if lang == 'pt' else 'Simple Bending') + ' (Art. 52 REBAP)</h2>')
    p.append('<div class="formula-box">$$\\mu = \\frac{M_{Ed}}{b\\,d^2 f_{cd}}\\;\\;;\\;\\omega = \\mu(1+\\mu)\\;\\;;\\;A_s = \\frac{\\omega\\,b\\,d\\,f_{cd}}{f_{syd}}$$</div>')
    p.append('<h2>5.2 ' + ('Esforço Transverso' if lang == 'pt' else 'Shear Force') + ' (Art. 53 REBAP)</h2>')
    p.append('<div class="formula-box">$$V_{Rd} = \\eta\\,\\tau_1\\,d\\,b_1\\;\\;;\\;\\eta = \\max(1.0,\\,1.6-d)$$</div>')
    p.append('<h2>5.3 ' + ('Amarração' if lang == 'pt' else 'Anchorage') + ' (Art. 80 REBAP)</h2>')
    p.append('<div class="formula-box">$$l_b = \\frac{\\phi}{4}\\cdot\\frac{f_{syd}}{f_{bd}}\\;\\;;\\;l_{b,net} = l_b\\cdot\\frac{A_{s,cal}}{A_{s,ef}}\\geq l_{b,min}$$</div>')
    p.append('<h2>5.4 ' + ('Tabela-resumo' if lang == 'pt' else 'Summary table') + '</h2>')
    p.append(tabela_armaduras_html)
    p.append('<div class="artigo-ref">Unidades: Msd kNm/m | Vsd kN/m | As cm²/m. '
             'Art. 52, 53, 90, 104, 105, 108, Tabela 48 REBAP.</div>')
    if verificacoes_html:
        p.append(f'<h2>5.5 Verificações</h2>{verificacoes_html}')
    p.append('<h2>5.6 ' + ('Diagramas' if lang == 'pt' else 'Diagrams') + '</h2>')
    p.append(diagramas_html)

    # 6. CONCLUSÃO
    p.append(f'<div class="page-break"></div><h1>6. {T["i6"].upper()}</h1>')
    p.append(f'<div class="status-final">{status_txt}</div>')
    p.append(f'<div class="footer"><p>{T["footer1"]} — {T["instituto"]}</p>')
    p.append(f'<p>{T["footer2"]}</p><p>{data_atual}</p></div>')
    p.append('</div></body></html>')

    return "\n".join(p).encode("utf-8")