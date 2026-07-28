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