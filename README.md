# Lucy Gama Artesanatos

Landing page do ateliê Lucy Gama Artesanatos — Pops e Qposkets personalizados, peças em cerâmica e esculturas autorais. Objetivo único da página: gerar conversas no WhatsApp.

HTML, CSS e JavaScript puros. GSAP por CDN. Sem build, sem npm: dá para abrir o `index.html` com dois cliques e publicar direto na Vercel.

## Estrutura

```
lucy-gama-artesanatos/
├── index.html
├── assets/
│   ├── css/style.css
│   ├── js/main.js
│   └── img/            placeholders SVG (trocar por fotos reais)
├── gerar-placeholders.py   só para regerar os placeholders
├── robots.txt
├── .gitignore
└── README.md
```

## O que trocar antes de publicar

1. **Número do WhatsApp** — está como `5543988290831` (o número informado, `43 8829-0831`, com o 9 de celular na frente). Confira e, se precisar, troque tudo de uma vez:
   `find . -name "*.html" -exec sed -i '' 's/5543988290831/55SEUNUMERO/g' {} +`
2. **Fotos** — já são fotos reais: `hero.webp` (Lucy com o Pop da Frida), `lucy-atelie.webp` (Lucy modelando em argila), `servico-pop.webp` (Pop do Dr. Rodolfo), `servico-qposket.webp`, `servico-ceramica.webp` e `servico-escultura.webp`. Os quatro blocos de serviço já estão com foto real. O resto de `assets/img/` ainda é placeholder gráfico na paleta da marca — faltam as 12 peças do portfólio e o fundo do CTA final. Substitua pelos arquivos reais em WebP mantendo os mesmos nomes, ou atualize o `src`, o `alt`, o `width` e o `height` no HTML — as dimensões declaradas evitam o pulo de layout que o Core Web Vitals penaliza.
3. **Domínio** — trocar `https://lucygamaartesanatos.com.br` no `canonical`, no Open Graph, no JSON-LD e no `robots.txt`.
4. **Instagram** — `https://www.instagram.com/lucygartesanatos`, no rodapé e no `sameAs` do JSON-LD.
5. **Cidade e UF** — confirmado: Londrina/PR. Aparece no JSON-LD (`LocalBusiness` e `areaServed`), na meta description, no Open Graph e no rodapé.
6. **`og.jpg`** — gerar uma imagem de compartilhamento 1200x630 em `assets/img/og.jpg`.
7. **Depoimentos** — a seção existe no HTML, comentada. Só publique com depoimento real, nome e autorização.

## Publicar

```bash
git init
git add .
git commit -m "Landing page Lucy Gama Artesanatos"
git branch -M main
git remote add origin git@github.com:USUARIO/lucy-gama-artesanatos.git
git push -u origin main
```

Na Vercel: **Add New → Project → importar o repositório**. Framework Preset `Other`, sem build command, output directory na raiz. Todo push na `main` republica sozinho.

## Paleta

| token | cor | uso |
| --- | --- | --- |
| `--creme` | `#FFF9F5` | fundo predominante |
| `--rosa` | `#F6D6DF` | seção sobre e CTA intermediário |
| `--lilas` | `#DCCEF2` | diferenciais |
| `--azul` | `#C9E3F2` | FAQ |
| `--amarelo` | `#F8E7A9` | destaques e números |
| `--roxo` | `#59446F` | títulos e identidade |
| `--rosa-queimado` | `#B86F89` | rótulos e detalhes |
| `--cta` | `#A85C79` | botões principais |
| `--grafite` | `#302B32` | texto |

O `--cta` é o rosa queimado um tom mais fechado, para o texto creme passar em contraste AA (4,5:1). O `--rosa-queimado` original continua nos elementos decorativos.
