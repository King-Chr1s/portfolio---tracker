import pandas as pd
from tracker import convertir_en_eur, calculer_performances


def test_convertir_en_eur_taux_1():
    """Si le taux de change est 1, la conversion ne doit rien changer."""
    assert convertir_en_eur(100, 1) == 100


def test_convertir_en_eur_taux_superieur_a_1():
    """100 dans une devise à taux 2 doit donner 50 en euros."""
    resultat = convertir_en_eur(100, 2)
    assert resultat == 50


def test_calculer_performances_plus_value():
    """Une ligne avec cours_actuel_eur > pru doit être en plus-value."""
    portefeuille_test = pd.DataFrame([
        {"pru": 100, "quantite": 2, "cours_actuel_eur": 120}
    ])
    resultat = calculer_performances(portefeuille_test)
    assert resultat["performance_pct"].iloc[0] == 20.0
    assert resultat["plus_moins_value_eur"].iloc[0] == 40.0


def test_calculer_performances_moins_value():
    """Une ligne avec cours_actuel_eur < pru doit être en moins-value."""
    portefeuille_test = pd.DataFrame([
        {"pru": 100, "quantite": 1, "cours_actuel_eur": 90}
    ])
    resultat = calculer_performances(portefeuille_test)
    assert resultat["performance_pct"].iloc[0] == -10.0