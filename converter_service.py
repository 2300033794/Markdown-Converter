from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Final
import sys

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent
PACKAGE_SRC: Final[Path] = PROJECT_ROOT / "packages" / "markitdown" / "src"

if str(PACKAGE_SRC) not in sys.path:
    sys.path.insert(0, str(PACKAGE_SRC))

from markitdown import MarkItDown


def convert_bytes_to_markdown(
    file_bytes: bytes,
    filename: str,
    *,
    use_plugins: bool = False,
) -> str:
    suffix = Path(filename).suffix

    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file_bytes)
        temp_path = Path(temp_file.name)

    try:
        converter = MarkItDown(enable_plugins=use_plugins)
        result = converter.convert(str(temp_path))
        return result.markdown
    finally:
        temp_path.unlink(missing_ok=True)
