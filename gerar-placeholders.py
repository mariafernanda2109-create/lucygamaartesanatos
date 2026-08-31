"""
Gera os placeholders SVG do ateliê Lucy Gama.
Formas orgânicas na paleta da marca, sem banco de imagem.
Rode só se precisar regerar: python3 gerar-placeholders.py
"""
import math, random, os

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img")

CREME = "#FFF9F5"
ROSA = "#F6D6DF"
LILAS = "#DCCEF2"
AZUL = "#C9E3F2"
AMARELO = "#F8E7A9"
ROXO = "#59446F"
ROSA_Q = "#B86F89"
GRAFITE = "#302B32"


def blob(cx, cy, r, semente, irregularidade=0.22, pontos=8):
    rnd = random.Random(semente)
    raios = [r * (1 + rnd.uniform(-irregularidade, irregularidade)) for _ in range(pontos)]
    pts = []
    for i, rr in enumerate(raios):
        a = 2 * math.pi * i / pontos
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = ""
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        if i == 0:
            d += f"M{xm:.1f},{ym:.1f} "
        x2, y2 = pts[(i + 1) % n]
        xm2, ym2 = (x1 + pts[(i + 2) % n][0]) / 2, (y1 + pts[(i + 2) % n][1]) / 2
        d += f"Q{x1:.1f},{y1:.1f} {xm2:.1f},{ym2:.1f} "
    return d + "Z"


def a_orelha(r):
    """Altura de onde a orelha caída sai da cabeça."""
    return r * 0.28


