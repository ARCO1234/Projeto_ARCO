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

        if(secao === "conta"){
            carregarSecao("contaConfig");
        }

        // depois você pode adicionar outras telas aqui
        // ex:
        // if(secao === "privacidade"){
        //     carregarSecao("privacidade");
        // }

    });

});
