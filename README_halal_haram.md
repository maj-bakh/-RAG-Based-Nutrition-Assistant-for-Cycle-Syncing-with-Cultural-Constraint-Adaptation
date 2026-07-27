
# Analyse Halal / Haram

## Objectif du fichier

L'objectif  est d'analyser le texte extrait par OCR afin d'identifier les ingrédients ou aliments liés aux catégories halal et haram Il permet également de proposer des recommandations alimentaires simples adaptées aux différentes phases du cycle menstruel.

## Fonctionnalités

Ce fichier permet de :

* lire les fichiers texte générés par l'OCR et stockés dans le dossier `ocr_results/` ;
* détecter des mots-clés tels que `porc`, `vin` ou `poulet halal` ;
* classifier le contenu selon quatre catégories : `halal`, `haram`, `a_verifier` ou `halal_likely` ;
* suggérer des repas simples en fonction de la phase du cycle menstruel (menstruelle, folliculaire, ovulatoire ou lutéale).

## Utilisation

![alt text](image.png)

## Remarque

Ce fichier constitue un prototype basé sur la détection de mots-clés. Les résultats sont fournis à titre indicatif et ne remplacent ni un avis religieux, ni les recommandations d'un professionnel de la santé ou de la nutrition.
