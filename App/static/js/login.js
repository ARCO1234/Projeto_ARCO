const btnEntrar = document.getElementById("btnEntrar");

btnEntrar.addEventListener("click", async function () {
    const email = document.getElementById("emaillogin").value;
    const senha = document.getElementById("senhalogin").value;

    if (email === "" || senha === "") {
        alert("Preencha todos os campos!");
        return;
    }

    try {
        const resposta = await fetch("/login", {
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

            if (dados.senha_temporaria) {
                window.location.href = "/nvsenha-page?primeiro_acesso=1";
            } else {
                window.location.href = "/Inicial-page";
            }
        } else {
            alert(dados.mensagem || "Erro ao fazer login.");
        }
    } catch (erro) {
        console.error("Erro na requisição de login:", erro);
        alert("Não foi possível conectar ao servidor.");
    }
});

document.getElementById("senhalogin").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        btnEntrar.click();
    }
});
