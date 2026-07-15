import pandas as pd
import yfinance as yf

# 1. Charger le portefeuille depuis le CSV
portefeuille = pd.read_csv("portefeuille.csv")

# 2. Récupérer le taux de change EUR/USD actuel (combien de dollars pour 1 euro)
taux_change = yf.Ticker("EURUSD=X")
eurusd = taux_change.history(period="1d")["Close"].iloc[-1]
print("Taux EUR/USD actuel :", round(eurusd, 4))
print()

# 3. Récupérer le cours actuel de chaque ligne, en convertissant si nécessaire
cours_actuels_eur = []
for index, ligne in portefeuille.iterrows():
    action = yf.Ticker(ligne["ticker"])
    historique = action.history(period="1d")
    cours_natif = historique["Close"].iloc[-1]

    if ligne["devise"] == "USD":
        cours_en_eur = cours_natif / eurusd
    else:
        cours_en_eur = cours_natif

    cours_actuels_eur.append(cours_en_eur)

portefeuille["cours_actuel_eur"] = cours_actuels_eur

# 4. Calculer valeur et performance (tout est maintenant en euros)
portefeuille["valeur_ligne"] = portefeuille["cours_actuel_eur"] * portefeuille["quantite"]
portefeuille["performance_pct"] = round(
    (portefeuille["cours_actuel_eur"] - portefeuille["pru"]) / portefeuille["pru"] * 100, 2
)

# 5. Afficher le détail
print(portefeuille)
print()

# 6. Valeur totale et répartition par compte
valeur_totale = portefeuille["valeur_ligne"].sum()
print("Valeur totale du portefeuille :", round(valeur_totale, 2), "€")

repartition = portefeuille.groupby("compte")["valeur_ligne"].sum()
print()
print(repartition)
# 7. Ajouter la plus/moins-value en euros (pas juste en %)
portefeuille["plus_moins_value_eur"] = round(
    (portefeuille["cours_actuel_eur"] - portefeuille["pru"]) * portefeuille["quantite"], 2
)

print()
print(portefeuille[["ticker", "nom", "compte", "valeur_ligne", "performance_pct", "plus_moins_value_eur"]])

# 8. Exporter le résultat dans un nouveau fichier CSV, horodaté
from datetime import datetime

date_du_jour = datetime.now().strftime("%Y-%m-%d_%Hh%M")
nom_fichier_export = f"export_{date_du_jour}.csv"

portefeuille.to_csv(nom_fichier_export, index=False)
print()
print("Export sauvegardé dans :", nom_fichier_export)