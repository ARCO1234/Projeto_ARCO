const icones = document.querySelectorAll('.icon');

function trocarIcones() {
    const modoEscuro = document.body.classList.contains('modo-escuro');

    icones.forEach(icone => {
        if (modoEscuro) {
            icone.src = icone.dataset.dark;
        } else {
            icone.src = icone.dataset.light;
        }
    });
}