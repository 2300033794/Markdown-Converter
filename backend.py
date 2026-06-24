from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from converter_service import convert_bytes_to_markdown


MAX_FILE_SIZE = 50 * 1024 * 1024
ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".txt", ".csv",
    ".json", ".xml", ".html", ".htm", ".zip", ".epub",
}

app = FastAPI(title="MarkItDown API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/convert")
async def convert(
    file: UploadFile = File(...),
    use_plugins: bool = False,
) -> dict[str, str]:
    safe_name = Path(file.filename or "upload").name
    extension = Path(safe_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension or 'none'}",
        )

    contents = await file.read(MAX_FILE_SIZE + 1)
    if not contents:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 50 MB.")

    try:
        markdown_text = convert_bytes_to_markdown(contents, safe_name, use_plugins=use_plugins)
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Could not convert the document: {exc}",
        ) from exc

    return {
        "filename": f"{Path(safe_name).stem}.md",
        "markdown": markdown_text,
    }

