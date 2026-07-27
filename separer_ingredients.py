import argparse
import json
import re
from pathlib import Path

# Base de connaissances (identique à la vôtre)
HALAL_HARAM_KB = {
    "porc": "haram", "pork": "haram", "bacon": "haram", "jambon": "haram",
    "ham": "haram", "saucisse": "haram", "alcool": "haram", "bière": "haram",
    "vin": "haram", "whisky": "haram", "champagne": "haram", "vodka": "haram",
    "rhum": "haram", "gelatine": "haram", "gélatine": "haram",
    "gélatine de porc": "haram", "gélatine animale": "haram", "âme": "haram",
    "sang": "haram", "gras animal": "haram", "foie gras": "haram", "suif": "haram",
    "virgin": "a_verifier", "poulet": "a_verifier", "dinde": "a_verifier",
    "veau": "a_verifier", "agneau": "a_verifier", "boeuf": "a_verifier",
    "bœuf": "a_verifier", "viande halal": "halal", "halal": "halal",
    "agneau halal": "halal", "poulet halal": "halal", "fromage halal": "halal",
    "yaourt": "halal", "légumes": "halal", "legumes": "halal", "salade": "halal",
    "riz": "halal", "quinoa": "halal", "lentilles": "halal", "patate douce": "halal",
    "pois chiches": "halal", "fruits": "halal", "miel": "halal", "oeuf": "halal",
    "œuf": "halal", "fromage": "a_verifier", "lait": "halal", "beurre": "halal",
    "huile d'olive": "halal", "huile de coco": "halal", "épices": "halal",
    "épinards": "halal", "brocoli": "halal", "avocat": "halal", "banane": "halal",
    "datte": "halal",
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿœæ'\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_and_categorize(text: str):
    normalized = normalize_text(text)
    categories = {"halal": [], "haram": [], "a_verifier": []}
    matched_spans = []

    # Les expressions longues prennent priorité sur leurs sous-termes.
    for term in sorted(HALAL_HARAM_KB, key=len, reverse=True):
        pattern = r"\b" + re.escape(term) + r"\b"
        found = False
        for match in re.finditer(pattern, normalized):
            overlaps_longer_term = any(
                match.start() < end and match.end() > start
                for start, end in matched_spans
            )
            if overlaps_longer_term:
                continue
            matched_spans.append(match.span())
            found = True

        if found:
            status = HALAL_HARAM_KB[term]
            if term not in categories[status]:
                categories[status].append(term)

    return categories


def analyze_stored_files(scan_dir: Path, profile: str | None = None):
    """Analyse récursivement les fichiers texte OCR déjà enregistrés."""
    root_dir = scan_dir / profile if profile else scan_dir
    if not root_dir.is_dir():
        raise FileNotFoundError(f"Dossier introuvable: {root_dir}")

    results = []
    for text_file in sorted(root_dir.rglob("*.txt")):
        content = text_file.read_text(encoding="utf-8", errors="replace")
        results.append({
            "fichier": str(text_file.relative_to(scan_dir)),
            "ingredients": find_and_categorize(content),
        })
    return results


def summarize_results(results):
    categories = ("halal", "haram", "a_verifier")
    return {
        "fichiers_analyses": len(results),
        "fichiers_avec_termes": sum(
            any(result["ingredients"].values()) for result in results
        ),
        "detections_par_categorie": {
            category: sum(
                len(result["ingredients"][category]) for result in results
            )
            for category in categories
        },
    }


def main():
    project_dir = Path(__file__).resolve().parent
    default_scan_dir = project_dir / "ocr_results"

    parser = argparse.ArgumentParser(
        description="Sépare les ingrédients des textes OCR enregistrés (Halal/Haram/À vérifier)."
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--text", help="Texte à analyser directement")
    input_group.add_argument("--file", help="Fichier .txt à analyser")
    parser.add_argument(
        "--scan",
        type=Path,
        help=f"Dossier OCR à analyser (par défaut: {default_scan_dir})",
    )
    parser.add_argument(
        "--profile",
        help="Analyser uniquement un sous-dossier/profil (ex. soul.body.mindd)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Enregistrer les résultats au format JSON dans ce fichier",
    )
    args = parser.parse_args()

    if args.text is not None or args.file is not None:
        if args.profile:
            parser.error("--profile s'utilise avec l'analyse du dossier OCR, pas --text/--file")
        if args.file:
            source = Path(args.file)
            if not source.is_file():
                parser.error(f"Fichier introuvable: {source}")
            content = source.read_text(encoding="utf-8", errors="replace")
            source_name = source.name
        else:
            content = args.text
            source_name = "Entrée directe"

        result = find_and_categorize(content)
        print(f"\n--- Analyse des ingrédients : {source_name} ---")
        print(json.dumps(result, indent=4, ensure_ascii=False))
        total = sum(len(values) for values in result.values())
        if result["haram"]:
            print(f"\nATTENTION: {len(result['haram'])} ingrédient(s) haram détecté(s)!")
        else:
            print(f"\nAnalyse terminée ({total} terme(s) trouvé(s)).")
        output_data = {"fichier": source_name, "ingredients": result}
    else:
        scan_dir = (args.scan or default_scan_dir).expanduser().resolve()
        try:
            results = analyze_stored_files(scan_dir, args.profile)
        except FileNotFoundError as error:
            parser.error(str(error))
        if not results:
            parser.error(f"Aucun fichier .txt trouvé dans {scan_dir}")

        summary = summarize_results(results)
        print(f"\n--- Analyse des données OCR : {scan_dir} ---")
        for result in results:
            found = " | ".join(
                f"{category}: {', '.join(terms)}"
                for category, terms in result["ingredients"].items()
                if terms
            ) or "aucun terme connu"
            print(f"{result['fichier']} -> {found}")
        print("\nRésumé:")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        output_data = {"resume": summary, "resultats": results}

    if args.output:
        output_path = args.output.expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(output_data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"\nRésultats enregistrés dans: {output_path}")


if __name__ == "__main__":
    main()
