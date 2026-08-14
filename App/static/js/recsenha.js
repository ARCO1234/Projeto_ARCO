/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const etapaEmail = document.getElementById("etapaEmail");
const etapaCodigo = document.getElementById("etapaCodigo");

const campoEmail = document.getElementById("email");
const campoCodigo = document.getElementById("codigo");
const emailMostrado = document.getElementById("emailMostrado");

const btnVoltarLogin = document.getElementById("btnVoltarLogin");
const btnEnviarEmail = document.getElementById("btnEnviarEmail");

const btnVoltar = document.getElementById("btnVoltar");
const btnProximo = document.getElementById("btnProximo");
const btnReenviar = document.getElementById("btnReenviar");


/* ==========================================================
                    ETAPA 1 - ENVIAR E-MAIL
========================================================== */

async function enviarEmail() {

    const email = campoEmail.value.trim();

    if (email === "") {
        alert("Digite seu e-mail.");
        campoEmail.focus();
        return;
    }

    btnEnviarEmail.disabled = true;
    const textoOriginal = btnEnviarEmail.textContent;
    btnEnviarEmail.textContent = "ENVIANDO...";

    try {
        const resposta = await fetch("/recuperar-senha", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const dados = await resposta.json();

        if (resposta.ok) {
            // Guarda o e-mail para usar nas próximas telas (verificação e redefinição)
            sessionStorage.setItem("emailRecuperacao", email);

            const mascarado = mascararEmail(email);
            emailMostrado.textContent = mascarado;

            etapaEmail.style.display = "none";
            etapaCodigo.style.display = "flex";
        } else {
            alert(dados.mensagem || "Não foi possível enviar o código.");
        }

    } catch (erro) {
        console.error("Erro ao enviar e-mail:", erro);
        alert("Não foi possível conectar ao servidor.");
    } finally {
        btnEnviarEmail.disabled = false;
        btnEnviarEmail.textContent = textoOriginal;
    }
}


/*
    Mostra só parte do e-mail, tipo: he****@gmail.com
*/
function mascararEmail(email) {
    const [usuario, dominio] = email.split("@");
    if (!dominio) return email;
    const visiveis = usuario.slice(0, 2);
    return `${visiveis}${"*".repeat(Math.max(usuario.length - 2, 3))}@${dominio}`;
}


/* ==========================================================
                ETAPA 2 - VALIDAR CÓDIGO
========================================================== */

async function validarCodigo() {

    const codigo = campoCodigo.value.trim();
    const email = sessionStorage.getItem("emailRecuperacao");

    if (codigo === "") {
        alert("Digite o código de verificação.");
        campoCodigo.focus();
        return;
    }

    if (!email) {
        alert("Sessão expirada, informe o e-mail novamente.");
        voltarParaEmail();
        return;
    }

    btnProximo.disabled = true;

    try {
        const resposta = await fetch("/verificar-codigo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, codigo })
        });

        const dados = await resposta.json();

        if (resposta.ok) {
            sessionStorage.setItem("reset_token", dados.reset_token);
            window.location.href = "/nvsenha-page";
        } else {
            alert(dados.mensagem || "Código inválido.");
        }

    } catch (erro) {
        console.error("Erro ao validar código:", erro);
        alert("Não foi possível conectar ao servidor.");
    } finally {
        btnProximo.disabled = false;
    }
}


/* ==========================================================
                REENVIAR CÓDIGO
========================================================== */

async function reenviarCodigo() {

    const email = sessionStorage.getItem("emailRecuperacao");

    if (!email) {
        alert("Sessão expirada, informe o e-mail novamente.");
        voltarParaEmail();
        return;
    }

    try {
        const resposta = await fetch("/recuperar-senha", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const dados = await resposta.json();
        alert(dados.mensagem || "Novo código enviado.");

    } catch (erro) {
        console.error("Erro ao reenviar código:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
}


/* ==========================================================
                    NAVEGAÇÃO
========================================================== */

function voltarParaEmail() {
    etapaCodigo.style.display = "none";
    etapaEmail.style.display = "flex";
}

function voltarLogin() {
    window.location.href = "/login-page";
}


/* ==========================================================
                        EVENTOS
========================================================== */

btnEnviarEmail.addEventListener("click", enviarEmail);
btnVoltarLogin.addEventListener("click", voltarLogin);

btnVoltar.addEventListener("click", voltarParaEmail);
btnProximo.addEventListener("click", validarCodigo);
btnReenviar.addEventListener("click", reenviarCodigo);

campoEmail.addEventListener("keypress", function (event) {
    if (event.key === "Enter") enviarEmail();
});

campoCodigo.addEventListener("keypress", function (event) {
    if (event.key === "Enter") validarCodigo();
});


console.log("Tela de recuperação de senha carregada com sucesso.");
