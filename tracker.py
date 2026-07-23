import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pandas as pd
import yfinance as yf
from datetime import datetime


def charger_portefeuille(chemin_csv):
    return pd.read_csv(chemin_csv)


def recuperer_taux_change():
    taux_change = yf.Ticker("EURUSD=X")
    return taux_change.history(period="1d")["Close"].iloc[-1]


def recuperer_cours(ticker, devise, eurusd):
    try:
        action = yf.Ticker(ticker)
        cours_natif = action.history(period="1d")["Close"].iloc[-1]
        return cours_natif / eurusd if devise == "USD" else cours_natif
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

eurusd = recuperer_taux_change()
print("Taux EUR/USD actuel :", round(eurusd, 4))

cours_actuels_eur = []
for index, ligne in portefeuille.iterrows():
    cours = recuperer_cours(ligne["ticker"], ligne["devise"], eurusd)
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