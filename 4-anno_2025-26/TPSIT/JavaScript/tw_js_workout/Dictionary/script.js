document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchbtn');
    const searchInput = document.getElementById('search_txt');
    const wordInput = document.getElementById('word');
    const meaningInput = document.getElementById('means');
    const addBtn = document.getElementById('add');
    const clearBtn = document.getElementById('clear');
    const tableToggleBtn = document.getElementById('toggle_table');
    const tableContainer = document.getElementById('dictionary_table_container');
    const tableBody = document.getElementById('dictionary_table_body');
    const resultOutput = document.getElementById('result_output');

    const dictionaryEntries = [
        { italian: 'ciao', english: 'hello' },
        { italian: 'grazie', english: 'thank you' },
        { italian: 'prego', english: "you're welcome" },
        { italian: 'per favore', english: 'please' },
        { italian: 'casa', english: 'house' },
        { italian: 'cane', english: 'dog' },
        { italian: 'gatto', english: 'cat' },
        { italian: 'acqua', english: 'water' },
        { italian: 'amore', english: 'love' },
        { italian: 'scuola', english: 'school' },
        { italian: 'libro', english: 'book' },
    ];

    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim().toLowerCase();

        if (!query) {
            resultOutput.textContent = 'Word not found';
            resultOutput.classList.remove('text-green-700');
            resultOutput.classList.add('text-red-600');
            return;
        }
        const match = dictionaryEntries.find((entry) => { return entry.italian === query || entry.english === query });

        if (match) {
            const ita = match.italian.trim().toLowerCase();
            const translation = ita === query ? match.english : match.italian;
            resultOutput.textContent = ` "${query}" --> ${translation}`;
            resultOutput.classList.remove('text-red-600');
            resultOutput.classList.add('text-green-700 p-5');
        } else {
            resultOutput.textContent = `"${query}" not in dictionary.`;
            resultOutput.classList.remove('text-green-700');
            resultOutput.classList.add('text-red-600');
        }
    });


    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            searchBtn.click();
        }
    });

    // Alterno la visibilità della tabella e genero i dati quando serve.
    tableToggleBtn.addEventListener('click', () => {
        const shouldShow = tableContainer.style.display === 'none';
        if (shouldShow) {
            // Svuoto il corpo della tabella prima di ricreare tutte le righe.
            tableBody.innerHTML = '';
            // Ordino le voci alfabeticamente per l'italiano.
            const orderedEntries = [...dictionaryEntries].sort((a, b) => a.italian.localeCompare(b.italian));
            // Genero ogni riga con le due colonne richieste.
            orderedEntries.forEach((entry, index) => {
                const row = document.createElement('tr');
                row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';
                row.innerHTML = `
                    <td class="px-4 py-3 font-medium text-gray-800">${entry.italian}</td>
                    <td class="px-4 py-3 text-gray-600">${entry.english}</td>`;
                tableBody.appendChild(row);
            });
            // Rendo visibile il contenitore e aggiorno il testo del bottone.
            tableContainer.style.display = 'block';
            tableContainer.classList.remove('hidden');
            tableToggleBtn.textContent = 'Nascondi tutte le traduzioni';
        } else {
            // Nascondo il contenitore e ripristino il testo originale del bottone.
            tableContainer.style.display = 'none';
            tableContainer.classList.add('hidden');
            tableToggleBtn.textContent = 'Mostra tutte le traduzioni';
        }
    });

    // Gestisco l'aggiunta di nuove parole italiane-inglesi.
    addBtn.addEventListener('click', () => {
        // Raccolgo le due parole e rimuovo eventuali spazi di troppo.
        const italianInput = wordInput.value.trim();
        const englishInput = meaningInput.value.trim();
        // Impedisco l'inserimento se uno dei due campi è vuoto.
        if (!italianInput || !englishInput) {
            alert('Compila sia la parola (italiano) che la traduzione (inglese).');
            return;
        }
        // Calcolo le versioni normalizzate per evitare duplicati.
        const ita = italianInput.toLowerCase();
        const normalizedEnglish = englishInput.toLowerCase();
        // Controllo se esiste già una voce con una delle due parole.
        const alreadyExists = dictionaryEntries.some((entry) => {
            const normalizedEntryItalian = entry.italian.trim().toLowerCase();
            const normalizedEntryEnglish = entry.english.trim().toLowerCase();
            return (
                normalizedEntryItalian === ita ||
                normalizedEntryEnglish === normalizedEnglish ||
                normalizedEntryItalian === normalizedEnglish ||
                normalizedEntryEnglish === ita
            );
        });
        // Blocco l'inserimento se trovo un duplicato.
        if (alreadyExists) {
            alert('La parola inserita è già presente nel dizionario.');
            return;
        }
        // Se arrivo qui posso salvare la nuova coppia nel dizionario.
        dictionaryEntries.push({ italian: italianInput, english: englishInput });
        alert('Nuova traduzione aggiunta con successo!');
        // Pulisco i campi per facilitare un nuovo inserimento.
        wordInput.value = '';
        meaningInput.value = '';
        // Se la tabella è visibile, la ricreo per mostrare subito la nuova voce.
        if (tableContainer.style.display === 'block') {
            tableBody.innerHTML = '';
            const orderedEntries = [...dictionaryEntries].sort((a, b) => a.italian.localeCompare(b.italian));
            orderedEntries.forEach((entry, index) => {
                const row = document.createElement('tr');
                row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';
                row.innerHTML = `
                    <td class="px-4 py-3 font-medium text-gray-800">${entry.italian}</td>
                    <td class="px-4 py-3 text-gray-600">${entry.english}</td>`;
                tableBody.appendChild(row);
            });
        }
    });

    clearBtn.addEventListener('click', () => {
        wordInput.value = '';
        meaningInput.value = '';
    });

});