def silhueta(tipo, w, h, cor):
    """Silhuetas discretas, sem traço infantil: só a forma, em baixa opacidade,
    apoiada numa linha de bancada."""
    cx, cy = w / 2, h / 2
    s = min(w, h)
    base = cy + s * 0.34          # linha da bancada
    op = ".62"
    p = [f'<line x1="0" y1="{base:.1f}" x2="{w}" y2="{base:.1f}" stroke="{GRAFITE}" stroke-width="{s*0.004:.1f}" opacity=".13"/>',
         f'<ellipse cx="{cx:.1f}" cy="{base:.1f}" rx="{s*0.30:.1f}" ry="{s*0.026:.1f}" fill="{GRAFITE}" opacity=".07"/>']

    def _pop(px, esc, opac):
        """Uma figura Pop: corpo trapezoidal, cabeça grande e uma franja discreta."""
        r = s * 0.185 * esc
        topo = base - s * 0.235 * esc
        larg = s * 0.155 * esc
        ombro = s * 0.085 * esc
        return [
            f'<path d="M{px-larg:.1f},{base:.1f} '
            f'C{px-larg*0.97:.1f},{topo+s*0.03*esc:.1f} {px-larg*0.77:.1f},{topo:.1f} {px-ombro:.1f},{topo:.1f} '
            f'L{px+ombro:.1f},{topo:.1f} '
            f'C{px+larg*0.77:.1f},{topo:.1f} {px+larg*0.97:.1f},{topo+s*0.03*esc:.1f} {px+larg:.1f},{base:.1f} Z" '
            f'fill="{cor}" opacity="{opac}"/>',
            f'<circle cx="{px:.1f}" cy="{topo - r*0.86:.1f}" r="{r:.1f}" fill="{cor}" opacity="{opac}"/>',
            f'<path d="M{px-r*0.55:.1f},{topo-r*1.32:.1f} C{px-r*0.20:.1f},{topo-r*1.50:.1f} {px+r*0.20:.1f},{topo-r*1.50:.1f} {px+r*0.55:.1f},{topo-r*1.32:.1f}" '
            f'fill="none" stroke="{CREME}" stroke-width="{s*0.012*esc:.1f}" stroke-linecap="round" opacity=".55"/>',
        ]

    def _cachorro(px, esc, opac):
        """Cãozinho sentado de frente: mesma linguagem da cabeça do Pop de pet,
        para ler bem mesmo em miniatura."""
        a = s * 0.20 * esc
        chy = base - a * 0.80                       # centro da cabeça
        r = a * 0.42
        return [
            f'<path d="M{px-a*0.34:.1f},{base:.1f} '
            f'C{px-a*0.38:.1f},{base-a*0.58:.1f} {px+a*0.38:.1f},{base-a*0.58:.1f} {px+a*0.34:.1f},{base:.1f} Z" '
            f'fill="{cor}" opacity="{opac}"/>',
            f'<circle cx="{px:.1f}" cy="{chy:.1f}" r="{r:.1f}" fill="{cor}" opacity="{opac}"/>',
            f'<path d="M{px-r*0.92:.1f},{chy-r*0.26:.1f} C{px-r*1.34:.1f},{chy+r*0.30:.1f} {px-r*1.00:.1f},{chy+r*0.80:.1f} {px-r*0.60:.1f},{chy+r*0.58:.1f} Z" '
            f'fill="{cor}" opacity="{opac}"/>',
            f'<path d="M{px+r*0.92:.1f},{chy-r*0.26:.1f} C{px+r*1.34:.1f},{chy+r*0.30:.1f} {px+r*1.00:.1f},{chy+r*0.80:.1f} {px+r*0.60:.1f},{chy+r*0.58:.1f} Z" '
            f'fill="{cor}" opacity="{opac}"/>',
            f'<ellipse cx="{px:.1f}" cy="{chy+r*0.40:.1f}" rx="{r*0.38:.1f}" ry="{r*0.27:.1f}" fill="{CREME}" opacity=".55"/>',
            f'<ellipse cx="{px:.1f}" cy="{chy+r*0.26:.1f}" rx="{r*0.12:.1f}" ry="{r*0.09:.1f}" fill="{cor}" opacity=".9"/>',
        ]

    if tipo == "pop":
        rc = s * 0.185
        topo = base - s * 0.235
        p.append(f'<path d="M{cx-s*0.155:.1f},{base:.1f} '
                 f'C{cx-s*0.150:.1f},{topo+s*0.03:.1f} {cx-s*0.120:.1f},{topo:.1f} {cx-s*0.085:.1f},{topo:.1f} '
                 f'L{cx+s*0.085:.1f},{topo:.1f} '
                 f'C{cx+s*0.120:.1f},{topo:.1f} {cx+s*0.150:.1f},{topo+s*0.03:.1f} {cx+s*0.155:.1f},{base:.1f} Z" '
                 f'fill="{cor}" opacity="{op}"/>')
        p.append(f'<circle cx="{cx:.1f}" cy="{topo - rc*0.86:.1f}" r="{rc:.1f}" fill="{cor}" opacity="{op}"/>')
        p.append(f'<path d="M{cx-rc*0.55:.1f},{topo-rc*1.32:.1f} C{cx-rc*0.20:.1f},{topo-rc*1.50:.1f} {cx+rc*0.20:.1f},{topo-rc*1.50:.1f} {cx+rc*0.55:.1f},{topo-rc*1.32:.1f}" '
                 f'fill="none" stroke="{CREME}" stroke-width="{s*0.012:.1f}" stroke-linecap="round" opacity=".55"/>')
    elif tipo == "pop_casal":
        # duas figuras lado a lado, uma um pouco mais alta que a outra
        p += _pop(cx - s * 0.150, 0.84, ".50")   # figura de trás, um pouco menor
        p += _pop(cx + s * 0.150, 0.94, ".66")   # figura da frente
        hx, hy, hr = cx, base - s * 0.480, s * 0.032
        p.append(f'<path d="M{hx:.1f},{hy+hr*1.1:.1f} '
                 f'C{hx-hr*1.9:.1f},{hy-hr*0.25:.1f} {hx-hr*0.75:.1f},{hy-hr*1.5:.1f} {hx:.1f},{hy-hr*0.45:.1f} '
                 f'C{hx+hr*0.75:.1f},{hy-hr*1.5:.1f} {hx+hr*1.9:.1f},{hy-hr*0.25:.1f} {hx:.1f},{hy+hr*1.1:.1f} Z" '
                 f'fill="{AMARELO}"/>')
    elif tipo == "pop_pet_solo":
        # o próprio pet virou Pop: cabeça grande de cachorro sobre o corpo
        corpo_cabeca = _pop(cx, 0.92, ".60")[:2]      # sem a franja do Pop humano
        p += corpo_cabeca
        r = s * 0.185 * 0.92
        topo = base - s * 0.235 * 0.92
        cyc = topo - r * 0.86
        p.append(f'<path d="M{cx-r*0.94:.1f},{cyc-a_orelha(r):.1f} C{cx-r*1.30:.1f},{cyc+r*0.30:.1f} {cx-r*1.00:.1f},{cyc+r*0.76:.1f} {cx-r*0.62:.1f},{cyc+r*0.58:.1f} Z" '
                 f'fill="{cor}" opacity=".70"/>')
        p.append(f'<path d="M{cx+r*0.94:.1f},{cyc-a_orelha(r):.1f} C{cx+r*1.30:.1f},{cyc+r*0.30:.1f} {cx+r*1.00:.1f},{cyc+r*0.76:.1f} {cx+r*0.62:.1f},{cyc+r*0.58:.1f} Z" '
                 f'fill="{cor}" opacity=".70"/>')
        p.append(f'<circle cx="{cx-r*0.34:.1f}" cy="{cyc-r*0.12:.1f}" r="{r*0.085:.1f}" fill="{CREME}" opacity=".75"/>')
        p.append(f'<circle cx="{cx+r*0.34:.1f}" cy="{cyc-r*0.12:.1f}" r="{r*0.085:.1f}" fill="{CREME}" opacity=".75"/>')
        p.append(f'<ellipse cx="{cx:.1f}" cy="{cyc+r*0.42:.1f}" rx="{r*0.38:.1f}" ry="{r*0.26:.1f}" fill="{CREME}" opacity=".55"/>')
        p.append(f'<ellipse cx="{cx:.1f}" cy="{cyc+r*0.28:.1f}" rx="{r*0.11:.1f}" ry="{r*0.08:.1f}" fill="{cor}" opacity=".9"/>')
    elif tipo == "pop_pet":
        # uma figura e o pet ao lado
        p += _pop(cx - s * 0.085, 0.94, ".64")
        p += _cachorro(cx + s * 0.250, 1.15, ".58")
    elif tipo == "pop_casal_pet":
        # casal e o pet junto, os três na mesma base
        p += _pop(cx - s * 0.205, 0.82, ".48")
        p += _pop(cx + s * 0.030, 0.92, ".64")
        p += _cachorro(cx + s * 0.268, 0.92, ".58")
        hx, hy, hr = cx - s * 0.088, base - s * 0.470, s * 0.030
        p.append(f'<path d="M{hx:.1f},{hy+hr*1.1:.1f} '
                 f'C{hx-hr*1.9:.1f},{hy-hr*0.25:.1f} {hx-hr*0.75:.1f},{hy-hr*1.5:.1f} {hx:.1f},{hy-hr*0.45:.1f} '
                 f'C{hx+hr*0.75:.1f},{hy-hr*1.5:.1f} {hx+hr*1.9:.1f},{hy-hr*0.25:.1f} {hx:.1f},{hy+hr*1.1:.1f} Z" '
                 f'fill="{AMARELO}"/>')
    elif tipo == "qposket":
        # figura esbelta sobre base redonda, silhueta bem diferente da do pop
        cabeca = base - s * 0.475
        cintura = base - s * 0.245
        ombro = base - s * 0.385
        # base / peanha
        p.append(f'<ellipse cx="{cx:.1f}" cy="{base-s*0.012:.1f}" rx="{s*0.125:.1f}" ry="{s*0.028:.1f}" fill="{cor}" opacity=".45"/>')
        p.append(f'<path d="M{cx-s*0.125:.1f},{base-s*0.055:.1f} L{cx-s*0.125:.1f},{base-s*0.012:.1f} '
                 f'C{cx-s*0.125:.1f},{base+s*0.016:.1f} {cx+s*0.125:.1f},{base+s*0.016:.1f} {cx+s*0.125:.1f},{base-s*0.012:.1f} '
                 f'L{cx+s*0.125:.1f},{base-s*0.055:.1f} Z" fill="{cor}" opacity="{op}"/>')
        # saia rodada
        p.append(f'<path d="M{cx-s*0.048:.1f},{cintura:.1f} '
                 f'C{cx-s*0.105:.1f},{cintura+s*0.10:.1f} {cx-s*0.165:.1f},{base-s*0.10:.1f} {cx-s*0.150:.1f},{base-s*0.055:.1f} '
                 f'C{cx-s*0.075:.1f},{base-s*0.020:.1f} {cx+s*0.075:.1f},{base-s*0.020:.1f} {cx+s*0.150:.1f},{base-s*0.055:.1f} '
                 f'C{cx+s*0.165:.1f},{base-s*0.10:.1f} {cx+s*0.105:.1f},{cintura+s*0.10:.1f} {cx+s*0.048:.1f},{cintura:.1f} Z" '
                 f'fill="{cor}" opacity="{op}"/>')
        # tronco
        p.append(f'<path d="M{cx-s*0.030:.1f},{ombro-s*0.030:.1f} '
                 f'C{cx-s*0.082:.1f},{ombro-s*0.020:.1f} {cx-s*0.086:.1f},{ombro+s*0.030:.1f} {cx-s*0.062:.1f},{cintura+s*0.01:.1f} '
                 f'L{cx+s*0.062:.1f},{cintura+s*0.01:.1f} '
                 f'C{cx+s*0.086:.1f},{ombro+s*0.030:.1f} {cx+s*0.082:.1f},{ombro-s*0.020:.1f} {cx+s*0.030:.1f},{ombro-s*0.030:.1f} Z" '
                 f'fill="{cor}" opacity="{op}"/>')
        # cabelo por trás, depois cabeça
        p.append(f'<path d="M{cx-s*0.108:.1f},{cabeca+s*0.02:.1f} '
                 f'C{cx-s*0.115:.1f},{cabeca-s*0.115:.1f} {cx+s*0.115:.1f},{cabeca-s*0.115:.1f} {cx+s*0.108:.1f},{cabeca+s*0.02:.1f} '
                 f'C{cx+s*0.112:.1f},{cabeca+s*0.13:.1f} {cx+s*0.080:.1f},{cabeca+s*0.16:.1f} {cx+s*0.066:.1f},{cabeca+s*0.10:.1f} '
                 f'L{cx-s*0.066:.1f},{cabeca+s*0.10:.1f} '
                 f'C{cx-s*0.080:.1f},{cabeca+s*0.16:.1f} {cx-s*0.112:.1f},{cabeca+s*0.13:.1f} {cx-s*0.108:.1f},{cabeca+s*0.02:.1f} Z" '
                 f'fill="{cor}" opacity=".78"/>')
        p.append(f'<circle cx="{cx:.1f}" cy="{cabeca:.1f}" r="{s*0.082:.1f}" fill="{cor}" opacity="{op}"/>')
        p.append(f'<path d="M{cx-s*0.075:.1f},{cabeca-s*0.026:.1f} C{cx-s*0.030:.1f},{cabeca-s*0.088:.1f} {cx+s*0.030:.1f},{cabeca-s*0.088:.1f} {cx+s*0.075:.1f},{cabeca-s*0.026:.1f} '
                 f'C{cx+s*0.040:.1f},{cabeca-s*0.052:.1f} {cx-s*0.040:.1f},{cabeca-s*0.052:.1f} {cx-s*0.075:.1f},{cabeca-s*0.026:.1f} Z" fill="{cor}" opacity=".85"/>')
    elif tipo == "vaso":
        topo = base - s * 0.60
        p.append(f'<path d="M{cx-s*0.075:.1f},{topo:.1f} '
                 f'C{cx-s*0.080:.1f},{topo+s*0.09:.1f} {cx-s*0.215:.1f},{topo+s*0.20:.1f} {cx-s*0.215:.1f},{topo+s*0.38:.1f} '
                 f'C{cx-s*0.215:.1f},{base-s*0.02:.1f} {cx-s*0.115:.1f},{base:.1f} {cx-s*0.095:.1f},{base:.1f} '
                 f'L{cx+s*0.095:.1f},{base:.1f} '
                 f'C{cx+s*0.115:.1f},{base:.1f} {cx+s*0.215:.1f},{base-s*0.02:.1f} {cx+s*0.215:.1f},{topo+s*0.38:.1f} '
                 f'C{cx+s*0.215:.1f},{topo+s*0.20:.1f} {cx+s*0.080:.1f},{topo+s*0.09:.1f} {cx+s*0.075:.1f},{topo:.1f} Z" '
                 f'fill="{cor}" opacity="{op}"/>')
        p.append(f'<ellipse cx="{cx:.1f}" cy="{topo:.1f}" rx="{s*0.075:.1f}" ry="{s*0.020:.1f}" fill="{CREME}" opacity=".45"/>')
        p.append(f'<path d="M{cx-s*0.135:.1f},{topo+s*0.40:.1f} C{cx-s*0.05:.1f},{topo+s*0.44:.1f} {cx+s*0.05:.1f},{topo+s*0.44:.1f} {cx+s*0.135:.1f},{topo+s*0.40:.1f}" '
                 f'fill="none" stroke="{CREME}" stroke-width="{s*0.013:.1f}" stroke-linecap="round" opacity=".5"/>')
    elif tipo == "tigela":
        boca = base - s * 0.24
        p.append(f'<path d="M{cx-s*0.28:.1f},{boca:.1f} '
                 f'C{cx-s*0.26:.1f},{base:.1f} {cx+s*0.26:.1f},{base:.1f} {cx+s*0.28:.1f},{boca:.1f} Z" fill="{cor}" opacity="{op}"/>')
        p.append(f'<ellipse cx="{cx:.1f}" cy="{boca:.1f}" rx="{s*0.28:.1f}" ry="{s*0.048:.1f}" fill="{cor}" opacity=".34"/>')
        p.append(f'<ellipse cx="{cx:.1f}" cy="{boca:.1f}" rx="{s*0.28:.1f}" ry="{s*0.048:.1f}" fill="none" stroke="{CREME}" stroke-width="{s*0.010:.1f}" opacity=".45"/>')
    elif tipo == "escultura":
        topo = base - s * 0.66
        p.append(f'<path d="M{cx-s*0.105:.1f},{base:.1f} '
                 f'C{cx-s*0.185:.1f},{base-s*0.22:.1f} {cx-s*0.030:.1f},{base-s*0.30:.1f} {cx-s*0.070:.1f},{topo+s*0.16:.1f} '
                 f'C{cx-s*0.105:.1f},{topo:.1f} {cx+s*0.095:.1f},{topo-s*0.02:.1f} {cx+s*0.100:.1f},{topo+s*0.17:.1f} '
                 f'C{cx+s*0.105:.1f},{base-s*0.30:.1f} {cx+s*0.020:.1f},{base-s*0.20:.1f} {cx+s*0.090:.1f},{base:.1f} Z" '
                 f'fill="{cor}" opacity="{op}"/>')
        p.append(f'<circle cx="{cx+s*0.020:.1f}" cy="{topo+s*0.11:.1f}" r="{s*0.034:.1f}" fill="{CREME}" opacity=".45"/>')
    elif tipo == "artista":
        topo = base - s * 0.62
        p.append(f'<circle cx="{cx-s*0.02:.1f}" cy="{topo+s*0.10:.1f}" r="{s*0.112:.1f}" fill="{cor}" opacity="{op}"/>')
        p.append(f'<path d="M{cx-s*0.255:.1f},{base:.1f} '
                 f'C{cx-s*0.235:.1f},{topo+s*0.30:.1f} {cx-s*0.130:.1f},{topo+s*0.21:.1f} {cx-s*0.02:.1f},{topo+s*0.21:.1f} '
                 f'C{cx+s*0.115:.1f},{topo+s*0.21:.1f} {cx+s*0.225:.1f},{topo+s*0.30:.1f} {cx+s*0.245:.1f},{base:.1f} Z" '
                 f'fill="{cor}" opacity="{op}"/>')
        p.append(f'<path d="M{cx+s*0.20:.1f},{topo+s*0.33:.1f} C{cx+s*0.24:.1f},{topo+s*0.47:.1f} {cx+s*0.15:.1f},{topo+s*0.52:.1f} {cx+s*0.075:.1f},{topo+s*0.50:.1f}" '
                 f'fill="none" stroke="{cor}" stroke-width="{s*0.052:.1f}" stroke-linecap="round" opacity="{op}"/>')
        p.append(f'<circle cx="{cx+s*0.045:.1f}" cy="{topo+s*0.50:.1f}" r="{s*0.055:.1f}" fill="{AMARELO}" opacity=".8"/>')
    elif tipo == "bancada":
        # três peças em alturas diferentes, como numa prateleira do ateliê
        px = cx - s * 0.30
        p.append(f'<path d="M{px-s*0.055:.1f},{base:.1f} C{px-s*0.058:.1f},{base-s*0.20:.1f} {px-s*0.020:.1f},{base-s*0.19:.1f} {px-s*0.028:.1f},{base-s*0.29:.1f} '
                 f'C{px-s*0.033:.1f},{base-s*0.36:.1f} {px+s*0.033:.1f},{base-s*0.36:.1f} {px+s*0.028:.1f},{base-s*0.29:.1f} '
                 f'C{px+s*0.020:.1f},{base-s*0.19:.1f} {px+s*0.058:.1f},{base-s*0.20:.1f} {px+s*0.055:.1f},{base:.1f} Z" fill="{cor}" opacity="{op}"/>')
        p.append(f'<path d="M{cx-s*0.13:.1f},{base:.1f} C{cx-s*0.145:.1f},{base-s*0.30:.1f} {cx-s*0.02:.1f},{base-s*0.27:.1f} {cx-s*0.045:.1f},{base-s*0.44:.1f} '
                 f'C{cx-s*0.060:.1f},{base-s*0.54:.1f} {cx+s*0.075:.1f},{base-s*0.54:.1f} {cx+s*0.065:.1f},{base-s*0.42:.1f} '
                 f'C{cx+s*0.050:.1f},{base-s*0.26:.1f} {cx+s*0.125:.1f},{base-s*0.28:.1f} {cx+s*0.115:.1f},{base:.1f} Z" fill="{cor}" opacity="{op}"/>')
        px = cx + s * 0.30
        p.append(f'<path d="M{px-s*0.105:.1f},{base-s*0.115:.1f} C{px-s*0.098:.1f},{base:.1f} {px+s*0.098:.1f},{base:.1f} {px+s*0.105:.1f},{base-s*0.115:.1f} Z" fill="{cor}" opacity="{op}"/>')
        p.append(f'<ellipse cx="{px:.1f}" cy="{base-s*0.115:.1f}" rx="{s*0.105:.1f}" ry="{s*0.022:.1f}" fill="{cor}" opacity=".34"/>')
        p.append(f'<circle cx="{cx-s*0.30:.1f}" cy="{base-s*0.42:.1f}" r="{s*0.030:.1f}" fill="{AMARELO}" opacity=".85"/>')
    return "\n  ".join(p)


