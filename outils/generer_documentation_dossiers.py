from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "node_modules", "dist", ".vite", "__pycache__"}

DOSSIERS = {
    "APPROVISIONNEMENT": (
        "Regroupe les nomenclatures, estimations de budget, suivis des achats "
        "et informations fournisseurs du projet."
    ),
    "COORDINATION DU PROJET": (
        "Regroupe les informations d'equipe, les comptes rendus de reunion "
        "et le suivi des taches."
    ),
    "ELECTRONIQUE": (
        "Regroupe l'architecture electronique, l'alimentation, la conception "
        "des sous-ensembles et les informations de cablage."
    ),
    "INFORMATIQUE": (
        "Regroupe l'architecture logicielle, le prototype de supervision, "
        "les communications, le firmware et la documentation d'integration."
    ),
    "LIVRABLES FINAUX": (
        "Regroupe les dossiers de conception, fabrication, electronique, "
        "informatique, robotique, qualite, rapports et validations."
    ),
    "MECANIQUE": (
        "Regroupe les etudes, calculs, sources de modelisation 3D, plans "
        "et informations de fabrication mecanique."
    ),
    "outils": (
        "Regroupe les scripts et dependances servant a generer ou mettre "
        "a jour les registres et documents du projet."
    ),
    "QUALITE ET SECURITE": (
        "Regroupe l'analyse des risques, les exigences, les pistes "
        "reglementaires et les activites de test et validation."
    ),
    "ROBOTIQUE": (
        "Regroupe l'architecture ROS 2, la cartographie, la maquette du robot "
        "et les travaux de navigation et simulation."
    ),
}


def project_entries(directory: Path) -> list[Path]:
    entries = []
    for path in directory.iterdir():
        if path.is_dir() and path.name in EXCLUDED_DIRS:
            continue
        entries.append(path)
    return sorted(entries, key=lambda path: (not path.is_dir(), path.name.casefold()))


def tree_lines(
    directory: Path, prefix: str = "", root_directory: Path | None = None
) -> list[str]:
    if root_directory is None:
        root_directory = directory
    entries = project_entries(directory)
    lines = []
    for index, path in enumerate(entries):
        last = index == len(entries) - 1
        branch = "└── " if last else "├── "
        label = path.name + ("/" if path.is_dir() else "")

        lines.append(prefix + branch + label)
        if path.is_dir():
            lines.extend(
                tree_lines(
                    path,
                    prefix + ("    " if last else "│   "),
                    root_directory,
                )
            )
    return lines


def write_readme(directory: Path, description: str) -> None:
    readme = directory / "README.md"
    if readme.exists():
        return

    subdirectories = [
        path for path in project_entries(directory) if path.is_dir()
    ]
    root_files = [path for path in project_entries(directory) if path.is_file()]
    lines = [
        f"# {directory.name}",
        "",
        description,
        "",
        "## Contenu du dossier",
        "",
    ]
    if subdirectories:
        for path in subdirectories:
            lines.append(f"- [{path.name}/](<{path.name}/>)")
    else:
        lines.append("Aucun sous-dossier pour le moment.")
    if root_files:
        lines.extend(["", "Fichiers directement presents a la racine :"])
        lines.extend(f"- `{path.name}`" for path in root_files)

    lines.extend(
        [
            "",
            "## Structure complete",
            "",
            "Voir [STRUCTURE_COMPLETE.md](<STRUCTURE_COMPLETE.md>) "
            "pour l'arborescence detaillee de ce dossier et de ses sous-dossiers.",
            "",
            "## Mise a jour",
            "",
            "Depuis la racine `PROJET BANQUE CENTRALE`, regenerer les structures "
            "avec :",
            "",
            "```powershell",
            "python .\\outils\\generer_documentation_dossiers.py",
            "```",
            "",
        ]
    )
    readme.write_text("\n".join(lines), encoding="utf-8")


def write_structure(directory: Path) -> tuple[int, int]:
    output = directory / "STRUCTURE_COMPLETE.md"
    lines = [
        f"# Structure complete - {directory.name}",
        "",
        f"**Dossier :** `{directory.relative_to(ROOT).as_posix()}/`",
        "",
        "Arborescence des dossiers et fichiers du perimetre ci-dessous. "
        "Les dependances generees (`node_modules`, `dist`, `.vite`, "
        "`__pycache__` et `.git`) sont exclues.",
        "",
        "```text",
        directory.name + "/",
        *tree_lines(directory),
        "```",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")

    folder_count = sum(
        1
        for path in directory.rglob("*")
        if path.is_dir()
        and not any(part in EXCLUDED_DIRS for part in path.relative_to(directory).parts)
    )
    file_count = sum(
        1
        for path in directory.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_DIRS for part in path.relative_to(directory).parts)
    )
    return folder_count, file_count


def main() -> None:
    for name, description in DOSSIERS.items():
        directory = ROOT / name
        if not directory.is_dir():
            raise FileNotFoundError(f"Dossier de projet introuvable : {directory}")
        write_readme(directory, description)

    for name in DOSSIERS:
        folder_count, file_count = write_structure(ROOT / name)
        print(f"{name}: {folder_count} sous-dossiers, {file_count} fichiers")


if __name__ == "__main__":
    main()
