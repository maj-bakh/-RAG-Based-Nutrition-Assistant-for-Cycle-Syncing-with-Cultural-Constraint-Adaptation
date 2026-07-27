# Prototype Halal/Haram et Recommandations Alimentaires

Ce projet contient un prototype pour analyser du texte OCR, détecter des ingrédients ou expressions halal/haram, et proposer des repas selon la phase du cycle.

## Structure du projet

- `OCR.py` : extraction du texte depuis les images existantes.
- `halal_haram_analyzer.py` : analyse du texte OCR et recommandations de repas.
- `ocr_results/` : résultats texte produits par `OCR.py`.

## Installation

```bash
pip install easyocr requests apify-client
```

## Exemples d’usage

1. Extraire le texte depuis les images :

```bash
python OCR.py
```

2. Analyser les textes OCR :

```bash
python halal_haram_analyzer.py --scan ocr_results --profile soul.body.mindd
```

3. Analyser un texte direct :

```bash
python halal_haram_analyzer.py --text "Poulet halal et riz"
```

4. Afficher des recommandations sur une phase :

```bash
python halal_haram_analyzer.py --recommend --phase luteal
```
