@echo off
echo ========================================
echo Compiling LaTeX Research Report
echo ========================================
echo.

REM Check if pdflatex is installed
where pdflatex >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pdflatex not found!
    echo Please install LaTeX distribution:
    echo - Windows: MiKTeX or TeX Live
    echo - Download: https://miktex.org/download
    echo.
    pause
    exit /b 1
)

echo Compiling report.tex...
echo.

REM First pass
pdflatex -interaction=nonstopmode report.tex

REM Second pass for references
pdflatex -interaction=nonstopmode report.tex

REM Clean up auxiliary files
echo.
echo Cleaning up auxiliary files...
del /Q *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.synctex.gz 2>nul

if exist report.pdf (
    echo.
    echo ========================================
    echo Success! Report compiled to report.pdf
    echo ========================================
    echo.
    start report.pdf
) else (
    echo.
    echo ========================================
    echo Compilation failed! Check errors above.
    echo ========================================
)

pause
