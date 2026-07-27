# Projet NTL - Prototype Halal/Haram et Nutrition

Ce projet contient un prototype pour :
- récupérer des publications Instagram et leurs descriptions,
- extraire du texte depuis des images avec OCR,
- analyser le texte pour détecter des termes halal / haram / à vérifier,
- proposer des recommandations de repas selon la phase du cycle.

## Fichiers principaux

- `scraper.py` : récupération des publications Instagram via Apify.
- `OCR.py` : extraction de texte à partir des images dans les dossiers des profils.
- `halal_haram_analyzer.py` : analyse des textes OCR et recommandations alimentaires.
- `ocr_results/` : dossiers de résultats OCR enregistrés.

## Installation

```bash
pip install apify-client requests easyocr
```

> Si tu veux exécuter tout le projet depuis zéro, ajoute aussi `pillow` si tu traites des images dans d'autres scripts :

```bash
pip install pillow
```

## Utilisation

1. Extraire le texte des images :

```bash
python OCR.py
```

2. Analyser les résultats OCR pour un profil spécifique :

```bash
python halal_haram_analyzer.py --scan ocr_results --profile soul.body.mindd
```

3. Analyser un texte directement :

```bash
python halal_haram_analyzer.py --text "Poulet halal et riz"
```

4. Obtenir des recommandations de repas pour une phase du cycle :

```bash
python halal_haram_analyzer.py --recommend --phase luteal
```

## Remarques

- `halal_haram_analyzer.py` utilise une base de connaissances simple des ingrédients.
- Les cas `a_verifier` sont ceux qui doivent être vérifiés manuellement : viande, fromage, etc.
- Le projet reste un prototype : il identifie des mots clés, il ne remplace pas un avis religieux ou nutritionnel.

## Sécurité

Ne laisse pas de jeton API dans le code source. Si tu utilises Apify, remplace la valeur de `APIFY_TOKEN` par une variable d'environnement dans `scraper.py`.
