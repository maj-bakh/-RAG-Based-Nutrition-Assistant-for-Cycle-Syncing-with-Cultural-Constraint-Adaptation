import argparse
import json
import re
from pathlib import Path

from separer_ingredients import find_and_categorize

# Dictionnaire de remplacement intelligent
# Clé: terme haram, Valeur: suggestion halal
SUGGESTIONS_MAP = {
    "porc": "viande de bœuf halal",
    "pork": "beef halal",
    "bacon": "bacon de dinde halal",
    "jambon": "jambon de dinde halal",
    "ham": "turkey ham",
    "saucisse": "saucisse de poulet halal",
    "alcool": "extrait sans alcool",
    "bière": "boisson maltée sans alcool",
    "vin": "jus de raisin",
    "whisky": "eau aromatisée",
    "champagne": "jus de pomme pétillant",
    "vodka": "eau",
    "rhum": "sirop de sucre",
    "gelatine": "agar-agar",
    "gelatine de porc": "agar-agar",
    "gelatine animale": "agar-agar",
    "gélatine": "agar-agar",
    "gélatine de porc": "agar-agar",
    "gélatine animale": "agar-agar",
    "sang": "substitut végétal",
    "gras animal": "huile végétale",
    "foie gras": "pâté de légumes",
    "suif": "margarine végétale",
}


def suggest_for_text(text: str) -> dict:
    """Suggère des alternatives uniquement aux termes détectés haram par l'autre script."""
    detected_haram = find_and_categorize(text)["haram"]
    replaceable_terms = [
        term for term in detected_haram if term in SUGGESTIONS_MAP
    ]
    terms = sorted(replaceable_terms, key=len, reverse=True)
    replacements = []
    seen_terms = set()

    if terms:
        pattern = re.compile(
            r"\b(?:" + "|".join(re.escape(term) for term in terms) + r")\b",
            re.IGNORECASE,
        )

        def replace_match(match):
            term = match.group(0).lower()
            suggestion = SUGGESTIONS_MAP[term]
            if term not in seen_terms:
                replacements.append({"terme": term, "suggestion": suggestion})
                seen_terms.add(term)
            return suggestion

        suggested_text = pattern.sub(replace_match, text)
    else:
        suggested_text = text

    return {
        "termes_haram_detectes": detected_haram,
        "remplacements": replacements,
        "termes_sans_suggestion": [
            term for term in detected_haram if term not in SUGGESTIONS_MAP
        ],
        "texte_suggere": suggested_text,
    }


def sanitize_with_suggestions(text: str) -> tuple[str, list]:
    """Compatibilité avec l'ancienne fonction, en se limitant aux termes haram détectés."""
    result = suggest_for_text(text)
    replacements = [
        (item["terme"], item["suggestion"])
        for item in result["remplacements"]
    ]
    return result["texte_suggere"], replacements


def process_file(input_path: str):
    p = Path(input_path)
    if not p.is_file():
        print(f"Fichier introuvable: {input_path}")
        return

    content = p.read_text(encoding="utf-8", errors="replace")
    result = suggest_for_text(content)
    cleaned_content = result["texte_suggere"]
    reps = result["remplacements"]

    output_path = p.with_stem(f"{p.stem}_suggested")
    output_path.write_text(cleaned_content, encoding="utf-8")

    print(f"✅ Fichier traité: {output_path.name}")
    print(
        "Termes haram détectés: "
        + ", ".join(result["termes_haram_detectes"] or ["aucun"])
    )
    if reps:
        print("🔄 Remplacements effectués:")
        for replacement in reps:
            print(
                f"   '{replacement['terme']}' ➜ "
                f"'{replacement['suggestion']}'"
            )
    elif result["termes_sans_suggestion"]:
        print(
            "Aucune suggestion configurée pour: "
            + ", ".join(result["termes_sans_suggestion"])
        )


def analyze_stored_data(scan_dir: Path, profile: str | None = None):
    """Analyse les fichiers OCR enregistrés sans modifier les originaux."""
    scan_dir = scan_dir.resolve()
    root_dir = scan_dir / profile if profile else scan_dir
    if not root_dir.is_dir():
        raise FileNotFoundError(f"Dossier introuvable: {root_dir}")

    text_files = sorted(root_dir.rglob("*.txt"))
    suggestions = []
    for text_file in text_files:
        original = text_file.read_text(encoding="utf-8", errors="replace")
        result = suggest_for_text(original)
        if result["termes_haram_detectes"]:
            suggestions.append({
                "fichier": str(text_file.relative_to(scan_dir)),
                **result,
            })

    return {
        "dossier_analyse": str(root_dir),
        "fichiers_analyses": len(text_files),
        "fichiers_avec_suggestions": len(suggestions),
        "note": "Suggestions indicatives; vérifier la certification halal des produits animaux.",
        "resultats": suggestions,
    }


def main():
    default_scan_dir = Path(__file__).resolve().parent / "ocr_results"
    parser = argparse.ArgumentParser(
        description="Propose des substitutions dans les textes OCR stockés, sans toucher aux originaux."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--text", help="Texte à traiter directement")
    input_group.add_argument("--file", help="Fichier .txt à traiter")
    parser.add_argument(
        "--scan",
        type=Path,
        help=f"Dossier OCR à analyser (par défaut: {default_scan_dir})",
    )
    parser.add_argument(
        "--profile",
        help="Analyser uniquement un profil (ex. soul.body.mindd)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Enregistrer le rapport des suggestions au format JSON",
    )
    args = parser.parse_args()

    if args.text is not None or args.file is not None:
        if args.profile or args.scan or args.output:
            parser.error("--scan, --profile et --output s'utilisent avec l'analyse du corpus OCR")
        if args.file:
            process_file(args.file)
            return

        result = suggest_for_text(args.text)
        print(f"Termes haram détectés: {', '.join(result['termes_haram_detectes']) or 'aucun'}")
        print(f"Texte proposé: {result['texte_suggere']}")
        for replacement in result["remplacements"]:
            print(
                f"  - {replacement['terme']} remplacé par "
                f"{replacement['suggestion']}"
            )
    else:
        scan_dir = (args.scan or default_scan_dir).expanduser().resolve()
        try:
            report = analyze_stored_data(scan_dir, args.profile)
        except FileNotFoundError as error:
            parser.error(str(error))
        if not report["fichiers_analyses"]:
            parser.error(f"Aucun fichier .txt trouvé dans {report['dossier_analyse']}")

        print(
            f"Fichiers analysés: {report['fichiers_analyses']} | "
            f"fichiers avec détection haram: {report['fichiers_avec_suggestions']}"
        )
        for result in report["resultats"]:
            print(f"\n{result['fichier']}")
            print(
                "  Détecté haram: "
                + ", ".join(result["termes_haram_detectes"])
            )
            for replacement in result["remplacements"]:
                print(f"  {replacement['terme']} → {replacement['suggestion']}")
            if result["termes_sans_suggestion"]:
                print(
                    "  Sans suggestion: "
                    + ", ".join(result["termes_sans_suggestion"])
                )
        if not report["resultats"]:
            print("Aucun terme classé haram par separer_ingredients.py n'a été trouvé.")
        print(report["note"])

        if args.output:
            output_path = args.output.expanduser().resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"Rapport enregistré dans: {output_path}")


if __name__ == "__main__":
    main()
