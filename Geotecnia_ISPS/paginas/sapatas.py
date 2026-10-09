"""Sapatas Rígidas — UI com LaTeX em designações, símbolos e equações."""

import math


import streamlit as st

try:
    from paginas import sapatas_desenho as SD
except Exception:
    try:
        from . import sapatas_desenho as SD
    except Exception:
        import sapatas_desenho as SD

try:
    from calculos import relatorios_sapatas as RS
except Exception:
    RS = None
from utils.traducoes import get_text

def ir_para_menu():
    """Volta ao menu de escolha da estrutura (Muros / Sapatas)."""
    st.session_state.pagina_atual = "menu_escolha"
    st.rerun()
# =============================================================================
# Tabelas de materiais
# =============================================================================
FCD_MPA = {"B15": 8.0, "B20": 10.7, "B25": 13.3, "B30": 16.7,
           "B35": 20.0, "B40": 23.3, "B45": 26.7, "B50": 30.0, "B55": 33.3}
FCTD_MPA = {"B15": 0.80, "B20": 0.93, "B25": 1.07, "B30": 1.20,
            "B35": 1.33, "B40": 1.47}
FY_MPA = {"A235": 235.0, "A400": 400.0, "A500": 500.0, "A500NR": 500.0}
TAU1_MPA = {"B16": 0.50, "B20": 0.60, "B25": 0.65, "B30": 0.75}
RHO_MIN = {"A235": 0.0025, "A400": 0.0015, "A500": 0.0012, "A500NR": 0.0012}
NOMINAL_BAR_DIAMETER_MM = 10.0


# =============================================================================
# Helpers matemáticos
# =============================================================================
def _ceil_step(x, step=0.05):
    return math.ceil((x - 1e-12) / step) * step

def _positive(x, floor=1e-9):
    return max(float(x), floor)

def fcd(classe):     return FCD_MPA.get(classe, 13.3)
def fctd(classe):    return FCTD_MPA.get(classe, 1.07)
def fy(tipo_aco):    return FY_MPA.get(tipo_aco, 400.0)
def fsyd(tipo_aco):  return fy(tipo_aco) / 1.15
def tau1(classe):    return TAU1_MPA.get(classe, 0.65)
def rho_min(tipo_aco): return RHO_MIN.get(tipo_aco, 0.0015)


# =============================================================================
# Meyerhof — slides 49–55
# =============================================================================
def meyerhof_factors_N(phi_deg):
    phi = math.radians(phi_deg)
    if abs(phi) < 1e-12:
        return 5.14, 1.0, 0.0
    Nq = math.exp(math.pi * math.tan(phi)) * math.tan(math.pi / 4 + phi / 2) ** 2
    Nc = (Nq - 1.0) / math.tan(phi)
    Ng = 2.0 * (Nq + 1.0) * math.tan(phi)
    return Nc, Nq, Ng

def meyerhof_shape_factors(B_eff, L_eff, phi_deg):
    B_eff = _positive(B_eff); L_eff = _positive(L_eff)
    ratio = min(B_eff, L_eff) / max(B_eff, L_eff)
    Nc, Nq, _ = meyerhof_factors_N(phi_deg)
    phi = math.radians(phi_deg)
    Fcs = 1.0 + ratio * (Nq / Nc if Nc else 0.0)
    Fqs = 1.0 + ratio * math.tan(phi)
    Fgs = 1.0 - 0.4 * ratio
    return Fcs, Fqs, Fgs

def meyerhof_depth_factors(Df, B_original, phi_deg):
    B_original = _positive(B_original); Df = max(float(Df), 0.0)
    phi = math.radians(phi_deg)
    Nc, _, _ = meyerhof_factors_N(phi_deg)
    x = Df / B_original
    if x <= 1.0:
        Fqd = 1.0 + 2.0 * math.tan(phi) * (1.0 - math.sin(phi)) ** 2 * x
    else:
        Fqd = 1.0 + 2.0 * math.tan(phi) * (1.0 - math.sin(phi)) ** 2 * math.atan(x)
    Fcd = 1.0 if abs(phi) < 1e-12 else Fqd - (1.0 - Fqd) / (Nc * math.tan(phi))
    return Fcd, Fqd, 1.0

def meyerhof_inclination_factors(beta_deg, phi_deg):
    beta = max(0.0, float(beta_deg)); phi = float(phi_deg)
    if beta <= 1e-12:
        return 1.0, 1.0, 1.0
    Fci = (1.0 - beta / 90.0) ** 2
    Fqi = Fci
    Fgi = 0.0 if phi <= 1e-12 else max(0.0, (1.0 - beta / phi) ** 2)
    return max(0.0, Fci), max(0.0, Fqi), Fgi

def water_adjusted_q_and_gamma(gamma, gamma_sat, Df, WT, gamma_w=9.81):
    gamma = float(gamma); gamma_sat = float(gamma_sat)
    Df = max(float(Df), 0.0); WT = float(WT)
    if WT <= 0.0 or WT >= Df:
        return gamma * Df, gamma
    gamma_sub = max(gamma_sat - gamma_w, 0.0)
    q = gamma * WT + gamma_sub * (Df - WT)
    return q, gamma_sub

def meyerhof_capacity(Bx, By, Df, c, phi_deg, gamma, q, ex=0.0, ey=0.0,
                      B2_ratio=None, L2_ratio=None, gamma_term=None, beta_deg=0.0):
    Bx = _positive(Bx); By = _positive(By)
    ex = abs(float(ex)); ey = abs(float(ey))
    eta_x = ex / Bx; eta_y = ey / By
    case, warnings = "centrada", []
    B_eff, L_eff = Bx, By
    if ex > 1e-9 and ey <= 1e-9:
        case = "excentricidade em uma direcção — área efectiva"
        B_eff = Bx - 2.0 * ex; L_eff = By
    elif ey > 1e-9 and ex <= 1e-9:
        case = "excentricidade em uma direcção — área efectiva"
        B_eff = Bx; L_eff = By - 2.0 * ey
    elif ex > 1e-9 and ey > 1e-9:
        if eta_x < 1.0/6.0 and eta_y < 1.0/6.0 and B2_ratio is not None and L2_ratio is not None:
            case = "Caso IV — Highter & Anders / slide 78"
            B2 = Bx * float(B2_ratio); L2 = By * float(L2_ratio)
            A_eff = By * B2 + 0.5 * (Bx + B2) * (By - L2)
            B_eff = A_eff / By; L_eff = By
        else:
            case = "biaxial — área efectiva do slide 78 não fechada"
            warnings.append("Ler B2/B e L2/L no ábaco do slide 78.")
            return {"ok": False, "qu": None, "A_eff": None, "B_eff": None, "L_eff": None,
                    "case": case, "warnings": warnings}
    if min(B_eff, L_eff) <= 0:
        warnings.append("Área efectiva inválida.")
        return {"ok": False, "qu": None, "A_eff": None, "B_eff": None, "L_eff": None,
                "case": case, "warnings": warnings}
    Nc, Nq, Ng = meyerhof_factors_N(phi_deg)
    Fcs, Fqs, Fgs = meyerhof_shape_factors(B_eff, L_eff, phi_deg)
    Fcd, Fqd, Fgd = meyerhof_depth_factors(Df, min(Bx, By), phi_deg)
    Fci, Fqi, Fgi = meyerhof_inclination_factors(beta_deg, phi_deg)
    if gamma_term is None: gamma_term = gamma
    termo_c = float(c) * Nc * Fcs * Fcd * Fci
    termo_q = float(q) * Nq * Fqs * Fqd * Fqi
    termo_g = 0.5 * float(gamma_term) * B_eff * Ng * Fgs * Fgd * Fgi
    qu = termo_c + termo_q + termo_g
    return {"ok": True, "qu": qu, "A_eff": B_eff * L_eff, "B_eff": B_eff, "L_eff": L_eff,
            "case": case, "warnings": warnings, "Nc": Nc, "Nq": Nq, "Ngamma": Ng,
            "Fcs": Fcs, "Fqs": Fqs, "Fgs": Fgs, "Fcd": Fcd, "Fqd": Fqd, "Fgd": Fgd,
            "Fci": Fci, "Fqi": Fqi, "Fgi": Fgi,
            "termo_c": termo_c, "termo_q": termo_q, "termo_g": termo_g}


