#!/usr/bin/env bash
# Quick wrapper to generate documentation for Java projects

echo "🚀 Generating documentation for Java projects..."
echo ""

cd "$(dirname "$0")"
python3 generate-docs.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✨ Documentation generated! Opening in browser..."
    
    # Try to open in default browser
    if command -v xdg-open &> /dev/null; then
        xdg-open docs/index.html
    elif command -v open &> /dev/null; then
        open docs/index.html
    elif command -v start &> /dev/null; then
        start docs/index.html
    else
        echo "📂 Please open docs/index.html manually in your browser"
    fi
else
    echo ""
    echo "❌ Documentation generation failed!"
    exit $exit_code
fi
