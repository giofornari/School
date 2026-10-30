const form = document.getElementById('mioForm');
const nominativo = document.getElementById('nominativo');
const eta = document.getElementById('eta');
const consenso = document.getElementById('consenso');
const password = document.getElementById('password');
const erroriGlobali = document.getElementById('errori-globali');
const messaggio = document.getElementById('messaggio');

function validaCampo(campo) {
    let valido = false;
    let errore = '';
    
    if (campo === 'nominativo') {
        valido = /^[a-zA-Z\s]+$/.test(nominativo.value) && nominativo.value !== '';
        errore = 'Solo lettere e spazi';
    } else if (campo === 'eta') {
        const num = parseInt(eta.value);
        valido = num >= 18 && num <= 100;
        errore = 'Età tra 18 e 100';
    } else if (campo === 'consenso') {
        valido = consenso.checked;
        errore = 'Accetta il consenso';
    } else if (campo === 'password') {
        valido = password.value.length >= 8 && password.value.length <= 20 && 
                 /[A-Z]/.test(password.value) && /[a-z]/.test(password.value) && 
                 /[0-9]/.test(password.value) && /[!@#$%^&*]/.test(password.value);
        errore = '8-20 caratteri, maiuscola, minuscola, numero e speciale';
    }
    
    const divErrore = document.getElementById('errore-' + campo);
    if (valido) {
        divErrore.classList.add('hidden');
    } else {
        divErrore.textContent = errore;
        divErrore.classList.remove('hidden');
    }
    return valido;
}

function pulisci() {
    document.getElementById('errore-nominativo').classList.add('hidden');
    document.getElementById('errore-eta').classList.add('hidden');
    document.getElementById('errore-consenso').classList.add('hidden');
    document.getElementById('errore-password').classList.add('hidden');
    erroriGlobali.classList.add('hidden');
    messaggio.classList.add('hidden');
}

nominativo.addEventListener('input', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') validaCampo('nominativo');
});

eta.addEventListener('input', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') validaCampo('eta');
});

consenso.addEventListener('change', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') validaCampo('consenso');
});

password.addEventListener('input', function() {
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    if (modalita === 'interattiva') validaCampo('password');
});

document.querySelectorAll('input[name="modalita"]').forEach(function(radio) {
    radio.addEventListener('change', pulisci);
});

form.addEventListener('submit', function(e) {
    e.preventDefault();
    const modalita = document.querySelector('input[name="modalita"]:checked').value;
    
    if (modalita === 'interattiva') {
        const v1 = validaCampo('nominativo');
        const v2 = validaCampo('eta');
        const v3 = validaCampo('consenso');
        const v4 = validaCampo('password');
        
        if (v1 && v2 && v3 && v4) {
            messaggio.className = 'mt-4 p-3 rounded-lg text-center font-semibold bg-green-100 text-green-700';
            messaggio.textContent = 'Dati corretti';
            messaggio.classList.remove('hidden');
        }
    } else {
        pulisci();
        const errori = [];
        
        if (!/^[a-zA-Z\s]+$/.test(nominativo.value) || nominativo.value === '') {
            errori.push('Nominativo: solo lettere e spazi');
        }
        if (parseInt(eta.value) < 18 || parseInt(eta.value) > 100) {
            errori.push('Età: tra 18 e 100');
        }
        if (!consenso.checked) {
            errori.push('Consenso: devi accettarlo');
        }
        const pwd = password.value;
        if (pwd.length < 8 || pwd.length > 20 || !/[A-Z]/.test(pwd) || !/[a-z]/.test(pwd) || 
            !/[0-9]/.test(pwd) || !/[!@#$%^&*]/.test(pwd)) {
            errori.push('Password: requisiti non soddisfatti');
        }
        
        if (errori.length > 0) {
            erroriGlobali.innerHTML = '<strong>Errori:</strong><br>' + errori.join('<br>');
            erroriGlobali.classList.remove('hidden');
        } else {
            messaggio.className = 'mt-4 p-3 rounded-lg text-center font-semibold bg-green-100 text-green-700';
            messaggio.textContent = 'Dati corretti';
            messaggio.classList.remove('hidden');
        }
    }
});
