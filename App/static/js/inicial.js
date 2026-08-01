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
                    AUTENTICAÇÃO / API
========================================================== */

const API_URL = "http://127.0.0.1:5000";

// Mapa simples de cores para ciclar nos cards (ajuste como preferir)
const CORES = ["azul", "ciano", "verde", "vermelho", "roxo", "amarelo"];

async function buscarTurmas() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login-page";
        return;
    }

    try {
        const resposta = await fetch(`${API_URL}/turmas`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (resposta.status === 401) {
            // Token expirado/inválido -> tenta renovar com o refresh token
            const renovou = await renovarToken();
            if (renovou) {
                return buscarTurmas();
            }
            window.location.href = "/login-page";
            return;
        }

        const turmas = await resposta.json();
        renderizarTurmas(turmas);

    } catch (erro) {
        console.error("Erro ao buscar turmas:", erro);
    }
}
async function buscarTurmas() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login-page";
        return;
    }

    try {
        const resposta = await fetch(`${API_URL}/turmas`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (resposta.status === 401) {
            // Token expirado/inválido -> tenta renovar com o refresh token
            const renovou = await renovarToken();
            if (renovou) {
                return buscarTurmas();
            }
            window.location.href = "/login-page";
            return;
        }

        const turmas = await resposta.json();
        renderizarTurmas(turmas);

    } catch (erro) {
        console.error("Erro ao buscar turmas:", erro);
    }
}

async function renovarToken() {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return false;

    try {
        const resposta = await fetch(`${API_URL}/refresh`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${refresh}`
            }
        });

        if (!resposta.ok) return false;

        const dados = await resposta.json();
        localStorage.setItem("access_token", dados.access_token);
        return true;

    } catch (erro) {
        console.error("Erro ao renovar token:", erro);
        return false;
    }
}

function renderizarTurmas(turmas) {
    listaTurmas.innerHTML = "";

    turmas.forEach(function (turma, indice) {
        const cor = CORES[indice % CORES.length];

        const card = document.createElement("article");
        card.className = `card-turma ${cor}`;

        const titulo = document.createElement("h1");
        // AJUSTE "nome" para o nome real da coluna na sua tabela "turma"
        titulo.textContent = `${turma.Serie} ${turma.Curso}`;

        card.appendChild(titulo);
        card.addEventListener("click", function () {
            alert("Você abriu: " + titulo.textContent.trim());
        });

        listaTurmas.appendChild(card);
    });
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


/*
    Botão do tema.
*/

btnTema.addEventListener("click", alternarTema);


document.addEventListener("click", function (event) {
    const clicouNoMenu = menuLateral.contains(event.target);
    const clicouNoBotao = btnMenu.contains(event.target);

    if (!clicouNoMenu && !clicouNoBotao) {
        menuLateral.classList.remove("ativo");
    }
});


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

buscarTurmas();
console.log("Página Inicial carregada com sucesso.");