# =============================================================================
# Pré-dimensionamento, tensões, estrutural, punçoamento, amarração
# (funções internas — só cálculo, sem UI)
# =============================================================================
def pre_dimensionar(tipo, bx, by, P, Mx, My, sigma_adm, weight_pct=0.10):
    bx = _positive(bx); by = _positive(by); P = float(P)
    Nr = P * (1.0 + weight_pct)
    ex = abs(float(Mx)) / _positive(Nr)
    ey = abs(float(My)) / _positive(Nr)
    sig = _positive(sigma_adm)
    if tipo == "quadrada": a, b = 0.0, 1.0
    elif tipo == "homotetica": a, b = 0.0, bx / by
    elif tipo == "bordos_equidistantes": a, b = (bx - by) / 2.0, 1.0
    elif tipo == "proporcionada": a, b = ex - ey, 1.0
    else: raise ValueError("Tipo de sapata inválido.")
    radical = (a + ey * b - ex) ** 2 + b * Nr / sig
    if radical < 0: raise ValueError("Radicando negativo.")
    By = (-a + ey * b + ex + math.sqrt(radical)) / b
    Bx = By * b + 2.0 * a
    Bx = max(Bx, bx + 0.05); By = max(By, by + 0.05)
    return {"Bx": _ceil_step(Bx), "By": _ceil_step(By), "Nr": Nr, "ex": ex, "ey": ey,
            "a": a, "b": b}

def stresses(Nr, Mx, My, Bx, By):
    Nr = float(Nr); Mx = float(Mx); My = float(My)
    Bx = _positive(Bx); By = _positive(By)
    ex = Mx / _positive(Nr); ey = My / _positive(Nr)
    eta_x = abs(ex) / Bx; eta_y = abs(ey) / By
    base = Nr / (Bx * By)
    inside = eta_x + eta_y <= 1.0/6.0 + 1e-12
    sig1 = base * (1 + 6*abs(ex)/Bx + 6*abs(ey)/By)
    sig2 = base * (1 + 6*abs(ex)/Bx - 6*abs(ey)/By)
    sig3 = base * (1 - 6*abs(ex)/Bx + 6*abs(ey)/By)
    sig4 = base * (1 - 6*abs(ex)/Bx - 6*abs(ey)/By)
    if not inside and abs(Mx) > 1e-9 and abs(My) <= 1e-9:
        a = Bx - 2*abs(ex)
        sigma_max = 4.0/3.0 * Nr / (a * By) if a > 0 else float("inf")
        sig1 = sig2 = sigma_max; sig3 = sig4 = 0.0
        zone = "fora_x"; sigma_min = 0.0; sigma_ref = sigma_max
    elif not inside and abs(My) > 1e-9 and abs(Mx) <= 1e-9:
        a = By - 2*abs(ey)
        sigma_max = 4.0/3.0 * Nr / (a * Bx) if a > 0 else float("inf")
        sig1 = sig4 = sigma_max; sig2 = sig3 = 0.0
        zone = "fora_y"; sigma_min = 0.0; sigma_ref = sigma_max
    elif inside:
        zone = "dentro"
        sigma_min = min(sig1, sig2, sig3, sig4)
        sigma_max = max(sig1, sig2, sig3, sig4)
        sigma_ref = (sigma_max + sigma_min) / 2.0
    else:
        zone = "montoya"
        sigma_min = min(sig1, sig2, sig3, sig4)
        sigma_max = max(sig1, sig2, sig3, sig4)
        sigma_ref = sigma_max
    return {"Nr": Nr, "ex": ex, "ey": ey, "eta_x": eta_x, "eta_y": eta_y,
            "sigma1": sig1, "sigma2": sig2, "sigma3": sig3, "sigma4": sig4,
            "sigma_max": sigma_max, "sigma_min": sigma_min, "sigma_med": base,
            "sigma_ref": sigma_ref, "inside_kern": inside, "zona": zone}

def rigid_footing_design(Bx, By, bx, by, cover_mm, trial_phi_mm=NOMINAL_BAR_DIAMETER_MM):
    a_x = (Bx - bx) / 2.0; a_y = (By - by) / 2.0
    amax = max(a_x, a_y)
    d_rigid_min = amax / 2.0
    d_target = max(2.0 * amax / 3.0, d_rigid_min)
    h = d_target + cover_mm/1000.0 + trial_phi_mm/2000.0
    h = max(h, max((Bx-bx)/4.0, (By-by)/4.0))
    h = _ceil_step(h, 0.05)
    d = h - cover_mm/1000.0 - trial_phi_mm/2000.0
    return {"a_x": a_x, "a_y": a_y, "a_max": amax, "h": h, "d_trial": d,
            "rigid": d >= d_rigid_min - 1e-9}

def console_moments(Bx, By, bx, by, Nr, Mx, My, sigma_max):
    q0 = Nr/(Bx*By)
    ex = Mx/Nr if abs(Nr) > 1e-12 else 0.0
    ey = My/Nr if abs(Nr) > 1e-12 else 0.0
    lx = (Bx-bx)/2.0 + 0.15*bx
    ly = (By-by)/2.0 + 0.15*by
    xs = bx/2.0 - 0.15*bx; xe = Bx/2.0
    qxs = q0*(1.0 + 12.0*ex*xs/(Bx**2)); qxe = q0*(1.0 + 12.0*ex*xe/(Bx**2))
    qxs_m = q0*(1.0 - 12.0*ex*xs/(Bx**2)); qxe_m = q0*(1.0 - 12.0*ex*xe/(Bx**2))
    sigma_ref_x = max((qxs+qxe)/2.0, (qxs_m+qxe_m)/2.0)
    ys = by/2.0 - 0.15*by; ye = By/2.0
    qys = q0*(1.0 + 12.0*ey*ys/(By**2)); qye = q0*(1.0 + 12.0*ey*ye/(By**2))
    qys_m = q0*(1.0 - 12.0*ey*ys/(By**2)); qye_m = q0*(1.0 - 12.0*ey*ye/(By**2))
    sigma_ref_y = max((qys+qye)/2.0, (qys_m+qye_m)/2.0)
    return {"lx": lx, "ly": ly, "sigma_ref_x": sigma_ref_x, "sigma_ref_y": sigma_ref_y,
            "MEd_x": sigma_ref_x * lx**2 / 2.0, "MEd_y": sigma_ref_y * ly**2 / 2.0,
            "warning": ""}

