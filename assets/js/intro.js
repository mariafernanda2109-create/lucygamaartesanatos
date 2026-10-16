/* =========================================================
   Lucy Gama Ateliê — abertura com a logo
   Carrega no <head>, antes do primeiro desenho da página, para
   decidir se a abertura aparece sem piscar na tela.

   Pula quando a pessoa pediu menos movimento, quando o link leva
   direto a uma seção (#), quando ela voltou pelo botão do navegador
   ou quando já viu a abertura nesta sessão.

   Sem JS, a classe "abrindo" nunca entra e o site aparece direto.
   ========================================================= */
(function () {
  var raiz = document.documentElement;
  var MINIMO = 2000;   // tempo mínimo na tela, para a logo ser vista
  var MAXIMO = 5000;   // em conexão lenta, não segura a pessoa além disso
  var SAIDA = 1200;    // duração da cortina subindo, igual ao CSS
  var CHAVE = 'lg-abertura';

  var navegacao = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
  var voltou = navegacao && navegacao.type === 'back_forward';
  var semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var jaViu = false;
  try { jaViu = sessionStorage.getItem(CHAVE) === '1'; } catch (erro) {}

  if (semMovimento || location.hash || voltou || jaViu) return;

  try { sessionStorage.setItem(CHAVE, '1'); } catch (erro) {}
  raiz.classList.add('abrindo');

  var terminou = false;

  function terminar() {
    if (terminou) return;
    terminou = true;

    var abertura = document.querySelector('.abertura');
    if (abertura) abertura.classList.add('abertura_saindo');
    raiz.classList.remove('abrindo');

    // o main.js segura a entrada do hero até aqui
    window.dispatchEvent(new Event('abertura:fim'));

    setTimeout(function () {
      if (abertura) abertura.classList.remove('abertura_saindo');
    }, SAIDA);
  }

  var esperas = [
    new Promise(function (pronto) { setTimeout(pronto, MINIMO); }),
    new Promise(function (pronto) { window.addEventListener('load', pronto, { once: true }); })
  ];
  if (document.fonts && document.fonts.ready) esperas.push(document.fonts.ready);

  Promise.all(esperas).then(terminar);
  setTimeout(terminar, MAXIMO);

  // clique ou tecla encurtam a espera
  document.addEventListener('click', function (evento) {
    if (evento.target.closest && evento.target.closest('.abertura')) terminar();
  });
  document.addEventListener('keydown', terminar, { once: true });
})();
