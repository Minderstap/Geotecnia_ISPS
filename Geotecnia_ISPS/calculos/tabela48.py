"""
Tabela 48 REBAP - Distribuição da armadura em lajes
Diâmetros comerciais disponíveis em Moçambique e espaçamentos correspondentes
"""

# ============================================================
# DIÂMETROS COMERCIAIS DISPONÍVEIS EM MOÇAMBIQUE (mm)
# ============================================================
DIAMETROS_COMERCIAIS = [6, 8, 10, 12, 16, 20, 25]

# ============================================================
# ÁREA DE SECÇÃO DE UM VARÃO (mm²)  ->  A = π·Ø²/4
# ============================================================
AREA_VARAO = {
    6: 28.3,
    8: 50.3,
    10: 78.5,
    12: 113.1,
    16: 201.1,
    20: 314.2,
    25: 490.9
}

# ============================================================
# ESPAÇAMENTOS COMERCIAIS TÍPICOS (mm)
# ============================================================
ESPACAMENTOS_COMERCIAIS = [100, 125, 150, 175, 200, 225, 250, 300, 350, 400]


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def calcular_espacamento(As_necessaria_mm2_m, diametro_mm):
    """
    Calcula o espaçamento teórico (mm) para um diâmetro e área de armadura por metro.
    As = (1000 / s) × A_varão   =>   s = (1000 × A_varão) / As
    """
    area_varao = AREA_VARAO[diametro_mm]
    espacamento = (1000.0 * area_varao) / As_necessaria_mm2_m
    return espacamento


def selecionar_armadura_comercial(As_necessaria_mm2_m, espacamento_max_mm=350, diametro_min=10):
    """
    Seleciona a melhor combinação diâmetro/espaçamento comercial (Tabela 48).
    Minimiza o excesso de aço, respeitando:
      - espaçamento máximo (Art. 105 REBAP)
      - diâmetro mínimo (varões principais em sapatas/muros: 10 mm)
    Retorna: (diametro_mm, espacamento_mm, As_efetiva_mm2_m)
    """
    if As_necessaria_mm2_m <= 0:
        As_necessaria_mm2_m = 1.0
    
    melhor = None
    for diametro in DIAMETROS_COMERCIAIS:
        if diametro < diametro_min:
            continue
        for esp in ESPACAMENTOS_COMERCIAIS:
            if esp > espacamento_max_mm:
                continue
            As_ef = AREA_VARAO[diametro] * 1000.0 / esp
            if As_ef >= As_necessaria_mm2_m * 0.98:
                if melhor is None or As_ef < melhor[2]:
                    melhor = (diametro, esp, As_ef)
    
    # Fallback de segurança: Ø25 c/c 100 mm
    if melhor is None:
        melhor = (25, 100, AREA_VARAO[25] * 10.0)
    
    return melhor


def formatar_armadura(diametro_mm, espacamento_mm):
    """Formata a armadura no padrão de desenho: ØX c/c Ymm"""
    return f"Ø{diametro_mm} c/c {espacamento_mm}mm"


def armadura_distribuicao(As_principal_mm2_m, percentagem=0.20, diametro_min=6):
    """
    Armadura de distribuição (Art. 108 REBAP): 20% da armadura principal.
    Retorna: (diametro_mm, espacamento_mm, As_efetiva_mm2_m)
    """
    As_dist = percentagem * As_principal_mm2_m
    return selecionar_armadura_comercial(As_dist, espacamento_max_mm=350, diametro_min=diametro_min)

def espacamento_cm(espacamento_mm):
    """Converte espaçamento de mm para cm em formato limpo (12.5, 15, 10...)"""
    return f"{espacamento_mm / 10.0:g}"

def formatar_armadura(diametro_mm, espacamento_mm):
    """Formata a armadura no padrão: Ø16@12.5cm"""
    return f"Ø{diametro_mm}@{espacamento_cm(espacamento_mm)}cm"