def flexural_reinforcement(M_kNm, h, cover_mm, tipo_aco, classe_betao, diam_trial=12.0):
    """Dimensionamento completo de uma secção (por metro de largura).

    Devolve: μ, ω, As,calc, As,mín (ρ·b·d), As,máx (0,04·b·h),
             aço principal Ø//mm e As,ef, e aço de distribuição (20%).
    """
    fcd_MPa = fcd(classe_betao); fsyd_MPa = fsyd(tipo_aco)
    b_mm = 1000.0
    d_mm = h*1000.0 - cover_mm - diam_trial/2.0
    M_Nmm = float(M_kNm) * 1e6
    mu = M_Nmm / (b_mm * d_mm**2 * fcd_MPa) if d_mm > 0 else float("inf")
    omega = mu*(1.0+mu)
    As_calc = omega*b_mm*d_mm*fcd_MPa/fsyd_MPa if d_mm > 0 else float("inf")
    As_min = rho_min(tipo_aco)*b_mm*d_mm
    As_max = 0.04 * b_mm * h * 1000.0

    candidates = [10,12,14,16,18,20,22,25,28,32]
    spacings = [75,80,100,125,150,175,200,225,250]
    best = None
    for dia in candidates:
        if dia < 10: continue
        d = h*1000.0 - cover_mm - dia/2.0
        if d <= 0: continue
        mu2 = M_Nmm/(b_mm*d**2*fcd_MPa); omega2 = mu2*(1+mu2)
        As2 = omega2*b_mm*d*fcd_MPa/fsyd_MPa
        Asmin2 = rho_min(tipo_aco)*b_mm*d
        req2 = max(As2, Asmin2)
        req2 = min(req2, As_max)
        abar = math.pi*dia**2/4.0
        Smax_principal = min(250.0, 2.0*h*1000.0)
        for sp in spacings:
            if sp > Smax_principal + 1e-9: continue
            Asef = abar*1000.0/sp
            if Asef+1e-9 >= req2:
                score = (Asef-req2, dia, sp)
                item = {"diam":dia,"esp":sp,"d_mm":d,"mu":mu2,"omega":omega2,
                        "As_calc":As2,"As_min":Asmin2,"As_max":As_max,
                        "As_req":req2,"As_ef":Asef,
                        "armadura":f"Ø{dia} // {sp} mm",
                        "Smax":Smax_principal}
                if best is None or score < best[0]: best = (score,item)
    if best is None:
        dia=25; sp=250
        d=h*1000-cover_mm-dia/2; abar=math.pi*dia**2/4; Asef=abar*1000/sp
        mu=M_Nmm/(1000*d**2*fcd_MPa); omega=mu*(1+mu)
        As2=omega*1000*d*fcd_MPa/fsyd_MPa
        Asmin2=rho_min(tipo_aco)*1000*d
        item = {"diam":dia,"esp":sp,"d_mm":d,"mu":mu,"omega":omega,
                "As_calc":As2,"As_min":Asmin2,"As_max":As_max,
                "As_req":max(As2,Asmin2),"As_ef":Asef,
                "armadura":f"Ø{dia} // {sp} mm",
                "Smax":min(250,2*h*1000)}
    else:
        item = best[1]

    # Armadura de distribuição: 20% da principal (Art. 108 REBAP)
    As_dist_req = 0.20 * item["As_ef"]
    best_d = None
    for dia in candidates:
        if dia < 6: continue
        for sp in spacings:
            if sp > 350: continue
            Asef = math.pi*dia**2/4.0 * 1000.0 / sp
            if Asef + 1e-9 >= As_dist_req:
                score = (Asef - As_dist_req, dia, sp)
                cand = {"diam_dist":dia,"esp_dist":sp,"As_ef_dist":Asef,
                        "armadura_dist":f"Ø{dia} // {sp} mm"}
                if best_d is None or score < best_d[0]: best_d = (score, cand)
    if best_d is None:
        item.update({"diam_dist":6,"esp_dist":200,
                     "As_ef_dist":math.pi*6**2/4*5,
                     "armadura_dist":"Ø6 // 200 mm"})
    else:
        item.update(best_d[1])
    item["As_dist"] = As_dist_req
    return item

def punch_check(Nsd, bx, by, d_m, Bx, By, tau1_MPa, sigma_med_kPa):
    d_m=float(d_m); bx=float(bx); by=float(by)
    u=2.0*(bx+by)+math.pi*d_m
    Au=(bx+d_m)*(by+d_m)-((4-math.pi)/4.0)*d_m**2
    Vsd_ef=float(Nsd)-sigma_med_kPa*Au
    tau_rd=(1.6-d_m)*tau1_MPa
    tau_sd=Vsd_ef/(u*d_m)/1000.0 if u*d_m>0 else float("inf")
    return {"u":u,"Au":Au,"Vsd_ef":Vsd_ef,"tau_sd":tau_sd,"tau_rd":tau_rd,
            "Vrd":u*d_m*tau_rd*1000.0,
            "ok":tau_sd <= tau_rd + 1e-12 and Vsd_ef <= u*d_m*tau_rd*1000.0 + 1e-9}

def anchorage(As_cal, As_ef, diam_mm, tipo_aco, classe_betao):
    fbd=2.25*fctd(classe_betao)
    lb=(diam_mm/4.0)*(fsyd(tipo_aco)/fbd)
    ratio=As_cal/max(As_ef,1e-9)
    lbnet=lb*ratio
    lbmin=max(0.3*lb,10*diam_mm,100.0)
    return {"fbd":fbd,"lb":lb,"lbnet":max(lbnet,lbmin),"lbmin":lbmin}


