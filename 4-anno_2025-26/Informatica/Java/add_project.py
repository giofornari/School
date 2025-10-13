#!/usr/bin/env python3
"""
Script per aggiungere automaticamente progetti Java al sito web showcase.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def get_project_output(project_path):
    """Esegue il progetto Java e cattura l'output."""
    try:
        # Trova tutti i file .java nella cartella src
        src_path = os.path.join(project_path, 'src')
        bin_path = os.path.join(project_path, 'bin')
        
        # Crea la cartella bin se non esiste
        os.makedirs(bin_path, exist_ok=True)
        
        # Compila i file Java
        java_files = [os.path.join(src_path, f) for f in os.listdir(src_path) if f.endswith('.java')]
        if not java_files:
            return None, "Nessun file Java trovato"
        
        compile_cmd = ['javac', '-d', bin_path] + java_files
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if compile_result.returncode != 0:
            return None, compile_result.stderr
        
        # Trova il file con il main (cerca Test* o il nome del progetto)
        project_name = os.path.basename(project_path)
        main_class = None
        
        # Cerca prima TestNomeProgetto
        test_class = f"Test{project_name}"
        for java_file in java_files:
            with open(java_file, 'r') as f:
                content = f.read()
                if 'public static void main' in content:
                    base_name = os.path.basename(java_file).replace('.java', '')
                    if base_name.startswith('Test'):
                        main_class = base_name
                        break
                    elif main_class is None:
                        main_class = base_name
        
        if not main_class:
            return None, "Nessuna classe con metodo main trovata"
        
        # Esegui il programma
        run_cmd = ['java', '-cp', bin_path, main_class]
        run_result = subprocess.run(run_cmd, capture_output=True, text=True)
        
        return run_result.stdout, None if run_result.returncode == 0 else run_result.stderr
        
    except Exception as e:
        return None, str(e)

