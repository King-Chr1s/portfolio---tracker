import yfinance as yf
# Récupérer les infos d'une action via son ticker (symbole boursier)
action = yf.Ticker("MC.PA")   # MC.PA = LVMH sur Euronext Paris

# Récupérer le cours actuel (ou le plus récent disponible)
historique = action.history(period="5d")
print(historique)
# Récupérer uniquement le dernier cours de clôture connu
dernier_cours = historique["Close"].iloc[-1]
print("Dernier cours LVMH :", round(dernier_cours, 2), "€")