# =============================================================================
# Traduções — PT / EN
# =============================================================================
TXT = {
    "pt": {
        "title": "Módulo de Sapatas Rígidas",
        # --- Formulário ---
        "h_geom": "## 1. Geometria e acções",
        "tipo_sapata": "**Tipo de sapata**",
        "t_quadrada": "Quadrada",
        "t_homotetica": "Homotética",
        "t_bordos": "Bordos equidistantes",
        "t_proporcionada": "Proporcionada",
        "h_solo": "## 2. Solo e materiais",
        "has_wt": "Existe nível freático?",
        "classe_betao": "**Classe do betão**",
        "tipo_aco_lbl": "**Tipo de aço**",
        "caso_iv": r"### Caso IV — slide 78 ($e_B/B$ e $e_L/L$)",
        "caso_iv_cap": "Só é necessário quando as duas excentricidades são não nulas.",
        "btn_calc": "🧮 Calcular e verificar",
        "btn_voltar": "↩️ Voltar ao Menu Principal",
        "info_calc": (r"As acções $N$, $M_x$, $M_y$, $H_x$, $H_y$ abaixo são tratadas "
                      r"como valores de cálculo. A aplicação não volta a majorá-las."),
        # --- Resultados ---
        "res_h": "# Resultados",
        "h_predim": "## 1️⃣ Pré-dimensionamento — slide 129",
        "h_altura": "## 2️⃣ Altura e rigidez — slide 131",
        "h_tensoes": "## 3️⃣ Tensões no terreno — slides 136–146",
        "h_meyerhof": "## 4️⃣ Capacidade de carga — Meyerhof, slides 49–55",
        "h_sigma": r"## 5️⃣ Comparação com $\sigma_{adm}$ — slide 131",
        "h_punco": "## 6️⃣ Punçoamento — slides 147–148",
        "h_corte": "##### Esforço transverso das consolas (Art. 53 REBAP)",
        "h_flexao": "## 8️⃣ Flexão — Método das Consolas, slides 156–158",
        "h_formulas": "**Fórmulas REBAP — Flexão, mínimos, máximos e distribuição**",
        "h_amarracao": "## 9️⃣ Amarração — slides 167–169",
        "h_desenho": "## 🔟 Desenhos de pormenorização",
        "h_conclusao": "## ✅ Conclusão",
        "h_relatorio": "## 📄 Relatório Técnico Completo",
        "h_dir_x": "Direcção X",
        "h_dir_y": "Direcção Y",
        "lbl_adoptado": "Adoptado:",
        "lbl_zona": "Zona:",
        "lbl_consolas": "Consolas:",
        "lbl_ok": "✅ OK",
        "lbl_nok": "❌ NÃO VERIFICA",
        "lbl_rigida_sim": "SIM",
        "lbl_rigida_nao": "NÃO",
        "lbl_rigida": "rígida:",
        "lbl_verif_fs": "**Verificação FS:**",
        "warn_montoya": ("Para o caso biaxial fora do núcleo, o PDF manda usar o "
                        "ábaco de Montoya — não foi digitalizado."),
        "err_cap": "Capacidade de carga não pode ser fechada com as hipóteses actuais.",
        "blk_principal": "**Armadura principal**",
        "blk_distrib": "**Armadura de distribuição**",
        "res_ok": "A solução satisfaz as verificações implementadas.",
        "res_nok": "A solução não satisfaz uma ou mais verificações.",
        "cap_rel": ("Inclui geometria, tensões, armaduras (principal + distribuição), "
                    "verificações e desenhos."),
        "btn_rel": "📥 Descarregar Relatório HTML Completo",
        "err_rel": "Erro ao gerar relatório:",
        # títulos das figuras
        "fig_conv": "Convenção de momentos",
        "fig_planta": "Planta",
        "fig_result": "Ponto de passagem da resultante",
        "fig_perfil": "Perfil",
        "fig_punco": "Punçoamento",
        "fig_consola": "Método das consolas",
        "fig_final": "Desenho final",

        "zona_dentro": "A — dentro do núcleo central",
        "zona_fora_x": "fora do terço central — eixo x",
        "zona_fora_y": "fora do terço central — eixo y",
        "zona_montoya": "B/C/D/E — Montoya necessário",
        "lbl_zonas": {
            "dentro": "A — dentro do núcleo central",
            "fora_x": "fora do terço central — eixo x",
            "fora_y": "fora do terço central — eixo y",
            "montoya": "B/C/D/E — Montoya necessário",
        },
        "lbl_min": "mín",
        "lbl_max": "máx",
    },
    "en": {
        "title": "Rigid Footings Module",
        # --- Form ---
        "h_geom": "## 1. Geometry and actions",
        "tipo_sapata": "**Footing type**",
        "t_quadrada": "Square",
        "t_homotetica": "Homothetic",
        "t_bordos": "Equal edges",
        "t_proporcionada": "Proportioned",
        "h_solo": "## 2. Soil and materials",
        "has_wt": "Water table present?",
        "classe_betao": "**Concrete class**",
        "tipo_aco_lbl": "**Steel type**",
        "caso_iv": r"### Case IV — slide 78 ($e_B/B$ and $e_L/L$)",
        "caso_iv_cap": "Only required when both eccentricities are non-zero.",
        "btn_calc": "🧮 Calculate and verify",
        "btn_voltar": "↩️ Back to Main Menu",
        "info_calc": (r"The actions $N$, $M_x$, $M_y$, $H_x$, $H_y$ below are treated "
                      r"as design values. The app does not factor them again."),
        # --- Results ---
        "res_h": "# Results",
        "h_predim": "## 1️⃣ Pre-sizing — slide 129",
        "h_altura": "## 2️⃣ Height and rigidity — slide 131",
        "h_tensoes": "## 3️⃣ Ground stresses — slides 136–146",
        "h_meyerhof": "## 4️⃣ Bearing capacity — Meyerhof, slides 49–55",
        "h_sigma": r"## 5️⃣ Comparison with $\sigma_{adm}$ — slide 131",
        "h_punco": "## 6️⃣ Punching shear — slides 147–148",
        "h_corte": "##### Shear force of the cantilevers (Art. 53 REBAP)",
        "h_flexao": "## 8️⃣ Bending — Cantilever Method, slides 156–158",
        "h_formulas": "**REBAP formulas — Bending, minima, maxima and distribution**",
        "h_amarracao": "## 9️⃣ Anchorage — slides 167–169",
        "h_desenho": "## 🔟 Detailing drawings",
        "h_conclusao": "## ✅ Conclusion",
        "h_relatorio": "## 📄 Full Technical Report",
        "h_dir_x": "Direction X",
        "h_dir_y": "Direction Y",
        "lbl_adoptado": "Adopted:",
        "lbl_zona": "Zone:",
        "lbl_consolas": "Cantilevers:",
        "lbl_ok": "✅ OK",
        "lbl_nok": "❌ DOES NOT VERIFY",
        "lbl_rigida_sim": "YES",
        "lbl_rigida_nao": "NO",
        "lbl_rigida": "rigid:",
        "lbl_verif_fs": "**FS check:**",
        "warn_montoya": ("For the biaxial case outside the kern, the PDF requires the "
                        "Montoya chart — it was not digitised."),
        "err_cap": "Bearing capacity cannot be closed with the current assumptions.",
        "blk_principal": "**Main reinforcement**",
        "blk_distrib": "**Distribution reinforcement**",
        "res_ok": "The solution satisfies the implemented checks.",
        "res_nok": "The solution does not satisfy one or more checks.",
        "cap_rel": ("Includes geometry, stresses, reinforcement (main + distribution), "
                    "checks and drawings."),
        "btn_rel": "📥 Download Full HTML Report",
        "err_rel": "Error generating report:",
        # figure titles
        "fig_conv": "Sign convention for moments",
        "fig_planta": "Plan",
        "fig_result": "Resultant passage point",
        "fig_perfil": "Section",
        "fig_punco": "Punching shear",
        "fig_consola": "Cantilever method",
        "fig_final": "Final drawing",

        "zona_dentro": "A — inside the central kern",
        "zona_fora_x": "outside the middle third — x axis",
        "zona_fora_y": "outside the middle third — y axis",
        "zona_montoya": "B/C/D/E — Montoya chart required",
        "lbl_zonas": {
            "dentro": "A — inside the central kern",
            "fora_x": "outside the middle third — x axis",
            "fora_y": "outside the middle third — y axis",
            "montoya": "B/C/D/E — Montoya chart required",
        },
        "lbl_min": "min",
        "lbl_max": "max",
    },
}

def _T(lang, k):
    return TXT.get(lang, TXT["pt"]).get(k, k)


