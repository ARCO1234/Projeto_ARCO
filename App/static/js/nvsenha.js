/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const inputNova = document.getElementById("nova");
const inputConfirma = document.getElementById("confirma");

const erroNova = document.getElementById("erro-nova");
const erroConfirma = document.getElementById("erro-confirma");

const btnProximo = document.getElementById("btn-proximo");


/* ==========================================================
                VALIDAÇÃO DA SENHA
========================================================== */

/*
    Esta função verifica se a senha atende
    a todos os requisitos definidos.
*/

function validar() {

    const senha = inputNova.value;
    const confirmarSenha = inputConfirma.value;

    const minimo = senha.length >= 8;
    const maximo = senha.length <= 25;
    const maiuscula = /[A-Z]/.test(senha);
    const minuscula = /[a-z]/.test(senha);
    const numero = /[0-9]/.test(senha);
    const simbolo = /[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]]/.test(senha);

    atualizarRegra("r-min", minimo);
    atualizarRegra("r-max", maximo);
    atualizarRegra("r-mai", maiuscula);
    atualizarRegra("r-min2", minuscula);
    atualizarRegra("r-num", numero);
    atualizarRegra("r-sim", simbolo);

    erroNova.textContent = "";
    erroConfirma.textContent = "";

    inputNova.classList.remove("erro", "ok");
    inputConfirma.classList.remove("erro", "ok");

    const senhaValida =
        minimo &&
        maximo &&
        maiuscula &&
        minuscula &&
        numero &&
        simbolo;

    if (senha !== "") {

        if (senhaValida) {
            inputNova.classList.add("ok");
        } else {
            inputNova.classList.add("erro");
        }

    }

    const senhasIguais =
        senha === confirmarSenha &&
        confirmarSenha !== "";

    if (confirmarSenha !== "") {

        if (senhasIguais) {

            inputConfirma.classList.add("ok");

        } else {

            inputConfirma.classList.add("erro");
            erroConfirma.textContent = "As senhas não coincidem.";

        }

    }

    btnProximo.disabled = !(senhaValida && senhasIguais);

}


/* ==========================================================
                ATUALIZA AS REGRAS
========================================================== */

/*
    Marca em verde as regras que já foram
    atendidas pelo usuário.
*/

function atualizarRegra(id, valida) {

    const regra = document.getElementById(id);

    if (valida) {
        regra.classList.add("valida");
    } else {
        regra.classList.remove("valida");
    }

}


/* ==========================================================
                BOTÃO VOLTAR
========================================================== */

/*
    Retorna para a tela de recuperação
    de senha.
*/

function voltar() {

    window.location.href = "../rec.senha/recsenha.html";

}


/* ==========================================================
                BOTÃO PRÓXIMO
========================================================== */

/*
    Envia o usuário para a tela que informa
    que a senha foi redefinida com sucesso.
*/

function avancar() {

    if (!btnProximo.disabled) {

        window.location.href = "../boa.senha/boasenha.html";

    }

}
