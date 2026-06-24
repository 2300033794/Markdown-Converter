$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Virtual environment not found. Create it with: python -m venv .venv"
}

Set-Location $ProjectRoot

$Backend = Start-Process `
    -FilePath $Python `
    -ArgumentList "-m", "uvicorn", "backend:app", "--host", "127.0.0.1", "--port", "8000" `
    -WindowStyle Hidden `
    -PassThru

try {
    Start-Sleep -Seconds 2
    & $Python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
}
finally {
    if (-not $Backend.HasExited) {
        Stop-Process -Id $Backend.Id
    }
}

