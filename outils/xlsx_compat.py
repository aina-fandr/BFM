from __future__ import annotations

import os
import posixpath
import re
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from openpyxl.workbook import Workbook


def save_workbook_compatible(workbook: Workbook, path: Path) -> None:
    workbook.save(path)
    normalize_relationship_targets(path)


def normalize_relationship_targets(path: Path) -> None:
    """Normalize internal OOXML relationship paths for spreadsheet readers."""
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=path.stem + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        with ZipFile(path, "r") as source, ZipFile(
            temp_path, "w", compression=ZIP_DEFLATED
        ) as target:
            for entry in source.infolist():
                data = source.read(entry.filename)
                if entry.filename.endswith(".rels"):
                    if "/_rels/" in entry.filename:
                        source_dir = entry.filename.split("/_rels/", 1)[0]
                    else:
                        source_dir = ""

                    def relative_target(match: re.Match[bytes]) -> bytes:
                        value = match.group(2)
                        if not value.startswith(b"/") or value.startswith(b"//"):
                            return match.group(0)
                        relative = posixpath.relpath(
                            value.lstrip(b"/"),
                            (source_dir or ".").encode("ascii"),
                        )
                        return match.group(1) + relative + match.group(3)

                    data = re.sub(
                        rb'(Target=")([^"]+)(")',
                        relative_target,
                        data,
                    )
                target.writestr(entry, data)
        os.replace(temp_path, path)
    except Exception:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
        raise

