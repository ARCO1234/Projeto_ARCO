const icones = document.querySelectorAll(".icon");

function atualizarIcones() {
    const modoEscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;

    icones.forEach(icone => {
        if (modoEscuro) {
            icone.src = icone.dataset.dark;
        } else {
            icone.src = icone.dataset.light;
        }
    });
}

atualizarIcones();

window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", atualizarIcones);