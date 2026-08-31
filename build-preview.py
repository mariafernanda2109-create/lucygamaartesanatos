"""
Gera as versões single-file a partir dos arquivos separados.
Os arquivos separados continuam sendo a fonte da verdade.

    python3 build-preview.py

Saída:
  preview/lucy-gama-artesanatos.html  -> documento completo, abre em qualquer lugar
  preview/artifact.html               -> só o conteúdo, para publicar como artifact
"""
import base64, os, re, urllib.parse

RAIZ = os.path.dirname(os.path.abspath(__file__))
PREVIEW = os.path.join(RAIZ, "preview")
os.makedirs(PREVIEW, exist_ok=True)

html = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
css = open(os.path.join(RAIZ, "assets/css/style.css"), encoding="utf-8").read()
js = open(os.path.join(RAIZ, "assets/js/main.js"), encoding="utf-8").read()


TIPOS = {".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".png": "image/png", ".avif": "image/avif"}


def img_data_uri(caminho_rel):
    caminho = os.path.join(RAIZ, caminho_rel)
    ext = os.path.splitext(caminho)[1].lower()

    if not os.path.exists(caminho):
        # arquivo citado no HTML mas ausente: avisa e mantém o caminho relativo
        print("  aviso: %s não existe, mantido como caminho relativo" % caminho_rel)
        return caminho_rel

    if ext == ".svg":
        with open(caminho, encoding="utf-8") as f:
            svg = f.read()
        return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg, safe="")

    with open(caminho, "rb") as f:
        dados = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (TIPOS.get(ext, "application/octet-stream"), dados)


# imagens viram data URI
def troca_src(m):
    return 'src="%s"' % img_data_uri(m.group(1))


saida = re.sub(r'src="(assets/img/[^"]+)"', troca_src, html)
saida = re.sub(r'href="assets/img/favicon\.svg"', 'href="%s"' % img_data_uri("assets/img/favicon.svg"), saida)

# CSS e JS inline
saida = saida.replace(
    '<link rel="stylesheet" href="assets/css/style.css">',
    "<style>\n%s\n</style>" % css,
)
saida = saida.replace(
    '<script src="assets/js/main.js"></script>',
    "<script>\n%s\n</script>" % js,
)

with open(os.path.join(PREVIEW, "lucy-gama-artesanatos.html"), "w", encoding="utf-8") as f:
    f.write(saida)

# versão artifact: sem doctype/html/head/body, mantendo title, style e conteúdo
cabeca = re.search(r"<head>(.*?)</head>", saida, re.S).group(1)
corpo = re.search(r"<body>(.*?)</body>", saida, re.S).group(1)

manter = []
for padrao in [r"<title>.*?</title>", r'<link rel="preconnect".*?>', r'<link href="https://fonts\.googleapis[^>]*>',
               r"<style>.*?</style>"]:
    manter += re.findall(padrao, cabeca, re.S)

cabeca_artifact = "\n".join(manter).replace(
    "<title>Lucy Gama Artesanatos | Funko Pops, Cerâmica e Esculturas</title>",
    "<title>Lucy Gama Artesanatos</title>",
)

with open(os.path.join(PREVIEW, "artifact.html"), "w", encoding="utf-8") as f:
    f.write(cabeca_artifact + "\n" + corpo.strip() + "\n")

for nome in ["lucy-gama-artesanatos.html", "artifact.html"]:
    caminho = os.path.join(PREVIEW, nome)
    print(nome, round(os.path.getsize(caminho) / 1024, 1), "KB")
