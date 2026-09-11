/* =========================================================
   Lucy Gama Ateliê
   A página funciona inteira sem este arquivo.
   Aqui só tem comportamento e movimento.
   ========================================================= */

/* ---------------------------------------------------------
   1. Preferência de movimento
   --------------------------------------------------------- */
const semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------------------------------------------------------
   2. Menu mobile
   --------------------------------------------------------- */
const botaoMenu = document.querySelector('.cabecalho_menu_botao');
const navegacao = document.querySelector('.cabecalho_nav');

function fecharMenu() {
  if (!botaoMenu || !navegacao) return;
  botaoMenu.setAttribute('aria-expanded', 'false');
  botaoMenu.setAttribute('aria-label', 'Abrir menu');
  navegacao.classList.remove('cabecalho_nav_aberto');
}

if (botaoMenu && navegacao) {
  botaoMenu.addEventListener('click', () => {
    const aberto = botaoMenu.getAttribute('aria-expanded') === 'true';
    botaoMenu.setAttribute('aria-expanded', String(!aberto));
    botaoMenu.setAttribute('aria-label', aberto ? 'Abrir menu' : 'Fechar menu');
    navegacao.classList.toggle('cabecalho_nav_aberto', !aberto);
  });

  navegacao.querySelectorAll('a').forEach((link) => link.addEventListener('click', fecharMenu));

  document.addEventListener('keydown', (evento) => {
    if (evento.key === 'Escape') fecharMenu();
  });

  document.addEventListener('click', (evento) => {
    if (!navegacao.classList.contains('cabecalho_nav_aberto')) return;
    if (navegacao.contains(evento.target) || botaoMenu.contains(evento.target)) return;
    fecharMenu();
  });
}

/* ---------------------------------------------------------
   3. Estado do cabeçalho ao rolar
   --------------------------------------------------------- */
const cabecalho = document.querySelector('.cabecalho');

if (cabecalho) {
  const atualizarCabecalho = () => {
    cabecalho.classList.toggle('cabecalho_rolado', window.scrollY > 8);
  };
  atualizarCabecalho();
  window.addEventListener('scroll', atualizarCabecalho, { passive: true });
}

/* ---------------------------------------------------------
   4. FAQ acordeão
   Abre um por vez, para a leitura não virar uma lista longa.
   --------------------------------------------------------- */
const perguntas = document.querySelectorAll('.faq_pergunta');

perguntas.forEach((pergunta) => {
  pergunta.addEventListener('click', () => {
    const aberto = pergunta.getAttribute('aria-expanded') === 'true';

    perguntas.forEach((outra) => {
      if (outra === pergunta) return;
      outra.setAttribute('aria-expanded', 'false');
      const respostaOutra = document.getElementById(outra.getAttribute('aria-controls'));
      if (respostaOutra) respostaOutra.classList.remove('faq_resposta_aberta');
    });

    pergunta.setAttribute('aria-expanded', String(!aberto));
    const resposta = document.getElementById(pergunta.getAttribute('aria-controls'));
    if (resposta) resposta.classList.toggle('faq_resposta_aberta', !aberto);
  });
});

/* ---------------------------------------------------------
   5. Filtro do portfólio
   --------------------------------------------------------- */
const filtros = document.querySelectorAll('.portfolio_filtro');
const pecas = document.querySelectorAll('.portfolio_item');
const statusPortfolio = document.querySelector('.portfolio_status');

function aplicarFiltro(categoria) {
  let visiveis = 0;

  pecas.forEach((peca) => {
    const categorias = (peca.dataset.categoria || '').split(' ');
    const mostrar = categoria === 'todos' || categorias.includes(categoria);

    peca.classList.toggle('portfolio_item_oculto', !mostrar);

    if (mostrar) {
      visiveis += 1;
      if (!semMovimento && typeof gsap !== 'undefined') {
        gsap.fromTo(peca, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .45, ease: 'power2.out' });
      }
    }
  });

  if (statusPortfolio) {
    statusPortfolio.textContent = visiveis === 1
      ? '1 peça em exibição.'
      : visiveis + ' peças em exibição.';
  }

  if (typeof ScrollTrigger !== 'undefined') ScrollTrigger.refresh();
}

filtros.forEach((filtro) => {
  filtro.addEventListener('click', () => {
    filtros.forEach((outro) => {
      const ativo = outro === filtro;
      outro.classList.toggle('portfolio_filtro_ativo', ativo);
      outro.setAttribute('aria-pressed', String(ativo));
    });
    aplicarFiltro(filtro.dataset.filtro);
  });
});