def gerar(nome, w, h, tipo, fundo, blobs, cor_peca, rotulo, semente):
    partes = [f'<rect width="{w}" height="{h}" fill="{fundo}"/>']
    rnd = random.Random(semente)
    for i, (cor, op) in enumerate(blobs):
        cx = rnd.uniform(w * 0.15, w * 0.85)
        cy = rnd.uniform(h * 0.15, h * 0.85)
        r = min(w, h) * rnd.uniform(0.30, 0.52)
        partes.append(f'<path d="{blob(cx, cy, r, semente + i * 7)}" fill="{cor}" opacity="{op}"/>')
    partes.append(silhueta(tipo, w, h, cor_peca))
    # pinceladas finas
    partes.append(f'<path d="M{w*0.08:.0f},{h*0.90:.0f} C{w*0.22:.0f},{h*0.84:.0f} {w*0.34:.0f},{h*0.95:.0f} {w*0.46:.0f},{h*0.89:.0f}" '
                  f'fill="none" stroke="{ROXO}" stroke-width="{min(w,h)*0.006:.1f}" stroke-linecap="round" opacity=".22"/>')
    partes.append(f'<circle cx="{w*0.86:.0f}" cy="{h*0.12:.0f}" r="{min(w,h)*0.018:.1f}" fill="{AMARELO}"/>')
    fonte = min(w, h) * 0.036
    partes.append(f'<text x="{w*0.06:.0f}" y="{h*0.955:.0f}" font-family="Manrope, system-ui, sans-serif" '
                  f'font-size="{fonte:.0f}" fill="{GRAFITE}" opacity=".45" letter-spacing="{fonte*0.06:.1f}">{rotulo}</text>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">\n  '
           + "\n  ".join(partes) + "\n</svg>\n")
    with open(os.path.join(SAIDA, nome), "w", encoding="utf-8") as f:
        f.write(svg)


