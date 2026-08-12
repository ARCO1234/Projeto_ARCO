/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const btnVoltar = document.getElementById("btnVoltar");
const btnEditar = document.getElementById("btnEditar");
const btnRelatorio = document.getElementById("btnRelatorio");
const botoesTrimestre = document.querySelectorAll("#trimestres button");


/* ==========================================================
                    BOTÃO VOLTAR
========================================================== */

/*
    Retorna para a tela anterior.
*/

btnVoltar.addEventListener("click", () => {

    history.back();

});


/* ==========================================================
                INICIAR RELATÓRIO
========================================================== */

/*
    Abre a tela onde o professor irá preencher
    o relatório do aluno.
*/

btnRelatorio.addEventListener("click", () => {

    window.location.href = "../frelatorio/frelatorio.html";

});


/* ==========================================================
                    EDITAR DADOS
========================================================== */

let editando = false;

btnEditar.addEventListener("click", () => {

    if(!editando){

        transformarEmInput("nomeAluno");

        transformarEmInput("turmaAluno");

        transformarEmInput("telefoneAluno");

        transformarEmInput("idadeAluno");

        transformarEmInput("dataNascimento");

        transformarEmInput("paiAluno");

        transformarEmInput("maeAluno");

        btnEditar.textContent = "💾 Salvar";

        editando = true;

    }

    else{

        salvarCampo("nomeAluno");

        salvarCampo("turmaAluno");

        salvarCampo("telefoneAluno");

        salvarCampo("idadeAluno");

        salvarCampo("dataNascimento");

        salvarCampo("paiAluno");

        salvarCampo("maeAluno");

        btnEditar.textContent = "✏ Editar";

        editando = false;

    }

});


/* ==========================================================
            TRANSFORMA TEXTO EM INPUT
========================================================== */

function transformarEmInput(id){

    const elemento = document.getElementById(id);

    const valor = elemento.textContent;

    elemento.innerHTML = `
        <input
            type="text"
            id="input_${id}"
            value="${valor}">
    `;

}


/* ==========================================================
                SALVAR CAMPO
========================================================== */

function salvarCampo(id){

    const elemento = document.getElementById(id);

    const input = document.getElementById(`input_${id}`);

    elemento.textContent = input.value;

}

/* ==========================================================
                TRIMESTRES
========================================================== */

botoesTrimestre.forEach((botao, indice) => {

    botao.addEventListener("click", () => {

        trocarTrimestre(indice + 1);

    });

});

function trocarTrimestre(trimestre){

    const relatorio = relatorios[trimestre];

    const titulo = document.querySelector("#statusRelatorio h2");

    const botao = document.getElementById("btnRelatorio");

    const imagem = document.querySelector("#statusRelatorio img");


    if(relatorio.status == "concluido"){

        titulo.textContent = "Relatório concluído";

        botao.textContent = "VISUALIZAR RELATÓRIO";

        imagem.src = "../imagens/concluido.png";

    }

    else{

        titulo.textContent = "Relatório pendente";

        botao.textContent = "INICIAR RELATÓRIO";

        imagem.src = "../imagens/alerta.png";

    }

}


/*Esse JavaScript funciona para demonstrar a tela, 
mas quando vocês integrarem com o banco de dados eu não recomendaria substituir
os <p> por <input> usando innerHTML. É mais robusto deixar os <input> já no HTML
com disabled e apenas habilitá-los quando o professor clicar em Editar.
Esse padrão facilita a validação dos campos, preserva eventos já associados 
aos elementos e torna a integração com a API mais simples.*/