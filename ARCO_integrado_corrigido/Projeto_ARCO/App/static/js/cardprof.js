function criarCardTurma(turma) {
    const card = document.createElement("div");
    card.className = "card";

    const nome = [turma.Serie, turma.Curso].filter(Boolean).join(" ") || "Turma";
    const materia = turma.materia || turma.Disciplina || "";

    card.innerHTML = `
        <div class="card-header">
            <h1>${nome}</h1>
            <h2>${materia}</h2>
        </div>
        <div class="card-footer">
            <button class="icon-btn" title="Horário" data-acao="horario">
                <img src="/static/img/relogio.png" alt="horário">
            </button>
            <button class="icon-btn" title="Atividades" data-acao="atividades">
                <img src="/static/img/formulario.png" alt="formulário">
            </button>
        </div>
    `;

    card.querySelector('[data-acao="horario"]').addEventListener("click", () => {
        window.location.href = "/horario-page";
    });

    return card;
}

async function carregarTurmas() {
    const container = document.getElementById("salas");
    const token = localStorage.getItem("access_token");

    try {
        const resposta = await fetch("/turmas", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);

        const turmas = await resposta.json();
        container.innerHTML = "";
        turmas.forEach((turma) => container.appendChild(criarCardTurma(turma)));
    } catch (erro) {
        console.error("Erro ao carregar turmas:", erro);
        container.innerHTML = "<p>Não foi possível carregar as turmas.</p>";
    }
}

document.addEventListener("DOMContentLoaded", carregarTurmas);
