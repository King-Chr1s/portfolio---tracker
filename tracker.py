import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pandas as pd
import yfinance as yf
from datetime import datetime


def charger_portefeuille(chemin_csv):
    return pd.read_csv(chemin_csv)


def obtenir_taux_change(devise):
    """Retourne le taux de change EUR -> devise (combien de `devise` pour 1 euro)."""
    if devise == "EUR":
        return 1
    taux = yf.Ticker(f"EUR{devise}=X")
    return taux.history(period="1d")["Close"].iloc[-1]


def convertir_en_eur(cours_natif, taux_change):
    """Convertit un cours exprimé dans une devise en euros, via le taux de change fourni."""
    return cours_natif / taux_change


def recuperer_cours(ticker, devise, taux_par_devise):
    try:
        action = yf.Ticker(ticker)
        cours_natif = action.history(period="1d")["Close"].iloc[-1]
        taux = taux_par_devise[devise]
        return convertir_en_eur(cours_natif, taux)
    except Exception as erreur:
        print(f"⚠️ Problème avec {ticker} : {erreur}")
        return None


def calculer_performances(portefeuille):
    portefeuille["valeur_ligne"] = portefeuille["cours_actuel_eur"] * portefeuille["quantite"]
    portefeuille["performance_pct"] = round(
        (portefeuille["cours_actuel_eur"] - portefeuille["pru"]) / portefeuille["pru"] * 100, 2
    )
    portefeuille["plus_moins_value_eur"] = round(
        (portefeuille["cours_actuel_eur"] - portefeuille["pru"]) * portefeuille["quantite"], 2
    )
    return portefeuille


def exporter_csv(portefeuille):
    date_du_jour = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    nom_fichier = f"export_{date_du_jour}.csv"
    portefeuille.to_csv(nom_fichier, index=False)
    return nom_fichier

def generer_html(portefeuille, valeur_totale, repartition):
    """Génère une page HTML affichant les résultats du tracker."""

    def couleur_performance(valeur):
        couleur = "green" if valeur >= 0 else "red"
        return f'<span style="color:{couleur}">{valeur}%</span>'

    tableau_html = portefeuille[["ticker", "nom", "compte", "valeur_ligne", "performance_pct", "plus_moins_value_eur"]].copy()
    tableau_html["performance_pct"] = tableau_html["performance_pct"].apply(couleur_performance)

    lignes_html = tableau_html.to_html(escape=False, index=False)
    date_generation = datetime.now().strftime("%d/%m/%Y à %Hh%M")

    contenu_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Portfolio Tracker</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            h1 {{ color: #222; }}
            table {{ border-collapse: collapse; width: 100%; background: white; }}
            th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: right; }}
            th {{ background-color: #333; color: white; text-align: center; }}
            td:first-child, td:nth-child(2), td:nth-child(3) {{ text-align: left; }}
            .resume {{ margin-top: 20px; font-size: 1.1em; }}
        </style>
    </head>
    <body>
        <h1>Portfolio Tracker</h1>
        <p>Dernière mise à jour : {date_generation}</p>

        {lignes_html}

        <div class="resume">
            <p><strong>Valeur totale du portefeuille :</strong> {round(valeur_totale, 2)} €</p>
            <p><strong>CTO :</strong> {round(repartition.get('CTO', 0), 2)} €</p>
            <p><strong>PEA :</strong> {round(repartition.get('PEA', 0), 2)} €</p>
        </div>
    </body>
    </html>
    """

    with open("rapport.html", "w", encoding="utf-8") as fichier:
        fichier.write(contenu_html)

    print("Page HTML générée : rapport.html")

# --- Programme principal ---

portefeuille = charger_portefeuille("portefeuille.csv")

devises_utilisees = portefeuille["devise"].unique()
taux_par_devise = {devise: obtenir_taux_change(devise) for devise in devises_utilisees}

print("Taux de change (EUR -> devise) :", taux_par_devise)

cours_actuels_eur = []
for index, ligne in portefeuille.iterrows():
    cours = recuperer_cours(ligne["ticker"], ligne["devise"], taux_par_devise)
    cours_actuels_eur.append(cours)

portefeuille["cours_actuel_eur"] = cours_actuels_eur

portefeuille = calculer_performances(portefeuille)

print()
print(portefeuille[["ticker", "nom", "compte", "valeur_ligne", "performance_pct", "plus_moins_value_eur"]])

valeur_totale = portefeuille["valeur_ligne"].sum()
print()
print("Valeur totale du portefeuille :", round(valeur_totale, 2), "€")

repartition = portefeuille.groupby("compte")["valeur_ligne"].sum()
print()
print(repartition)

generer_html(portefeuille, valeur_totale, repartition)

nom_export = exporter_csv(portefeuille)
print()
print("Export sauvegardé dans :", nom_export)
import matplotlib.pyplot as plt

def generer_graphique(portefeuille):
    plt.figure(figsize=(8, 5))
    plt.bar(portefeuille["ticker"], portefeuille["performance_pct"])
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Performance (%)")
    plt.title("Performance par ligne du portefeuille")
    plt.tight_layout()
    plt.savefig("performance_graphique.png")
    print("Graphique sauvegardé dans : performance_graphique.png")
generer_graphique(portefeuille)