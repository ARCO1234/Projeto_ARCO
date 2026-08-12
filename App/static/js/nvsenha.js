/* ==========================================================
                    CAPTURA DOS ELEMENTOS
========================================================== */

const campoSenha = document.getElementById("senhanova");
const campoConfirmar = document.getElementById("confirmasenha");
const btnProximo = document.getElementById("btnProximo");
const btnVoltar = document.getElementById("btnVoltar");

const requisitos = {
    min: { elemento: document.getElementById("req-min"), regex: /.{8,}/ },
    max: { elemento: document.getElementById("req-max"), regex: /^.{0,25}$/ },
    maiuscula: { elemento: document.getElementById("req-maiuscula"), regex: /[A-Z]/ },
    minuscula: { elemento: document.getElementById("req-minuscula"), regex: /[a-z]/ },
    numero: { elemento: document.getElementById("req-numero"), regex: /[0-9]/ },
    simbolo: { elemento: document.getElementById("req-simbolo"), regex: /[#@!$%^&*()_+\-=[\]{};':"\\|,.<>/?]/ }
};


/* ==========================================================
                VALIDAÇÃO EM TEMPO REAL
========================================================== */

function validarSenha() {
    const senha = campoSenha.value;
    let todosValidos = true;

    for (const chave in requisitos) {
        const { elemento, regex } = requisitos[chave];
        const valido = regex.test(senha);

        if (valido) {
            elemento.classList.add("valido");
        } else {
            elemento.classList.remove("valido");
            todosValidos = false;
        }
    }

    verificarTudo(todosValidos);
}

function verificarTudo(senhaValida) {
    const senhasIguais = campoSenha.value === campoConfirmar.value && campoConfirmar.value.length > 0;
    btnProximo.disabled = !(senhaValida && senhasIguais);
}


/* ==========================================================
                ENVIO PARA O BACKEND
========================================================== */

async function redefinirSenha() {

    const novaSenha = campoSenha.value;
    const params = new URLSearchParams(window.location.search);
    const primeiroAcesso = params.get("primeiro_acesso") === "1";

    if (btnProximo.disabled) return;

    btnProximo.disabled = true;
    const textoOriginal = btnProximo.textContent;
    btnProximo.textContent = "SALVANDO...";

    try {
        let resposta;

        if (primeiroAcesso) {
            // Veio direto do login com senha temporária: usa o token
            // que já está salvo, sem precisar de código por e-mail.
            const token = localStorage.getItem("access_token");

            if (!token) {
                alert("Sessão expirada, faça login novamente.");
                window.location.href = "/login-page";
                return;
            }

            resposta = await fetch("/definir-senha-inicial", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({ nova_senha: novaSenha })
            });
        } else {
            // Fluxo normal de "esqueci minha senha"
            const resetToken = sessionStorage.getItem("reset_token");

            if (!resetToken) {
                alert("Sessão expirada, informe o e-mail novamente.");
                window.location.href = "/recsenha-page";
                return;
            }

            resposta = await fetch("/redefinir-senha", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + resetToken
                },
                body: JSON.stringify({ nova_senha: novaSenha })
            });
        }

        let dados;
        try {
            dados = await resposta.json();
        } catch {
            dados = {};
        }

        if (resposta.ok) {
            sessionStorage.removeItem("emailRecuperacao");
            sessionStorage.removeItem("reset_token");

            if (primeiroAcesso) {
                window.location.href = "/Inicial-page";
            } else {
                window.location.href = "/boasenha-page";
            }
        } else {
            alert(dados.mensagem || "Não foi possível redefinir a senha.");
            btnProximo.disabled = false;
            btnProximo.textContent = textoOriginal;
        }

    } catch (erro) {
        console.error("Erro ao redefinir senha:", erro);
        alert("Não foi possível conectar ao servidor.");
        btnProximo.disabled = false;
        btnProximo.textContent = textoOriginal;
    }
}


/* ==========================================================
                    NAVEGAÇÃO
========================================================== */

function voltar() {
    window.location.href = "/recsenha-page";
}


/* ==========================================================
                        EVENTOS
========================================================== */

campoSenha.addEventListener("input", validarSenha);
campoConfirmar.addEventListener("input", validarSenha);

btnProximo.addEventListener("click", redefinirSenha);
btnVoltar.addEventListener("click", voltar);


console.log("Tela de nova senha carregada com sucesso.");
