"""
Tabela de factores de capacidade de carga de Meyerhof (1963)
com interpolacao linear para angulos intermediarios.
"""
import math


# φ' : (Nc, Nq, Nγ)
_TAB = {
    0:  (5.14,   1.00,   0.00),
    1:  (5.38,   1.09,   0.07),
    2:  (5.63,   1.20,   0.15),
    3:  (5.90,   1.31,   0.24),
    4:  (6.19,   1.43,   0.34),
    5:  (6.49,   1.57,   0.45),
    6:  (6.81,   1.72,   0.57),
    7:  (7.16,   1.88,   0.71),
    8:  (7.53,   2.06,   0.86),
    9:  (7.92,   2.25,   1.03),
    10: (8.35,   2.47,   1.22),
    11: (8.80,   2.71,   1.44),
    12: (9.28,   2.97,   1.69),
    13: (9.81,   3.26,   1.97),
    14: (10.37,  3.59,   2.29),
    15: (10.98,  3.94,   2.65),
    16: (11.63,  4.34,   3.06),
    17: (12.34,  4.77,   3.53),
    18: (13.10,  5.26,   4.07),
    19: (13.93,  5.80,   4.68),
    20: (14.83,  6.40,   5.39),
    21: (15.82,  7.07,   6.20),
    22: (16.88,  7.82,   7.13),
    23: (18.05,  8.66,   8.20),
    24: (19.32,  9.60,   9.44),
    25: (20.72,  10.66, 10.88),
    26: (22.25,  11.85, 12.54),
    27: (23.94,  13.20, 14.47),
    28: (25.80,  14.72, 16.72),
    29: (27.86,  16.44, 19.34),
    30: (30.14,  18.40, 22.40),
    31: (32.67,  20.63, 25.99),
    32: (35.49,  23.18, 30.22),
    33: (38.64,  26.09, 35.19),
    34: (42.16,  29.44, 41.06),
    35: (46.12,  33.30, 48.03),
    36: (50.59,  37.75, 56.31),
    37: (55.63,  42.92, 66.19),
    38: (61.35,  48.93, 78.03),
    39: (67.87,  55.96, 92.25),
    40: (75.31,  64.20, 109.41),
    41: (83.86,  73.90, 130.22),
    42: (93.71,  85.38, 155.55),
    43: (105.11, 99.02, 186.54),
    44: (118.37, 115.31, 224.64),
    45: (133.88, 134.88, 271.76),
    46: (152.10, 158.51, 330.35),
    47: (173.64, 187.21, 403.67),
    48: (199.26, 222.31, 496.01),
    49: (229.93, 265.51, 613.16),
    50: (266.89, 319.07, 762.89),
}


def meyerhof_N(phi_d_deg):
    """
    Devolve (Nc, Nq, Ngamma) interpolados linearmente da tabela Meyerhof.
    Suporta phi'_d em [0, 50] graus com passos de 1 grau.
    """
    if phi_d_deg <= 0:
        return _TAB[0]
    if phi_d_deg >= 50:
        return _TAB[50]

    phi_lo = int(math.floor(phi_d_deg))
    phi_hi = phi_lo + 1

    frac = phi_d_deg - phi_lo

    nc_lo, nq_lo, ng_lo = _TAB[phi_lo]
    nc_hi, nq_hi, ng_hi = _TAB[phi_hi]

    nc = nc_lo + frac * (nc_hi - nc_lo)
    nq = nq_lo + frac * (nq_hi - nq_lo)
    ng = ng_lo + frac * (ng_hi - ng_lo)

    return nc, nq, ng


def meyerhof_completo(phi_d_deg, c_d, q_efetivo, gamma_solo, B, Df=0.0,
                      B_L=1.0):
    """
    Capacidade de carga pelo metodo de Meyerhof (1963) com tabela.
    Devolve dict com q_ult, Nc, Nq, Ngamma, factores e termos.
    """
    Nc, Nq, Ngamma = meyerhof_N(phi_d_deg)
    phi_r = math.radians(phi_d_deg)

    # Factores de forma (DeBeer 1970)
    Fcs = 1.0 + B_L * (Nq / Nc) if Nc > 1e-6 else 1.0
    Fqs = 1.0 + B_L * math.tan(phi_r)
    Fgs = 1.0 - 0.4 * B_L

    # Factores de profundidade (Hansen 1970)
    if B <= 0:
        Fcd = Fqd = Fgd = 1.0
    else:
        Df_B = Df / B
        if Df_B <= 1.0:
            Fqd = 1.0 + 2.0 * math.tan(phi_r) * (1.0 - math.sin(phi_r)) ** 2 * Df_B
        else:
            Fqd = 1.0 + 2.0 * math.tan(phi_r) * (1.0 - math.sin(phi_r)) ** 2 * math.atan(Df_B)
        if phi_d_deg > 0.5 and Nc > 1e-6:
            Fcd = Fqd - (1.0 - Fqd) / (Nc * math.tan(phi_r))
        else:
            Fcd = 1.0 + 0.4 * Df_B
        Fgd = 1.0

    termo_c = c_d * Nc * Fcs * Fcd
    termo_q = q_efetivo * Nq * Fqs * Fqd
    termo_g = 0.5 * gamma_solo * B * Ngamma * Fgs * Fgd
    q_ult = termo_c + termo_q + termo_g

    return {
        "q_ult": q_ult,
        "Nc": Nc, "Nq": Nq, "Ngamma": Ngamma,
        "Fcs": Fcs, "Fqs": Fqs, "Fgs": Fgs,
        "Fcd": Fcd, "Fqd": Fqd, "Fgd": Fgd,
        "termo_c": termo_c, "termo_q": termo_q, "termo_g": termo_g,
    }