import yfinance as yf
import pandas as pd
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def recuperer_historique_mensuel(ticker, periode="2y"):
    action = yf.Ticker(ticker)
    historique = action.history(period=periode, interval="1mo")
    return historique["Close"]


def simuler_dca(ticker, montant_mensuel, periode="2y"):
    cours_mensuels = recuperer_historique_mensuel(ticker, periode)

    nb_actions_total = 0
    montant_investi_total = 0
    historique_valeur = []

    for date, cours in cours_mensuels.items():
        nb_actions_achetees = montant_mensuel / cours
        nb_actions_total += nb_actions_achetees
        montant_investi_total += montant_mensuel
        historique_valeur.append(nb_actions_total * cours)

    dernier_cours = cours_mensuels.iloc[-1]
    valeur_actuelle = nb_actions_total * dernier_cours
    performance_pct = round((valeur_actuelle - montant_investi_total) / montant_investi_total * 100, 2)

    return {
        "ticker": ticker,
        "montant_investi": round(montant_investi_total, 2),
        "valeur_actuelle": round(valeur_actuelle, 2),
        "performance_pct": performance_pct,
        "historique_valeur": historique_valeur
    }


def simuler_investissement_unique(ticker, montant_total, periode="2y"):
    cours_mensuels = recuperer_historique_mensuel(ticker, periode)
    premier_cours = cours_mensuels.iloc[0]
    dernier_cours = cours_mensuels.iloc[-1]

    nb_actions = montant_total / premier_cours
    valeur_actuelle = nb_actions * dernier_cours
    performance_pct = round((valeur_actuelle - montant_total) / montant_total * 100, 2)

    return {
        "valeur_actuelle": round(valeur_actuelle, 2),
        "performance_pct": performance_pct
    }


def comparer_tickers(tickers, montant_mensuel, periode="2y"):
    resultats = []
    for ticker in tickers:
        try:
            resultat = simuler_dca(ticker, montant_mensuel, periode)
            resultats.append(resultat)
        except Exception as erreur:
            print(f"⚠️ Problème avec {ticker} : {erreur}")
    return resultats


def generer_graphique_comparaison(resultats):
    plt.figure(figsize=(9, 5))
    for resultat in resultats:
        plt.plot(resultat["historique_valeur"], label=resultat["ticker"])
    plt.xlabel("Mois écoulés")
    plt.ylabel("Valeur du portefeuille (€)")
    plt.title("Évolution de la valeur - DCA comparé")
    plt.legend()
    plt.tight_layout()
    plt.savefig("dca_comparaison.png")
    print("Graphique sauvegardé dans : dca_comparaison.png")


# --- Programme principal ---

with open("config_dca.json", "r", encoding="utf-8") as fichier_config:
    config = json.load(fichier_config)

tickers_a_comparer = config["tickers_a_comparer"]
montant_mensuel = config["montant_mensuel"]
periode = config["periode"]

resultats = comparer_tickers(tickers_a_comparer, montant_mensuel, periode)

print(f"Comparaison DCA sur {periode}, {montant_mensuel}€/mois\n")
for resultat in resultats:
    print(f"{resultat['ticker']} -> Investi : {resultat['montant_investi']}€ | "
          f"Valeur actuelle : {resultat['valeur_actuelle']}€ | "
          f"Performance : {resultat['performance_pct']}%")

print()

ticker_reference = tickers_a_comparer[0]
montant_total_equivalent = montant_mensuel * len(resultats[0]["historique_valeur"])

resultat_unique = simuler_investissement_unique(ticker_reference, montant_total_equivalent, periode)

print(f"--- Comparaison DCA vs investissement unique sur {ticker_reference} ---")
print(f"DCA : {resultats[0]['valeur_actuelle']}€ (performance {resultats[0]['performance_pct']}%)")
print(f"Unique : {resultat_unique['valeur_actuelle']}€ (performance {resultat_unique['performance_pct']}%)")

generer_graphique_comparaison(resultats)