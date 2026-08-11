/**
 * auth-guard.js
 *
 * Como o token JWT fica salvo no localStorage (não em cookie), o Flask
 * não consegue barrar o carregamento de uma página HTML protegida no
 * servidor (@jwt_required() não enxerga localStorage). Por isso, toda
 * página que exige login precisa incluir este script ANTES do resto
 * do conteúdo carregar de verdade.
 *
 * O que ele faz:
 *   1. Se não existe access_token salvo -> manda direto pro login.
 *   2. Se existe, confirma com o backend se o token ainda é válido
 *      (não expirou, não foi revogado). Se for inválido, limpa o
 *      localStorage e manda pro login também.
 *
 * Uso: incluir <script src="/static/js/auth-guard.js"></script> como
 * o PRIMEIRO script de qualquer página que só usuário logado pode ver.
 */

(function () {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login-page";
        return;
    }

    fetch("/verificar-token", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
        .then(function (resposta) {
            if (!resposta.ok) {
                throw new Error("Token inválido ou expirado");
            }
            return resposta.json();
        })
        .then(function (dados) {
            // Deixa disponível pro resto da página, se precisar saber o papel do usuário
            window.tipoUsuarioLogado = dados.tipo;
        })
        .catch(function () {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            window.location.href = "/login-page";
        });
})();
