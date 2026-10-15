# Lucy Gama Ateliê

Landing page do ateliê Lucy Gama Ateliê — Pops e Icons personalizados, peças em cerâmica e esculturas autorais. Objetivo único da página: gerar conversas no WhatsApp.

HTML, CSS e JavaScript puros. GSAP por CDN. Sem build, sem npm: dá para abrir o `index.html` com dois cliques e publicar direto na Vercel.

## Estrutura

Publicado em https://lucygamaatelie.vercel.app.

## Estrutura

```
lucy-gama-artesanatos/
├── index.html              landing page
├── privacidade.html        política de privacidade (LGPD)
├── termos.html             termos de uso
├── 404.html                página de erro, servida pela Vercel
├── assets/
│   ├── css/style.css
│   ├── js/main.js
│   └── img/                fotos em WebP, cada uma com versões -480 e -720
├── favicon.ico
├── robots.txt
├── sitemap.xml
├── vercel.json             headers de segurança (CSP, X-Frame-Options etc.)
├── build-preview.py        gera a versão single-file em preview/
├── gerar-placeholders.py   regera os placeholders SVG de reserva
└── README.md
```

## Dados do ateliê

- **WhatsApp** — `5543999360866`, em todos os links `wa.me` e no JSON-LD. Para trocar tudo de uma vez:
  `find . -name "*.html" -exec sed -i 's/5543999360866/55SEUNUMERO/g' {} +`
- **Instagram** — `https://www.instagram.com/lucygartesanatos`, no rodapé e no `sameAs` do JSON-LD.
- **Cidade** — Londrina/PR, no JSON-LD (`LocalBusiness` e `areaServed`), na meta description, no Open Graph e no rodapé.
- **Domínio** — `https://lucygamaatelie.vercel.app`. Se mudar, trocar no `canonical`, no Open Graph e no JSON-LD de cada página, no `robots.txt` e no `sitemap.xml`.

## Fotos

Todas as peças do portfólio são fotos reais. Para incluir uma nova:

1. Exportar em WebP, até 900–1000px no lado maior.
2. Gerar as versões menores com o mesmo nome e o sufixo da largura (`obra-20-480.webp`, `obra-20-720.webp`). Imagens com menos de 820px de largura não precisam.
3. No HTML, copiar um `<figure class="portfolio_item">` existente e ajustar `src`, `srcset`, `alt`, `width`, `height` e `data-categoria`. O `sizes` é o mesmo das outras peças. As dimensões declaradas evitam o pulo de layout que o Core Web Vitals penaliza.

## Pendências

- **Depoimentos** — a seção existe no `index.html`, comentada. Só publicar com depoimento real, nome e autorização.
- **Icons** — o filtro tem uma peça só. Faltam fotos de mais Icons.
- **Ao mudar uma página**, atualizar o `lastmod` dela no `sitemap.xml`.

## Publicar

O repositório está ligado ao projeto `lucygamaartesanatos` na Vercel. Todo push na `main` republica sozinho. Framework Preset `Other`, sem build command, output directory na raiz.

Para publicar pela linha de comando, a pasta precisa estar ligada ao projeto:

```bash
vercel link --project lucygamaartesanatos --yes
vercel --prod
```

## Medição

Vercel Web Analytics, sem cookie (precisa estar ligado no painel). O `main.js` manda um evento `whatsapp` a cada clique num link do WhatsApp, com a origem do clique. Eventos nomeados só aparecem no plano Pro. A propriedade está verificada no Google Search Console pela meta `google-site-verification`.

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