/* ---------------------------------------------------------
   6. Carrossel dos serviços (só no celular)
   Avança um card a cada 3s enquanto a seção está na tela.
   Pausa quando a pessoa toca, arrasta ou usa o teclado, e
   volta a andar 4s depois. Não roda com "menos movimento".
   --------------------------------------------------------- */
const trilho = document.querySelector('.servicos_lista');
const telaCelular = window.matchMedia('(max-width: 47.99em)');

if (trilho && !semMovimento) {
  const cards = [...trilho.querySelectorAll('.servicos_bloco')];
  const INTERVALO = 3000;
  const PAUSA_APOS_TOQUE = 4000;

  let relogio = null;
  let retomada = null;
  let naTela = false;

  const passo = () => {
    if (cards.length < 2) return;
    const largura = cards[1].offsetLeft - cards[0].offsetLeft;
    const atual = Math.round(trilho.scrollLeft / largura);
    const proximo = atual >= cards.length - 1 ? 0 : atual + 1;
    trilho.scrollTo({ left: proximo * largura, behavior: 'smooth' });
  };

  const parar = () => {
    clearInterval(relogio);
    relogio = null;
  };

  const andar = () => {
    if (relogio || !naTela || !telaCelular.matches || document.hidden) return;
    relogio = setInterval(passo, INTERVALO);
  };

  // qualquer interação segura o carrossel por um tempo
  const segurar = () => {
    parar();
    clearTimeout(retomada);
    retomada = setTimeout(andar, PAUSA_APOS_TOQUE);
  };

  ['pointerdown', 'touchstart', 'wheel', 'focusin'].forEach((evento) => {
    trilho.addEventListener(evento, segurar, { passive: true });
  });

  // só anda enquanto a seção está visível
  new IntersectionObserver((entradas) => {
    naTela = entradas[0].isIntersecting;
    naTela ? andar() : parar();
  }, { threshold: .25 }).observe(trilho);

  document.addEventListener('visibilitychange', () => (document.hidden ? parar() : andar()));

  // ao passar pra tablet/desktop o carrossel deixa de existir
  telaCelular.addEventListener('change', () => {
    if (telaCelular.matches) { andar(); } else { parar(); trilho.scrollLeft = 0; }
  });
}

/* ---------------------------------------------------------
   7. Animações GSAP
   Só rodam se a biblioteca carregou e se a pessoa não pediu
   menos movimento. Nada de conteúdo depende disso.
   --------------------------------------------------------- */
if (!semMovimento && typeof gsap !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);

  // entrada do hero
  gsap.timeline({ defaults: { ease: 'power3.out', duration: 1 } })
    .from('.hero_selo', { opacity: 0, y: 16 })
    .from('.hero_titulo', { opacity: 0, y: 30 }, '-=0.8')
    .from('.hero_subtitulo', { opacity: 0, y: 24 }, '-=0.78')
    .from('.hero_apoio', { opacity: 0, y: 20 }, '-=0.82')
    .from('.hero_acoes', { opacity: 0, y: 20 }, '-=0.8')
    .from('.hero_descer', { opacity: 0, duration: .8 }, '-=0.6')
    .from('.hero_figura', { opacity: 0, scale: 1.04, duration: 1.3 }, '-=1.25');

  // revelar blocos ao rolar
  gsap.utils.toArray('[data-anim="revelar"]').forEach((elemento) => {
    gsap.from(elemento, {
      opacity: 0,
      y: 24,
      duration: .9,
      ease: 'power2.out',
      scrollTrigger: { trigger: elemento, start: 'top 88%', once: true }
    });
  });

  // sequências com stagger
  const sequencias = [
    ['.servicos_bloco', '.servicos_lista'],
    ['.portfolio_item', '.portfolio_galeria'],
    ['.diferenciais_card', '.diferenciais_lista'],
    ['.processo_passo', '.processo_lista']
  ];

  sequencias.forEach(([alvo, gatilho]) => {
    if (!document.querySelector(alvo)) return;
    gsap.from(alvo, {
      opacity: 0,
      y: 26,
      duration: .8,
      stagger: .1,
      ease: 'power2.out',
      scrollTrigger: { trigger: gatilho, start: 'top 82%', once: true }
    });
  });

  // parallax discreto na foto do ateliê, só no desktop
  ScrollTrigger.matchMedia({
    '(min-width: 64em)': () => {
      gsap.to('.sobre_foto', {
        yPercent: -5,
        ease: 'none',
        scrollTrigger: { trigger: '.sobre', start: 'top bottom', end: 'bottom top', scrub: true }
      });
    }
  });

  // recalcula posições depois que fontes e imagens carregam
  window.addEventListener('load', () => ScrollTrigger.refresh());
}
