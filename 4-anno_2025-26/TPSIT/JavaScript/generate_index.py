#!/usr/bin/env python3
"""
Generate an index.html page that lists all projects and exercises in the repository.
This script scans all directories and creates a beautiful landing page.
"""

import os
import json
from pathlib import Path
from datetime import datetime
import re

# Directories to ignore during scanning
IGNORED_DIRS = {
    '.git',
    '__pycache__',
    'node_modules',
    '.vscode',
    '.idea',
    'venv',
    'env',
    '.pytest_cache',
    'dist',
    'build',
    'sdfiles'
}

def scan_directory(base_path, dir_name):
    """Scan a directory recursively for HTML, Python, and JavaScript files."""
    dir_path = base_path / dir_name
    if not dir_path.exists():
        return None
    
    files = []
    js_files_to_hide = set()  # JS files referenziati in HTML
    
    # Prima passa: trova tutti i file .js referenziati negli HTML
    for file_path in dir_path.rglob("*.html"):
        if any(ignored in file_path.parts for ignored in IGNORED_DIRS):
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Trova tutti i src="*.js"
                js_refs = re.findall(r'src=["\']([^"\']*\.(?:js|mjs))["\']', content, re.IGNORECASE)
                for js_ref in js_refs:
                    # Risolvi il path relativo
                    js_file = file_path.parent / js_ref.lstrip('./')
                    if js_file.exists():
                        js_files_to_hide.add(js_file)
        except:
            pass
    
    # Recursively find all files
    for file_path in sorted(dir_path.rglob("*")):
        # Skip files in ignored directories
        if any(ignored in file_path.parts for ignored in IGNORED_DIRS):
            continue
        
        # Skip JS files che sono referenziati in HTML
        if file_path in js_files_to_hide:
            continue
            
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext in ['.html', '.htm', '.py', '.js', '.mjs']:
                # Get file size
                size = file_path.stat().st_size
                size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
                
                # Get modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                # Get relative path from the category directory
                rel_path = file_path.relative_to(dir_path)
                
                # Extract title for HTML files
                display_name = file_path.name
                if ext in ['.html', '.htm']:
                    title = extract_html_title(file_path)
                    if title:
                        display_name = title
                
                files.append({
                    'name': file_path.name,
                    'display_name': display_name,
                    'path': f"{dir_name}/{rel_path}",
                    'type': ext[1:].upper(),
                    'size': size_str,
                    'modified': mtime.strftime('%Y-%m-%d'),
                    'subfolder': str(rel_path.parent) if rel_path.parent != Path('.') else '',
                    'is_html': ext in ['.html', '.htm']
                })
    
    return {
        'name': dir_name,
        'files': files,
        'count': len(files)
    } if files else None

