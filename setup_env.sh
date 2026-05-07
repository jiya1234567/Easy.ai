#!/bin/bash
echo "--- OMEGA-CORE ENVIRONMENT SETUP ---"

# 1. Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 2. Add local bin to PATH (Common fix for Codespaces)
echo "Adding local bin to PATH..."
export PATH=$PATH:~/.local/bin
echo "export PATH=\$PATH:~/.local/bin" >> ~/.bashrc

# 3. Verify installation
if command -v streamlit &> /dev/null
then
    echo "SUCCESS: Streamlit is now in your PATH."
    streamlit --version
else
    echo "WARNING: 'streamlit' command still not found. Using 'python -m streamlit' instead."
fi

echo "------------------------------------"
echo "You can now run the app using:"
echo "streamlit run app.py"
echo "OR"
echo "python -m streamlit run app.py"
