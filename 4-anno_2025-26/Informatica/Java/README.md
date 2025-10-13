# Java Lessons — School Projects 📚

![Java](https://img.shields.io/badge/Java-007396.svg?style=for-the-badge&logo=java&logoColor=white)
![School Project](https://img.shields.io/badge/School-Project-29AB87?style=for-the-badge&logo=gradle&logoColor=white)
![Files](https://img.shields.io/badge/Files-student%20materials-blueviolet?style=for-the-badge&logo=google-drive&logoColor=white)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen?style=for-the-badge&logo=github)
![License](https://img.shields.io/github/license/bigBrodyG/JavaProjects?style=for-the-badge)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange?style=for-the-badge&logo=github)
![Last Commit](https://img.shields.io/github/last-commit/bigBrodyG/JavaProjects?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/bigBrodyG/JavaProjects?style=for-the-badge)

## 🌐 Live Showcase

**[View the interactive showcase website →](https://bigBrodyG.github.io/JavaProjects/)**

All projects are automatically compiled and run with each commit. The website displays source code, build status, and program output.

---

## 🚀 Automatic Documentation Generator

This repository includes an **automatic documentation generator** that scans all Java projects and creates a beautiful interactive showcase website.

### ✨ Features

- 🔍 **Auto-discovery**: Automatically finds all Java projects in the workspace
- 🏗️ **Auto-compilation**: Compiles and runs each project to capture output
- 📝 **HTML Generation**: Creates individual interactive pages for each project
- 🎨 **Beautiful UI**: Modern dark theme with syntax highlighting
- ▶️ **Run in Browser**: Execute code with animated output display
- 📊 **Index Page**: Auto-generated overview of all projects

### 🎯 How It Works

#### When you create a new Java project:

1. Create a new directory (e.g., `MyNewProject/`)
2. Add the standard structure:
   ```
   MyNewProject/
   ├── src/
   │   └── MyNewProject.java  (with main method)
   ├── bin/
   └── lib/
   ```

3. Run the generator:
   ```bash
   ./generate-docs.py
   ```
   or
   ```bash
   python3 generate-docs.py
   ```

4. **That's it!** Your project is automatically:
   - ✅ Compiled and tested
   - ✅ Added to the website with its own page
   - ✅ Listed on the index page
   - ✅ Output captured and displayed

### 📁 Project Structure

Each Java project should follow this structure:

```
ProjectName/
├── src/              # Source files
│   └── *.java        # Your Java files (one must have main method)
├── bin/              # Compiled classes (auto-generated)
├── lib/              # External libraries (optional)
└── README.md         # Project documentation (optional)
```

### 🎨 Project Types

The generator automatically categorizes projects:

- **📚 Teoria (Theory)**: Basic concepts, classes (e.g., Cerchio, Punto, Rettangolo, Libro)
- **🔬 Laboratorio (Lab)**: Practical exercises (e.g., mergeArray, vocalcount, OggettoCD)

### 🔧 Manual Customization

If you want to customize project descriptions or types, edit the script:

```python
# In generate-docs.py

def generate_project_description(project: Dict) -> str:
    descriptions = {
        'yourproject': 'Your custom description here',
        # Add more...
    }
```

### 📦 Generated Files

After running the generator, you'll find in `docs/`:

```
docs/
├── index.html                 # Main showcase page
├── projectname.html          # Individual project page
├── projectname-output.txt    # Captured output
└── ...
```

### 🌐 View the Showcase

Open `docs/index.html` in your browser to see all your projects!

### 🛠️ Requirements

- Python 3.6+
- Java JDK (javac and java commands available)
- No additional Python packages required (uses only standard library)

### 💡 Quick Start

1. Create a new Java project in the workspace
2. Run `./generate-docs.py`
3. Open `docs/index.html` in browser
4. Enjoy! 🎉

---
