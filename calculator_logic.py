import math
from pcm import frekvence_tonu, nejblizsi_ton, vytvor_vlnu


def analyzuj_usek(pocet_vzorku, opakovani, fs):
    """Vrátí frekvenci, nejbližší tón, odchylku a délku úseku."""
    if fs <= 0:
        raise ValueError("Vzorkovací frekvence musí být kladná.")
    if pocet_vzorku <= 0:
        raise ValueError("Úsek neobsahuje žádné vzorky.")
    if opakovani < 1:
        raise ValueError("Počet opakování musí být alespoň 1.")

    frekvence = fs / pocet_vzorku
    ton, odchylka = nejblizsi_ton(frekvence)
    delka = pocet_vzorku * opakovani / fs
    return {
        "vzorky": pocet_vzorku,
        "frekvence": frekvence,
        "ton": ton,
        "odchylka": odchylka,
        "delka": delka,
        "pocet_celkem": pocet_vzorku * opakovani,
    }


def delka_skladby(pocty_vzorku, opakovani_vsech, fs):
    """Spočítá délku skladby z počtů vzorků jednotlivých úseků."""
    if fs <= 0:
        raise ValueError("Vzorkovací frekvence musí být kladná.")
    if opakovani_vsech < 1:
        raise ValueError("Opakování celé skladby musí být alespoň 1.")
    return sum(pocty_vzorku) * opakovani_vsech / fs


def vypocitej_ton(fs, delka, midi, hloubka, tvar):
    """Vygeneruje jednu periodu tónu a doporučené opakování."""
    if fs <= 0:
        raise ValueError("Vzorkovací frekvence musí být kladná.")
    if not math.isfinite(delka) or delka <= 0:
        raise ValueError("Délka tónu musí být kladné číslo.")

    idealni = frekvence_tonu(midi)
    n = max(1, round(fs / idealni))
    skutecna = fs / n
    odchylka = 1200 * math.log2(skutecna / idealni)
    opakovani = max(1, round(delka * fs / n))
    skutecna_delka = opakovani * n / fs
    hodnoty = vytvor_vlnu(n, hloubka, tvar)
    zapis = " ".join(format(hodnota, f"0{hloubka}b") for hodnota in hodnoty)

    return {
        "idealni": idealni,
        "skutecna": skutecna,
        "odchylka": odchylka,
        "vzorky": n,
        "opakovani": opakovani,
        "skutecna_delka": skutecna_delka,
        "zapis": zapis,
    }