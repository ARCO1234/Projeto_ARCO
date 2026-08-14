const botoes = document.querySelectorAll('.divEsquerd button');
const caminhoAtual = window.location.pathname.toLowerCase();

botoes.forEach((botao) => {
    const caminhoDoBotao = (botao.dataset.path || '').toLowerCase();

    if (caminhoDoBotao === caminhoAtual) {
        botao.classList.add('ativo');
        botao.setAttribute('aria-current', 'page');
    }

    botao.addEventListener('click', () => {
        botoes.forEach((item) => {
            item.classList.remove('ativo');
            item.removeAttribute('aria-current');
        });
        botao.classList.add('ativo');
    });
});