def _img_local(caminho, width=None):
    from utils.imagens import img_base64_html
    return img_base64_html(caminho, width=width)


# =============================================================================
# Helper: rótulo LaTeX + campo numérico por baixo
# =============================================================================
def _campo(txt_pt, txt_en, simb, unidade, valor, key,
           minv=None, maxv=None, passo=None, formato="%.2f"):
    """Rótulo com LaTeX + number_input com label escondida.

    Nota: construir o markdown com if/else em vez de concatenar '${simb}$' + '${uni}'
    para evitar produzir '$$' quando a unidade é vazia (isso quebra o MathJax).
    """
    lang = st.session_state.get("language", "pt")
    txt = txt_pt if lang == "pt" else txt_en
    if unidade:
        st.markdown(f"**{txt}** &nbsp;—&nbsp; ${simb}$ &nbsp;[{unidade}]")
    else:
        st.markdown(f"**{txt}** &nbsp;—&nbsp; ${simb}$")
    kw = {"value": valor, "key": key, "label_visibility": "collapsed",
          "format": formato}
    if minv is not None: kw["min_value"] = minv
    if maxv is not None: kw["max_value"] = maxv
    if passo is not None: kw["step"] = passo
    return st.number_input(f"{txt} {simb}", **kw)


def _campo_int(txt_pt, txt_en, simb, unidade, valor, key,
               minv=None, maxv=None, passo=None):
    lang = st.session_state.get("language", "pt")
    txt = txt_pt if lang == "pt" else txt_en
    if unidade:
        st.markdown(f"**{txt}** &nbsp;—&nbsp; ${simb}$ &nbsp;[{unidade}]")
    else:
        st.markdown(f"**{txt}** &nbsp;—&nbsp; ${simb}$")
    kw = {"value": valor, "key": key, "label_visibility": "collapsed"}
    if minv is not None: kw["min_value"] = int(minv)
    if maxv is not None: kw["max_value"] = int(maxv)
    if passo is not None: kw["step"] = int(passo)
    return st.number_input(f"{txt} {simb}", **kw)


# =============================================================================
# FORMULÁRIO
# =============================================================================
def mostrar():
    lang = st.session_state.get("language", "pt")
    st.markdown(f"# 📐 {_T(lang,'title')}")
    st.markdown(_img_local("assets/Picture4.png"), unsafe_allow_html=True)
    st.info(_T(lang, "info_calc"))

    # ---------------------------------------------------------------
    # 1) Geometria e acções
    # ---------------------------------------------------------------
    st.markdown(_T(lang, "h_geom"))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(_T(lang, "tipo_sapata"))
        tipo = st.selectbox(
            "tipo", ["quadrada","homotetica","bordos_equidistantes","proporcionada"],
            format_func=lambda x: {
                "quadrada": _T(lang, "t_quadrada"),
                "homotetica": _T(lang, "t_homotetica"),
                "bordos_equidistantes": _T(lang, "t_bordos"),
                "proporcionada": _T(lang, "t_proporcionada")}[x],
            label_visibility="collapsed", key="sap_tipo")

        bx = _campo("Comprimento do pilar em x", "Column length x",
                    "b_x", "m", 0.40, "sap_bx", minv=0.05, passo=0.05)
        by = _campo("Comprimento do pilar em y", "Column length y",
                    "b_y", "m", 0.30, "sap_by", minv=0.05, passo=0.05)

    with c2:
        N  = _campo("Carga vertical de cálculo", "Design vertical load",
                    "N", "kN", 1000.0, "sap_N", minv=0.0, passo=50.0, formato="%.1f")
        Mx = _campo("Momento em torno de x", "Bending moment about x",
                    "M_x", "kN·m", 0.0, "sap_Mx", passo=10.0, formato="%.1f")
        My = _campo("Momento em torno de y", "Bending moment about y",
                    "M_y", "kN·m", 0.0, "sap_My", passo=10.0, formato="%.1f")
        Hx = _campo("Acção horizontal em x", "Horizontal action x",
                    "H_x", "kN", 0.0, "sap_Hx", passo=10.0, formato="%.1f")
        Hy = _campo("Acção horizontal em y", "Horizontal action y",
                    "H_y", "kN", 0.0, "sap_Hy", passo=10.0, formato="%.1f")

    with c3:
        sigma_adm = _campo("Tensão admissível", "Allowable stress",
                           r"\sigma_{adm}", "kPa", 300.0, "sap_sig",
                           minv=1.0, passo=10.0, formato="%.1f")
        FS   = _campo("Factor de segurança requerido", "Required safety factor",
                      "FS", "", 3.0, "sap_FS", minv=1.0, passo=0.5, formato="%.2f")
        peso = _campo("Peso da sapata / N", "Footing weight / N",
                      "N_{sap}/N", "", 0.10, "sap_peso",
                      minv=0.0, maxv=0.30, passo=0.01, formato="%.2f")

    # ---------------------------------------------------------------
    # 2) Solo e materiais
    # ---------------------------------------------------------------
    st.markdown(_T(lang, "h_solo"))
    c1, c2, c3 = st.columns(3)
    with c1:
        gamma     = _campo("Peso específico natural", "Natural unit weight",
                           r"\gamma", "kN/m³", 18.0, "sap_g",
                           minv=1.0, passo=0.5, formato="%.2f")
        gamma_sat = _campo("Peso específico saturado", "Saturated unit weight",
                           r"\gamma_{sat}", "kN/m³", 20.0, "sap_gsat",
                           minv=1.0, passo=0.5, formato="%.2f")
        has_wt = st.checkbox(_T(lang, "has_wt"), value=False, key="sap_has_wt")
        WT = _campo("Profundidade do N.F. (a partir do NT)",
                    "Water table depth (from G.L.)",
                    "z_w", "m", 0.0, "sap_WT", minv=0.0, passo=0.1, formato="%.2f")
        phi = _campo("Ângulo de atrito efectivo", "Effective friction angle",
                     r"\phi'", "°", 30.0, "sap_phi",
                     minv=0.0, maxv=45.0, passo=1.0, formato="%.1f")
        c_  = _campo("Coesão efectiva", "Effective cohesion",
                     "c'", "kPa", 0.0, "sap_c",
                     minv=0.0, passo=1.0, formato="%.2f")

    with c2:
        Df = _campo("Profundidade de fundação", "Foundation depth",
                    "D_f", "m", 1.50, "sap_Df", minv=0.0, passo=0.10, formato="%.2f")
        st.markdown(_T(lang, "classe_betao") + " &nbsp;—&nbsp; $f_{ck}$")
        classe_betao = st.selectbox("bet", list(FCD_MPA.keys()), index=2,
                                    label_visibility="collapsed", key="sap_bet")
        st.markdown(_T(lang, "tipo_aco_lbl") + " &nbsp;—&nbsp; $f_{yk}$")
        tipo_aco = st.selectbox("aco", ["A235","A400","A500","A500NR"], index=1,
                                label_visibility="collapsed", key="sap_aco")
        cover = _campo("Recobrimento nominal", "Nominal cover",
                       "c_{nom}", "mm", 50.0, "sap_rec",
                       minv=20.0, passo=5.0, formato="%.0f")

    with c3:
        st.markdown(_T(lang, "caso_iv"))
        st.caption(_T(lang, "caso_iv_cap"))
        B2 = _campo("Leitura do ábaco — B2/B", "Chart reading — B2/B",
                    "B_2/B", "", 0.25, "sap_B2",
                    minv=0.0, maxv=1.0, passo=0.01, formato="%.2f")
        L2 = _campo("Leitura do ábaco — L2/L", "Chart reading — L2/L",
                    "L_2/L", "", 0.80, "sap_L2",
                    minv=0.0, maxv=1.0, passo=0.01, formato="%.2f")

    if st.button(_T(lang, "btn_calc"), type="primary", use_container_width=True):
        executar_calculo(lang, tipo, bx, by, N, Mx, My, Hx, Hy,
                         sigma_adm, FS, peso, gamma, gamma_sat,
                         WT if has_wt else -1.0, c_, phi, Df,
                         classe_betao, tipo_aco, cover, B2, L2)

    st.divider()
    if st.button(_T(lang, "btn_voltar"), use_container_width=True,
                 key="sap_btn_voltar"):
        ir_para_menu()

