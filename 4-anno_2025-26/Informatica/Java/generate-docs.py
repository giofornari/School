#!/usr/bin/env python3
"""
Automatic Java Project Documentation Generator
Scans all Java projects in the workspace and generates:
1. Individual project HTML pages
2. Updated index.html with all projects
3. Output text files
"""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional

# Configuration
WORKSPACE_ROOT = Path(__file__).parent
DOCS_DIR = WORKSPACE_ROOT / "docs"
EXCLUDED_DIRS = {'.git', '.github', '.vscode', 'docs', 'node_modules', '__pycache__'}

# Project type badges
PROJECT_TYPES = {
    'theory': {'emoji': '📚', 'label': 'Teoria', 'class': 'theory'},
    'lab': {'emoji': '🔬', 'label': 'Laboratorio', 'class': 'success'},
}


def find_java_projects() -> List[Dict]:
    """Find all Java projects in the workspace."""
    projects = []
    
    for item in WORKSPACE_ROOT.iterdir():
        if not item.is_dir() or item.name in EXCLUDED_DIRS:
            continue
            
        src_dir = item / "src"
        if not src_dir.exists():
            continue
            
        # Find Java files
        java_files = list(src_dir.glob("*.java"))
        if not java_files:
            continue
            
        project = {
            'name': item.name,
            'path': item,
            'src_dir': src_dir,
            'java_files': java_files,
            'main_file': None,
            'type': 'theory'  # default
        }
        
        # Find main file (usually the one with same name as directory or containing main method)
        for java_file in java_files:
            if java_file.stem == item.name or java_file.stem.lower() == item.name.lower():
                project['main_file'] = java_file
                break
        
        # If no matching file, find one with main method
        if not project['main_file']:
            for java_file in java_files:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'public static void main' in content:
                        project['main_file'] = java_file
                        break
        
        if project['main_file']:
            projects.append(project)
    
    return projects


def compile_and_run_project(project: Dict) -> tuple[bool, str]:
    """Compile and run a Java project, return (success, output)."""
    try:
        # Compile
        bin_dir = project['path'] / 'bin'
        bin_dir.mkdir(exist_ok=True)
        
        compile_cmd = [
            'javac',
            '-d', str(bin_dir),
            str(project['main_file'])
        ]
        
        result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, f"Compilation Error:\n{result.stderr}"
        
        # Run
        class_name = project['main_file'].stem
        run_cmd = [
            'java',
            '-cp', str(bin_dir),
            class_name
        ]
        
        result = subprocess.run(
            run_cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(project['path'])
        )
        
        return True, result.stdout
        
    except subprocess.TimeoutExpired:
        return False, "Execution timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def escape_for_js(text: str) -> str:
    """Escape text for JavaScript string."""
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')


