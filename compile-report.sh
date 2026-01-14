#!/bin/bash

echo "========================================"
echo "Compiling LaTeX Research Report"
echo "========================================"
echo ""

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "[ERROR] pdflatex not found!"
    echo "Please install LaTeX distribution:"
    echo "- Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "- macOS: brew install mactex"
    echo "- Or download from: https://www.latex-project.org/get/"
    echo ""
    exit 1
fi

echo "Compiling report.tex..."
echo ""

# First pass
pdflatex -interaction=nonstopmode report.tex

# Second pass for references
pdflatex -interaction=nonstopmode report.tex

# Clean up auxiliary files
echo ""
echo "Cleaning up auxiliary files..."
rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.synctex.gz

if [ -f "report.pdf" ]; then
    echo ""
    echo "========================================"
    echo "Success! Report compiled to report.pdf"
    echo "========================================"
    echo ""
    
    # Try to open PDF with default viewer
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open report.pdf
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open report.pdf 2>/dev/null || echo "Please open report.pdf manually"
    fi
else
    echo ""
    echo "========================================"
    echo "Compilation failed! Check errors above."
    echo "========================================"
    exit 1
fi
