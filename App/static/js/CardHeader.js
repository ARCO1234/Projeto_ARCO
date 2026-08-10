 const botoes = document.querySelectorAll('.divEsquerd button');

 botoes.forEach(botao => {
    botao.addEventListener('click', () => {
        botoes.forEach(b => b.classList.remove('ativo'));
        botao.classList.add('ativo');
    });

 });

 botoes[5].classList.add('ativo');

