// ============================================================
//  Sistema di Prenotazione Consulenza Informatica
// ============================================================

// --- REGEX PATTERNS ---
const PATTERNS = {
    // Almeno 3 caratteri qualsiasi
    username: /^.{3,}$/,
    // Almeno 8 caratteri, deve contenere almeno una lettera e almeno un numero
    password: /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/,
    // Esattamente 10 cifre
    phone: /^\d{10}$/,
    // URL standard con protocollo opzionale
    url: /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_+.~#?&/=]*)?$/,
    // Data nel formato AAAA-MM-GG con mesi e giorni validi
    date: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/
};

// --- ICONS MAP per i servizi ---
const SERVICE_ICONS = { Linux: '🐧', Windows: '🪟', Android: '🤖', Database: '🗄️' };

// ============================================================
//  HELPER: Sicurezza — evita XSS nei contenuti dinamici
// ============================================================
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// ============================================================
//  HELPER: Gestione errori e stili dei campi
// ============================================================
function showError(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideError(id) {
    document.getElementById(id).classList.add('hidden');
}

function setFieldState(fieldId, isValid) {
    const el = document.getElementById(fieldId);
    if (!el) return;
    el.classList.remove('border-gray-300', 'border-red-400', 'border-green-400');
    el.classList.add(isValid ? 'border-green-400' : 'border-red-400');
}

// ============================================================
//  LOGICA DATE
// ============================================================

/**
 * Converte una stringa YYYY-MM-DD in un oggetto Date locale
 * (usando costruttore con valori separati per evitare problemi UTC)
 */
function parseLocalDate(dateStr) {
    const [y, m, d] = dateStr.split('-').map(Number);
    return new Date(y, m - 1, d);
}

/**
 * Calcola la data della prestazione: 7 gg dopo la richiesta.
 * Se cade di sabato (6) o domenica (0), sposta al lunedì successivo.
 */
function calcolaDataPrestazione(dateStr) {
    const data = parseLocalDate(dateStr);
    data.setDate(data.getDate() + 7);

    const giorno = data.getDay(); // 0=Dom, 6=Sab
    if (giorno === 6) data.setDate(data.getDate() + 2); // Sab → Lun
    if (giorno === 0) data.setDate(data.getDate() + 1); // Dom → Lun

    return data;
}

function formatDataIT(date) {
    return date.toLocaleDateString('it-IT', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatDataISO(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

// ============================================================
//  VALIDAZIONE
// ============================================================
function validaForm(data) {
    const errori = {};

    if (!PATTERNS.username.test(data.username))
        errori.username = true;

    if (!PATTERNS.password.test(data.password))
        errori.password = true;

    if (!PATTERNS.phone.test(data.phone))
        errori.phone = true;

    if (!data.siteUrl || !PATTERNS.url.test(data.siteUrl))
        errori.siteUrl = true;

    if (data.orgName.length < 2)
        errori.orgName = true;

    if (data.services.length === 0)
        errori.services = true;

    // Verifica formato regex + validità effettiva della data
    if (!PATTERNS.date.test(data.date) || isNaN(parseLocalDate(data.date).getTime()))
        errori.date = true;

    return errori;
}

// ============================================================
//  GENERAZIONE RIEPILOGO
// ============================================================
function summaryRow(etichetta, valore) {
    return `
        <div class="p-3.5 bg-gray-50 rounded-xl">
            <p class="text-xs text-gray-400 font-medium mb-1">${etichetta}</p>
            <p class="text-sm font-semibold text-gray-800 break-all">${escapeHtml(String(valore))}</p>
        </div>`;
}

function mostraRiepilogo(data) {
    const dataRichiesta = parseLocalDate(data.date);
    const dataPrestazione = calcolaDataPrestazione(data.date);

    const richiestaFormattata = formatDataIT(dataRichiesta);
    const prestazioneFormattata = formatDataIT(dataPrestazione);
    const prestazioneISO = formatDataISO(dataPrestazione);

    // Password oscurata per sicurezza
    const passwordOscurata = '•'.repeat(data.password.length);

    const serviziHtml = data.services.map(s =>
        `<span class="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
            ${SERVICE_ICONS[s] || ''} ${escapeHtml(s)}
        </span>`
    ).join('');

    // Nascondi il form
    document.getElementById('formSection').classList.add('hidden');

    const summarySection = document.getElementById('summarySection');
    summarySection.classList.remove('hidden');
    summarySection.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">

            <!-- Header verde successo -->
            <div class="bg-gradient-to-r from-emerald-500 to-green-600 px-8 py-7">
                <div class="flex items-center gap-4">
                    <div class="flex-shrink-0 w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="text-white text-2xl font-bold tracking-tight">Richiesta Confermata!</h1>
                        <p class="text-green-100 text-sm mt-0.5">Il modulo è stato ricevuto correttamente</p>
                    </div>
                </div>
            </div>

            <div class="px-8 py-7 space-y-6">

                <!-- Riepilogo dati -->
                <div>
                    <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-4">Riepilogo Dati Inseriti</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        ${summaryRow('👤 Nome Utente', data.username)}
                        ${summaryRow('🔒 Password', passwordOscurata)}
                        ${summaryRow('📞 Telefono', data.phone)}
                        ${summaryRow('🌐 Sito Web', data.siteUrl)}
                        ${summaryRow('🏢 Organizzazione', data.orgName)}
                        ${summaryRow('📅 Data Richiesta', richiestaFormattata)}
                    </div>
                    <!-- Servizi selezionati -->
                    <div class="mt-3 p-4 bg-gray-50 rounded-xl">
                        <p class="text-xs font-medium text-gray-400 mb-2">Ambiti di Consulenza Selezionati</p>
                        <div class="flex flex-wrap gap-2">${serviziHtml}</div>
                    </div>
                </div>

                <hr class="border-gray-100">

                <!-- Data Appuntamento -->
                <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-5">
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center mt-0.5">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                            </svg>
                        </div>
                        <div>
                            <p class="text-sm font-semibold text-blue-800">📌 Data Appuntamento Pianificata</p>
                            <p class="text-xl font-bold text-blue-900 mt-1 capitalize">${escapeHtml(prestazioneFormattata)}</p>
                            <p class="text-xs font-mono text-blue-500 mt-1">${escapeHtml(prestazioneISO)}</p>
                            <p class="text-xs text-gray-500 mt-2">
                                ⚙️ Calcolata automaticamente 7 giorni dalla data di richiesta.
                                Se cade nel weekend, viene spostata al primo lunedì disponibile.
                            </p>
                        </div>
                    </div>
                </div>

                <hr class="border-gray-100">

                <!-- Valore Aggiunto -->
                <div class="bg-gradient-to-br from-slate-800 to-blue-900 rounded-xl p-6 text-white">
                    <p class="text-xs font-semibold text-blue-300 uppercase tracking-widest mb-4">
                        Perché scegliere la nostra consulenza IT
                    </p>
                    <ul class="space-y-3 text-sm text-gray-200">
                        <li class="flex items-start gap-2.5">
                            <span class="text-green-400 font-bold mt-0.5 flex-shrink-0">✓</span>
                            <span>
                                <strong class="text-white">Expertise certificata</strong> su Linux, Windows, Android e Database:
                                soluzioni su misura per ogni esigenza aziendale.
                            </span>
                        </li>
                        <li class="flex items-start gap-2.5">
                            <span class="text-green-400 font-bold mt-0.5 flex-shrink-0">✓</span>
                            <span>
                                <strong class="text-white">Riduzione dei rischi</strong> grazie a professionisti aggiornati
                                sulle ultime best practice di sicurezza e vulnerabilità emergenti.
                            </span>
                        </li>
                        <li class="flex items-start gap-2.5">
                            <span class="text-green-400 font-bold mt-0.5 flex-shrink-0">✓</span>
                            <span>
                                <strong class="text-white">Ottimizzazione dei costi</strong>: un investimento nella consulenza
                                riduce i downtime e aumenta la produttività dell'intera organizzazione.
                            </span>
                        </li>
                        <li class="flex items-start gap-2.5">
                            <span class="text-green-400 font-bold mt-0.5 flex-shrink-0">✓</span>
                            <span>
                                <strong class="text-white">Supporto continuo</strong> e monitoraggio proattivo per garantire
                                la continuità operativa della tua infrastruttura IT.
                            </span>
                        </li>
                    </ul>
                </div>

                <!-- Torna al form -->
                <div class="pt-1">
                    <button id="btnNuovaRichiesta"
                        class="w-full border-2 border-gray-200 hover:border-blue-400 hover:bg-blue-50 text-gray-600 hover:text-blue-700 font-semibold py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                        </svg>
                        Nuova Richiesta
                    </button>
                </div>

            </div>
        </div>`;

    // Listener per tornare al form
    document.getElementById('btnNuovaRichiesta').addEventListener('click', resetForm);

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================
//  RESET: torna al form pulito
// ============================================================
function resetForm() {
    const summarySection = document.getElementById('summarySection');
    summarySection.classList.add('hidden');
    summarySection.innerHTML = '';

    document.getElementById('formSection').classList.remove('hidden');
    document.getElementById('consultingForm').reset();

    // Ripristina stili dei campi
    document.querySelectorAll('.field-input').forEach(el => {
        el.classList.remove('border-red-400', 'border-green-400');
        el.classList.add('border-gray-300');
    });

    // Ripristina stili checkbox-opzioni
    document.querySelectorAll('.service-option').forEach(label => {
        label.classList.remove('border-blue-500', 'bg-blue-50');
        label.classList.add('border-gray-200');
    });

    // Nascondi tutti i messaggi di errore
    document.querySelectorAll('.error-msg').forEach(el => el.classList.add('hidden'));

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================
//  SUBMIT HANDLER
// ============================================================
document.getElementById('consultingForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Raccolta valori
    const username  = document.getElementById('username').value.trim();
    const password  = document.getElementById('password').value;          // NON trim password
    const phone     = document.getElementById('phone').value.trim();
    const siteUrl   = document.getElementById('siteUrl').value.trim();
    const orgName   = document.getElementById('orgName').value.trim();
    const date      = document.getElementById('requestDate').value;

    const services = [];
    document.querySelectorAll('.service-checkbox:checked').forEach(cb => services.push(cb.value));

    const data   = { username, password, phone, siteUrl, orgName, services, date };
    const errori = validaForm(data);
    const valido = Object.keys(errori).length === 0;

    // Applica feedback visivo a ogni campo
    const campi = [
        { fieldId: 'username',    errorId: 'usernameError', errore: errori.username },
        { fieldId: 'password',    errorId: 'passwordError', errore: errori.password },
        { fieldId: 'phone',       errorId: 'phoneError',    errore: errori.phone },
        { fieldId: 'siteUrl',     errorId: 'urlError',      errore: errori.siteUrl },
        { fieldId: 'orgName',     errorId: 'orgNameError',  errore: errori.orgName },
        { fieldId: 'requestDate', errorId: 'dateError',     errore: errori.date }
    ];

    campi.forEach(({ fieldId, errorId, errore }) => {
        setFieldState(fieldId, !errore);
        errore ? showError(errorId) : hideError(errorId);
    });

    errori.services ? showError('servicesError') : hideError('servicesError');

    if (valido) mostraRiepilogo(data);
});

// ============================================================
//  VALIDAZIONE IN TEMPO REALE (on blur)
// ============================================================
const blurValidators = {
    username:    (el) => PATTERNS.username.test(el.value.trim()),
    password:    (el) => PATTERNS.password.test(el.value),
    phone:       (el) => PATTERNS.phone.test(el.value.trim()),
    siteUrl:     (el) => !!el.value.trim() && PATTERNS.url.test(el.value.trim()),
    orgName:     (el) => el.value.trim().length >= 2,
    requestDate: (el) => PATTERNS.date.test(el.value) && !isNaN(parseLocalDate(el.value).getTime())
};

Object.entries(blurValidators).forEach(([id, validator]) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('blur', function () {
        if (this.value === '') return; // non validare se vuoto (l'utente non ha ancora toccato il campo)
        setFieldState(id, validator(this));
    });
});

// ============================================================
//  STYLING DINAMICO CHECKBOX SERVIZI
// ============================================================
document.querySelectorAll('.service-checkbox').forEach(cb => {
    cb.addEventListener('change', function () {
        const label = this.closest('.service-option');
        if (this.checked) {
            label.classList.add('border-blue-500', 'bg-blue-50');
            label.classList.remove('border-gray-200');
        } else {
            label.classList.remove('border-blue-500', 'bg-blue-50');
            label.classList.add('border-gray-200');
        }
        // Rimuovi l'errore servizi non appena almeno uno è selezionato
        const anyChecked = document.querySelectorAll('.service-checkbox:checked').length > 0;
        if (anyChecked) hideError('servicesError');
    });
});
