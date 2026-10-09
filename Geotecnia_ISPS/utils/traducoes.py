"""
Sistema de traduções para Português e Inglês
"""

TRADUCOES = {
    "pt": {
        # --- CAPA E MENU ---
        "titulo_instituto": "INSTITUTO SUPERIOR POLITÉCNICO DE SONGO",
        "titulo_grupo": "HYDRAULIC-GEOSTRUCT (GRUPO III)",
        "titulo_disciplina": "Muros de Contenção e Fundações Superficiais",
        "subtitulo_relatorio": "RELATÓRIO TÉCNICO DE DIMENSIONAMENTO",
        "bem_vindo": "Seja Bem-Vindo",
        "senhor": "Senhor",
        "senhora": "Senhora",
        "que_estrutura": "Que estrutura pretende dimensionar?",
        "muros_contencao": "Muros de Contenção",
        "sapatas_rigidas": "Sapatas Rígidas",
        "fundações_superficiais": "Fundações Superficiais (Tensões, Excentricidade, etc.)",
        "gravidade": "Gravidade",
        "consola": "Consola",
        "contrafortes": "Contrafortes",
        
        # --- SIDEBAR E NAVEGAÇÃO ---
        "pag_inicial": "🏠 Pag. Inicial",
        "guiao_uso": "📖 Guião de Uso",
        "suporte": "📞 Suporte Técnico",
        "voltar_menu": " Voltar ao Menu Principal",
        
        # --- FORMULÁRIOS GERAIS ---
        "caixa_entrada": "📝 Caixa de Entrada",
        "nome": "1. Qual é o seu Nome Completo?",
        "curso": "Curso que frequenta",
        "genero": "3. Género:",
        "masculino": "Masculino",
        "feminino": "Feminino",
        "entrar": "Entrar no Programa 🚀",
        
        # --- MUROS ---
        "modulo_muros": "🧱 Módulo de Muros de Contenção",
        "selecione_tipo": "Selecione o tipo de muro:",
        "selecione_solo": "Selecione o tipo de solo:",
        "solo_unico": " Solo Único",
        "solos_estratificados": "🟫 Solos Estratificados",
        
        # --- GEOMETRIA ---
        "geometria": "📐 Geometria do Muro",
        "altura_muro": "Altura do muro H [m]",
        "largura_base": "Largura da base B [m]",
        "largura_topo": "Largura do topo a [m]",
        "inclinacao_terrapleno": "Inclinação do terrapleno i [°]",
        
        # --- SOLO ---
        "solo_retido": "🟫 Solo Retido (Ativo) - Acima da Base",
        "solo_fundacao": "🟫 Solo de Fundação (Abaixo da Base)",
        "peso_especifico": "Peso específico natural γ [kN/m³]",
        "peso_saturado": "Peso específico saturado γ_sat [kN/m³]",
        "angulo_atrito": "Ângulo de atrito interno φ' [°]",
        "coesao_efetiva": "Coesão efetiva c' [kPa]",
        "coesao_nao_drenada": "Coesão não drenada Cu [kPa]",
        "sobrecarga": "Sobrecarga no terrapleno q [kPa]",
        "nivel_freatico": "Altura do Nível Freático a partir da base [m] (0 = sem água)",
        
        # --- MÉTODO ---
        "metodo_calculo": "🔢 Método de Cálculo do Impulso",
        "metodo": "Método:",
        "rankine": "Rankine",
        "coulomb": "Coulomb",
        "angulo_atrito_estrutura": "Ângulo de atrito solo-estrutura δ [°]",
        "angulo_atrito_base": "Ângulo de atrito solo-base δb [°]",
        
        # --- EC7 ---
        "abordagem_ec7": "⚖️ Abordagem de Cálculo (EC7 - DA1)",
        "combinacao": "Selecione a Combinação de Cálculo:",
        "combinacao1": "Combinação 1 (A1 + M1 + R1)",
        "combinacao2": "Combinação 2 (A2 + M2 + R1) - *Recomendada*",
        "calcular_geotecnica": "Calcular e Verificar Geotécnica (EC7)",
        
        # --- RESULTADOS ---
        "resultados": "📊 Resultados",
        "valores_calculo": "📋 Valores de Cálculo (EC7 - Pág. 79)",
        "coeficiente_impulso": " Coeficiente de Impulso Ativo",
        "impulso_ativo": "💪 Cálculo do Impulso Ativo",
        "subpressao": "💧 Subpressão na Base",
        "peso_estrutura": "️ Peso da Estrutura",
        "momentos": "🔄 Momentos",
        "resultante_excentricidade": "📍 Resultante e Excentricidade",
        "verificacoes": "🔍 Verificações de Segurança (EC7)",
        
        # --- VERIFICAÇÕES ---
        "derrubamento": "Derrubamento (EQU)",
        "deslizamento": "Deslizamento",
        "capacidade_carga": "Capacidade de Carga (STR/GEO)",
        "satisfaz": "✅ SATISFAZ",
        "nao_satisfaz": "❌ NÃO SATISFAZ",
        "muro_satisfaz": "🎉 **MURO SATISFAZ TODAS AS VERIFICAÇÕES SEGUNDO O EC7!**",
        "muro_nao_satisfaz": "️ **O MURO NÃO SATISFAZ TODAS AS VERIFICAÇÕES. REDIMENSIONAR.**",
        
        # --- RELATÓRIO ---
        "exportar_relatorio": "📄 Exportar Relatório Técnico",
        "descarregar_relatorio": "📥 Descarregar Relatório HTML",
        "converter_pdf": "💡 **Como converter para PDF:** Abra o HTML no navegador → Ctrl+P → 'Salvar como PDF'",
        
        # --- FÓRMULAS LATEX ---
        "formula_phi_d": r"\phi'_d = \arctan\left(\frac{\tan(\phi')}{\gamma_\phi}\right)",
        "formula_delta_d": r"\delta_d = \arctan\left(\frac{\tan(\delta)}{\gamma_\phi}\right)",
        "formula_ka_rankine": r"K_a = \frac{1 - \sin(\phi'_d)}{1 + \sin(\phi'_d)}",
        "formula_ka_rankine_inclinado": r"K_{a\gamma} = \frac{\cos i - \sqrt{\cos^2 i - \cos^2\phi'_d}}{\cos i + \sqrt{\cos^2 i - \cos^2\phi'_d}}\,\cos i \quad ; \quad K_{aq} = K_{a\gamma}",
        "formula_ka_coulomb": r"K_a = \frac{\cos^2(\phi'_d - \alpha)}{\cos^2(\alpha) \cdot \cos(\alpha + \delta_d) \left[1 + \sqrt{\frac{\sin(\phi'_d + \delta_d) \cdot \sin(\phi'_d - i)}{\cos(\alpha + \delta_d) \cdot \cos(\alpha - i)}}\right]^2}",
        "formula_impulso": r"I_a = \frac{1}{2} K_a \gamma H^2 + K_a q H",
        "formula_subpressao": r"U = \frac{1}{2} \gamma_w z_w B",
        "formula_excentricidade": r"e = \frac{B}{2} - \frac{M_{est} - M_{derr}}{V_d}",
        "formula_largura_efetiva": r"B' = B - 2|e|",
        "formula_deslizamento_drenado": r"R_{d,h} = \frac{V_d \cdot \tan(\delta_b)}{\gamma_{Rh}}",
        "formula_deslizamento_nao_drenado": r"R_{d,h} = \frac{c_u \cdot B'}{\gamma_{Rh}}",
        "formula_capacidade_carga": r"q_{R,d} = \frac{c' N_c + q' N_q + 0.5 \gamma B' N_\gamma}{\gamma_{Rv}}",
        "altura_muro_lbl": "Altura do muro",
        "altura_total": "Altura total",
        "lbl_largura_base": "Largura da base",
        "lbl_largura_topo": "Largura do topo",
        "lbl_inclinacao": "Inclinação do terrapleno",
        "lbl_gamma": "Peso específico natural",
        "lbl_gamma_sat": "Peso específico saturado",
        "lbl_phi": "Ângulo de atrito interno",
        "lbl_c": "Coesão efetiva",
        "lbl_q": "Sobrecarga no terrapleno",
        "lbl_cu": "Coesão não drenada",
        "lbl_delta_b": "Ângulo de atrito solo-base",
        "nivel_freatico_lbl": "Altura do Nível Freático a partir da base",
        "lbl_altura_camada": "Altura da camada",
        "unidade_m": "m",
        "unidade_graus": "°",
        "unidade_knm3": "kN/m³",
        "unidade_kpa": "kPa",
        "sufixo_fund": "(Fundação)",
        
        # --- LEGENDA E MENSAGENS ---
        "legenda": "Legenda",
        "info_rankine": "ℹ️ Rankine: δ = 0°",
        "info_delta_b": "ℹ️ δb é o atrito na interface base da sapata / solo de fundação",
        "info_gamma_sat": "ℹ️ O peso específico saturado só será usado na zona abaixo do nível freático",
        "dentro_nucleo": "✅ e ≤ B/6 ({B6:.3f} m) → Resultante dentro do núcleo central",
        "fora_nucleo": "⚠️ e > B/6 ({B6:.3f} m) → Resultante fora do núcleo central",
        "forca_negativa": "⚠️ Força vertical negativa! Redimensionar!",
        
                # ============ MURO EM CONSOLA ============
        "consola_dados": "Muro em Consola — Dados de Entrada",
        "consola_ec7": "1. Abordagem de Cálculo (EC7 - DA1)",
        "consola_geom": "2. Geometria",
        "consola_solo_ativo": "3. Solo Retido (Lado ACTIVO)",
        "consola_solo_fund": "4. Solo de Fundação",
        "consola_metodo": "5. Método de Impulso",
        "consola_materiais": "6. Materiais (REBAP)",
        "consola_btn_geo": "🧮 Calcular e Verificar Geotecnia (EC7)",
        "consola_btn_arm": "⚙️ Prosseguir com Armaduras (REBAP)",
        "consola_btn_voltar_geo": "↩️ Voltar ao Cálculo Geotécnico",
        "consola_res_geo": "Resultados — Muro em Consola (EC7)",
        "consola_pesos": "Pesos",
        "consola_momentos": "Momentos e Resultante",
        "consola_verif": "Verificações (EC7)",
        "consola_estrutura": "Estrutura do Muro",
        "consola_esquema_final": "Esquema Final",
        "consola_dim_arm": "Dimensionamento Estrutural (REBAP)",
        "consola_stem": "Stem (Fuste)",
        "consola_bh": "Talão (bh)",
        "TALAO": "Talão",
        "BETÃO": "Betão",
        "consola_bt": "Biqueira (bt)",
        "consola_face_sup": "Superior",
        "consola_face_inf": "Inferior",
        "consola_face_dir": "Direita",
        "consola_face_esq": "Esquerda",
        "consola_pormenor": "Pormenorização",
        "consola_diagramas": "Diagramas das Lajes",
        "consola_tabela_arm": "Tabela-resumo de Armaduras",

        # Fórmulas LaTeX — Consola
        "formula_alpha_coulomb": r"\alpha = 45^\circ + \frac{\phi'_d}{2} + \frac{1}{2}\left[\arcsin\!\left(\frac{\sin i}{\sin\phi'_d}\right) - i\right]",
        "formula_ka_coulomb_consola": r"K_{a\gamma} = \left[\frac{\mathrm{cosec}\,\beta\,\sin(\beta-\phi'_d)}{\sqrt{\sin(\beta+\delta_d)} + \sqrt{\frac{\sin(\phi'_d+\delta_d)\,\sin(\phi'_d-i)}{\sin(\beta-i)}}}\right]^2",
        "formula_kaq_coulomb": r"K_{aq} = K_{a\gamma}\cdot\frac{\sin\beta}{\sin(\beta-i)}",
        "formula_impulso_consola": r"I_a = \tfrac{1}{2}K_a\,\gamma\,{h''}^2 + K_{aq}\,q_d\,h''",
        "formula_flexao": r"\mu = \frac{M_{Ed}}{b\,d^2 f_{cd}}\;;\;\omega = \mu(1+\mu)\;;\;A_s = \frac{\omega\,b\,d\,f_{cd}}{f_{syd}}",
        "formula_VRd_corte": r"V_{Rd} = \eta\,\tau_1\,d\,b_1 \quad;\quad \eta = \max(1.0,\,1.6-d)",
        "formula_amarracao": r"l_b = \frac{\phi}{4}\cdot\frac{f_{syd}}{f_{bd}}\;;\;l_{b,net} = l_b\cdot\frac{A_{s,cal}}{A_{s,ef}}\geq l_{b,min}",

        # ============ MURO COM CONTRAFORTES ============
        "cf_dados": "Muro com Contrafortes — Dados de Entrada",
        "cf_geom": "2. Geometria (Picture5)",
        "cf_b1": "b1 — Consola 2 [m]",
        "cf_b2": "b2 — Base do stem [m]",
        "cf_b3": "b3 — Consola 1 [m]",
        "cf_t": "t — Topo do paramento [m]",
        "cf_H": "H — Altura total [m]",
        "cf_hc": "hc — Altura do contraforte [m]",
        "cf_hb": "hb — Espessura da base [m]",
        "cf_B_calc": "B = b1 + b2 + b3 = {b1:.2f} + {b2:.2f} + {b3:.2f} = **{B:.2f} m** (bloqueado)",
        "cf_erro_hc": "hc deve ser ≤ H − hb.",
        "cf_erro_t": "t deve ser ≤ b2.",
        "cf_solo_ativo": "3. Solo Retido (lado ACTIVO)",
        "cf_solo_fund": "4. Solo de Fundação",
        "cf_materiais": "5. Materiais (REBAP)",
        "cf_btn": "🧮 Calcular e Verificar (EC7, Rankine)",
        "cf_res": "Resultados — Muro com Contrafortes (EC7, Rankine)",
        "cf_pesos": "Pesos (o contraforte contribui favoravelmente)",
        "cf_verif": "Verificações (EC7)",
        "cf_esquema": "Esquema da Estrutura",
        "cf_dim_arm": "Dimensionamento Estrutural (REBAP) — Consola 1, Consola 2 e Paramento",
        "cf_paramento": "Paramento Vertical",
        "cf_consola1": "Consola 1",
        "cf_consola2": "Consola 2 (inclui peso do contraforte)",
        "cf_graficos": "Gráficos das Três Peças",
        "cf_tabela_pecas": "Tabela-resumo das Peças",
        
        "cf_momentos": "Momentos, Resultante e Excentricidade",
        "cf_b1": "b1 — Consola 2 (frente) [m]",
        "cf_b3": "b3 — Consola 1 (talão) [m]",
        "cf_sobrecarga": "Sobrecarga no terrapleno q [kPa]",
        "cf_info_sem_agua": "ℹ️ O nível freático não é considerado no lado activo (não entra em nenhum cálculo).",
                
        
        # --- TABELAS ---
        "parametros_minorados": "**Parâmetros minorados:**",
        "resultados_finais": "**Resultados:**",
        "parametro": "Parâmetro",
        "valor": "Valor",
        "grandeza": "Grandeza",
        "unidade": "Unidade",
        "simbolo": "Símbolo",
        "formula": "Fórmula",
        "valor_caracteristico": "Valor Característico",
        "valor_calculo": "Valor de Cálculo",


        # --- SAPATAS ---
        "modulo_sapatas": "📐 Módulo de Sapatas Rígidas",
        "sap_tipo": "Tipo de sapata",
        "sap_homotetica": "Homotética",
        "sap_bordos": "Bordos Equidistantes",
        "sap_quadrada": "Quadrada",
        "sap_proporcionada": "Proporcionada",
        "sap_dimensoes": "Dimensões e Acções",
        "sap_solo": "Solo e Fundação",
        "sap_calcular": "🧮 Calcular e Verificar",
        "sap_resultados": "📊 Resultados do Dimensionamento",
        
        # --- SAPATAS ---
        "modulo_sapatas": "📐 Módulo de Sapatas Rígidas",
        "em_desenvolvimento": " Em desenvolvimento.",

        # ---TOQUES FINAIS ---
         "espessura_base": "Espessura da base",
        "comprimento_biqueira": "Comprimento da biqueira",
        "comprimento_talao": "Comprimento do talão",
        "espessura_stem": "Espessura do stem",
        "verificacao_b": "B = {bt:.2f} + {ts:.2f} + {bh:.2f} = {B:.2f} m",
        "verificacao_hr": "HR = H − tb = {H:.2f} − {D:.2f} = {HR:.2f} m",
        "erro_d": "HR = H − tb deve ser ≥ 0.1 m.",
        "classe_betao": "Classe do betão",
        "tipo_aco": "Tipo de aço",
        "recobrimento": "Recobrimento nominal",
        "consola_legenda_corpo": "H = Altura total | HR = H − tb | B = bt + ts + bh | bt = Biqueira | bh = Talão | ts = Espessura do stem | tb = Espessura da base",
        "stem": "Stem (Fuste)",
        "unidade_mm": "mm",
        
    },
    
    "en": {
        # --- COVER AND MENU ---
        "titulo_instituto": "SONGO POLYTECHNIC INSTITUTE",
        "titulo_grupo": "HYDRAULIC-GEOSTRUCT (GROUP III)",
        "titulo_disciplina": "Retaining Walls and Shallow Foundations",
        "subtitulo_relatorio": "TECHNICAL DESIGN REPORT",
        "bem_vindo": "Welcome",
        "senhor": "Mr.",
        "senhora": "Mrs.",
        "que_estrutura": "Which structure do you want to design?",
        "muros_contencao": "Retaining Walls",
        "sapatas_rigidas": "Rigid Footings",
        "fundações_superficiais": "Shallow Foundations (Stresses, Eccentricity, etc.)",
        "gravidade": "Gravity",
        "consola": "Cantilever",
        "contrafortes": "Counterfort",
        
        # --- SIDEBAR AND NAVIGATION ---
        "pag_inicial": "🏠 Home Page",
        "guiao_uso": "📖 User Guide",
        "suporte": "📞 Technical Support",
        "voltar_menu": " Back to Main Menu",
        
        # --- GENERAL FORMS ---
        "caixa_entrada": "📝 Entry Box",
        "nome": "1. What is your Full Name?",
        "curso": "2. Course you attend:",
        "genero": "3. Gender:",
        "masculino": "Male",
        "feminino": "Female",
        "entrar": "Enter Program 🚀",
        
        # --- WALLS ---
        "modulo_muros": "🧱 Retaining Walls Module",
        "selecione_tipo": "Select wall type:",
        "selecione_solo": "Select soil type:",
        "solo_unico": "🟫 Single Soil",
        "solos_estratificados": "🟫 Stratified Soils",
        
        # --- GEOMETRY ---
        "geometria": "📐 Wall Geometry",
        "altura_muro": "Wall height H [m]",
        "largura_base": "Base width B [m]",
        "largura_topo": "Top width a [m]",
        "inclinacao_terrapleno": "Backfill slope i [°]",
        
        # --- SOIL ---
        "solo_retido": "🟫 Retained Soil (Active) - Above Base",
        "solo_fundacao": "🟫 Foundation Soil (Below Base)",
        "peso_especifico": "Natural unit weight γ [kN/m³]",
        "peso_saturado": "Saturated unit weight γ_sat [kN/m³]",
        "angulo_atrito": "Internal friction angle φ' [°]",
        "coesao_efetiva": "Effective cohesion c' [kPa]",
        "coesao_nao_drenada": "Undrained cohesion Cu [kPa]",
        "sobrecarga": "Backfill surcharge q [kPa]",
        "nivel_freatico": "Water table height from base [m] (0 = no water)",
        
        # --- METHOD ---
        "metodo_calculo": "🔢 Earth Pressure Calculation Method",
        "metodo": "Method:",
        "rankine": "Rankine",
        "coulomb": "Coulomb",
        "angulo_atrito_estrutura": "Soil-structure friction angle δ [°]",
        "angulo_atrito_base": "Soil-base friction angle δb [°]",
        
        # --- EC7 ---
        "abordagem_ec7": "⚖️ Calculation Approach (EC7 - DA1)",
        "combinacao": "Select Calculation Combination:",
        "combinacao1": "Combination 1 (A1 + M1 + R1)",
        "combinacao2": "Combination 2 (A2 + M2 + R1) - *Recommended*",
        "calcular_geotecnica": "Calculate and Check Geotechnical (EC7)",
        
        # --- RESULTS ---
        "resultados": "📊 Results",
        "valores_calculo": "📋 Design Values (EC7 - Page 79)",
        "coeficiente_impulso": "📐 Active Earth Pressure Coefficient",
        "impulso_ativo": "💪 Active Earth Pressure Calculation",
        "subpressao": "💧 Base Uplift Pressure",
        "peso_estrutura": "️ Structure Weight",
        "momentos": "🔄 Moments",
        "resultante_excentricidade": "📍 Resultant and Eccentricity",
        "verificacoes": " Safety Checks (EC7)",
        
        # --- CHECKS ---
        "derrubamento": "Overturning (EQU)",
        "deslizamento": "Sliding",
        "capacidade_carga": "Bearing Capacity (STR/GEO)",
        "satisfaz": "✅ SATISFIES",
        "nao_satisfaz": "❌ DOES NOT SATISFY",
        "muro_satisfaz": "🎉 **WALL SATISFIES ALL CHECKS ACCORDING TO EC7!**",
        "muro_nao_satisfaz": "️ **WALL DOES NOT SATISFY ALL CHECKS. RESIZE.**",
        
        # --- REPORT ---
        "exportar_relatorio": " Export Technical Report",
        "descarregar_relatorio": "📥 Download HTML Report",
        "converter_pdf": "💡 **How to convert to PDF:** Open HTML in browser → Ctrl+P → 'Save as PDF'",
        
        # --- LATEX FORMULAS ---
        "formula_phi_d": r"\phi'_d = \arctan\left(\frac{\tan(\phi')}{\gamma_\phi}\right)",
        "formula_delta_d": r"\delta_d = \arctan\left(\frac{\tan(\delta)}{\gamma_\phi}\right)",
                "formula_ka_rankine_inclinado": r"K_{a\gamma} = \frac{\cos i - \sqrt{\cos^2 i - \cos^2\phi'_d}}{\cos i + \sqrt{\cos^2 i - \cos^2\phi'_d}}\,\cos i \quad ; \quad K_{aq} = K_{a\gamma}",
        "formula_ka_rankine": r"K_a = \frac{1 - \sin(\phi'_d)}{1 + \sin(\phi'_d)} \quad ; \quad K_{aq} = K_a",
        "formula_ka_coulomb": r"K_a = \frac{\sin^2(\beta + \phi'_d)}{\sin^2(\beta)\,\sin(\beta - \delta_d)\left[1 + \sqrt{\frac{\sin(\phi'_d + \delta_d)\,\sin(\phi'_d - i)}{\sin(\beta - \delta_d)\,\sin(\beta + i)}}\right]^2}\,,\;\beta = 90^\circ",
        "formula_impulso": r"I_a = \frac{1}{2} K_a \gamma H^2 + K_a q H",
        "formula_subpressao": r"U = \frac{1}{2} \gamma_w z_w B",
        "formula_excentricidade": r"e = \frac{B}{2} - \frac{M_{est} - M_{derr}}{V_d}",
        "formula_largura_efetiva": r"B' = B - 2|e|",
        "formula_deslizamento_drenado": r"R_{d,h} = \frac{V_d \cdot \tan(\delta_b)}{\gamma_{Rh}}",
        "formula_deslizamento_nao_drenado": r"R_{d,h} = \frac{c_u \cdot B'}{\gamma_{Rh}}",
        "formula_capacidade_carga": r"q_{R,d} = \frac{c' N_c + q' N_q + 0.5 \gamma B' N_\gamma}{\gamma_{Rv}}",
        "altura_muro_lbl": "Wall height",
        "altura_total": "Total height",
        "lbl_largura_base": "Base width",
        "lbl_largura_topo": "Top width",
        "lbl_inclinacao": "Backfill slope",
        "lbl_gamma": "Natural unit weight",
        "lbl_gamma_sat": "Saturated unit weight",
        "lbl_phi": "Internal friction angle",
        "lbl_c": "Effective cohesion",
        "lbl_q": "Backfill surcharge",
        "lbl_cu": "Undrained cohesion",
        "lbl_delta_b": "Soil-base friction angle",
        "nivel_freatico_lbl": "Water table height above base",
        "lbl_altura_camada": "Layer height",
        "unidade_m": "m",
        "unidade_graus": "°",
        "unidade_knm3": "kN/m³",
        "unidade_kpa": "kPa",
        "sufixo_fund": "(Foundation)",
        
        # --- LEGEND AND MESSAGES ---
        "legenda": "Legend",
        "altura":  "Height",
        "info_rankine": "ℹ️ Rankine: δ = 0°",
        "info_delta_b": "ℹ️ δb is the friction at the footing base / foundation soil interface",
        "info_gamma_sat": "ℹ️ Saturated unit weight is only used below the water table",
        "dentro_nucleo": "✅ e ≤ B/6 ({B6:.3f} m) → Resultant within the kern",
        "fora_nucleo": "⚠️ e > B/6 ({B6:.3f} m) → Resultant outside the kern",
        "forca_negativa": "⚠️ Negative vertical force! Resize!",
        
                # ============ CANTILEVER WALL ============
        "consola_dados": "Cantilever Wall — Input Data",
        "consola_ec7": "1. Calculation Approach (EC7 - DA1)",
        "consola_geom": "2. Geometry",
        "consola_solo_ativo": "3. Retained Soil (ACTIVE side)",
        "consola_solo_fund": "4. Foundation Soil",
        "consola_metodo": "5. Earth Pressure Method",
        "consola_materiais": "6. Materials (REBAP)",
        "consola_btn_geo": "🧮 Calculate and Check Geotechnics (EC7)",
        "consola_btn_arm": "⚙️ Proceed with Reinforcement (REBAP)",
        "consola_btn_voltar_geo": "↩️ Back to Geotechnical Calculation",
        "consola_res_geo": "Results — Cantilever Wall (EC7)",
        "consola_pesos": "Weights",
        "consola_momentos": "Moments and Resultant",
        "consola_verif": "Checks (EC7)",
        "consola_estrutura": "Wall Structure",
        "consola_esquema_final": "Final Schematic",
        "consola_dim_arm": "Structural Design (REBAP)",
        "consola_stem": "Stem",
        "consola_bh": "Heel (bh)",
        "TALAO": "Heel",
        "BETÃO": "Concrete",
        "consola_bt": "Toe (bt)",
        "consola_face_sup": "Top",
        "consola_face_inf": "Bottom",
        "consola_face_dir": "Right",
        "consola_face_esq": "Left",
        "consola_pormenor": "Detailing",
        "consola_diagramas": "Slab Diagrams",
        "consola_tabela_arm": "Reinforcement Summary Table",

        "cf_momentos": "Moments, Resultant and Eccentricity",
        "cf_b1": "b1 — Cantilever 2 (front) [m]",
        "cf_b3": "b3 — Cantilever 1 (heel) [m]",
        "cf_sobrecarga": "Backfill surcharge q [kPa]",
        "cf_info_sem_agua": "ℹ️ Water table is not considered on the active side (not used in any calculation).",

        # LaTeX — Cantilever
        "formula_alpha_coulomb": r"\alpha = 45^\circ + \frac{\phi'_d}{2} + \frac{1}{2}\left[\arcsin\!\left(\frac{\sin i}{\sin\phi'_d}\right) - i\right]",
        "formula_ka_coulomb_consola": r"K_{a\gamma} = \left[\frac{\mathrm{cosec}\,\beta\,\sin(\beta-\phi'_d)}{\sqrt{\sin(\beta+\delta_d)} + \sqrt{\frac{\sin(\phi'_d+\delta_d)\,\sin(\phi'_d-i)}{\sin(\beta-i)}}}\right]^2",
        "formula_kaq_coulomb": r"K_{aq} = K_{a\gamma}\cdot\frac{\sin\beta}{\sin(\beta-i)}",
        "formula_impulso_consola": r"I_a = \tfrac{1}{2}K_a\,\gamma\,{h''}^2 + K_{aq}\,q_d\,h''",
        "formula_flexao": r"\mu = \frac{M_{Ed}}{b\,d^2 f_{cd}}\;;\;\omega = \mu(1+\mu)\;;\;A_s = \frac{\omega\,b\,d\,f_{cd}}{f_{syd}}",
        "formula_VRd_corte": r"V_{Rd} = \eta\,\tau_1\,d\,b_1 \quad;\quad \eta = \max(1.0,\,1.6-d)",
        "formula_amarracao": r"l_b = \frac{\phi}{4}\cdot\frac{f_{syd}}{f_{bd}}\;;\;l_{b,net} = l_b\cdot\frac{A_{s,cal}}{A_{s,ef}}\geq l_{b,min}",

        # ============ COUNTERFORT WALL ============
        "cf_dados": "Counterfort Wall — Input Data",
        "cf_geom": "2. Geometry (Picture5)",
        "cf_b1": "b1 — Cantilever 2 [m]",
        "cf_b2": "b2 — Stem base [m]",
        "cf_b3": "b3 — Cantilever 1 [m]",
        "cf_t": "t — Stem top [m]",
        "cf_H": "H — Total height [m]",
        "cf_hc": "hc — Counterfort height [m]",
        "cf_hb": "hb — Base thickness [m]",
        "cf_B_calc": "B = b1 + b2 + b3 = {b1:.2f} + {b2:.2f} + {b3:.2f} = **{B:.2f} m** (locked)",
        "cf_erro_hc": "hc must be ≤ H − hb.",
        "cf_erro_t": "t must be ≤ b2.",
        "cf_solo_ativo": "3. Retained Soil (ACTIVE side)",
        "cf_solo_fund": "4. Foundation Soil",
        "cf_materiais": "5. Materials (REBAP)",
        "cf_btn": "🧮 Calculate and Check (EC7, Rankine)",
        "cf_res": "Results — Counterfort Wall (EC7, Rankine)",
        "cf_pesos": "Weights (counterfort contributes favorably)",
        "cf_verif": "Checks (EC7)",
        "cf_esquema": "Structure Schematic",
        "cf_dim_arm": "Structural Design (REBAP) — Cantilever 1, Cantilever 2 and Stem",
        "cf_paramento": "Vertical Stem",
        "cf_consola1": "Cantilever 1",
        "cf_consola2": "Cantilever 2 (includes counterfort weight)",
        "cf_graficos": "Diagrams of the Three Elements",
        "cf_tabela_pecas": "Summary Table of Elements",

# ============ LATEX FORMULAS — CANTILEVER ============
"formula_ka_coulomb_consola": r"K_{a\gamma}^{LS;EL}=\left[\frac{\mathrm{cosec}\,\beta\,\sin(\beta-\phi')}{\sqrt{\sin(\beta+\delta)}+\sqrt{\frac{\sin(\phi'+\delta)\,\sin(\phi'-i)}{\sin(\beta-i)}}}\right]^2",
"formula_kaq_coulomb": r"K_{aq}^{LS;EL}=K_{a\gamma}^{LS;EL}\cdot\frac{\sin\beta}{\sin(\beta-i)}",
"formula_alpha_coulomb": r"\alpha = 45^\circ + \frac{\phi'_d}{2} + \frac{1}{2}\left[\arcsin\!\left(\frac{\sin i}{\sin\phi'_d}\right) - i\right]",
"formula_impulso_consola": r"I_a = \tfrac{1}{2}K_a\gamma h''^2 + K_{aq}\,q_d\,h''",
"formula_VRd_corte": r"V_{Rd} = \eta\,\tau_1\,d\,b_1 \quad;\quad \eta = 1.6-d",
"formula_flexao": r"\mu = \frac{M_{Ed}}{b\,d^2 f_{cd}}\;;\;\omega = \mu(1+\mu)\;;\;A_s = \frac{\omega\,b\,d\,f_{cd}}{f_{syd}}",
"formula_amarracao": r"l_b = \frac{\phi}{4}\cdot\frac{f_{syd}}{f_{bd}}\;;\;l_{b,net} = l_b\cdot\frac{A_{s,cal}}{A_{s,ef}}\geq l_{b,min}",
"formula_tensao_punco": r"\tau_{sd} = \frac{V_{sd,ef}}{u\cdot d}\leq \tau_{rd}=(1.6-d)\tau_1",
        
        # --- TABLES ---
        "parametros_minorados": "**Design parameters (factored):**",
        "resultados_finais": "**Results:**",
        "parametro": "Parameter",
        "valor": "Value",
        "grandeza": "Quantity",
        "unidade": "Unit",
        "simbolo": "Symbol",
        "formula": "Formula",
        "valor_caracteristico": "Characteristic Value",
        "valor_calculo": "Design Value",

        "modulo_sapatas": "📐 Rigid Footings Module",
        "sap_tipo": "Footing type",
        "sap_homotetica": "Homothetic",
        "sap_bordos": "Equal edges",
        "sap_quadrada": "Square",
        "sap_proporcionada": "Proportioned",
        "sap_dimensoes": "Dimensions and Actions",
        "sap_solo": "Soil and Foundation",
        "sap_calcular": "🧮 Calculate and Verify",
        "sap_resultados": "📊 Design Results",
        
        # --- FOOTINGS ---
        "modulo_sapatas": "📐 Rigid Footings Module",
        "em_desenvolvimento": " Under development.",

        # --- FINAL TRANSLATES THAT WAS MISSING ---
        "Esquema Final do Muro": "Final Scheme of the Wall",
        "ESQUEMA FINAL — MURO DE GRAVIDADE (Solo Único)" :  "FINAL SCHEME — GRAVITY WALL (Single Soil)",
        "Topo" : "Top",
        "espessura_base": "Base thickness",
        "comprimento_biqueira": "Toe length",
        "comprimento_talao": "Heel length",
        "espessura_stem": "Stem thickness",
        "verificacao_b": "B = {bt:.2f} + {ts:.2f} + {bh:.2f} = {B:.2f} m",
        "verificacao_hr": "HR = H − tb = {H:.2f} − {D:.2f} = {HR:.2f} m",
        "erro_d": "HR = H − tb must be ≥ 0.1 m.",
        "classe_betao": "Concrete class",
        "tipo_aco": "Steel type",
        "recobrimento": "Nominal cover",
        "consola_legenda_corpo": "H = Total height | HR = H − tb | B = bt + ts + bh | bt = Toe | bh = Heel | ts = Stem thickness | tb = Base thickness",
        "stem": "Stem",
        "unidade_mm": "mm",
     
    }
}

def get_text(key, lang="pt", **kwargs):
    """
    Obtém texto traduzido a partir do dicionário TRADUCOES.
    Suporta formatação de strings com kwargs (ex: {B6:.3f}).
    """
    # Obtém o dicionário do idioma selecionado, ou fallback para 'pt'
    lang_dict = TRADUCOES.get(lang, TRADUCOES["pt"])
    
    # Obtém o texto, ou a própria chave se não existir (para facilitar depuração)
    text = lang_dict.get(key, key)
    
    # Se houver argumentos de formatação, aplica-os
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            # Se falhar a formatação, retorna o texto original sem formatar
            pass
            
    return text