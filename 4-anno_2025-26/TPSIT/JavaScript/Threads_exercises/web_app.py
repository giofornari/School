from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from bs4 import BeautifulSoup
import threading
from requests import get
import time

app = Flask(__name__)
CORS(app)

# Template HTML per l'interfaccia web
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Scraper Multithread</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        #loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #results {
            margin-top: 20px;
        }
        .result-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 10px;
        }
        .result-title {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
        }
        .url-list {
            max-height: 300px;
            overflow-y: auto;
        }
        .url-item {
            padding: 8px;
            background: white;
            margin-bottom: 5px;
            border-radius: 4px;
            word-break: break-all;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Web Scraper Multithread</h1>
        <p class="subtitle">Cerca una parola in oltre 2000 siti web</p>
        
        <form id="searchForm">
            <div class="input-group">
                <label for="searchWord">Cosa vuoi cercare?</label>
                <input type="text" id="searchWord" name="searchWord" 
                       placeholder="Es: python, javascript, technology..." required>
            </div>
            <button type="submit" id="searchBtn">Avvia Ricerca</button>
        </form>

        <div id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 10px; color: #667eea;">Ricerca in corso...</p>
        </div>

        <div id="results"></div>
    </div>

    <script>
        document.getElementById('searchForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const searchWord = document.getElementById('searchWord').value;
            const searchBtn = document.getElementById('searchBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Mostra loading
            searchBtn.disabled = true;
            loading.style.display = 'block';
            results.innerHTML = '';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ search_word: searchWord })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    results.innerHTML = `
                        <div class="result-box">
                            <div class="result-title">📊 Risultati della Ricerca</div>
                            <div class="stats">
                                <div class="stat-item">
                                    <div class="stat-number">${data.count}</div>
                                    <div class="stat-label">Trovati</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-number">${data.total_urls}</div>
                                    <div class="stat-label">Siti Analizzati</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-number">${data.execution_time}s</div>
                                    <div class="stat-label">Tempo di Esecuzione</div>
                                </div>
                            </div>
                            ${data.found_urls.length > 0 ? `
                                <div style="margin-top: 20px;">
                                    <strong>Siti dove è stata trovata "${searchWord}":</strong>
                                    <div class="url-list">
                                        ${data.found_urls.map(url => `<div class="url-item">✅ ${url}</div>`).join('')}
                                    </div>
                                </div>
                            ` : `<p style="margin-top: 20px; text-align: center;">❌ Nessun risultato trovato</p>`}
                        </div>
                    `;
                } else {
                    results.innerHTML = `<div class="result-box" style="color: red;">❌ ${data.message}</div>`;
                }
            } catch (error) {
                results.innerHTML = `<div class="result-box" style="color: red;">❌ Errore: ${error.message}</div>`;
            } finally {
                searchBtn.disabled = false;
                loading.style.display = 'none';
            }
        });
    </script>
</body>
</html>
'''

def load_urls():
    """Carica gli URL dal file urls.txt"""
    try:
        with open('urls.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def scrape_url(url, search_word, results, lock):
    """Funzione per lo scraping di un singolo URL"""
    try:
        resp = get(url, timeout=5)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            page_text = soup.get_text()
            
            if search_word.lower() in page_text.lower():
                with lock:
                    results.append(url)
    except Exception:
        pass

@app.route('/')
def index():
    """Pagina principale"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint per la ricerca"""
    data = request.get_json()
    search_word = data.get('search_word', '')
    
    if not search_word:
        return jsonify({
            'success': False,
            'message': 'Parola di ricerca mancante'
        }), 400
    
    urls = load_urls()
    
    if not urls:
        return jsonify({
            'success': False,
            'message': 'Nessun URL trovato nel file urls.txt'
        }), 404
    
    # Preparazione per il threading
    results = []
    lock = threading.Lock()
    threads = []
    
    start_time = time.time()
    
    # Crea e avvia i thread
    for url in urls:
        t = threading.Thread(target=scrape_url, args=(url, search_word, results, lock))
        threads.append(t)
        t.start()
    
    # Aspetta che tutti i thread finiscano
    for t in threads:
        t.join()
    
    execution_time = round(time.time() - start_time, 2)
    
    return jsonify({
        'success': True,
        'search_word': search_word,
        'count': len(results),
        'total_urls': len(urls),
        'found_urls': results,
        'execution_time': execution_time
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'webscraper'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
