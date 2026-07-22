import pandas as pd
import yfinance as yf

portefeuille = pd.read_csv("portefeuille.csv")

taux_change = yf.Ticker("EURUSD=X")
eurusd = taux_change.history(period="1d")["Close"].iloc[-1]
print("Taux EUR/USD actuel :", round(eurusd, 4))
print()

cours_actuels_eur = []
for index, ligne in portefeuille.iterrows():
    ...
cours_actuels_eur = []
for index, ligne in portefeuille.iterrows():
    try:
        action = yf.Ticker(ligne["ticker"])
        cours_natif = action.history(period="1d")["Close"].iloc[-1]
        cours_en_eur = cours_natif / eurusd if ligne["devise"] == "USD" else cours_natif
    except Exception as erreur:
        print(f"⚠️ Problème avec {ligne['ticker']} : {erreur}")
        cours_en_eur = None

    cours_actuels_eur.append(cours_en_eur)

portefeuille["cours_actuel_eur"] = cours_actuels_eur