def read_java_file(file_path: Path) -> str:
    """Read Java file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def detect_project_type(project: Dict) -> str:
    """Detect if project is theory or lab based on naming conventions."""
    name_lower = project['name'].lower()
    
    # Lab indicators
    if any(word in name_lower for word in ['merge', 'count', 'array', 'cd', 'oggetto']):
        return 'lab'
    
    # Theory indicators (geometric shapes, basic classes)
    if any(word in name_lower for word in ['cerchio', 'punto', 'rettangolo', 'libro', 'triangolo']):
        return 'theory'
    
    return 'theory'  # default


def generate_project_description(project: Dict) -> str:
    """Generate a description for the project based on its name and content."""
    descriptions = {
        'cerchio': 'Classe per calcolare area e circonferenza di un cerchio',
        'punto': 'Rappresentazione di un punto nel piano cartesiano',
        'rettangolo': 'Calcolo di vertici e proprietà di un rettangolo',
        'libro': 'Gestione di oggetti libro con calcolo del prezzo',
        'mergearray': 'Unione e ordinamento di array',
        'oggettocd': 'Gestione di un catalogo CD',
        'vocalcount': 'Conteggio delle vocali in una stringa',
    }
    
    name_lower = project['name'].lower()
    for key, desc in descriptions.items():
        if key in name_lower:
            return desc
    
    # Generic description
    return f"Progetto Java: {project['name']}"


def generate_project_html(project: Dict, success: bool, output: str) -> str:
    """Generate HTML page for a project."""
    
    java_code = read_java_file(project['main_file'])
    java_code_escaped = escape_for_js(java_code)
    output_escaped = escape_for_js(output)
    
    # Get icon based on project name
    icon = 'fa-code'
    name_lower = project['name'].lower()
    if 'libro' in name_lower or 'book' in name_lower:
        icon = 'fa-book'
    elif 'cerchio' in name_lower or 'circle' in name_lower:
        icon = 'fa-circle'
    elif 'punto' in name_lower or 'point' in name_lower:
        icon = 'fa-dot-circle'
    elif 'rettangolo' in name_lower or 'rectangle' in name_lower:
        icon = 'fa-square'
    elif 'array' in name_lower:
        icon = 'fa-list'
    elif 'cd' in name_lower:
        icon = 'fa-compact-disc'
    
    html_template = f'''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project['name']} - Java Project</title>
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
            --accent-warning: #ffd60a;
            --accent-error: #ff4757;
            --border-default: #2d3551;
            --border-accent: rgba(0, 212, 255, 0.3);
            --glow-primary: rgba(0, 212, 255, 0.4);
            --glow-secondary: rgba(124, 58, 237, 0.4);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
            --shadow-glow: 0 0 20px var(--glow-primary);
        }}
        
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
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
            border-bottom: 1px solid var(--border-light);
            box-shadow: var(--shadow-sm);
        }}
        
        header h1 {{
            font-size: 1.5em;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-primary);
        }}
        
        header h1 i {{
            color: var(--accent-primary);
        }}
        
        .back-btn {{
            background: var(--bg-primary);
            color: var(--text-primary);
            border: 1px solid var(--border-light);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .back-btn:hover {{
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .container {{
            display: flex;
            flex: 1;
            overflow: hidden;
            background: var(--bg-primary);
        }}
        
        .left-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-light);
        }}
        
        .tabs {{
            display: flex;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-light);
            padding: 0 16px;
            overflow-x: auto;
        }}
        
        .tab-button {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 12px 20px;
            cursor: pointer;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            white-space: nowrap;
            transition: all 0.2s ease;
            font-family: 'Fira Code', monospace;
            border: 1px solid transparent;
        }}
        
        .tab-button:hover {{
            color: var(--text-primary);
            background: var(--bg-secondary);
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
            position: relative;
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
            font-family: 'Fira Code', 'Consolas', monospace;
            color: var(--text-primary) !important;
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
            color: var(--text-primary);
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
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px var(--glow-primary);
        }}
        
        .run-btn:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 0 30px var(--glow-primary), var(--shadow-lg);
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
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .copy-btn:hover {{
            background: var(--bg-tertiary);
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
        
        .status-indicator.running {{
            color: var(--accent-warning);
        }}
        
        .output-wrapper {{
            flex: 1;
            overflow: auto;
            padding: 24px;
            background: var(--bg-code);
        }}
        
        .output-box {{
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            color: var(--text-secondary);
            padding: 16px;
            background: var(--bg-primary);
            border-radius: 8px;
            border: 1px solid var(--border-default);
            min-height: 100px;
        }}
        
        .output-box.success {{
            border-color: var(--accent-success);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        }}
        
        .output-box.error {{
            border-color: var(--accent-error);
            box-shadow: 0 0 20px rgba(255, 71, 87, 0.2);
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
            height: 10px;
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
        
        @media (max-width: 1024px) {{
            .container {{
                flex-direction: column;
            }}
            
            .right-panel {{
                width: 100%;
                height: 50%;
                border-left: none;
                border-top: 2px solid var(--border-default);
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>
            <i class="fas {icon}"></i>
            {project['name']}
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
                    {project['main_file'].name}
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
                    <div id="output" class="output-box">{output}</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const sourceCode = ["{java_code_escaped}"];
        const projectName = "{project['name']}";
        const buildStatus = "{'success' if success else 'error'}";
        const precompiledOutput = "{output_escaped}";
        
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            const selectedTab = document.getElementById(tabId);
            if (selectedTab) {{
                selectedTab.classList.add('active');
            }}
            
            const clickedButton = document.querySelector(`[data-tab="${{tabId}}"]`);
            if (clickedButton) {{
                clickedButton.classList.add('active');
            }}
            
            hljs.highlightAll();
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.tab-button').forEach(button => {{
                button.addEventListener('click', function() {{
                    const tabId = this.getAttribute('data-tab');
                    switchTab(tabId);
                }});
            }});
        }});
        
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
            
            statusIndicator.innerHTML = '<div class="status-indicator success"><i class="fas fa-check-circle"></i> Eseguito con successo</div>';
            output.className = 'output-box success';
            
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


def generate_index_html(projects: List[Dict]) -> str:
    """Generate the main index.html with all projects."""
    
    project_cards = []
    for project in projects:
        proj_type = PROJECT_TYPES[project['type']]
        description = generate_project_description(project)
        
        card = f'''        <a href="{project['name'].lower()}.html" class="project-card">
            <div class="card-header">
                <h2>{project['name']}</h2>
                <span class="status-badge {proj_type['class']}">
                    {proj_type['emoji']} {proj_type['label']}
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
        '''
        project_cards.append(card)
    
    cards_html = '\n'.join(project_cards)
    
    index_template = f'''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Java Projects Showcase</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #0a0e27;
            --bg-secondary: #151932;
            --bg-tertiary: #1e2642;
            --text-primary: #f0f3ff;
            --text-secondary: #a0a8c0;
            --text-muted: #6b7599;
            --accent-primary: #00d4ff;
            --accent-secondary: #7c3aed;
            --accent-tertiary: #ff006e;
            --accent-success: #00ff88;
            --accent-warning: #ffd60a;
            --accent-error: #ff4757;
            --border-default: #2d3551;
            --border-accent: rgba(0, 212, 255, 0.3);
            --glow-primary: rgba(0, 212, 255, 0.4);
            --glow-secondary: rgba(124, 58, 237, 0.4);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.6);
            --shadow-glow: 0 0 20px var(--glow-primary);
        }}
        
        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 60px;
            padding: 40px 20px;
        }}
        
        h1 {{
            font-size: 3.5em;
            margin-bottom: 12px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 50%, var(--accent-tertiary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1.5px;
            text-shadow: 0 0 40px var(--glow-primary);
        }}
        
        h1 .emoji {{
            display: inline-block;
            animation: bounce 2s ease-in-out infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .subtitle {{
            font-size: 1.25em;
            color: var(--text-primary);
            margin-bottom: 100px;
            font-weight: 500;
            opacity: 0.9;
        }}
        
        .github-link {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
            padding: 16px 36px;
            border-radius: 12px;
            color: var(--text-primary);
            text-decoration: none;
            transition: all 0.3s ease;
            border: 2px solid var(--border-default);
            font-weight: 600;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
            margin: 16px;
        }}
        
        .github-link::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--glow-primary), transparent);
            transition: left 0.5s;
        }}
        
        .github-link:hover::before {{
            left: 100%;
        }}
        
        .github-link:hover {{
            border-color: var(--accent-primary);
            transform: translateY(-3px);
            box-shadow: var(--shadow-glow), var(--shadow-lg);
            color: var(--accent-primary);
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 24px;
            margin-bottom: 60px;
        }}
        
        .project-card {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border-radius: 20px;
            padding: 32px;
            text-decoration: none;
            color: inherit;
            display: block;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid var(--border-default);
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }}
        
        .project-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, var(--glow-primary) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.5s ease;
        }}
        
        .project-card:hover::before {{
            opacity: 0.15;
        }}
        
        .project-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 16px 48px rgba(0, 212, 255, 0.25), 0 0 40px var(--glow-secondary);
            border-color: var(--accent-primary);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 18px;
            gap: 12px;
            position: relative;
            z-index: 1;
        }}
        
        .card-header h2 {{
            font-size: 1.7em;
            flex: 1;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
        }}
        
        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .status-badge.success {{
            background: rgba(0, 255, 136, 0.15);
            color: var(--accent-success);
            border: 2px solid var(--accent-success);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
        }}
        
        .status-badge.theory {{
            background: rgba(255, 215, 0, 0.15);
            color: #ffd700;
            border: 2px solid #ffd700;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        }}
        
        .status-badge.error {{
            background: rgba(255, 71, 87, 0.15);
            color: var(--accent-error);
            border: 2px solid var(--accent-error);
            box-shadow: 0 0 15px rgba(255, 71, 87, 0.4);
        }}
        
        .card-description {{
            color: var(--text-primary);
            font-size: 1em;
            line-height: 1.7;
            margin-bottom: 24px;
            min-height: 48px;
            position: relative;
            z-index: 1;
            opacity: 0.85;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding-top: 20px;
            border-top: 2px solid var(--border-default);
            position: relative;
            z-index: 1;
        }}
        
        .view-link {{
            color: var(--accent-primary);
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .project-card:hover .view-link {{
            gap: 14px;
            color: var(--accent-secondary);
            text-shadow: 0 0 10px var(--glow-secondary);
        }}
        
        footer {{
            text-align: center;
            color: var(--text-secondary);
            padding: 40px 20px;
            margin-top: 60px;
            border-top: 2px solid var(--border-default);
        }}
        
        footer a {{
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 700;
            transition: all 0.3s;
            position: relative;
        }}
        
        footer a:hover {{
            color: var(--accent-secondary);
            text-shadow: 0 0 10px var(--glow-secondary);
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.5em;
            }}
            
            .projects-grid {{
                grid-template-columns: 1fr;
            }}
            
            body {{
                padding: 20px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Java homeworks and exercises</h1>
            <p class="subtitle">My own showcase for all my exercises in Java ICT class. <br></p>
            <a href="https://github.com/bigBrodyG/JavaProjects" class="github-link">
                <i class="fab fa-github"></i>
                View on GitHub
            </a>
        </header>
        
        <div class="projects-grid">
            
{cards_html}
        
        </div>
        
        <footer>
            <p style="margin-top: 10px;">
                <a href="https://github.com/bigBrodyG/JavaProjects">bigBrodyG/JavaProjects</a>
            </p>
        </footer>
    </div>
</body>
</html>'''
    
    return index_template


def main():
    """Main function to generate all documentation."""
    print("🔍 Scanning for Java projects...")
    projects = find_java_projects()
    
    if not projects:
        print("❌ No Java projects found!")
        return
    
    print(f"✅ Found {len(projects)} projects: {', '.join(p['name'] for p in projects)}")
    
    # Create docs directory if it doesn't exist
    DOCS_DIR.mkdir(exist_ok=True)
    
    # Process each project
    for project in projects:
        print(f"\n📦 Processing {project['name']}...")
        
        # Detect project type
        project['type'] = detect_project_type(project)
        print(f"   Type: {PROJECT_TYPES[project['type']]['label']}")
        
        # Compile and run
        success, output = compile_and_run_project(project)
        
        if success:
            print(f"   ✅ Compiled and executed successfully")
        else:
            print(f"   ⚠️  Compilation/execution failed")
        
        # Generate HTML
        html_content = generate_project_html(project, success, output)
        html_file = DOCS_DIR / f"{project['name'].lower()}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   📝 Generated {html_file.name}")
        
        # Save output to text file
        output_file = DOCS_DIR / f"{project['name'].lower()}-output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"   💾 Saved output to {output_file.name}")
    
    # Generate index.html
    print("\n📄 Generating index.html...")
    index_content = generate_index_html(projects)
    index_file = DOCS_DIR / "index.html"
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Generated {index_file.name}")
    
    print(f"\n🎉 Documentation generated successfully!")
    print(f"📂 Output directory: {DOCS_DIR}")
    print(f"🌐 Open {index_file} in your browser to view the showcase")


if __name__ == "__main__":
    main()
