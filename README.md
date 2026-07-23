# Portfolio Tracker

Un outil en ligne de commande qui calcule automatiquement la valeur et la performance d'un portefeuille d'investissement (PEA + CTO), avec récupération des cours en direct et conversion de devises.

## Fonctionnalités

- Lecture d'un portefeuille depuis un fichier CSV (ticker, PRU, quantité, compte, devise)
- Récupération des cours actuels via Yahoo Finance (`yfinance`)
- Conversion automatique EUR/USD pour les lignes cotées en dollars
- Calcul de la valeur, de la performance (%) et de la plus/moins-value (€) par ligne
- Agrégation par enveloppe (PEA / CTO)
- Export horodaté des résultats en CSV
- Génération d'un graphique de performance par ligne (`matplotlib`)
- Gestion des erreurs : un ticker invalide ou indisponible n'interrompt pas l'exécution

## Installation

1. Cloner le dépôt :
```bash
   git clone https://github.com/King-Chr1s/portfolio-tracker.git
   cd portfolio-tracker
```

2. Installer les dépendances :
```bash
   pip3 install -r requirements.txt
```

## Utilisation

1. Renseigner son portefeuille dans `portefeuille.csv`, au format :
2. Lancer le tracker :
```bash
   python3 tracker.py
```

3. Résultats produits :
   - Tableau détaillé affiché dans le terminal
   - Fichier `export_AAAA-MM-JJ_HHhMM.csv` avec le détail complet
   - Fichier `performance_graphique.png` avec le graphique en barres

## Structure du projet

| Fichier | Rôle |
|---|---|
| `tracker.py` | Script principal |
| `portefeuille.csv` | Données du portefeuille (à personnaliser) |
| `requirements.txt` | Dépendances Python |
| `.gitignore` | Fichiers exclus du suivi Git (exports, cache) |

## Technologies utilisées

- Python 3.9+
- pandas (manipulation de données)
- yfinance (récupération de cours boursiers)
- matplotlib (visualisation)

## Notes

Projet réalisé dans le cadre d'un apprentissage progressif de Python, pandas, Git/GitHub et des bonnes pratiques de développement (gestion d'erreurs, structuration en fonctions, branches Git).