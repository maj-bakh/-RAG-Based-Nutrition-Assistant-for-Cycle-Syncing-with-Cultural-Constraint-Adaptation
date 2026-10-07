# CycleSync Halal

### RAG-Based Nutrition Assistant for Cycle Syncing with Cultural Constraint Adaptation

<p align="center">
  <img src="image.png" alt="CycleSync Halal Logo" width="280"/>
</p>

<p align="center">
  An intelligent nutrition assistant combining menstrual cycle phases with cultural and religious dietary constraints.
</p>

<p align="center">
  Instagram Data Collection · Multilingual OCR · Ingredient Analysis · Halal/Haram Classification · Personalized Recommendations
</p>

## Table of Contents

* [About the Project](#about-the-project)
* [Team](#team)
* [Objectives](#objectives)
* [Architecture](#architecture)
* [Key Features](#key-features)
* [Project Structure](#project-structure)
* [Technologies](#technologies)
* [Installation](#installation)
* [Usage](#usage)
* [Analyzed Instagram Accounts](#analyzed-instagram-accounts)
* [Demo](#demo)
* [Security](#security)
* [Limitations and Disclaimer](#limitations-and-disclaimer)
* [License](#license)

## About the Project

CycleSync Halal is a research and experimental prototype that explores the use of Retrieval-Augmented Generation (RAG) to provide personalized nutrition recommendations based on menstrual cycle phases while taking cultural and religious dietary constraints into account.

The project was developed around the idea of combining nutrition, artificial intelligence, data processing, and cultural awareness in a single system. It uses food and wellness content collected from selected Instagram accounts as a source of unstructured data, then processes this content through OCR, ingredient extraction, Halal/Haram classification, and recommendation components.

The system is designed to answer a simple question:

> How can nutrition recommendations be personalized according to both the menstrual cycle and an individual's cultural or religious dietary constraints?

The project explores this question through a complete data processing pipeline, from social media content collection to ingredient analysis and personalized recommendations.

### Problem Statement

Existing nutrition resources may provide recommendations based on menstrual cycle phases without considering cultural or religious dietary requirements.

This project explores an approach that considers both:

* Nutritional needs associated with different menstrual cycle phases
* Cultural and religious dietary constraints, particularly Halal and Haram ingredients

### Proposed Approach

The system follows a data processing pipeline:

1. Collects food and wellness content from selected Instagram accounts using Apify.
2. Extracts text from food images using EasyOCR.
3. Processes multilingual content, including English, French, and Arabic.
4. Identifies and analyzes ingredients.
5. Classifies ingredients according to Halal/Haram compatibility.
6. Associates food recommendations with menstrual cycle phases.
7. Produces meal suggestions according to the selected phase and dietary constraints.

## Team

This project is developed by two contributors:

| Role                      | Name          | GitHub                                         |
| ------------------------- | ------------- | ---------------------------------------------- |
| Product Owner             | Sara EL-ATEIF | [@elateifsara](https://github.com/elateifsara) |
| Developer & Data Engineer | Majda Bakhari | [@maj-bakh](https://github.com/maj-bakh)       |

### Roles and Contributions

**Sara EL-ATEIF — Product Owner**

* Provided the initial project idea.
* Defined and clarified the cultural and religious constraints considered by the project.
* Contributed to the definition of the project's functional direction and requirements.

**Majda Bakhari — Developer & Data Engineer**

* Designed and implemented the technical pipeline.
* Developed the data collection, OCR, ingredient processing, and classification components.
* Implemented the recommendation logic and project structure.
* Managed the technical integration of the different components.

## Objectives

The main objectives of the project are to:

* Explore the use of RAG-based approaches for personalized nutrition.
* Combine unstructured social media data with structured ingredient knowledge.
* Process multilingual food-related content using OCR.
* Identify potential Halal and Haram ingredients.
* Provide recommendations according to menstrual cycle phases.
* Explore the adaptation of AI-based nutrition systems to cultural constraints.

## Architecture

The project follows a multi-stage data processing pipeline:

```text
Instagram Content
       |
       v
Apify Instagram Scraper
       |
       v
Images + Captions
       |
       v
Multilingual OCR
(EasyOCR)
       |
       v
Text Extraction
       |
       v
Ingredient Extraction
       |
       v
Halal/Haram Analysis
       |
       v
Cycle Phase Analysis
       |
       v
Personalized Recommendations
```

### System Workflow

```text
+---------------------------+
|     Instagram Content     |
|      Data Collection      |
+-------------+-------------+
              |
              v
+---------------------------+
|      Apify Scraper        |
|    Images + Captions      |
+-------------+-------------+
              |
              v
+---------------------------+
|     Multilingual OCR      |
|  English / French / Arabic|
+-------------+-------------+
              |
              v
+---------------------------+
|    Ingredient Extraction  |
+-------------+-------------+
              |
              v
+---------------------------+
|   Halal / Haram Analysis  |
|       Classification      |
+-------------+-------------+
              |
              v
+---------------------------+
|     Menstrual Cycle       |
|      Phase Analysis       |
+-------------+-------------+
              |
              v
+---------------------------+
| Personalized Nutrition    |
|      Recommendations      |
+---------------------------+
```

## Key Features

### Instagram Data Collection

The project uses Apify to collect food and wellness content from selected Instagram accounts.

### Multilingual OCR

EasyOCR is used to extract text from images, with support for:

* English
* French
* Arabic

### Ingredient Classification

Detected ingredients are classified into four categories:

| Category       | Description                                                               |
| -------------- | ------------------------------------------------------------------------- |
| `halal`        | Ingredients identified as compatible with Halal requirements              |
| `haram`        | Ingredients identified as prohibited                                      |
| `a_verifier`   | Ingredients requiring additional verification                             |
| `halal_likely` | No prohibited ingredient detected, but confirmation may still be required |

### Cycle-Based Recommendations

The system supports four menstrual cycle phases:

| Phase      | Main Focus                                  |
| ---------- | ------------------------------------------- |
| Menstrual  | Iron, magnesium and supportive foods        |
| Follicular | Light proteins and energy                   |
| Ovulatory  | Antioxidants and omega-3                    |
| Luteal     | Complex carbohydrates, fiber and vitamin B6 |

### Ingredient Alternatives

When an ingredient is considered incompatible or requires verification, the system can provide alternative ingredient suggestions.

## Project Structure

```text
-RAG-Based-Nutrition-Assistant-for-Cycle-Syncing-with-Cultural-Constraint-Adaptation/
│
├── scraper.py
├── OCR.py
├── halal_haram_analyzer.py
├── remplacer_par_suggestion.py
├── separer_ingredients.py
├── transformationJSON.py
├── ocr_data.json
├── requirement.txt
│
├── README.md
├── README_project.md
├── README_halal_haram.md
│
├── soul.body.mindd/
├── manskis_wellness/
│
├── ocr_results/
│   ├── soul.body.mindd/
│   │   ├── post_1_description_1.txt
│   │   └── ...
│   │
│   └── manskis_wellness/
│       └── ...
│
└── image.png
```

## Technologies

| Technology | Purpose                                |
| ---------- | -------------------------------------- |
| Python     | Core development and data processing   |
| Apify      | Instagram data collection              |
| EasyOCR    | Multilingual text extraction           |
| Pillow     | Image processing                       |
| Requests   | HTTP requests                          |
| JSON       | Structured data storage                |
| RAG        | Retrieval-based information processing |

## Installation

### Prerequisites

* Python 3.9 or later
* An Apify account and API token

### Clone the Repository

```bash
git clone https://github.com/maj-bakh/-RAG-Based-Nutrition-Assistant-for-Cycle-Syncing-with-Cultural-Constraint-Adaptation.git

cd -RAG-Based-Nutrition-Assistant-for-Cycle-Syncing-with-Cultural-Constraint-Adaptation
```

### Install Dependencies

```bash
pip install -r requirement.txt
```

Alternatively:

```bash
pip install apify-client requests easyocr pillow
```

### Configure the Apify Token

Linux / macOS:

```bash
export APIFY_TOKEN="your_apify_token"
```

Windows CMD:

```bash
set APIFY_TOKEN=your_apify_token
```

Windows PowerShell:

```bash
$env:APIFY_TOKEN="your_apify_token"
```

Do not commit API credentials to the repository.

## Usage

### 1. Collect Instagram Data

```bash
python scraper.py
```

This step collects the configured Instagram content and stores the retrieved images and captions.

### 2. Extract Text with OCR

```bash
python OCR.py
```

The extracted text is organized under:

```text
ocr_results/
```

### 3. Analyze Ingredients

Analyze OCR results:

```bash
python halal_haram_analyzer.py --scan ocr_results --profile soul.body.mindd
```

Analyze text directly:

```bash
python halal_haram_analyzer.py --text "Poulet halal, riz, épinards et huile d'olive"
```

### 4. Generate Recommendations

```bash
python halal_haram_analyzer.py --recommend --phase luteal
```

Available phases:

```text
menstrual
follicular
ovulatory
luteal
```

## Analyzed Instagram Accounts

The current pipeline is configured to work with the following accounts:

| Account                                                         | Focus                              |
| --------------------------------------------------------------- | ---------------------------------- |
| [soul.body.mindd](https://www.instagram.com/soul.body.mindd/)   | Holistic wellness and nutrition    |
| [manskis_wellness](https://www.instagram.com/manskis_wellness/) | Women's wellness and cycle syncing |

The scraper retrieves the configured recent posts from these accounts during execution.

## Demo

A short demonstration of the project is available here:

[Watch the project demo](https://drive.google.com/file/d/1xRCHAQOLqIw9c5Ah7C3ZkBSU2E8Y30Ng/view?usp=sharing)

## Security

API credentials should never be stored directly in the source code.

Recommended practices:

* Store `APIFY_TOKEN` as an environment variable.
* Keep `.env` files out of version control.
* Never publish API keys on GitHub.
* Rotate credentials if they are accidentally exposed.

Example:

```bash
echo "APIFY_TOKEN=your_token" > .env
echo ".env" >> .gitignore
```

## Limitations and Disclaimer

This project is a research and experimental prototype.

The Halal/Haram classification relies on a simplified knowledge base and keyword-based analysis. It should not be considered a definitive religious ruling or a substitute for certification from a qualified Halal authority.

The nutritional recommendations are intended for research and informational purposes only. They do not constitute medical or nutritional advice and should not replace consultation with qualified healthcare or nutrition professionals.

The project is intended to demonstrate a technical approach for combining data extraction, OCR, ingredient analysis, cultural constraints, and personalized recommendation systems.

## License

This project is distributed under the MIT License.

See the `LICENSE` file for more information.

## Authors

### Sara EL-ATEIF

Product Owner
GitHub: [@elateifsara](https://github.com/elateifsara)

### Majda Bakhari

Developer & Data Engineer
GitHub: [@maj-bakh](https://github.com/maj-bakh)