# =============================================================================
# EXECUÇÃO E APRESENTAÇÃO
# =============================================================================
def executar_calculo(lang, tipo, bx, by, N, Mx, My, Hx, Hy, sigma_adm, FS, peso_pct,
                     gamma, gamma_sat, WT, c, phi, Df,
                     classe_betao, tipo_aco, cover, B2_ratio, L2_ratio):
    st.markdown("---")
    st.markdown(_T(lang, "res_h"))

    # 1. Pré-dimensionamento
    pre = pre_dimensionar(tipo, bx, by, N, Mx, My, sigma_adm, peso_pct)
    Bx, By = pre["Bx"], pre["By"]
    Nr = pre["Nr"]
    ex, ey = pre["ex"], pre["ey"]
    st.markdown(_T(lang, "h_predim"))
    st.latex(r"B_y=\frac{1}{b}\left[-a+e_y b+e_x"
             r"+\sqrt{(a+e_y b-e_x)^2+b\,\frac{N+P}{\sigma_{adm}}}\right],\qquad "
             r"B_x=B_y\,b+2a")
    st.markdown(
        f"{_T(lang,'lbl_adoptado')} $B_x = \\mathbf{{{Bx:.2f}}}$ m &nbsp;|&nbsp; "
        f"$B_y = \\mathbf{{{By:.2f}}}$ m &nbsp;|&nbsp; "
        f"$N_r = \\mathbf{{{Nr:.1f}}}$ kN")

    # 2. Altura / rigidez
    rig = rigid_footing_design(Bx, By, bx, by, cover, NOMINAL_BAR_DIAMETER_MM)
    h = rig["h"]
    st.markdown(_T(lang, "h_altura"))
    st.latex(r"d\ge\frac{a_{\max}}{2}\,,\qquad "
             r"\frac{2a_{\max}}{3}\le d\le a_{\max}")
    st.markdown(
        f"{_T(lang,'lbl_consolas')} $a_x = {rig['a_x']:.3f}$ m | "
        f"$a_y = {rig['a_y']:.3f}$ m | "
        f"$a_{{\\max}} = {rig['a_max']:.3f}$ m")
    st.markdown(
        f"{_T(lang,'lbl_adoptado')} $h = \\mathbf{{{h:.2f}}}$ m | "
        f"$d_{{\\text{{nom}}}} = \\mathbf{{{rig['d_trial']:.3f}}}$ m | "
        f"{_T(lang,'lbl_rigida')} "
        f"**{_T(lang,'lbl_rigida_sim') if rig['rigid'] else _T(lang,'lbl_rigida_nao')}**")

        # 3. Tensões
    ten = stresses(Nr, Mx, My, Bx, By)
    st.markdown(_T(lang, "h_tensoes"))
    st.latex(r"\sigma_i=\frac{N_r}{B_x B_y}"
             r"\left(1\pm 6\eta_x\pm 6\eta_y\right)")
    st.markdown(
        f"$e_x = {ex:+.4f}$ m | $e_y = {ey:+.4f}$ m | "
        f"$\\eta_x = {ten['eta_x']:.4f}$ | $\\eta_y = {ten['eta_y']:.4f}$")
    _zona_map = _T(lang, "lbl_zonas")
    _zona_txt = _zona_map.get(ten['zona'], ten['zona']) if isinstance(_zona_map, dict) else ten['zona']
    st.markdown(f"{_T(lang,'lbl_zona')} **{_zona_txt}**")
    cols = st.columns(4)
    for col, name, val in zip(cols,
                          ["σ₁", "σ₂", "σ₃", "σ₄"],
                          [ten['sigma1'], ten['sigma2'], ten['sigma3'], ten['sigma4']]):
        col.metric(name, f"{val:.1f} kPa")
    st.markdown(
        f"$\\sigma_{{\\max}} = \\mathbf{{{ten['sigma_max']:.1f}}}$ kPa | "
        f"$\\sigma_{{\\min}} = \\mathbf{{{ten['sigma_min']:.1f}}}$ kPa")
    if not ten["inside_kern"] and abs(Mx)>1e-9 and abs(My)>1e-9:
        st.warning(_T(lang, "warn_montoya"))

    # 4. Meyerhof
    q_base, gamma_term = water_adjusted_q_and_gamma(gamma, gamma_sat, Df, WT)
    H = math.hypot(Hx, Hy); V = max(Nr, 1e-9)
    beta = math.degrees(math.atan2(H, V)) if H > 0 else 0.0
    cap = meyerhof_capacity(Bx, By, Df, c, phi, gamma, q_base, ex, ey,
                            B2_ratio, L2_ratio, gamma_term, beta)
    st.markdown(_T(lang, "h_meyerhof"))
    st.latex(r"q_u = c\,N_c F_{cs}F_{cd}F_{ci} + q\,N_q F_{qs}F_{qd}F_{qi}"
             r" + \tfrac{1}{2}\,\gamma\,B\,N_\gamma F_{\gamma s}F_{\gamma d}F_{\gamma i}")
    st.markdown(f"$q' = {q_base:.2f}$ kPa &nbsp;|&nbsp; $\\beta = {beta:.2f}^\\circ$")
    if cap.get("ok"):
        qadm_FS = cap["qu"]/FS
        q_appl_eff = Nr/cap["A_eff"]
        ok_FS = qadm_FS >= q_appl_eff
        st.markdown(
            f"$A' = \\mathbf{{{cap['A_eff']:.3f}}}$ m² &nbsp;|&nbsp; "
            f"$B' = \\mathbf{{{cap['B_eff']:.3f}}}$ m &nbsp;|&nbsp; "
            f"$L' = \\mathbf{{{cap['L_eff']:.3f}}}$ m")
        st.markdown(
            f"$q_u = \\mathbf{{{cap['qu']:.1f}}}$ kPa &nbsp;|&nbsp; "
            f"$q_u/FS = \\mathbf{{{qadm_FS:.1f}}}$ kPa &nbsp;|&nbsp; "
            f"$q_{{apl,ef}} = \\mathbf{{{q_appl_eff:.1f}}}$ kPa")
        st.markdown(f"{_T(lang,'lbl_verif_fs')} "
                    f"{_T(lang,'lbl_ok') if ok_FS else _T(lang,'lbl_nok')}")
        simbolos = [
            "N<sub>c</sub>", "N<sub>q</sub>", "N<sub>γ</sub>",
            "F<sub>cs</sub>", "F<sub>qs</sub>", "F<sub>γs</sub>",
            "F<sub>cd</sub>", "F<sub>qd</sub>", "F<sub>γd</sub>",
            "F<sub>ci</sub>", "F<sub>qi</sub>", "F<sub>γi</sub>",
        ]
        valores = [cap[k] for k in ["Nc","Nq","Ngamma","Fcs","Fqs","Fgs",
                                    "Fcd","Fqd","Fgd","Fci","Fqi","Fgi"]]
        linhas = "".join(
            f"<tr>"
            f"<td style='padding:6px 14px;border:1px solid #ddd;"
            f"text-align:center;'>{s}</td>"
            f"<td style='padding:6px 14px;border:1px solid #ddd;"
            f"text-align:center;'>{v:.4f}</td>"
            f"</tr>"
            for s, v in zip(simbolos, valores)
        )
        hdr1 = "Factor" if lang == "pt" else "Factor"
        hdr2 = "Valor" if lang == "pt" else "Value"
        tab_cap = (
            "<table style='border-collapse:collapse;"
            "margin:10px auto;font-size:13px;'>"
            "<tr style='background:#34495e;color:#fff;'>"
            f"<th style='padding:6px 14px;border:1px solid #ddd;"
            f"text-align:center;'>{hdr1}</th>"
            f"<th style='padding:6px 14px;border:1px solid #ddd;"
            f"text-align:center;'>{hdr2}</th>"
            "</tr>"
            f"{linhas}</table>"
        )
        st.markdown(tab_cap, unsafe_allow_html=True)
    else:
        ok_FS = False
        st.error(_T(lang, "err_cap"))
        for w in cap.get("warnings", []):
            st.write(f"• {w}")

    # 5. σadm
    ok_sig = ten["sigma_max"] <= sigma_adm + 1e-9 if sigma_adm > 0 else True
    st.markdown(_T(lang, "h_sigma"))
    st.markdown(
        f"$\\sigma_{{\\max}} = \\mathbf{{{ten['sigma_max']:.1f}}}$ kPa vs "
        f"$\\sigma_{{adm}} = \\mathbf{{{sigma_adm:.1f}}}$ kPa → "
        f"{'✅' if ok_sig else '❌'}")

    # 6. Punçoamento
    d = h - cover/1000.0 - NOMINAL_BAR_DIAMETER_MM/2000.0
    punc = punch_check(N, bx, by, d, Bx, By, tau1(classe_betao), ten["sigma_med"])
    st.markdown(_T(lang, "h_punco"))
    st.caption(f"$d = h - c - \\varnothing/2 = {d:.3f}$ m")
    st.latex(r"\tau_{sd} = \frac{V_{sd,ef}}{u\,d} \le \tau_{rd} = (1.6-d)\,\tau_1")
    st.markdown(
        f"$u = {punc['u']:.3f}$ m | $A_u = {punc['Au']:.4f}$ m² | "
        f"$V_{{sd,ef}} = {punc['Vsd_ef']:.1f}$ kN | "
        f"$V_{{Rd}} = {punc['Vrd']:.1f}$ kN")
    st.markdown(
        f"$\\tau_{{sd}} = {punc['tau_sd']:.4f}$ MPa | "
        f"$\\tau_{{Rd}} = {punc['tau_rd']:.4f}$ MPa → "
        f"**{_T(lang,'lbl_ok') if punc['ok'] else _T(lang,'lbl_nok')}**")

    # 8. Flexão + distribuição
    cms = console_moments(Bx, By, bx, by, Nr, Mx, My, ten["sigma_max"])
    arm_x = flexural_reinforcement(cms["MEd_x"], h, cover, tipo_aco, classe_betao)
    arm_y = flexural_reinforcement(cms["MEd_y"], h, cover, tipo_aco, classe_betao)

    st.markdown(_T(lang, "h_flexao"))
    st.markdown(
        f"$l_x = {cms['lx']:.3f}$ m | "
        f"$\\sigma_{{ref,x}} = {cms['sigma_ref_x']:.1f}$ kPa | "
        f"$M_{{Ed,x}} = {cms['MEd_x']:.1f}$ kN·m/m")
    st.markdown(
        f"$l_y = {cms['ly']:.3f}$ m | "
        f"$\\sigma_{{ref,y}} = {cms['sigma_ref_y']:.1f}$ kPa | "
        f"$M_{{Ed,y}} = {cms['MEd_y']:.1f}$ kN·m/m")

    st.markdown(_T(lang, "h_formulas"))
    st.latex(r"\mu = \frac{M_{Ed}}{b\,d^2 f_{cd}}\;;\; "
             r"\omega = \mu(1+\mu)\;;\; "
             r"A_s = \frac{\omega\,b\,d\,f_{cd}}{f_{syd}}")
    st.latex(r"A_{s,\min} = \rho\,b\,d\;;\quad "
             r"A_{s,\max} = 0{,}04\,b\,h\;;\quad "
             r"A_{s,dist} = 0{,}20\,A_s")

    def _bloco_direcao(nome, arm, Msd, lado):
        st.markdown(f"#### {nome}")
        st.markdown(
            f"$M_{{Ed}} = \\mathbf{{{Msd:.2f}}}$ kN·m/m | "
            f"$\\mu = {arm['mu']:.5f}$ | $\\omega = {arm['omega']:.5f}$")
        st.markdown(
        f"$A_{{s,calc}} = {arm['As_calc']/100:.2f}$ cm²/m | "
        f"$A_{{s,\\text{{{_T(lang, 'lbl_min')}}}}} = {arm['As_min']/100:.2f}$ cm²/m | "
        f"$A_{{s,\\text{{{_T(lang, 'lbl_max')}}}}} = {arm['As_max']/100:.2f}$ cm²/m")
        st.success(f"{_T(lang,'blk_principal')} ({lado}): {arm['armadura']} "
                   f"— $A_{{s,ef}} = {arm['As_ef']/100:.2f}$ cm²/m")
        st.info(f"{_T(lang,'blk_distrib')} ({lado}): {arm['armadura_dist']} "
                f"— $A_{{s,dist}} = {arm['As_dist']/100:.2f}$ cm²/m "
                f"({arm['As_ef_dist']/100:.2f} cm²/m "
                f"{'efectiva' if lang=='pt' else 'effective'})")

    cols = st.columns(2)
    with cols[0]:
        _bloco_direcao(_T(lang, "h_dir_x"), arm_x, cms["MEd_x"], "X")
    with cols[1]:
        _bloco_direcao(_T(lang, "h_dir_y"), arm_y, cms["MEd_y"], "Y")

    st.markdown(_T(lang, "h_corte"))
    st.latex(r"V_{Rd} = \eta\,\tau_1\,d\,b_1\;;\quad "
             r"\eta = 1{,}6-d\ (\geq 0{,}6)")

    # 9. Amarração
    anch_x = anchorage(arm_x['As_req'], arm_x['As_ef'], arm_x['diam'], tipo_aco, classe_betao)
    anch_y = anchorage(arm_y['As_req'], arm_y['As_ef'], arm_y['diam'], tipo_aco, classe_betao)
    st.markdown(_T(lang, "h_amarracao"))
    st.latex(r"l_b = \frac{\phi}{4}\cdot\frac{f_{syd}}{f_{bd}}\;;\; "
             r"l_{b,net} = l_b\cdot\frac{A_{s,cal}}{A_{s,ef}} \ge l_{b,\min}")
    st.markdown(f"$f_{{bd}} = {anch_x['fbd']:.3f}$ MPa")
    dirx = _T(lang, "h_dir_x")
    diry = _T(lang, "h_dir_y")
    st.markdown(
        f"{dirx}: $l_{{b,net}} = \\mathbf{{{anch_x['lbnet']:.0f}}}$ mm | "
        f"{diry}: $l_{{b,net}} = \\mathbf{{{anch_y['lbnet']:.0f}}}$ mm")

    # 10. Desenhos
    st.markdown(_T(lang, "h_desenho"))
    svg_conv = SD.svg_convencao_momentos(lang)
    svg_plan = SD.svg_planta_sapata(Bx, By, bx, by, ten['ex'], ten['ey'], Mx, My, lang)
    svg_res  = SD.svg_ponto_resultante(Bx, By, ten['ex'], ten['ey'],
                                       ten['eta_x'], ten['eta_y'],
                                       ten['inside_kern'], lang)
    svg_perf = SD.svg_perfil_sapata(Bx, bx, h, Df, WT,
                                    ten['sigma1'], ten['sigma2'],
                                    ten['sigma_max'], ten['sigma_min'], lang)
    svg_punc = SD.svg_puncoamento(Bx, By, bx, by, d,
                                  ten['sigma_max'], ten['sigma_min'],
                                  punc['Vsd_ef'], punc['Vrd'],
                                  punc['tau_sd'], punc['tau_rd'], lang)
    svg_disp = SD.svg_disposicoes_construtivas(
        Bx, bx, h, ten['sigma1'], ten['sigma2'],
        arm_x['As_req']/100, arm_y['As_req']/100,
        arm_x['diam'], arm_x['esp'], lang)
    svg_fin  = SD.svg_final_sapata(Bx, By, bx, by, h,
                                   arm_x['armadura'], arm_y['armadura'],
                                   arm_x['armadura_dist'], arm_y['armadura_dist'],
                                   lang)
    for key_title, svg in [("fig_conv", svg_conv),
                           ("fig_planta", svg_plan),
                           ("fig_result", svg_res),
                           ("fig_perfil", svg_perf),
                           ("fig_punco", svg_punc),
                           ("fig_consola", svg_disp),
                           ("fig_final", svg_fin)]:
        st.markdown(f"### {_T(lang, key_title)}")
        st.markdown(svg, unsafe_allow_html=True)

    # 11. Conclusão
    all_ok = bool(ok_sig and punc['ok'] and rig['rigid']
                  and (ok_FS if cap.get('ok') else False))
    st.markdown(_T(lang, "h_conclusao"))
    if all_ok:
        st.success(_T(lang, "res_ok"))
    else:
        st.error(_T(lang, "res_nok"))

    # 12. Relatório
    if RS is not None:
        st.markdown("---")
        st.markdown(_T(lang, "h_relatorio"))
        st.caption(_T(lang, "cap_rel"))
        try:
            html_bytes = RS.gerar_relatorio_html_sapatas(
                nome=st.session_state.get("nome", "Utilizador"),
                curso=st.session_state.get("curso", ""),
                genero=st.session_state.get("genero", "Masculino"),
                lang=lang, tipo_sapata=tipo,
                bx=bx, by=by, P_kN=N, Mx_kNm=Mx, My_kNm=My,
                sigma_adm_kPa=sigma_adm,
                classe_betao=classe_betao, tipo_aco=tipo_aco,
                recobrimento_mm=cover,
                gamma_solo=gamma, gamma_sat=gamma_sat,
                phi_solo=phi, c_solo=c, cu_solo=0.0,
                Df=Df, WT=WT if WT > 0 else 0.0,
                Bx=Bx, By=By, h=h, Nr=Nr,
                ex=ten['ex'], ey=ten['ey'],
                eta_x=ten['eta_x'], eta_y=ten['eta_y'],
                sigma1=ten['sigma1'], sigma2=ten['sigma2'],
                sigma3=ten['sigma3'], sigma4=ten['sigma4'],
                sigma_max=ten['sigma_max'], sigma_min=ten['sigma_min'],
                sigma_ref=ten['sigma_ref'], zona=ten['zona'],
                phi_d=phi, c_d=c, delta_d=phi, q_d=gamma*Df,
                qr_ec7=cap.get("qu", 0.0) or 0.0,
                Nc=cap.get("Nc", 0.0) or 0.0,
                Nq=cap.get("Nq", 0.0) or 0.0,
                Ngamma=cap.get("Ngamma", 0.0) or 0.0,
                termo_c=cap.get("termo_c", 0.0) or 0.0,
                termo_q=cap.get("termo_q", 0.0) or 0.0,
                termo_g=cap.get("termo_g", 0.0) or 0.0,
                ok_carga=ok_sig, ok_desliz=True, ok_derr=True,
                Vd_kN=Nr, Hd_kN=math.hypot(Hx, Hy),
                Rd_kN=0.0, Mest_kNm=0.0, Mderr_kNm=0.0,
                ok_punco=punc['ok'], ok_corte=True,
                Vsd_punco=punc['Vsd_ef'], Vrd_punco=punc['Vrd'],
                tau_sd=punc['tau_sd'], tau_rd=punc['tau_rd'],
                Vsd_corte=0.0, Vrd_corte=0.0,
                armadura_x=arm_x['armadura'],
                armadura_y=arm_y['armadura'],
                As_x=arm_x['As_calc']/100, As_y=arm_y['As_calc']/100,
                As_min_x=arm_x['As_min']/100, As_min_y=arm_y['As_min']/100,
                As_max_x=arm_x['As_max']/100, As_max_y=arm_y['As_max']/100,
                As_f_x=arm_x['As_ef']/100, As_f_y=arm_y['As_ef']/100,
                armadura_dist_x=arm_x['armadura_dist'],
                armadura_dist_y=arm_y['armadura_dist'],
                As_dist_x=arm_x['As_dist']/100,
                As_dist_y=arm_y['As_dist']/100,
                combo_ec7="EC7 (DA1)",
                svg_convencao=svg_conv, svg_resultante=svg_res,
                svg_planta=svg_plan, svg_perfil=svg_perf,
                svg_punco=svg_punc, svg_disposicoes=svg_disp,
                svg_final=svg_fin,
                fbd_MPa=anch_x['fbd'],
                lb_net_x=anch_x['lbnet'], lb_net_y=anch_y['lbnet'],
                d_mm=d*1000,
            )
            st.download_button(
                label=_T(lang, "btn_rel"),
                data=html_bytes,
                file_name=f"Relatorio_Sapata_{st.session_state.get('nome','User').replace(' ','_')}.html",
                mime="text/html",
                use_container_width=True,
                type="primary",
                key="sap_btn_rel",
            )
        except Exception as e:
            st.error(f"{_T(lang,'err_rel')} {e}")
            import traceback
            st.code(traceback.format_exc())
   

if __name__ == "__main__":
    mostrar()