PECAS = [
    # nome, w, h, tipo, fundo, blobs, cor da peça, rótulo, semente
    # o hero usa foto real (assets/img/hero.webp); o placeholder abaixo fica só de reserva
    ("hero-reserva.svg", 900, 1080, "pop", CREME, [(ROSA, .85), (LILAS, .55), (AMARELO, .45)], ROSA_Q, "peça no ateliê", 11),
    # a seção sobre usa foto real (assets/img/lucy-atelie.webp); placeholder de reserva
    ("lucy-atelie-reserva.svg", 720, 900, "artista", "#FBEFF2", [(LILAS, .5), (AZUL, .45)], ROXO, "Lucy no ateliê", 23),
    # o bloco de Pops usa foto real (assets/img/servico-pop.webp); placeholder de reserva
    ("servico-pop-reserva.svg", 800, 640, "pop", "#FDF3F6", [(ROSA, .8), (AMARELO, .35)], ROSA_Q, "Pop personalizado", 31),
    # o bloco de Qposkets usa foto real (assets/img/servico-qposket.webp); placeholder de reserva
    ("servico-qposket-reserva.svg", 800, 640, "qposket", "#FBF6E9", [(AMARELO, .7), (ROSA, .35)], ROSA_Q, "Qposket personalizado", 103),
    # o bloco de cerâmica usa foto real (assets/img/servico-ceramica.webp); placeholder de reserva
    ("servico-ceramica-reserva.svg", 800, 640, "vaso", "#F5F1FB", [(LILAS, .8), (ROSA, .3)], ROXO, "peça em cerâmica", 37),
    # o bloco de esculturas usa foto real (assets/img/servico-escultura.webp); placeholder de reserva
    ("servico-escultura-reserva.svg", 800, 640, "escultura", "#EFF6FB", [(AZUL, .85), (LILAS, .35)], ROXO, "escultura autoral", 41),
    # esta peça usa foto real (assets/img/obra-01.webp); placeholder de reserva
    ("obra-01-reserva.svg", 800, 1000, "pop", "#FDF3F6", [(ROSA, .8), (AMARELO, .3)], ROSA_Q, "Pop sob encomenda", 53),
    # esta peça usa foto real (assets/img/obra-02.webp); placeholder de reserva
    ("obra-02-reserva.svg", 900, 700, "vaso", "#F5F1FB", [(LILAS, .75)], ROXO, "utilitários", 59),
    # esta peça usa foto real (assets/img/obra-03.webp); placeholder de reserva
    ("obra-03-reserva.svg", 800, 800, "tigela", "#EFF6FB", [(AZUL, .8), (AMARELO, .25)], ROXO, "prato esmaltado", 61),
    # esta peça usa foto real (assets/img/obra-04.webp); placeholder de reserva
    ("obra-04-reserva.svg", 800, 1000, "escultura", "#FBF6E9", [(AMARELO, .7), (ROSA, .35)], ROSA_Q, "escultura em resina", 67),
    # esta peça usa foto real (assets/img/obra-05.webp); placeholder de reserva
    ("obra-05-reserva.svg", 900, 700, "bancada", "#FDF3F6", [(ROSA, .7), (LILAS, .4)], ROXO, "processo manual", 71),
    # esta peça usa foto real (assets/img/obra-06.webp); placeholder de reserva
    ("obra-06-reserva.svg", 800, 800, "pop", "#F5F1FB", [(LILAS, .8), (AZUL, .3)], ROSA_Q, "Pop de pet", 73),
    # esta peça usa foto real (assets/img/obra-07.webp); placeholder de reserva
    ("obra-07-reserva.svg", 800, 1000, "vaso", "#EFF6FB", [(AZUL, .75), (ROSA, .3)], ROXO, "cerâmica utilitária", 79),
    # esta peça usa foto real (assets/img/obra-08.webp); placeholder de reserva
    ("obra-08-reserva.svg", 900, 700, "escultura", "#FDF3F6", [(ROSA, .75), (AMARELO, .3)], ROXO, "peça autoral", 83),
    ("obra-09.svg", 800, 800, "tigela", "#FBF6E9", [(AMARELO, .65), (LILAS, .35)], ROSA_Q, "conjunto sob encomenda", 89),
    ("obra-10.svg", 800, 1000, "qposket", "#FBF6E9", [(AMARELO, .7), (LILAS, .3)], ROSA_Q, "Qposket sob encomenda", 107),
    # esta peça usa foto real (assets/img/obra-11.webp); placeholder de reserva
    ("obra-11-reserva.svg", 800, 800, "qposket", "#FDF3F6", [(ROSA, .75), (AZUL, .3)], ROXO, "Qposket autoral", 109),
    # esta peça usa foto real (assets/img/obra-12.webp); placeholder de reserva
    ("obra-12-reserva.svg", 900, 700, "pop_casal", "#FDF3F6", [(ROSA, .8), (AMARELO, .3)], ROSA_Q, "Pop de casal", 113),
    # esta peça usa foto real (assets/img/obra-14.webp); placeholder de reserva
    ("obra-14-reserva.svg", 800, 800, "pop_pet_solo", "#FDF3F6", [(ROSA, .8), (AMARELO, .3)], ROSA_Q, "Pop de pet", 127),
    # esta peça usa foto real (assets/img/obra-15.webp); placeholder de reserva
    ("obra-15-reserva.svg", 900, 700, "pop_casal", "#FBF6E9", [(AMARELO, .7), (ROSA, .3)], ROSA_Q, "Pop de casal", 131),
    # esta peça usa foto real (assets/img/obra-16.webp); placeholder de reserva
    ("obra-16-reserva.svg", 800, 1000, "pop_casal", "#EFF6FB", [(AZUL, .8), (LILAS, .3)], ROXO, "Pop de casal", 137),
    ("obra-17.svg", 900, 700, "pop_casal_pet", "#F5F1FB", [(LILAS, .8), (ROSA, .3)], ROXO, "Pop de casal com pet", 139),
    ("obra-18.svg", 800, 1000, "pop_pet", "#FDF3F6", [(ROSA, .75), (AZUL, .3)], ROSA_Q, "Pop com pet", 149),
    ("cta-final.svg", 1600, 900, "bancada", "#F7EEF1", [(ROSA, .8), (LILAS, .5), (AMARELO, .35)], ROXO, "bancada do ateliê", 97),
]

os.makedirs(SAIDA, exist_ok=True)
for peca in PECAS:
    gerar(*peca)

# favicon simples
with open(os.path.join(SAIDA, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<rect width="64" height="64" rx="16" fill="{ROXO}"/>'
            f'<path d="M22 18v22h20" fill="none" stroke="{CREME}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="45" cy="21" r="5" fill="{AMARELO}"/></svg>\n')

print("\n".join(sorted(os.listdir(SAIDA))))
