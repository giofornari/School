const form = document.getElementById('mioForm');
const nominativo = document.getElementById('nominativo');
const eta = document.getElementById('eta');
const consenso = document.getElementById('consenso');
const password = document.getElementById('password');
const erroriGlobali = document.getElementById('errori-globali');
const messaggio = document.getElementById('messaggio');

function controllaNominativo(valore) {
    return /^[a-zA-Z\s]+$/.test(valore) && valore.trim() !== '';
}

function controllaEta(valore) {
    const numero = parseInt(valore);
    return numero >= 18 && numero <= 100;
}

function controllaPassword(valore) {
    if (valore.length < 8 || valore.length > 20) return false;
    if (!/[A-Z]/.test(valore)) return false;
    if (!/[a-z]/.test(valore)) return false;
    if (!/[0-9]/.test(valore)) return false;
    if (!/[!@#$%^&*]/.test(valore)) return false;
    return true;
}

function mostraErrore(campo, testo) {
    const divErrore = document.getElementById('errore-' + campo);
    divErrore.textContent = testo;
    divErrore.classList.remove('hidden');
    document.getElementById(campo).classList.add('border-red-500');
}

function nascondiErrore(campo) {
    const divErrore = document.getElementById('errore-' + campo);
    divErrore.classList.add('hidden');
    document.getElementById(campo).classList.remove('border-red-500');
    document.getElementById(campo).classList.add('border-green-500');
}

function validaCampo(campo) {
    let valido = false;
    let testoErrore = '';
    
    if (campo === 'nominativo') {
        valido = controllaNominativo(nominativo.value);
        testoErrore = 'Deve contenere solo lettere e spazi';
    } else if (campo === 'eta') {
        valido = controllaEta(eta.value);
        testoErrore = 'Deve essere tra 18 e 100';
    } else if (campo === 'consenso') {
        valido = consenso.checked;
        testoErrore = 'Devi accettare il consenso';
    } else if (campo === 'password') {
        valido = controllaPassword(password.value);
        testoErrore = 'Deve avere 8-20 caratteri, maiuscola, minuscola, numero e carattere speciale';
    }
    
    if (valido) {
        nascondiErrore(campo);
    } else {
        mostraErrore(campo, testoErrore);
    }
    
    return valido;
}

function pulisciErrori() {
    document.getElementById('errore-nominativo').classList.add('hidden');
    document.getElementById('errore-eta').classList.add('hidden');
    document.getElementById('errore-consenso').classList.add('hidden');
    document.getElementById('errore-password').classList.add('hidden');
    erroriGlobali.classList.add('hidden');
    messaggio.classList.add('hidden');
    
    nominativo.classList.remove('border-red-500', 'border-green-500');
    eta.classList.remove('border-red-500', 'border-green-500');
    password.classList.remove('border-red-500', 'border-green-500');
}

nominativo.addEventListener('input', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') {
        validaCampo('nominativo');
    }
});

eta.addEventListener('input', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') {
        validaCampo('eta');
    }
});

consenso.addEventListener('change', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') {
        validaCampo('consenso');
    }
});

password.addEventListener('input', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') {
        validaCampo('password');
    }
});

const radioModalita = document.querySelectorAll('input[name="modalita"]');
for (let i = 0; i < radioModalita.length; i++) {
    radioModalita[i].addEventListener('change', pulisciErrori);
}

form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    
    if (modalita === 'interattiva') {
        const nomeValido = validaCampo('nominativo');
        const etaValida = validaCampo('eta');
        const consensoValido = validaCampo('consenso');
        const passwordValida = validaCampo('password');
        
        erroriGlobali.classList.add('hidden');
        
        if (nomeValido && etaValida && consensoValido && passwordValida) {
            messaggio.className = 'mt-4 p-3 rounded-lg text-center font-semibold bg-green-100 text-green-700';
            messaggio.textContent = 'Dati corretti';
            messaggio.classList.remove('hidden');
        } else {
            messaggio.classList.add('hidden');
        }
        
    } else {
        pulisciErrori();
        
        const listaErrori = [];
        
        if (!controllaNominativo(nominativo.value)) {
            listaErrori.push('Nominativo: deve contenere solo lettere e spazi');
        }
        if (!controllaEta(eta.value)) {
            listaErrori.push('Età: deve essere tra 18 e 100');
        }
        if (!consenso.checked) {
            listaErrori.push('Consenso: devi accettarlo');
        }
        if (!controllaPassword(password.value)) {
            listaErrori.push('Password: 8-20 caratteri, maiuscola, minuscola, numero e carattere speciale');
        }
        
        if (listaErrori.length > 0) {
            erroriGlobali.innerHTML = '<strong>Errori:</strong><br>' + listaErrori.join('<br>');
            erroriGlobali.classList.remove('hidden');
            messaggio.classList.add('hidden');
        } else {
            erroriGlobali.classList.add('hidden');
            messaggio.className = 'mt-4 p-3 rounded-lg text-center font-semibold bg-green-100 text-green-700';
            messaggio.textContent = 'Dati corretti';
            messaggio.classList.remove('hidden');
        }
    }
});
