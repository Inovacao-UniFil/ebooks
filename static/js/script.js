
document.addEventListener("DOMContentLoaded", function () {

    const telefoneInput = document.getElementById('telefone');
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    const escolaridadeSelect = document.getElementById('escolaridade');
    const consentimentoCheckbox = document.getElementById('consentimento');
    const consentimentoWrapper = document.getElementById('consentimentoWrapper');
    const titulo = document.getElementById('titulo');
    const mensagem = document.getElementById('mensagem');
    const mensagemTexto = document.getElementById('mensagem-texto');
    const spinner = document.getElementById('spinner');

    const nomeError = document.getElementById('nomeError');
    const emailError = document.getElementById('emailError');
    const telefoneError = document.getElementById('telefoneError');
    const escolaridadeError = document.getElementById('escolaridadeError');
    const consentimentoError = document.getElementById('consentimentoError');

    // Atualiza o título conforme o parâmetro da URL ao carregar a página
    window.addEventListener('DOMContentLoaded', () => {
        const params = new URLSearchParams(window.location.search);
        const ebook = params.get('ebook');
        
        const nomesEbook = { 
        'gastronomia': 'Gastronomia', 
        'enem': 'ENEM', 
        'ia': 'Inteligência Artificial' 
        };
        
        if(nomesEbook[ebook]) {
        titulo.textContent = `Baixe o e-book gratuito ${nomesEbook[ebook]}!`;
        }
    });

    // Máscara de telefone
    telefoneInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 11) value = value.slice(0, 11);
        if (value.length > 6) {
        e.target.value = `(${value.slice(0,2)}) ${value.slice(2,7)}-${value.slice(7)}`;
        } else if (value.length > 2) {
        e.target.value = `(${value.slice(0,2)}) ${value.slice(2)}`;
        } else {
        e.target.value = value;
        }
    });

    // Função para validar nome completo (nome e sobrenome)
    function validarNomeCompleto(nome) {
        const nomesTrimmed = nome.trim().split(/\s+/);
        return nomesTrimmed.length >= 2 && nomesTrimmed.every(parte => parte.length >= 2);
    }

    // Função para validar e-mail
    function validarEmail(email) {
        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regexEmail.test(email);
    }

    // Função para validar telefone completo (11 dígitos)
    function validarTelefone(telefone) {
        const numeroLimpo = telefone.replace(/\D/g, '');
        return numeroLimpo.length === 11;
    }

    // ===== VALIDAÇÃO EM TEMPO REAL - NOME =====
    nomeInput.addEventListener('blur', () => {
        const nome = nomeInput.value.trim();
        if (nome && !validarNomeCompleto(nome)) {
        nomeInput.classList.add('error');
        nomeError.classList.add('show');
        }
    });

    nomeInput.addEventListener('input', () => {
        // Remove erro enquanto digita
        nomeInput.classList.remove('error');
        nomeError.classList.remove('show');
    });

    nomeInput.addEventListener('focus', () => {
        nomeInput.classList.remove('error');
        nomeError.classList.remove('show');
    });

    // ===== VALIDAÇÃO EM TEMPO REAL - EMAIL =====
    emailInput.addEventListener('blur', () => {
        const email = emailInput.value.trim();
        if (email && !validarEmail(email)) {
        emailInput.classList.add('error');
        emailError.classList.add('show');
        }
    });

    emailInput.addEventListener('input', () => {
        emailInput.classList.remove('error');
        emailError.classList.remove('show');
    });

    emailInput.addEventListener('focus', () => {
        emailInput.classList.remove('error');
        emailError.classList.remove('show');
    });

    // ===== VALIDAÇÃO EM TEMPO REAL - TELEFONE =====
    telefoneInput.addEventListener('blur', () => {
        const telefone = telefoneInput.value;
        if (telefone && !validarTelefone(telefone)) {
        telefoneInput.classList.add('error');
        telefoneError.classList.add('show');
        }
    });

    telefoneInput.addEventListener('focus', () => {
        telefoneInput.classList.remove('error');
        telefoneError.classList.remove('show');
    });

    // ===== VALIDAÇÃO EM TEMPO REAL - ESCOLARIDADE =====
    escolaridadeSelect.addEventListener('blur', () => {
        if (!escolaridadeSelect.value) {
        escolaridadeSelect.classList.add('error');
        escolaridadeError.classList.add('show');
        }
    });

    escolaridadeSelect.addEventListener('change', () => {
        escolaridadeSelect.classList.remove('error');
        escolaridadeError.classList.remove('show');
    });

    escolaridadeSelect.addEventListener('focus', () => {
        escolaridadeSelect.classList.remove('error');
        escolaridadeError.classList.remove('show');
    });

    // ===== VALIDAÇÃO EM TEMPO REAL - CONSENTIMENTO =====
    consentimentoCheckbox.addEventListener('change', () => {
        if (consentimentoCheckbox.checked) {
        consentimentoWrapper.classList.remove('error');
        consentimentoError.classList.remove('show');
        }
    });

    document.getElementById('ebookForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const nome = nomeInput.value.trim();
        const email = emailInput.value.trim();
        const telefone = telefoneInput.value;
        const escolaridade = escolaridadeSelect.value;
        const consentimento = consentimentoCheckbox.checked;
        let downloadurl = ""
        let temErro = false;

        // Validação do nome completo
        if (!validarNomeCompleto(nome)) {
        nomeInput.classList.add('error');
        nomeError.classList.add('show');
        temErro = true;
        } else {
        nomeInput.classList.remove('error');
        nomeError.classList.remove('show');
        }

        // Validação do e-mail
        if (!validarEmail(email)) {
        emailInput.classList.add('error');
        emailError.classList.add('show');
        temErro = true;
        } else {
        emailInput.classList.remove('error');
        emailError.classList.remove('show');
        }

        // Validação do telefone
        if (!validarTelefone(telefone)) {
        telefoneInput.classList.add('error');
        telefoneError.classList.add('show');
        temErro = true;
        } else {
        telefoneInput.classList.remove('error');
        telefoneError.classList.remove('show');
        }

        // Validação da escolaridade
        if (!escolaridade) {
        escolaridadeSelect.classList.add('error');
        escolaridadeError.classList.add('show');
        temErro = true;
        } else {
        escolaridadeSelect.classList.remove('error');
        escolaridadeError.classList.remove('show');
        }

        // Validação do consentimento
        if (!consentimento) {
        consentimentoWrapper.classList.add('error');
        consentimentoError.classList.add('show');
        temErro = true;
        } else {
        consentimentoWrapper.classList.remove('error');
        consentimentoError.classList.remove('show');
        }

        // Se houver erro, não prossegue
        if (temErro) {
        return;
        }

        const params = new URLSearchParams(window.location.search);
        const ebook = params.get('ebook');

        // Exibe mensagem de aviso de download
        mensagem.style.display = 'flex';
        mensagem.classList.remove('sucesso');
        spinner.style.display = 'block';
        mensagemTexto.textContent = 'O download iniciará automaticamente...';

        // Envio dos dados ao CRM
        try {
        await fetch("/send_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nomeInput.value,
            email: emailInput.value,
            telefone: telefoneInput.value,
            escolaridade: escolaridadeSelect.value,
            ebookFile: ebookFile
        })
        })
        .then(response => response.json())
        .then(data => {
        console.log("Received Data:", data);
        downloadurl = data.downloadurl
        })
        .catch(error => {
        });
        
        } catch (error) {
            console.log('Erro ao enviar dados ao CRM:', error);
        }


        // Inicia o download automático e exibe confirmação final
        setTimeout(() => {
        const link = document.createElement('a');
        link.href = downloadurl;
        link.download = ebookFile;
        //link.click();
        
        // Exibe confirmação final de sucesso
        spinner.style.display = 'none';
        mensagem.classList.add('sucesso');
        mensagemTexto.textContent = 'Download concluído! Aproveite sua leitura.';
        }, 1200);
    });
});