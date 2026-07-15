# Portefeuille avec PRU et cours actuels (fictifs pour l'exercice)
portefeuille = [
    {"ticker": "EssilorLuxottica", "pru": 170.5, "cours_actuel": 175.0},
    {"ticker": "Pernod Ricard", "pru": 67.25, "cours_actuel": 61.20},
    {"ticker": "Veolia", "pru": 34.51, "cours_actuel": 33.80}
]

for ligne in portefeuille:
    performance_pct = (ligne["cours_actuel"] - ligne["pru"]) / ligne["pru"] * 100
    performance_pct = round(performance_pct, 2)

    if performance_pct > 0:
        statut = "PLUS-VALUE"
    elif performance_pct < 0:
        statut = "MOINS-VALUE"
    else:
        statut = "ÉQUILIBRE"

    print(ligne["ticker"], "-", statut, "-", performance_pct, "%")