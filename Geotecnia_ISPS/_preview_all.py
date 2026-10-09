# -*- coding: utf-8 -*-
"""Gera previews HTML dos desenhos alterados (PT e EN)."""
import io
import sys

sys.path.insert(0, '.')
from paginas import sapatas_desenho as SD
from paginas import muros as MG

D = dict(Bx=2.0, By=2.5, bx=0.40, by=0.50, h=0.60, Df=1.20, WT=0.8,
         sigma1=145.0, sigma2=98.0, sigma_max=145.0, sigma_min=98.0,
         ex=0.06, ey=-0.04, eta_x=0.06, eta_y=0.032, Mx=18.5, My=12.3,
         As_x=14.82, As_y=11.85, diam_x=12, esp_x=150,
         arm_x="Ø12 c/c 150mm", arm_y="Ø10 c/c 200mm",
         arm_dist_x="1.20 m", arm_dist_y="1.10 m", d=0.50)


def sapatas(l):
    return [
        ('1. Convenção de momentos', SD.svg_convencao_momentos(l)),
        ('2. Planta', SD.svg_planta_sapata(
            D['Bx'], D['By'], D['bx'], D['by'], D['ex'], D['ey'],
            D['Mx'], D['My'], l)),
        ('3. Perfil', SD.svg_perfil_sapata(
            D['Bx'], D['bx'], D['h'], D['Df'], D['WT'], D['sigma1'],
            D['sigma2'], D['sigma_max'], D['sigma_min'], l)),
        ('4. Ponto resultante', SD.svg_ponto_resultante(
            D['Bx'], D['By'], D['ex'], D['ey'], D['eta_x'], D['eta_y'],
            True, l)),
        ('5. Punçoamento', SD.svg_puncoamento(
            D['Bx'], D['By'], D['bx'], D['by'], D['d'], l)),
        ('6. Disposições construtivas', SD.svg_disposicoes_construtivas(
            D['Bx'], D['bx'], D['h'], D['sigma1'], D['sigma2'],
            D['As_x'], D['As_y'], D['diam_x'], D['esp_x'], l)),
        ('7. Desenho final', SD.svg_final_sapata(
            D['Bx'], D['By'], D['bx'], D['by'], D['h'], D['arm_x'],
            D['arm_y'], D['arm_dist_x'], D['arm_dist_y'], l)),
    ]


def muros(l):
    return [
        ('Muro gravidade — Solo único c/ N.F.', MG._svg_esquema_muro_gravidade(
            H=5.0, B=3.5, a=1.0, i=0.0, gamma_sol=18.0, gamma_sat=20.0,
            phi=30.0, c_linha=0.0, q=10.0, z_w=2.0, gamma_fund=18.0,
            phi_fund=28.0, Ka=0.3333, tipo_solo='unico', W_d=412.5,
            IaH_d=45.0, U_d=24.0, lang=l)),
        ('Muro gravidade — Estratificados c/ N.F.',
         MG._svg_esquema_muro_gravidade(
             H=5.0, B=3.5, a=1.0, i=0.0, gamma_sol=17.0, gamma_sat=19.0,
             phi=28.0, c_linha=2.0, q=0.0, z_w=2.0, gamma_fund=18.0,
             phi_fund=30.0, Ka1=0.34, Ka2=0.30, tipo_solo='estratificado',
             H1=2.5, gamma1=17.0, gamma1_sat=19.0, gamma2=18.0,
             gamma2_sat=20.0, phi1=28.0, phi2=32.0, Ka=0.32, W_d=412.5,
             IaH_d=45.0, U_d=24.0, lang=l)),
        ('Muro gravidade — i = 20°', MG._svg_esquema_muro_gravidade(
            H=5.0, B=3.5, a=1.0, i=20.0, gamma_sol=18.0, gamma_sat=20.0,
            phi=30.0, c_linha=0.0, q=10.0, z_w=2.0, gamma_fund=18.0,
            phi_fund=28.0, Ka=0.3333, tipo_solo='unico', W_d=412.5,
            IaH_d=45.0, U_d=24.0, lang=l)),
    ]


html = ['<html><body style="background:#eef1f4;font-family:Segoe UI,Arial">']
for lang in ('pt', 'en'):
    html.append('<h1 style="color:#2c3e50">SAPATAS — %s</h1>' % lang.upper())
    for tit, svg in sapatas(lang):
        html.append('<h3>%s</h3>' % tit)
        html.append(svg)
    html.append('<h1 style="color:#2c3e50">MUROS DE GRAVIDADE — %s</h1>'
                % lang.upper())
    for tit, svg in muros(lang):
        html.append('<h3>%s</h3>' % tit)
        html.append(svg)
html.append('</body></html>')

io.open('_preview_all.html', 'w', encoding='utf-8').write('\n'.join(html))
print('escrito _preview_all.html')