// Database utenti con password criptate in MD5
const usersDatabase = [
    {
        username: 'admin',
        passwordHash: '0192023a7bbd73250516f069df18b500', // admin123
        role: 'amministratore'
    },
    {
        username: 'mario',
        passwordHash: '5b7a0e20dd6a6e8fe6c8b8e4e2e3e2e1', // mario123
        role: 'utente'
    },
    {
        username: 'laura',
        passwordHash: 'c93ccd78b2076528346216b3b2f701e6', // laura123
        role: 'utente'
    },
    {
        username: 'giuseppe',
        passwordHash: '482c811da5d5b4bc6d497ffa98491e38', // giuseppe123
        role: 'utente'
    },
    {
        username: 'superadmin',
        passwordHash: '5b54c88e6fc3e3e7c2bf3b2c2f0e0e0a', // super123
        role: 'amministratore'
    }
];

// Riferimenti agli elementi DOM
const loginForm = document.getElementById('loginForm');
const messageDiv = document.getElementById('message');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const welcomeDiv = document.getElementById('welcomeMessage');

// Funzione per criptare la password in MD5
function hashPassword(password) {
    return CryptoJS.MD5(password).toString();
}

// Funzione per cercare l'utente nel database
function authenticateUser(username, password) {
    const passwordHash = hashPassword(password);

    const user = usersDatabase.find(u =>
        u.username.toLowerCase() === username.toLowerCase() &&
        u.passwordHash === passwordHash
    );

    return user;
}

// Funzione per mostrare messaggi di errore
function showError(message) {
    messageDiv.className = 'p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 text-sm';
    messageDiv.textContent = message;
    messageDiv.classList.remove('hidden');
}

// Funzione per mostrare il messaggio di benvenuto
function showWelcome(user) {
    // Nascondi messaggio di errore e campi del form
    messageDiv.classList.add('hidden');
    usernameInput.parentElement.classList.add('hidden');
    passwordInput.parentElement.classList.add('hidden');
    document.querySelector('.flex.items-center.justify-between').classList.add('hidden');
    document.querySelector('button[type="submit"]').classList.add('hidden');
    document.querySelector('.mt-6.text-sm.text-center').classList.add('hidden');

    // Mostra messaggio di benvenuto
    welcomeDiv.classList.remove('hidden');

    const roleSpan = document.getElementById('welcomeRole');
    const roleIcon = user.role === 'amministratore' ? '👑' : '👤';
    roleSpan.textContent = `${roleIcon} ${user.role.toUpperCase()}`;
    roleSpan.className = user.role === 'amministratore'
        ? 'inline-block px-3 py-1 ml-2 text-white font-semibold rounded-full text-xs bg-red-500'
        : 'inline-block px-3 py-1 ml-2 text-white font-semibold rounded-full text-xs bg-green-500';

}

// Funzione per logout
function logout() {
    // Mostra di nuovo i campi del form
    usernameInput.parentElement.classList.remove('hidden');
    passwordInput.parentElement.classList.remove('hidden');
    document.querySelector('.flex.items-center.justify-between').classList.remove('hidden');
    document.querySelector('button[type="submit"]').classList.remove('hidden');
    document.querySelector('.mt-6.text-sm.text-center').classList.remove('hidden');

    // Nascondi messaggio di benvenuto
    welcomeDiv.classList.add('hidden');
    messageDiv.classList.add('hidden');

    // Pulisci i campi
    usernameInput.value = '';
    passwordInput.value = '';
    usernameInput.focus();
}

// Gestione dell'invio del form
loginForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    // Validazione base
    if (!username || !password) {
        showError('⚠️ Compilare tutti i campi!');
        return;
    }

    // Tentativo di autenticazione
    const user = authenticateUser(username, password);

    if (user) {
        // Successo
        showWelcome(user);
    } else {
        // Errore
        showError('❌ Credenziali non valide! Nome utente o password errati.');
        passwordInput.value = '';
        passwordInput.focus();
    }
});

// Focus automatico sul campo username al caricamento
window.addEventListener('load', function () {
    usernameInput.focus();
});

// Funzione helper per generare hash MD5 (usa nella console)
function generatePasswordHash(password) {
    console.log(`Password: "${password}" -> Hash MD5: "${hashPassword(password)}"`);
}