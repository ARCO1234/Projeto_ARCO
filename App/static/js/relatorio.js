document.addEventListener("click", (e) => {
 
    const botaoFiltro = e.target.closest(".btn-filtro");
 
    // Clicou em um botão de filtro (Trimestre, Aluno, etc.)
    if (botaoFiltro) {
 
        const dropdownDoClicado = botaoFiltro.parentElement.querySelector(".dropdown-filtro");
 
        // fecha todos os outros dropdowns antes de abrir/fechar este
        document.querySelectorAll(".dropdown-filtro.aberto").forEach(d => {
            if (d !== dropdownDoClicado) {
                d.classList.remove("aberto");
            }
        });
 
        if (dropdownDoClicado) {
            dropdownDoClicado.classList.toggle("aberto");
        }
 
        return;
    }
 
    // Clicou em "Remover filtros" dentro de algum dropdown
    const botaoRemover = e.target.closest(".btn-remover-filtros");
    if (botaoRemover) {
 
        const dropdown = botaoRemover.closest(".dropdown-filtro");
 
        dropdown.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.checked = false;
        });
 
        return;
    }
 
    // Clicou em qualquer outro lugar fora de um .filtro -> fecha tudo
    if (!e.target.closest(".filtro")) {
        document.querySelectorAll(".dropdown-filtro.aberto").forEach(d => {
            d.classList.remove("aberto");
        });
    }
 
});
 
