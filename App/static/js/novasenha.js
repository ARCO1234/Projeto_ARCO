const campoSenha = document.getElementById("senhanova");
const campoConfirmar = document.getElementById("confirmasenha");
const btnProximo = document.getElementById("btn-proximo");

const requisitos = {
    min: { elemento: document.getElementById("req-min"), regex: /.{8,}/ },
    max: { elemento: document.getElementById("req-max"), regex: /^.{0,25}$/ },
    maiuscula: { elemento: document.getElementById("req-maiuscula"), regex: /[A-Z]/ },
    minuscula: { elemento: document.getElementById("req-minuscula"), regex: /[a-z]/ },
    numero: { elemento: document.getElementById("req-numero"), regex: /[0-9]/ },
    simbolo: { elemento: document.getElementById("req-simbolo"), regex: /[#@!$%^&*()_+\-=[\]{};':"\\|,.<>/?]/ }
};

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

campoSenha.addEventListener("input", validarSenha);
campoConfirmar.addEventListener("input", validarSenha);