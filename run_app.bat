@echo off
echo --- OMEGA-CORE APP LAUNCHER ---
echo.
echo Trying to run Streamlit via python module...
py -m streamlit run streamlit_app.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 'py' command failed. Trying 'python'...
    python -m streamlit run streamlit_app.py
)
pause
