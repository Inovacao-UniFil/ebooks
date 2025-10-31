document.getElementById("dynamicForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Evita o envio padrão do formulário
        if(!validateForm()){ return }
        submitButton.disabled = true;
        submitButton.innerHTML = '<table><td><div class="loader"></div></td><td><div>Enviando...</div></td></table>';
        nomeCompleto.disabled=true;
        email.disabled=true;
        telefone.disabled=true;
        fetch("/send_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nomeCompleto.value,
            email: email.value,
            telefone: telefone.value,
            
        })
        })
        .then(response => response.json())
        .then(data => {
        console.log("Received Data:", data);
        window.location.href = data.url;
        })
        .catch(error => {
        matricula.classList.add("is-invalid");
        matriculaFeedback.textContent = data.error;
        });
        // Redireciona para a página de sucesso
    });