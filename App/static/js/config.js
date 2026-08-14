/* ==========================================================
                    CARREGAR SEÇÕES
========================================================== */

const areaConfig = document.getElementById("area-config");
const botoes = document.querySelectorAll(".item-config");


/* ==========================================================
        FUNÇÃO QUE CARREGA O HTML DA SEÇÃO
========================================================== */

async function carregarSecao(nomeArquivo){

    try{

        const resposta = await fetch(`../templates/${nomeArquivo}.html`);

        const html = await resposta.text();

        areaConfig.innerHTML = html;

    }catch(erro){

        areaConfig.innerHTML = "<p>Erro ao carregar a seção.</p>";

        console.error(erro);
    }
}


/* ==========================================================
        CARREGA A TELA DE CONTA AO ABRIR A PÁGINA
========================================================== */

carregarSecao("contaConfig");


/* ==========================================================
        TROCA DE SEÇÕES AO CLICAR NO MENU
========================================================== */

botoes.forEach(botao => {

    botao.addEventListener("click", () => {

        botoes.forEach(b => b.classList.remove("ativo"));

        botao.classList.add("ativo");

        const secao = botao.dataset.secao;

        carregarSecao(secao + "Config");
    });
});

/* ==========================================================
                DADOS JAVA SCRIPT
========================================================== */

document.addEventListener("change", (e) => {

    if (e.target.classList.contains("input-arquivo")) {

        const linha = e.target.closest(".linha-dados");
        const nomeArquivo = linha.querySelector(".nome-arquivo");
        const btnAtualizar = linha.querySelector(".btn-atualizar");

        if (e.target.files.length > 0) {
            nomeArquivo.textContent = e.target.files[0].name;
            btnAtualizar.disabled = false;
        }

    }

});

/* ==========================================================
            MÓDULO: EDITAR MODELO DE FORMULÁRIOS
========================================================== */

document.addEventListener("click", (e) => {

    // Alternar entre as abas "vigentes" / "arquivadas"
    const aba = e.target.closest(".aba-formulario");
    if (aba) {
        document.querySelectorAll(".aba-formulario").forEach(a => a.classList.remove("ativa"));
        aba.classList.add("ativa");
    }

    // Ligar/desligar o status (check verde) de uma pergunta
    const botaoStatus = e.target.closest(".btn-status-pergunta");
    if (botaoStatus) {
        botaoStatus.classList.toggle("ativo");
    }

    // Excluir o card da pergunta
    const botaoExcluir = e.target.closest(".btn-excluir-pergunta");
    if (botaoExcluir) {
        botaoExcluir.closest(".card-pergunta").remove();
    }

});
