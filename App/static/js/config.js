// Cada chave corresponde ao "data-secao" do botão,
// e aponta pra uma ROTA do Flask (não um arquivo estático).
// Essas rotas ainda não existem no back-end — quando existirem,
// devem devolver o HTML já processado via render_template().
// Até lá, o fetch vai falhar com 404 (é esperado).
const arquivosSecao = {
    conta:        '/configuracoes/conta',
    privacidade:  '/configuracoes/privacidade',
    sobre:        '/configuracoes/sobre',
    dados:        '/configuracoes/dados',
    formularios:  '/configuracoes/formularios'
};

// Busca o HTML da rota da seção e injeta dentro da área de conteúdo
function carregarSecao(nome) {

    const arquivo = arquivosSecao[nome];

    if (!arquivo) {
        console.error('Seção não encontrada:', nome);
        return;
    }

    fetch(arquivo)
        .then(r => r.text())
        .then(html => {
            document.getElementById('area-config').innerHTML = html;
        })
        .catch(err => console.error('Erro ao carregar seção:', err));

}

// Delegação de evento: escuta clique em qualquer botão do menu-config
document.addEventListener('click', function (e) {

    const botao = e.target.closest('.item-config');

    if (botao) {

        // tira "ativo" de todos os botões...
        document.querySelectorAll('.item-config').forEach(b => {
            b.classList.remove('ativo');
        });

        // ...e coloca só no que foi clicado
        botao.classList.add('ativo');

        carregarSecao(botao.dataset.secao);

    }

});

// Assim que a página abre, já carrega a primeira seção
carregarSecao('conta');
