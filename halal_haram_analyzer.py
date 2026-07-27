import argparse
import re
from pathlib import Path

# Base de connaissances simple halal / haram / à vérifier
HALAL_HARAM_KB = {
    "porc": "haram",
    "pork": "haram",
    "bacon": "haram",
    "jambon": "haram",
    "ham": "haram",
    "saucisse": "haram",
    "alcool": "haram",
    "bière": "haram",
    "vin": "haram",
    "whisky": "haram",
    "champagne": "haram",
    "vodka": "haram",
    "rhum": "haram",
    "gelatine": "haram",
    "gélatine": "haram",
    "gélatine de porc": "haram",
    "gélatine animale": "haram",
    "âme": "haram",
    "sang": "haram",
    "gras animal": "haram",
    "foie gras": "haram",
    "suif": "haram",
    "virgin": "a_verifier",
    "poulet": "a_verifier",
    "dinde": "a_verifier",
    "veau": "a_verifier",
    "agneau": "a_verifier",
    "boeuf": "a_verifier",
    "bœuf": "a_verifier",
    "viande halal": "halal",
    "halal": "halal",
    "agneau halal": "halal",
    "poulet halal": "halal",
    "fromage halal": "halal",
    "yaourt": "halal",
    "légumes": "halal",
    "legumes": "halal",
    "salade": "halal",
    "riz": "halal",
    "quinoa": "halal",
    "lentilles": "halal",
    "patate douce": "halal",
    "pois chiches": "halal",
    "fruits": "halal",
    "miel": "halal",
    "oeuf": "halal",
    "œuf": "halal",
    "fromage": "a_verifier",
    "lait": "halal",
    "yaourt": "halal",
    "beurre": "halal",
    "huile d'olive": "halal",
    "huile de coco": "halal",
    "épices": "halal",
    "épinards": "halal",
    "brocoli": "halal",
    "avocat": "halal",
    "banane": "halal",
    "datte": "halal",
}

PHASE_MEALS = {
    "menses": [
        "Soupe de lentilles et légumes",
        "Smoothie banane, dattes et lait d'amande",
        "Salade tiède de quinoa aux épinards",
    ],
    "follicular": [
        "Salade de quinoa, pois chiches et légumes frais",
        "Poisson grillé avec riz complet",
        "Yaourt nature aux baies et graines",
    ],
    "ovulatory": [
        "Omelette aux épinards et tomates",
        "Poulet halal rôti et patate douce",
        "Salade de pois chiches, avocat et légumes verts",
    ],
    "luteal": [
        "Curry de lentilles et légumes racines",
        "Riz complet, légumes rôtis et quinoa",
        "Soupe de légumes et pain complet",
    ],
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿœæ'\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_terms(text: str):
    normalized = normalize_text(text)
    found = []
    for term in sorted(HALAL_HARAM_KB.keys(), key=len, reverse=True):
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, normalized):
            found.append((term, HALAL_HARAM_KB[term]))
    return found


def classify_text(text: str):
    found = find_terms(text)
    if not found:
        return "halal_likely", found

    statuses = {status for _, status in found}
    if "haram" in statuses:
        return "haram", found
    if "a_verifier" in statuses:
        return "a_verifier", found
    return "halal", found


def recommend_meals(phase: str):
    phase = phase.lower()
    if phase in ("menstrual", "menses", "menstruelle", "règles"):
        key = "menses"
    elif phase in ("follicular", "folliculaire"):
        key = "follicular"
    elif phase in ("ovulatory", "ovulatoire", "ovulation"):
        key = "ovulatory"
    elif phase in ("luteal", "lutéale", "luteale"):
        key = "luteal"
    else:
        key = "luteal"
    return PHASE_MEALS.get(key, PHASE_MEALS["luteal"])


def analyze_ocr_results(root_dir: str, profile: str = None):
    root_path = Path(root_dir)
    if not root_path.exists():
        print(f"Dossier introuvable: {root_dir}")
        return

    if profile:
        root_path = root_path / profile

    text_files = sorted(root_path.rglob("*.txt"))
    if not text_files:
        print(f"Aucun fichier .txt trouvé dans {root_path}")
        return

    results = []
    for text_file in text_files:
        content = text_file.read_text(encoding="utf-8")
        status, found = classify_text(content)
        results.append((text_file, status, found))

    for text_file, status, found in results:
        found_text = ", ".join([f"{term}({status})" for term, status in found]) or "Aucun terme connu"
        print(f"{text_file.relative_to(root_dir)} -> {status}")
        print(f"   Termes détectés: {found_text}")

    summary = {"halal": 0, "haram": 0, "a_verifier": 0, "halal_likely": 0}
    for _, status, _ in results:
        summary[status] = summary.get(status, 0) + 1

    print("\nRésumé:")
    for key in ["halal", "haram", "a_verifier", "halal_likely"]:
        print(f"  {key}: {summary[key]}")


def main():
    parser = argparse.ArgumentParser(description="Analyseur halal/haram et suggestions de régime pour le projet OCR.")
    parser.add_argument("--scan", default="ocr_results", help="Dossier à scanner pour les fichiers texte OCR")
    parser.add_argument("--profile", help="Sous-dossier du profil à analyser (ex. soul.body.mindd)")
    parser.add_argument("--phase", help="Phase du cycle pour les recommandations (menstrual, follicular, ovulatory, luteal)")
    parser.add_argument("--recommend", action="store_true", help="Afficher des recommandations de repas adaptées à la phase")
    parser.add_argument("--text", help="Analyser directement un texte donné")
    args = parser.parse_args()

    if args.text:
        status, found = classify_text(args.text)
        print(f"Texte: {args.text}")
        print(f"Statut: {status}")
        print("Termes détectés:")
        for term, status_term in found:
            print(f"  - {term}: {status_term}")
        return

    analyze_ocr_results(args.scan, args.profile)

    if args.recommend:
        phase = args.phase or "luteal"
        print(f"\nRecommandations pour la phase: {phase}")
        for meal in recommend_meals(phase):
            print(f"  - {meal}")


if __name__ == "__main__":
    main()