def extract_html_title(file_path):
    """Extract the <title> tag content from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # Read first 2KB
            match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except:
        pass
    return None

def generate_html(projects):
    """Generate the HTML content for the index page using Tailwind CSS."""
    
    # Count total files
    total_files = sum(p['count'] for p in projects)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JavaScript Homemade - Projects & Exercises</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    animation: {{
                        'fade-in': 'fadeIn 0.6s ease-out',
                        'slide-up': 'slideUp 0.6s ease-out',
                        'bounce-slow': 'bounce 2s infinite',
                    }},
                    keyframes: {{
                        fadeIn: {{
                            '0%': {{ opacity: '0' }},
                            '100%': {{ opacity: '1' }},
                        }},
                        slideUp: {{
                            '0%': {{ opacity: '0', transform: 'translateY(30px)' }},
                            '100%': {{ opacity: '1', transform: 'translateY(0)' }},
                        }},
                    }},
                }}
            }}
        }}
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        .animate-float {{ animation: float 3s ease-in-out infinite; }}
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
        <!-- Header -->
        <header class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 md:p-12 mb-8 text-center border border-white/20 animate-fade-in">
            <div class="text-6xl mb-6 animate-float">🚀</div>
            <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
                JavaScript Homemade
            </h1>
            <p class="text-gray-600 text-lg mb-8">Interactive Projects & Coding Exercises</p>
            
            <div class="flex flex-wrap justify-center gap-4">
                <div class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-8 py-4 rounded-2xl shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 cursor-default">
                    <div class="text-3xl font-bold">{len(projects)}</div>
                    <div class="text-sm uppercase tracking-wider opacity-90">Categories</div>
                </div>
                <div class="bg-gradient-to-r from-purple-500 to-pink-600 text-white px-8 py-4 rounded-2xl shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 cursor-default">
                    <div class="text-3xl font-bold">{total_files}</div>
                    <div class="text-sm uppercase tracking-wider opacity-90">Total Files</div>
                </div>
            </div>
        </header>

"""
    
    # Generate project sections
    for idx, project in enumerate(projects):
        delay_class = f"animate-slide-up" if idx % 2 == 0 else "animate-slide-up"
        html += f"""
        <section class="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-6 md:p-8 mb-6 border border-white/20 hover:shadow-indigo-200/50 hover:-translate-y-1 transition-all duration-300 {delay_class}">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 pb-6 border-b-2 border-gradient-to-r from-indigo-200 to-purple-200">
                <h2 class="text-2xl md:text-3xl font-bold text-gray-800 flex items-center gap-3">
                    <span class="text-3xl">📁</span>
                    {project['name']}
                </h2>
                <span class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-6 py-2 rounded-full text-sm font-bold shadow-lg">
                    {project['count']} files
                </span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
"""
        
        for file in project['files']:
            # Determine file type colors
            type_colors = {
                'HTML': 'from-orange-500 to-red-500',
                'HTM': 'from-orange-500 to-red-500',
                'PY': 'from-blue-600 to-blue-800',
                'JS': 'from-yellow-400 to-yellow-600',
                'MJS': 'from-yellow-400 to-yellow-600'
            }
            color = type_colors.get(file['type'], 'from-gray-500 to-gray-700')
            
            subfolder_badge = ""
            if file['subfolder']:
                subfolder_badge = f"""
                    <div class="text-xs text-gray-500 mt-1 flex items-center gap-1">
                        <span>📂</span>
                        <span>{file['subfolder']}</span>
                    </div>
                """
            
            # Determina se mostrare il menu o link diretto
            if file['is_html']:
                # Escape delle virgolette nel titolo
                safe_title = file['display_name'].replace("'", "\\'")
                onclick = f"openModal('{file['path']}', '{safe_title}')"
                html += f"""
                <div onclick="{onclick}" 
                   class="group bg-white hover:bg-gradient-to-br hover:from-indigo-50 hover:to-purple-50 rounded-2xl p-5 shadow-md hover:shadow-xl border-2 border-gray-100 hover:border-indigo-300 transition-all duration-300 hover:-translate-y-2 cursor-pointer">
                    <div class="flex items-start justify-between mb-3">
                        <span class="bg-gradient-to-r {color} text-white text-xs font-bold px-3 py-1 rounded-lg shadow-md uppercase tracking-wide">
                            {file['type']}
                        </span>
                    </div>
                    <h3 class="font-bold text-gray-800 group-hover:text-indigo-600 mb-2 transition-colors line-clamp-2">
                        {file['display_name']}
                    </h3>
                    {subfolder_badge}
                    <div class="flex items-center justify-between text-xs text-gray-500 mt-4 pt-3 border-t border-gray-200 group-hover:border-indigo-200 transition-colors">
                        <span class="flex items-center gap-1">
                            <span>📦</span>
                            <span>{file['size']}</span>
                        </span>
                        <span class="flex items-center gap-1">
                            <span>📅</span>
                            <span>{file['modified']}</span>
                        </span>
                    </div>
                </div>
"""
            else:
                html += f"""
                <a href="{file['path']}" 
                   class="group bg-white hover:bg-gradient-to-br hover:from-indigo-50 hover:to-purple-50 rounded-2xl p-5 shadow-md hover:shadow-xl border-2 border-gray-100 hover:border-indigo-300 transition-all duration-300 hover:-translate-y-2 cursor-pointer">
                    <div class="flex items-start justify-between mb-3">
                        <span class="bg-gradient-to-r {color} text-white text-xs font-bold px-3 py-1 rounded-lg shadow-md uppercase tracking-wide">
                            {file['type']}
                        </span>
                    </div>
                    <h3 class="font-bold text-gray-800 group-hover:text-indigo-600 mb-2 transition-colors line-clamp-2">
                        {file['display_name']}
                    </h3>
                    {subfolder_badge}
                    <div class="flex items-center justify-between text-xs text-gray-500 mt-4 pt-3 border-t border-gray-200 group-hover:border-indigo-200 transition-colors">
                        <span class="flex items-center gap-1">
                            <span>📦</span>
                            <span>{file['size']}</span>
                        </span>
                        <span class="flex items-center gap-1">
                            <span>📅</span>
                            <span>{file['modified']}</span>
                        </span>
                    </div>
                </a>
"""
        
        html += """
            </div>
        </section>
"""
    
    html += f"""
        <!-- Footer -->
        <footer class="text-center text-white mt-12 pb-8">
            <a href="https://github.com/bigBrodyG/DIYJavaScript" 
               target="_blank"
               class="inline-flex items-center gap-3 bg-white/20 backdrop-blur-xl hover:bg-white/30 text-white font-bold px-8 py-4 rounded-2xl transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl border border-white/30 mb-6">
                <span class="text-2xl">⭐</span>
                <span>View on GitHub</span>
            </a>
            <p class="text-white/80 text-sm mt-4">
                Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
            </p>
        </footer>
    </div>

    <!-- Modal per selezione visualizzazione -->
    <div id="viewModal" class="hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-50 items-center justify-center">
        <div class="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full mx-4">
            <h2 id="modalTitle" class="text-2xl font-bold text-gray-800 mb-6 text-center">Choose View Mode</h2>
            <div class="space-y-3">
                <button onclick="viewPage()" class="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-xl flex items-center justify-center gap-3">
                    <span class="text-2xl">🌐</span>
                    <span>View Page</span>
                </button>
                <button onclick="viewSource()" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-xl flex items-center justify-center gap-3">
                    <span class="text-2xl">📝</span>
                    <span>View Source Code</span>
                </button>
                <button onclick="viewJavaScript()" class="w-full bg-gradient-to-r from-yellow-500 to-orange-600 hover:from-yellow-600 hover:to-orange-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-xl flex items-center justify-center gap-3">
                    <span class="text-2xl">⚡</span>
                    <span>View JavaScript</span>
                </button>
                <button onclick="closeModal()" class="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-xl transition-all duration-300">
                    Cancel
                </button>
            </div>
        </div>
    </div>

    <!-- Modal per visualizzazione codice -->
    <div id="codeModal" class="hidden fixed inset-0 bg-black/90 backdrop-blur-sm z-50 items-center justify-center">
        <div class="bg-gray-900 rounded-3xl shadow-2xl p-6 max-w-6xl w-full mx-4 max-h-[90vh] flex flex-col">
            <div class="flex justify-between items-center mb-4">
                <h2 id="codeTitle" class="text-xl font-bold text-white"></h2>
                <button onclick="closeCodeModal()" class="text-white hover:text-red-400 text-2xl font-bold">&times;</button>
            </div>
            <div class="flex-1 overflow-auto rounded-xl">
                <pre class="!m-0"><code id="codeContent" class="!text-sm"></code></pre>
            </div>
        </div>
    </div>

    <script>
        console.log('🎉 DIY JavaScript - Projects loaded!');
        console.log('📊 Categories: {len(projects)} | Files: {total_files}');
        
        let currentPath = '';
        let currentTitle = '';

        function openModal(path, title) {{
            currentPath = path;
            currentTitle = title;
            document.getElementById('modalTitle').textContent = title;
            const modal = document.getElementById('viewModal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }}

        function closeModal() {{
            const modal = document.getElementById('viewModal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }}

        function closeCodeModal() {{
            const modal = document.getElementById('codeModal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }}

        function viewPage() {{
            window.open(currentPath, '_blank');
            closeModal();
        }}

        async function viewSource() {{
            try {{
                const response = await fetch(currentPath);
                const code = await response.text();
                document.getElementById('codeTitle').textContent = currentTitle + ' - HTML Source';
                document.getElementById('codeContent').textContent = code;
                document.getElementById('codeContent').className = 'language-html';
                hljs.highlightElement(document.getElementById('codeContent'));
                closeModal();
                const codeModal = document.getElementById('codeModal');
                codeModal.classList.remove('hidden');
                codeModal.classList.add('flex');
            }} catch(e) {{
                alert('Error loading source code: ' + e.message);
            }}
        }}

        async function viewJavaScript() {{
            try {{
                const response = await fetch(currentPath);
                const html = await response.text();
                
                // Estrai tutti i <script> tags
                const scriptRegex = /<script[^>]*>([\\s\\S]*?)<\\/script>/gi;
                const scripts = [];
                let match;
                while ((match = scriptRegex.exec(html)) !== null) {{
                    const content = match[1].trim();
                    if (content && !match[0].includes('src=')) {{
                        scripts.push(content);
                    }}
                }}
                
                if (scripts.length === 0) {{
                    alert('No inline JavaScript found in this page.');
                    return;
                }}
                
                const jsCode = scripts.join('\\n\\n// ========================================\\n\\n');
                document.getElementById('codeTitle').textContent = currentTitle + ' - JavaScript Code';
                document.getElementById('codeContent').textContent = jsCode;
                document.getElementById('codeContent').className = 'language-javascript';
                hljs.highlightElement(document.getElementById('codeContent'));
                closeModal();
                const codeModal = document.getElementById('codeModal');
                codeModal.classList.remove('hidden');
                codeModal.classList.add('flex');
            }} catch(e) {{
                alert('Error loading JavaScript: ' + e.message);
            }}
        }}

        // Chiudi modal cliccando fuori
        document.getElementById('viewModal').addEventListener('click', (e) => {{
            if (e.target.id === 'viewModal') closeModal();
        }});
        
        document.getElementById('codeModal').addEventListener('click', (e) => {{
            if (e.target.id === 'codeModal') closeCodeModal();
        }});
        
        // Intersection Observer for animations
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('section').forEach(section => {{
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            section.style.transition = 'all 0.6s ease-out';
            observer.observe(section);
        }});
    </script>
</body>
</html>
"""
    
    return html

def main():
    """Main function to generate the index page."""
    base_path = Path(__file__).parent
    
    print(f"🔍 Scanning directory: {base_path}")
    print(f"🚫 Ignoring directories: {', '.join(sorted(IGNORED_DIRS))}\n")
    
    # Scan all directories (excluding hidden and special ones)
    projects = []
    for item in sorted(base_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and item.name not in IGNORED_DIRS:
            print(f"📂 Scanning {item.name}...")
            project = scan_directory(base_path, item.name)
            if project:
                projects.append(project)
                print(f"   ✓ Found {project['count']} files")
            else:
                print(f"   ⊘ No valid files found")
    
    if not projects:
        print("\n⚠️  No projects found!")
        return
    
    # Generate HTML
    html_content = generate_html(projects)
    
    # Write to index.html
    output_file = base_path / "index.html"
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"\n✅ Generated index.html successfully!")
    print(f"📊 Found {len(projects)} categories with {sum(p['count'] for p in projects)} total files")
    for project in projects:
        print(f"   • {project['name']}: {project['count']} files")

if __name__ == "__main__":
    main()
