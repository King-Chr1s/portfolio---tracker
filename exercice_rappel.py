import pandas as pd

portefeuille = pd.DataFrame([
    {"ticker": "EssilorLuxottica", "pru": 170.5, "cours_actuel": 175.0, "compte": "PEA"},
    {"ticker": "Pernod Ricard", "pru": 67.25, "cours_actuel": 61.20, "compte": "PEA"},
    {"ticker": "Amazon", "pru": 180.0, "cours_actuel": 195.0, "compte": "CTO"},
    {"ticker": "Microsoft", "pru": 410.0, "cours_actuel": 430.0, "compte": "CTO"}
])

# Étape 1 : ajoute une colonne "valeur_ligne" = pru * 1 (on suppose 1 action par ligne ici)
# À toi de compléter avec la bonne syntaxe (celle vue en Q2)
portefeuille["valeur_ligne"] = portefeuille["pru"] * 1
portefeuille["performance_pct"] = round(
    (portefeuille["cours_actuel"] - portefeuille["pru"]) / portefeuille["pru"] * 100, 2
)

# Étape 2 : calcule la somme de "valeur_ligne" regroupée par "compte"
# À toi de compléter avec la bonne syntaxe (celle vue en Q2, mais l'autre outil)
somme_par_compte = portefeuille.groupby("compte")["valeur_ligne"].sum()
print(somme_par_compte)