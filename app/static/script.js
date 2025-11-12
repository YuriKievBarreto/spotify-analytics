const botao = document.getElementById("botao");

document.addEventListener("click", (e) => {
  if (e.target.id === "botao") {
    fetch('http://127.0.0.1:8000/api/v1/user/me', {
    method: 'GET',
    // ⭐️ Esta linha força o navegador a incluir o Cookie de sessão
    credentials: 'include' 
})
.then(response => {
    if (response.status === 401) {
        console.error("Autenticação falhou! Redirecionar para login.");
        window.location.href = 'http://127.0.0.1:8000/api/v1/auth/login';
    } else {
        console.log("encontrado")
        console.log("redirecionando para dashboard")
        window.location.href = 'http://127.0.0.1:8000/static/dashboard.html'

    }
})

  }
});
