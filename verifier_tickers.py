import yfinance as yf

tickers_a_tester = [
    "MSFT", "EUNL.DE", "GOOGL", "TTWO", "V", "AMZN", "NOW", "UBER", "NVDA",
    "DCAM.PA", "EL.PA", "RI.PA", "EN.PA", "BMW.DE", "TTE.PA",
    "ISP.MI", "VIE.PA", "SGO.PA", "ALKAL.PA", "ALCPB.PA"
]

for ticker in tickers_a_tester:
    try:
        action = yf.Ticker(ticker)
        historique = action.history(period="5d")
        if not historique.empty:
            dernier_cours = historique["Close"].iloc[-1]
            print(f"✅ {ticker} -> OK, dernier cours : {round(dernier_cours, 2)}")
        else:
            print(f"⚠️ {ticker} -> Aucune donnée renvoyée")
    except Exception as erreur:
        print(f"❌ {ticker} -> Erreur : {erreur}")