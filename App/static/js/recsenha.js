/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const campoCodigo = document.getElementById("codigo");

const btnVoltar = document.getElementById("btnVoltar");

const btnProximo = document.getElementById("btnProximo");

const btnReenviar = document.getElementById("btnReenviar");


/* ==========================================================
                    VOLTAR PARA O LOGIN
========================================================== */

/*
    Retorna para a tela de login.
*/

function voltarLogin() {

    window.location.href = "../login/login.html";

}


/* ==========================================================
                    VALIDAR CÓDIGO
========================================================== */

/*
    Verifica se o usuário digitou
    um código antes de prosseguir.
*/

function validarCodigo() {

    const codigo = campoCodigo.value.trim();

    if (codigo === "") {

        alert("Digite o código de verificação.");

        campoCodigo.focus();

        return;

    }

    /*
        Futuramente aqui será feita
        a validação do código enviado
        para o e-mail.
    */

    alert("Código validado com sucesso!");

    window.location.href = "../nv.senha/nvsenha.html";
}


/* ==========================================================
                REENVIAR CÓDIGO
========================================================== */

/*
    Simula o reenvio do código.
*/

function reenviarCodigo() {

    alert("Um novo código foi enviado para seu e-mail.");

}


/* ==========================================================
                    EVENTOS
========================================================== */

/*
    Clique no botão Voltar.
*/

btnVoltar.addEventListener("click", voltarLogin);


/*
    Clique no botão Próximo.
*/

btnProximo.addEventListener("click", validarCodigo);


/*
    Clique no botão Reenviar.
*/

btnReenviar.addEventListener("click", reenviarCodigo);


/* ==========================================================
                TECLA ENTER
========================================================== */

/*
    Pressionar Enter executa
    a mesma ação do botão Próximo.
*/

campoCodigo.addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        validarCodigo();
        

    }

});


/* ==========================================================
                INICIALIZAÇÃO
========================================================== */

console.log("Tela de recuperação de senha carregada com sucesso.");
