#!/usr/bin/env python3
"""
Generate an index.html page that lists all projects and exercises in the repository.
This script scans all directories and creates a beautiful landing page.
"""

import os
import json
from pathlib import Path
from datetime import datetime

def scan_directory(base_path, dir_name):
    """Scan a directory for HTML, Python, and JavaScript files."""
    dir_path = base_path / dir_name
    if not dir_path.exists():
        return None
    
    files = []
    for file_path in sorted(dir_path.glob("*")):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext in ['.html', '.htm', '.py', '.js', '.mjs']:
                # Get file size
                size = file_path.stat().st_size
                size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
                
                # Get modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                files.append({
                    'name': file_path.name,
                    'path': f"{dir_name}/{file_path.name}",
                    'type': ext[1:].upper(),
                    'size': size_str,
                    'modified': mtime.strftime('%Y-%m-%d')
                })
    
    return {
        'name': dir_name,
        'files': files,
        'count': len(files)
    } if files else None

def generate_html(projects):
    """Generate the HTML content for the index page."""
    
    # Count total files
    total_files = sum(p['count'] for p in projects)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIY JavaScript - Projects & Exercises</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            text-align: center;
        }}

        h1 {{
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        .emoji {{
            font-size: 3rem;
            margin-bottom: 20px;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            font-weight: bold;
        }}

        .stat-number {{
            font-size: 2rem;
            display: block;
        }}

        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}

        .project-section {{
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
        }}

        .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }}

        .project-title {{
            font-size: 1.8rem;
            color: #333;
        }}

        .project-count {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
        }}

        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}

        .file-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }}

        .file-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
        }}

        .file-name {{
            font-size: 1.1rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            word-break: break-word;
        }}

        .file-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #666;
            margin-top: 10px;
        }}

        .file-type {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 5px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-bottom: 8px;
        }}

        .file-type.html {{
            background: #e34c26;
        }}

        .file-type.py {{
            background: #3776ab;
        }}

        .file-type.js {{
            background: #f7df1e;
            color: #333;
        }}

        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }}

        .github-link {{
            color: white;
            text-decoration: none;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 10px;
            transition: background 0.3s;
        }}

        .github-link:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}

        .last-updated {{
            margin-top: 20px;
            opacity: 0.8;
            font-size: 0.9rem;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8rem;
            }}

            .stats {{
                gap: 15px;
            }}

            .files-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="emoji">🎡 🚀 💻</div>
            <h1>DIY JavaScript</h1>
            <p class="subtitle">Projects & Exercises Collection</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">{len(projects)}</span>
                    <span class="stat-label">Categories</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{total_files}</span>
                    <span class="stat-label">Total Files</span>
                </div>
            </div>
        </header>

"""
    
    # Generate project sections
    for project in projects:
        html += f"""
        <section class="project-section">
            <div class="project-header">
                <h2 class="project-title">{project['name']}</h2>
                <span class="project-count">{project['count']} files</span>
            </div>
            <div class="files-grid">
"""
        
        for file in project['files']:
            file_type_class = file['type'].lower()
            html += f"""
                <a href="{file['path']}" class="file-card">
                    <span class="file-type {file_type_class}">{file['type']}</span>
                    <div class="file-name">{file['name']}</div>
                    <div class="file-meta">
                        <span>📦 {file['size']}</span>
                        <span>📅 {file['modified']}</span>
                    </div>
                </a>
"""
        
        html += """
            </div>
        </section>
"""
    
    html += f"""
        <footer>
            <a href="https://github.com/bigBrodyG/DIYJavaScript" class="github-link" target="_blank">
                <span>⭐</span>
                <span>View on GitHub</span>
            </a>
            <p class="last-updated">Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}</p>
        </footer>
    </div>

    <script>
        // Add some interactivity
        console.log('🎉 DIY JavaScript - Projects loaded successfully!');
        console.log('📊 Total categories: {len(projects)}');
        console.log('📁 Total files: {total_files}');
    </script>
</body>
</html>
"""
    
    return html

def main():
    """Main function to generate the index page."""
    base_path = Path(__file__).parent
    
    # Scan all directories (excluding hidden and special ones)
    projects = []
    for item in sorted(base_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and item.name != 'node_modules':
            project = scan_directory(base_path, item.name)
            if project:
                projects.append(project)
    
    if not projects:
        print("⚠️  No projects found!")
        return
    
    # Generate HTML
    html_content = generate_html(projects)
    
    # Write to index.html
    output_file = base_path / "index.html"
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"✅ Generated index.html successfully!")
    print(f"📊 Found {len(projects)} categories with {sum(p['count'] for p in projects)} total files")
    for project in projects:
        print(f"   • {project['name']}: {project['count']} files")

if __name__ == "__main__":
    main()
