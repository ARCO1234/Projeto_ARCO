const btnEntrar = document.getElementById("btnEntrar");

const usuarios = {
    "admin@email.com": "123456",
    "joao@email.com": "abc123",
    "maria@email.com": "senha321"
};

btnEntrar.addEventListener("click", function () {

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    if (email === "" || senha === "") {
        alert("Preencha todos os campos!");
        return;
    }

    if (usuarios[email] === senha) {

        alert("Login realizado com sucesso!");

        window.location.href = "../inicial/inicial.html";

    } else {

        alert("Email ou senha incorretos!");

    }
});
