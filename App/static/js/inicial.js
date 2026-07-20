/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const btnMenu = document.getElementById("btnMenu");
const menuLateral = document.getElementById("menuLateral");
const btnTema = document.getElementById("btnTema");
const menuPrincipal = document.getElementById("menuPrincipal");
const btnNotificacoes = document.getElementById("btnNotificacoes");
const telaNotificacoes = document.getElementById("telaNotificacoes");
const btnFecharNotificacao = document.getElementById("btnFecharNotificacao");

/* ==========================================================
                    MENU LATERAL
========================================================== */

/*
    Abre e fecha o menu lateral.
*/

function alternarMenu() {

    menuLateral.classList.toggle("ativo");

}


/* ==========================================================
                    MODO ESCURO
========================================================== */

/*
    Alterna entre o modo claro e o modo escuro.
*/

function alternarTema() {

    document.body.classList.toggle("modo-escuro");

    if (document.body.classList.contains("modo-escuro")) {

        btnTema.textContent = "🌙";

    } else {

        btnTema.textContent = "☀️";

    }

}


/* ==========================================================
                    EVENTOS
========================================================== */

/*
    Botão do menu.
*/

btnMenu.addEventListener("click", alternarMenu);

/* ==========================================================
                    NOTIFICAÇÕES
========================================================== */

/*
    Abre a tela de notificações
    dentro do menu lateral.
*/

btnNotificacoes.addEventListener("click", function(event){

    event.preventDefault();

    menuPrincipal.style.display = "none";

    telaNotificacoes.classList.add("ativo");

});


/*
    Fecha a tela de notificações
    e retorna ao menu principal.
*/

btnFecharNotificacao.addEventListener("click", function(){

    telaNotificacoes.classList.remove("ativo");

    menuPrincipal.style.display = "flex";

});

/*
    Botão do tema.
*/

btnTema.addEventListener("click", alternarTema);


/* ==========================================================
            FECHAR MENU AO CLICAR FORA
========================================================== */

/*
    Fecha o menu quando o usuário
    clicar fora dele.
*/

document.addEventListener("click", function (event) {

    const clicouNoMenu = menuLateral.contains(event.target);
    const clicouNoBotao = btnMenu.contains(event.target);

    if (!clicouNoMenu && !clicouNoBotao) {

        menuLateral.classList.remove("ativo");

    }

});


/* ==========================================================
                CARDS DAS TURMAS
========================================================== */

/*
    Seleciona todos os cards.
*/

const cards = document.querySelectorAll(".card-turma");


/*
    Adiciona um evento de clique
    para cada card.
*/

cards.forEach(function (card) {

    card.addEventListener("click", function () {

        /*
            Futuramente esta parte poderá
            abrir a turma correspondente.
        */

        alert("Você abriu: " + card.textContent.trim());

    });

});


/* ==========================================================
                INICIALIZAÇÃO
========================================================== */

console.log("Página Inicial carregada com sucesso.");