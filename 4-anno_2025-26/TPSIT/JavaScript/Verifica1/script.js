let collection = [
    { titolo: "Inception", regista: "Christopher Nolan", anno: 2010 },
    { titolo: "Interstellar", regista: "Christopher Nolan", anno: 2014 },
    { titolo: "Avatar", regista: "James Cameron", anno: 2009 },
    { titolo: "Dune", regista: "David Lynch", anno: 2021 },
    { titolo: "Tenet", regista: "Christopher Nolan", anno: 2020 }
];

let seen = [...collection];

const tbody = document.getElementById('tablella');
const noResults = document.getElementById('errore');
const resultOutput = document.getElementById('result_output');
const searchInput = document.getElementById('search_txt');
const searchBtn = document.getElementById('searchbtn');
const showAllBtn = document.getElementById('show_all');
const filmForm = document.getElementById('filmForm');
const titoloInput = document.getElementById('titolo');
const registaInput = document.getElementById('regista');
const annoInput = document.getElementById('anno');
const sortBy = document.getElementById('sortBy');

const renderTable = (films) => {
    tbody.innerHTML = '';
    
    if (films.length === 0) {
        noResults.classList.remove('hidden');
        resultOutput.textContent = 'Non ghe miga gninta';
        resultOutput.className = 'mt-3 text-sm font-semibold text-red-500';
        return;
    }
    
    noResults.classList.add('hidden');
    resultOutput.textContent = `Trovati ${films.length} film`;
    resultOutput.className = 'mt-3 text-sm font-semibold text-green-600';
    
    films.forEach(film => {
        const row = tbody.insertRow();
        row.className = 'hover:bg-green-50 transition-colors duration-200';
        row.innerHTML = `
            <td class="px-6 py-4 text-gray-800 font-medium">${film.titolo}</td>
            <td class="px-6 py-4 text-gray-700">${film.regista}</td>
            <td class="px-6 py-4 text-gray-600">${film.anno}</td>
        `;
    });
};

document.addEventListener('DOMContentLoaded', () => {
    renderTable(seen);
    
    searchBtn.addEventListener('click', () => {
        const regista = searchInput.value.trim();
        
        if (!regista) {
            resultOutput.textContent = 'damen un nom de un regista';
            resultOutput.className = 'mt-3 text-sm font-semibold text-orange-500';
            return;
        }
        seen = collection.filter(film => 
            film.regista.toLowerCase().includes(regista.toLowerCase())
        );
        renderTable(seen);        
    });
    
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchBtn.click();
        }
    });
    
    showAllBtn.addEventListener('click', () => {
        seen = [...collection];
        renderTable(seen);
        searchInput.value = '';
        sortBy.value = '';
        resultOutput.textContent = 'To fat vder tut';
        resultOutput.className = 'mt-3 text-sm font-semibold text-green-600';
    });
    
    filmForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const titolo = titoloInput.value.trim();
        const regista = registaInput.value.trim();
        const annoValue = annoInput.value;
        const anno = parseInt(annoValue);
        
        if (!titolo || !regista || !annoValue) {
            resultOutput.textContent = 'Scrivi tut, par dio';
            resultOutput.className = 'mt-3 text-sm font-semibold text-red-500';
            return;
        }
                
        if (collection.find(film => 
            film.titolo.toLowerCase() === titolo.toLowerCase() && film.regista.toLowerCase() === regista.toLowerCase() && film.anno === anno)) {
            resultOutput.textContent = 'ghel sa nel catalogo!';
            resultOutput.className = 'mt-3 text-sm font-semibold text-orange-500';
            return;
        }
        
        collection.push({ titolo, regista, anno });
        seen = [...collection];
        renderTable(seen);
        filmForm.reset();
        resultOutput.textContent = `Film "${titolo}" richiesto!`;
        resultOutput.className = 'mt-3 text-sm font-semibold text-green-600';
    });
    
    sortBy.addEventListener('change', () => {
        const sortByValue = sortBy.value;     
        const sorted = [...seen].sort((a, b) => {
            if (sortByValue === 'anno') return a.anno - b.anno;
            return a[sortByValue].localeCompare(b[sortByValue], undefined, { sensitivity: 'base' });
        });
        
        renderTable(sorted);
        resultOutput.className = 'mt-3 text-sm font-semibold text-green-600';
    });
});