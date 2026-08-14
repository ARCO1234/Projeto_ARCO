/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */


const btnTema = document.getElementById("btnTema");
const btnVoltar = document.getElementById("btnVoltar");




/* ==========================================================
                    BOTÃO VOLTAR
========================================================== */

/*
    Retorna para a tela inicial.
*/

function voltarPagina(){

    window.location.href = "../templates/inicial.html";

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
    Botão do VOLTAR.
*/
btnVoltar.addEventListener("click", voltarPagina);

/*
    Botão do tema.
*/

btnTema.addEventListener("click", alternarTema);





/* ==========================================================
                INICIALIZAÇÃO
========================================================== */

console.log("Página Inicial carregada com sucesso.");
