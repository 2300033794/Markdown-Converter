# Web application

The application has a FastAPI backend on port `8000` and a Streamlit frontend
on port `8501`.

## Install

```powershell
cd "C:\Clone Files\Markdown\markitdown"
.\.venv\Scripts\python.exe -m pip install -r requirements-app.txt
.\.venv\Scripts\python.exe -m pip install -e "packages\markitdown[all]"
```

## Run frontend and backend

```powershell
.\run.ps1
```

Then open <http://127.0.0.1:8501>. Press `Ctrl+C` to stop both services.
