#!/usr/bin/env python3
"""Tworzy przenośne paczki ZIP szablonu dokumentacji projektu."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT_FILES = (
    ".gitignore",
    "README.md",
    "literatura.bib",
    "main.tex",
)
SOURCE_DIRS = (
    "assets",
    "backmatter",
    "chapters",
    "config",
    "docs",
)
TOOL_FILES = ("create_release.py",)
IGNORED_NAMES = (
    "build",
    "dist",
    "tmp",
    "__pycache__",
    "*.aux",
    "*.bbl",
    "*.bcf",
    "*.blg",
    "*.fdb_latexmk",
    "*.fls",
    "*.log",
    "*.lof",
    "*.lot",
    "*.out",
    "*.pdf",
    "*.pyc",
    "*.run.xml",
    "*.synctex.gz",
    "*.toc",
    "*.xdv",
    ".DS_Store",
    "Thumbs.db",
)
DEFAULT_ARCHIVES = {
    "local": Path("dist/szablon-projektu-local.zip"),
    "online": Path("dist/szablon-projektu-online.zip"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Utwórz ZIP szablonu projektu bez wyników kompilacji. Wariant "
            "lokalny zawiera latexmkrc, a internetowy jest przeznaczony do "
            "Prism, Overleaf lub podobnej platformy."
        )
    )
    parser.add_argument(
        "--target",
        choices=("local", "online"),
        help="wariant paczki; bez tej opcji program zapyta o wybór",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="opcjonalna własna ścieżka wynikowego pliku ZIP",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="katalog projektu; domyślnie ustalany automatycznie",
    )
    return parser.parse_args()


def choose_target(requested: str | None) -> str:
    if requested:
        return requested
    if not sys.stdin.isatty():
        raise ValueError(
            "Brak interaktywnego terminala. Podaj --target local albo --target online."
        )

    print("Wybierz wariant paczki:")
    print("  1. local  - komputer lokalny; LuaLaTeX, opcjonalnie LatexMk z Perlem")
    print("  2. online - Prism/Overleaf; bez lokalnego latexmkrc")
    while True:
        answer = input("Wariant [1/2, domyślnie 1]: ").strip().lower()
        if answer in {"", "1", "local", "l"}:
            return "local"
        if answer in {"2", "online", "o"}:
            return "online"
        print("Wpisz 1 dla wariantu local albo 2 dla wariantu online.")


def copy_required(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Brak wymaganego elementu: {source}")
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(*IGNORED_NAMES),
        )
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def variant_readme(target: str) -> str:
    if target == "local":
        return """# Wariant lokalny

Paczka jest przeznaczona do kompilacji na komputerze. Podstawowy wariant wymaga
MiKTeX-a i korzysta bezpośrednio z LuaLaTeX; Perl nie jest potrzebny:

```text
lualatex main.tex
```

Gotowy dokument powstanie jako `main.pdf` w katalogu projektu. Szczegółowa
konfiguracja TeXstudio i obsługa bibliografii są opisane w `README.md`.

Paczka zawiera także `latexmkrc`. Opcjonalna automatyzacja przez:

```text
latexmk main.tex
```

wymaga w systemie Windows interpretera Perl, np. Strawberry Perl. LatexMk
automatycznie uruchamia LuaLaTeX i Biber, a wynik zapisuje w `build/main.pdf`.
"""
    return """# Wariant internetowy

Paczka jest przeznaczona do Prism, Overleaf lub podobnego edytora. Nie zawiera
lokalnego pliku `latexmkrc`. Po zaimportowaniu archiwum ustaw:

- dokument główny: `main.tex`;
- kompilator: LuaLaTeX.

Plików pomocniczych i PDF nie należy dodawać ręcznie do paczki źródłowej.
Lokalna instalacja Perla nie jest potrzebna, ponieważ środowiskiem kompilacji
zarządza platforma internetowa.
"""


def configure_main_for_target(staging: Path, target: str) -> None:
    """Dodaj wskazanie LuaLaTeX wyłącznie do wariantu internetowego."""
    if target != "online":
        return

    main_path = staging / "main.tex"
    source = main_path.read_text(encoding="utf-8")
    program_directive = "% !TeX program = lualatex\n"
    if not source.startswith(program_directive):
        main_path.write_text(program_directive + source, encoding="utf-8")


def write_release_tree(project_root: Path, staging: Path, target: str) -> None:
    for name in ROOT_FILES:
        copy_required(project_root / name, staging / name)
    if target == "local":
        copy_required(project_root / "latexmkrc", staging / "latexmkrc")
    for name in SOURCE_DIRS:
        copy_required(project_root / name, staging / name)

    tools_dir = staging / "tools"
    tools_dir.mkdir(parents=True)
    for name in TOOL_FILES:
        copy_required(project_root / "tools" / name, tools_dir / name)

    configure_main_for_target(staging, target)
    (staging / "WARIANT.md").write_text(variant_readme(target), encoding="utf-8")


def create_zip(staging: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive.with_suffix(archive.suffix + ".tmp")
    if temporary.exists():
        temporary.unlink()
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as handle:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    handle.write(path, path.relative_to(staging).as_posix())
        temporary.replace(archive)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    try:
        target = choose_target(args.target)
    except ValueError as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 2

    output = args.output or DEFAULT_ARCHIVES[target]
    if not output.is_absolute():
        output = project_root / output
    output = output.resolve()

    if not (project_root / "main.tex").is_file():
        print(f"Błąd: nie znaleziono main.tex w {project_root}", file=sys.stderr)
        return 2
    if output.suffix.lower() != ".zip":
        print("Błąd: plik wynikowy musi mieć rozszerzenie .zip.", file=sys.stderr)
        return 2

    try:
        with tempfile.TemporaryDirectory(prefix="project-release-") as temporary:
            staging = Path(temporary) / "szablon-projektu"
            staging.mkdir()
            write_release_tree(project_root, staging, target)
            create_zip(staging, output)
    except (FileNotFoundError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(output) as handle:
        files = [item for item in handle.infolist() if not item.is_dir()]
        unsafe = [
            item.filename
            for item in files
            if item.filename.startswith("/") or ".." in Path(item.filename).parts
        ]
        if unsafe:
            print("Błąd: archiwum zawiera niebezpieczne ścieżki.", file=sys.stderr)
            return 1

    shown_output = output.relative_to(project_root) if project_root in output.parents else output
    print(f"Utworzono: {shown_output}")
    print(f"Wariant: {target}")
    print(f"Liczba plików: {len(files)}")
    print(f"Rozmiar: {output.stat().st_size / 1024:.1f} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
