const btnMenu = document.getElementById("btnMenu");
const menuLateral = document.getElementById("menuLateral");
const btnTema = document.getElementById("btnTema");
const menuPrincipal = document.getElementById("menuPrincipal");
const btnNotificacoes = document.getElementById("btnNotificacoes");
const telaNotificacoes = document.getElementById("telaNotificacoes");
const btnFecharNotificacao = document.getElementById("btnFecharNotificacao");
const listaTurmas = document.querySelector(".lista-turmas");
const btnSair = document.getElementById("btnSair");

const CORES = ["azul", "ciano", "verde", "vermelho", "roxo", "amarelo"];

async function renovarToken() {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return false;

    try {
        const resposta = await fetch("/refresh", {
            method: "POST",
            headers: { "Authorization": `Bearer ${refresh}` }
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

async function buscarTurmas() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/login-page";
        return;
    }

    try {
        const resposta = await fetch("/turmas", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (resposta.status === 401 && await renovarToken()) {
            return buscarTurmas();
        }

        if (!resposta.ok) {
            throw new Error(`Falha ao buscar turmas: ${resposta.status}`);
        }

        renderizarTurmas(await resposta.json());
    } catch (erro) {
        console.error(erro);
        listaTurmas.innerHTML = "<p>Não foi possível carregar as turmas.</p>";
    }
}

function renderizarTurmas(turmas) {
    listaTurmas.innerHTML = "";

    turmas.forEach((turma, indice) => {
        const card = document.createElement("article");
        card.className = `card-turma ${CORES[indice % CORES.length]}`;

        const titulo = document.createElement("h1");
        titulo.textContent = [turma.Serie, turma.Curso].filter(Boolean).join(" ") || "Turma";
        card.appendChild(titulo);
        listaTurmas.appendChild(card);
    });
}

btnMenu.addEventListener("click", () => menuLateral.classList.toggle("ativo"));

btnTema.addEventListener("click", () => {
    document.body.classList.toggle("modo-escuro");
    btnTema.textContent = document.body.classList.contains("modo-escuro") ? "🌙" : "☀️";
});

btnNotificacoes.addEventListener("click", (event) => {
    event.preventDefault();
    menuPrincipal.style.display = "none";
    telaNotificacoes.classList.add("ativo");
});

btnFecharNotificacao.addEventListener("click", () => {
    telaNotificacoes.classList.remove("ativo");
    menuPrincipal.style.display = "flex";
});

document.addEventListener("click", (event) => {
    if (!menuLateral.contains(event.target) && !btnMenu.contains(event.target)) {
        menuLateral.classList.remove("ativo");
    }
});

btnSair.addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
});

buscarTurmas();
