const btnEntrar = document.getElementById("btnEntrar");
const btnEsqueciSenha = document.getElementById("btnEsqueciSenha");

btnEntrar.addEventListener("click", async function () {
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    if (email === "" || senha === "") {
        alert("Preencha todos os campos!");
        return;
    }

    try {
        const resposta = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ e_mail: email, senha: senha })
        });

        const dados = await resposta.json();

        if (resposta.ok) {
            localStorage.setItem("access_token", dados.access_token);
            localStorage.setItem("refresh_token", dados.refresh_token);
            window.location.href = "/Inicial-page";
        } else {
            alert(dados.mensagem || "Erro ao fazer login.");
        }
    } catch (erro) {
        console.error("Erro na requisição de login:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
});

btnEsqueciSenha.addEventListener("click", function () {
    window.location.href = "/recsenha-page";
});

document.getElementById("senha").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        btnEntrar.click();
    }
});
