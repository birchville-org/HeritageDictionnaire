# Héritage du Sanskrit — Dictionnaire sanskrit-français (VitePress & PDF Indexé)

[![Deploy VitePress to GitHub Pages](https://github.com/birchville-org/HeritageDictionnaire/actions/workflows/deploy.yml/badge.svg)](https://github.com/birchville-org/HeritageDictionnaire/actions/workflows/deploy.yml)
[![Live Service](https://img.shields.io/badge/Live_Service-github.io-b45309?style=flat&logo=github)](https://birchville-org.github.io/HeritageDictionnaire/)

> 🌐 **Service en ligne (GitHub Pages) :**  
> **[https://birchville-org.github.io/HeritageDictionnaire/](https://birchville-org.github.io/HeritageDictionnaire/)**

Ce projet modernise et enrichit l'accès lexicographique au dictionnaire *Héritage du Sanskrit* de **Gérard Huet** (INRIA Paris, version 3.75 / 3.84). Il combine deux réalisations majeures :

1. **Document Outlines (Signets hiérarchiques)** injectés directement dans le PDF de 1217 pages sans altérer la mise en page TeX.
2. **Plateforme web interactive VitePress & Recherche plein-texte**, avec navigation par classe phonétique et moteur de recherche local intégré (comme dans le projet de grammaire grecque).

---

## 🚀 Démarrage rapide

### 1. Prérequis & Installation
```bash
# Dépendances Node.js (VitePress)
npm install

# Environnement Python (pour les scripts d'indexation et conversion)
python3 -m venv venv
./venv/bin/pip install pymupdf pypdf
```

### 2. Lancer le serveur de développement
```bash
npm run docs:dev
```
*Le site est accessible en local sur `http://localhost:5173` (ou port configuré).*

### 3. Compiler pour la production
```bash
npm run docs:build
```
*Les fichiers statiques prêts pour le déploiement sont générés dans `docs/.vitepress/dist`.*

---

## 📑 1. PDF avec Signets Hiérarchiques (208 Outlines)

Le fichier d'origine [input/HeritageDictionnaire.pdf](input/HeritageDictionnaire.pdf) (1217 pages) ne comportait aucun signet.

Le script [scripts/index_pdf.py](scripts/index_pdf.py) extrait la signature typographique des entrées (polices TeX `Velthuis-dvng10` et `CMSL10`) et injecte une arborescence complète :
* **Niveau 1 :** Frontmatter (Titre, Notice, Avant-propos, Préface 1998, L'alphabet devanāgarī, Abréviations) et Dictionnaire.
* **Niveau 2 :** Les 43 lettres traditionnelles du sanskrit (`अ (a)`, `क (ka)`, `प (pa)`, `स (sa)`, etc.).
* **Niveau 3 :** Sous-sections phonétiques pour les lettres volumineuses (`ak-`, `ag-`, `ka-`, `kā-`, `ki-`, `ku-`, `kṛ-`, `ke-`, `ko-`, `kṣ-`, etc.).

Le fichier résultant est généré dans :
* [output/HeritageDictionnaire_indexed.pdf](output/HeritageDictionnaire_indexed.pdf)
* [docs/public/HeritageDictionnaire_indexed.pdf](docs/public/HeritageDictionnaire_indexed.pdf)

Pour régénérer l'index PDF à tout moment :
```bash
npm run index:pdf
```

---

## 🌐 2. Dictionnaire VitePress & Recherche Instantanée

* **23 261 entrées lexicales** réparties en 46 pages par lettre (`docs/dict/*.md`).
* **Moteur de recherche VitePress local (`detailedView`)** :
  * Recherche plein-texte instantanée accessible via raccourci `⌘K` / `Ctrl+K` ou le bouton de recherche.
  * Recherche en devanāgarī (ex. `योग`, `शिव`, `धर्म`).
  * Recherche en translittération IAST (ex. `śiva`, `dharma`, `akampya`).
  * Recherche dans les définitions françaises (ex. `destructeur`, `imperturbable`).
* **Typographie sanskrite** : Rendu optimisé via *Noto Serif Devanagari* et mise en évidence des catégories grammaticales, racines verbales (`√`) et liens croisés.

Pour régénérer les pages du dictionnaire à partir des données StarDict :
```bash
npm run build:dict
```