def read_java_file(file_path):
    """Legge il contenuto di un file Java."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def escape_for_js(text):
    """Escapa il testo per l'uso in JavaScript."""
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def generate_project_html(project_name, java_code, output, main_file):
    """Genera il file HTML per un progetto."""
    
    status = "success" if output else "error"
    output_display = output if output else "Errore di esecuzione"
    
    html_template = f'''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Java Project</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/java.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #0a0e27;
            --bg-secondary: #151932;
            --bg-tertiary: #1e2642;
            --bg-code: #0f1421;
            --text-primary: #f0f3ff;
            --text-secondary: #a0a8c0;
            --text-muted: #6b7599;
            --accent-primary: #00d4ff;
            --accent-secondary: #7c3aed;
            --accent-success: #00ff88;
            --accent-error: #ff4757;
            --border-default: #2d3551;
            --border-accent: rgba(0, 212, 255, 0.3);
            --glow-primary: rgba(0, 212, 255, 0.4);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
        }}
        
        body {{
            font-family: 'DM Sans', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        header {{
            background: var(--bg-secondary);
            padding: 20px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-md);
        }}
        
        header h1 {{
            font-size: 1.5em;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        header h1 i {{
            color: var(--accent-primary);
        }}
        
        .back-btn {{
            background: var(--bg-primary);
            color: var(--text-primary);
            border: 1px solid var(--border-default);
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .back-btn:hover {{
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
            transform: translateY(-1px);
        }}
        
        .container {{
            display: flex;
            flex: 1;
            overflow: hidden;
        }}
        
        .left-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
        }}
        
        .tabs {{
            display: flex;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-default);
            padding: 0 16px;
        }}
        
        .tab-button {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 12px 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }}
        
        .tab-button:hover {{
            color: var(--text-primary);
            border-color: var(--border-accent);
        }}
        
        .tab-button.active {{
            color: var(--accent-primary);
            background: var(--bg-primary);
            border-color: var(--accent-primary);
            box-shadow: 0 0 12px var(--glow-primary);
        }}
        
        .code-area {{
            flex: 1;
            overflow: auto;
        }}
        
        .tab-content {{
            display: none;
            height: 100%;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .tab-content pre {{
            margin: 0;
            height: 100%;
        }}
        
        .tab-content pre code {{
            display: block;
            padding: 24px !important;
            background: var(--bg-code) !important;
            height: 100%;
            font-size: 14px;
            line-height: 1.6;
            font-family: 'Fira Code', monospace;
        }}
        
        .right-panel {{
            width: 45%;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            border-left: 2px solid var(--border-default);
        }}
        
        .run-header {{
            background: var(--bg-tertiary);
            padding: 16px 24px;
            border-bottom: 2px solid var(--border-default);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .run-header h2 {{
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .controls {{
            display: flex;
            gap: 10px;
        }}
        
        .run-btn {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }}
        
        .run-btn:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 0 30px var(--glow-primary);
        }}
        
        .run-btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}
        
        .copy-btn {{
            background: var(--bg-primary);
            color: var(--text-primary);
            border: 1px solid var(--border-default);
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .copy-btn:hover {{
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }}
        
        .output-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .status-bar {{
            padding: 12px 24px;
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-default);
        }}
        
        .status-indicator {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 500;
        }}
        
        .status-indicator.success {{
            color: var(--accent-success);
        }}
        
        .status-indicator.error {{
            color: var(--accent-error);
        }}
        
        .output-wrapper {{
            flex: 1;
            overflow: auto;
            padding: 24px;
            background: var(--bg-code);
        }}
        
        .output-box {{
            font-family: 'Fira Code', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            color: var(--text-secondary);
            padding: 16px;
            background: var(--bg-primary);
            border-radius: 8px;
            border: 1px solid var(--border-default);
        }}
        
        .output-box.success {{
            border-color: var(--accent-success);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        }}
        
        .output-box.error {{
            border-color: var(--accent-error);
            color: var(--accent-error);
        }}
        
        .spinner {{
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid var(--border-default);
            border-top-color: var(--accent-primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-primary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--border-default);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent-primary);
        }}
    </style>
</head>
<body>
    <header>
        <h1>
            <i class="fas fa-code"></i>
            {project_name}
        </h1>
        <a href="index.html" class="back-btn">
            <i class="fas fa-arrow-left"></i>
            Torna alla Home
        </a>
    </header>
    
    <div class="container">
        <div class="left-panel">
            <div class="tabs">
                <button class="tab-button active" data-tab="source">
                    <i class="fas fa-file-code"></i>
                    {main_file}
                </button>
            </div>
            
            <div class="code-area">
                <div id="source" class="tab-content active">
                    <pre><code class="language-java">{java_code}</code></pre>
                </div>
            </div>
        </div>
        
        <div class="right-panel">
            <div class="run-header">
                <h2>
                    <i class="fas fa-terminal"></i>
                    Output
                </h2>
                <div class="controls">
                    <button class="run-btn" id="runBtn" onclick="runCode()">
                        <i class="fas fa-play"></i>
                        Esegui
                    </button>
                    <button class="copy-btn" onclick="copyCode()">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
            </div>
            
            <div class="output-container">
                <div class="status-bar">
                    <div id="statusIndicator"></div>
                </div>
                <div class="output-wrapper">
                    <div id="output" class="output-box">{output_display}</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const projectName = "{project_name}";
        const buildStatus = "{status}";
        const precompiledOutput = "{escape_for_js(output_display)}";
        
        function copyCode() {{
            const activeTab = document.querySelector('.tab-content.active code');
            if (activeTab) {{
                navigator.clipboard.writeText(activeTab.textContent);
                const btn = document.querySelector('.copy-btn');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copiato!';
                setTimeout(() => {{
                    btn.innerHTML = originalText;
                }}, 2000);
            }}
        }}
        
        async function runCode() {{
            const runBtn = document.getElementById('runBtn');
            const output = document.getElementById('output');
            const statusIndicator = document.getElementById('statusIndicator');
            
            runBtn.disabled = true;
            runBtn.innerHTML = '<div class="spinner"></div> Esecuzione...';
            
            statusIndicator.innerHTML = '<div class="status-indicator running"><div class="spinner"></div> Esecuzione in corso...</div>';
            output.className = 'output-box';
            output.textContent = '';
            
            await new Promise(resolve => setTimeout(resolve, 500));
            
            statusIndicator.innerHTML = '<div class="status-indicator {status}"><i class="fas fa-check-circle"></i> Eseguito con successo</div>';
            output.className = 'output-box {status}';
            
            let i = 0;
            const outputText = precompiledOutput;
            const typeSpeed = 2;
            
            function typeWriter() {{
                if (i < outputText.length) {{
                    output.textContent += outputText.charAt(i);
                    i++;
                    setTimeout(typeWriter, typeSpeed);
                }} else {{
                    runBtn.disabled = false;
                    runBtn.innerHTML = '<i class="fas fa-redo"></i> Ri-esegui';
                }}
            }}
            
            typeWriter();
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            hljs.highlightAll();
            
            const statusIndicator = document.getElementById('statusIndicator');
            if (buildStatus === 'success') {{
                statusIndicator.innerHTML = 
                    '<div class="status-indicator success"><i class="fas fa-check-circle"></i> Compilato con successo</div>';
            }} else {{
                statusIndicator.innerHTML = 
                    '<div class="status-indicator error"><i class="fas fa-times-circle"></i> Errori di compilazione</div>';
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_template

def add_project_to_index(project_name, description, badge_type="theory"):
    """Aggiunge il progetto all'index.html."""
    index_path = 'docs/index.html'
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trova il punto dove inserire il nuovo progetto (prima del </div> finale)
    insert_marker = '        </div>\n        \n        <footer>'
    
    badge_html = {
        "theory": '📚 Teoria',
        "lab": '🔬 Laboratorio'
    }
    
    project_card = f'''        
        <a href="{project_name.lower()}.html" class="project-card">
            <div class="card-header">
                <h2>{project_name}</h2>
                <span class="status-badge {"theory" if badge_type == "theory" else "success"}">
                    {badge_html.get(badge_type, badge_html["theory"])}
                </span>
            </div>
            <p class="card-description">{description}</p>
            <div class="card-footer">
                <span class="view-link">
                    Visualizza ed Esegui
                    <i class="fas fa-arrow-right"></i>
                </span>
            </div>
        </a>
        
        </div>
        
        <footer>'''
    
    new_content = content.replace(insert_marker, project_card)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 add_project.py <nome_progetto> [descrizione] [badge_type]")
        print("Esempio: python3 add_project.py Orario 'Gestione orari' theory")
        sys.exit(1)
    
    project_name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else f"Progetto {project_name}"
    badge_type = sys.argv[3] if len(sys.argv) > 3 else "theory"
    
    # Percorsi
    workspace_path = os.getcwd()
    project_path = os.path.join(workspace_path, project_name)
    
    if not os.path.exists(project_path):
        print(f"❌ Progetto '{project_name}' non trovato!")
        sys.exit(1)
    
    print(f"📦 Elaborazione progetto: {project_name}")
    
    # Ottieni l'output del progetto
    output, error = get_project_output(project_path)
    
    if error and not output:
        print(f"⚠️  Errore durante l'esecuzione: {error}")
        output = f"Errore:\n{error}"
    
    # Trova il file Java principale
    src_path = os.path.join(project_path, 'src')
    main_file = None
    java_code = None
    
    for filename in os.listdir(src_path):
        if filename.endswith('.java'):
            file_path = os.path.join(src_path, filename)
            content = read_java_file(file_path)
            if 'public static void main' in content:
                main_file = filename
                java_code = content
                break
    
    if not main_file:
        print("❌ Nessun file con metodo main trovato!")
        sys.exit(1)
    
    print(f"📄 File principale: {main_file}")
    
    # Genera HTML
    html_content = generate_project_html(project_name, java_code, output, main_file)
    
    # Salva HTML
    docs_path = os.path.join(workspace_path, 'docs')
    os.makedirs(docs_path, exist_ok=True)
    
    html_file = os.path.join(docs_path, f'{project_name.lower()}.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Creato: {html_file}")
    
    # Salva output
    output_file = os.path.join(docs_path, f'{project_name.lower()}-output.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output if output else "")
    
    print(f"✅ Creato: {output_file}")
    
    # Aggiorna index.html
    add_project_to_index(project_name, description, badge_type)
    print(f"✅ Aggiornato: docs/index.html")
    
    print(f"\n🎉 Progetto '{project_name}' aggiunto al sito con successo!")

if __name__ == '__main__':
    main()
