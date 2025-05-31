#!/bin/bash

# Full installation and execution script for ISO/OSI Simulation Project
# Requires: git, gcc, make

set -e # Exit on any error

# Check for required dependencies
check_dependencies() {
    local missing=()
    for dep in git gcc make; do
        if ! command -v $dep &> /dev/null; then
            missing+=("$dep")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        echo "ERROR: Missing required dependencies:"
        for dep in "${missing[@]}"; do
            echo "  - $dep"
        done
        echo
        echo "Install with:"
        echo "  sudo apt update && sudo apt install -y build-essential git"
        exit 1
    fi
}

# Clone repository
clone_project() {
    echo "📥 Cloning repository..."
    git clone https://github.com/Franciuto/C-ISO-OSI.git
    cd C-ISO-OSI
    echo "✅ Repository cloned successfully"
}

# Compile project
compile_project() {
    echo "🔧 Compiling project..."
    make
    echo "✅ Compilation completed"
    echo
}

# Run simulation
run_simulation() {
    echo "🚀 Starting ISO/OSI Simulation..."
    echo "---------------------------------"
    ./osi_simulation
}

# Main installation and execution flow
main() {
    echo "🛠️  Starting ISO/OSI Simulation Installation"
    echo "========================================"
    
    # Check dependencies
    check_dependencies
    
    # Clone and enter project
    clone_project
    
    # Compile project
    compile_project
    
    # Run simulation
    run_simulation
}

main
