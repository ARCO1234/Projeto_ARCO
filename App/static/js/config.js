/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const btnVoltar = document.getElementById("btnVoltar");
const btnTema = document.getElementById("btnTema");

const btnConta = document.getElementById("btnConta");
const btnPrivacidade = document.getElementById("btnPrivacidade");
const btnAparencia = document.getElementById("btnAparencia");
const btnNotificacoes = document.getElementById("btnNotificacoes");
const btnAjuda = document.getElementById("btnAjuda");

const inputPesquisa = document.getElementById("inputPesquisa");


/* ==========================================================
                    BOTÃO VOLTAR
========================================================== */

/*
    Retorna para a tela inicial.
*/

function voltarPagina(){

    window.location.href = "../inicial/inicial.html";

}


/* ==========================================================
                    MODO ESCURO
========================================================== */

/*
    Alterna entre o modo claro e escuro.
*/

function alternarTema(){

    document.body.classList.toggle("modo-escuro");
    trocarIcones();

    if(document.body.classList.contains("modo-escuro")){

        btnTema.textContent = "🌙";
        localStorage.setItem("tema","escuro");

    }

    else{

        btnTema.textContent = "☀️";
        localStorage.setItem("tema","claro");

    }

}


/* ==========================================================
                CARREGAR TEMA SALVO
========================================================== */

/*
    Mantém o tema escolhido pelo usuário.
*/

function carregarTema(){

    const tema = localStorage.getItem("tema");

    if(tema === "escuro"){

        document.body.classList.add("modo-escuro");
        btnTema.textContent = "🌙";

    }

}


/* ==========================================================
            MENU DE CONFIGURAÇÕES
========================================================== */

function abrirConta(){

    alert("Configurações da Conta.");

}


function abrirPrivacidade(){

    alert("Configurações de Privacidade.");

}


function abrirAparencia(){

    alert("Configurações de Aparência.");

}


function abrirNotificacoes(){

    alert("Configurações de Notificações.");

}


function abrirAjuda(){

    alert("Central de Ajuda.");

}


/* ==========================================================
                    PESQUISA
========================================================== */

/*
    Apenas demonstra o funcionamento.
*/

inputPesquisa.addEventListener("keyup", function(){
    console.log("Pesquisando:", inputPesquisa.value);

});


/* ==========================================================
                    EVENTOS
========================================================== */

btnVoltar.addEventListener("click", voltarPagina);
btnTema.addEventListener("click", alternarTema);
btnConta.addEventListener("click", function(event){
    event.preventDefault();
    abrirConta();

});

btnPrivacidade.addEventListener("click", function(event){

    event.preventDefault();
    abrirPrivacidade();

});

btnAparencia.addEventListener("click", function(event){

    event.preventDefault();
    abrirAparencia();

});

btnNotificacoes.addEventListener("click", function(event){

    event.preventDefault();
    abrirNotificacoes();

});

btnAjuda.addEventListener("click", function(event){

    event.preventDefault();
    abrirAjuda();

});


/* ==========================================================
                INICIALIZAÇÃO
========================================================== */

carregarTema();

console.log("Tela de Configurações carregada com sucesso.");