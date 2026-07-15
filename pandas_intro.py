import pandas as pd

# La même donnée qu'avant, mais en DataFrame (tableau structuré)
portefeuille = pd.DataFrame([
    {"ticker": "EssilorLuxottica", "pru": 170.5, "cours_actuel": 175.0},
    {"ticker": "Pernod Ricard", "pru": 67.25, "cours_actuel": 61.20},
    {"ticker": "Veolia", "pru": 34.51, "cours_actuel": 33.80}
])

# Afficher tout le tableau
print(portefeuille)
print()

# Créer une nouvelle colonne "performance_pct" pour TOUTES les lignes d'un coup
portefeuille["performance_pct"] = round(
    (portefeuille["cours_actuel"] - portefeuille["pru"]) / portefeuille["pru"] * 100, 2
)

print(portefeuille)
# Filtrer : n'afficher que les lignes en moins-value
en_moins_value = portefeuille[portefeuille["performance_pct"] < 0]
print(en_moins_value)
# Trier le portefeuille par performance, du pire au meilleur
portefeuille_trie = portefeuille.sort_values("performance_pct")
print(portefeuille_trie)

print()

# Trier du meilleur au pire (ordre inversé)
portefeuille_trie_desc = portefeuille.sort_values("performance_pct", ascending=False)
print(portefeuille_trie_desc)