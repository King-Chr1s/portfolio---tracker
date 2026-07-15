import pandas as pd

portefeuille = pd.read_csv("portefeuille.csv")
print(portefeuille)
# Regrouper par type de compte et calculer la valeur moyenne du PRU
moyenne_par_compte = portefeuille.groupby("compte")["pru"].mean()
print(moyenne_par_compte)