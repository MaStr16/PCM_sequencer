import math


#-----------------------------------------------------------
# Základní konstanty
#-----------------------------------------------------------

OUTPUT_RATE = 44100
MAX_SECONDS = 120
NAZVY_TONU = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
TVARY = ["Sinusová", "Obdélníková", "Trojúhelníková", "Pilová"]

#-----------------------------------------------------------
# Určování tónů
#-----------------------------------------------------------

def nazev_tonu(midi):
    return NAZVY_TONU[midi % 12] + str(midi // 12 - 1)

def frekvence_tonu(midi):
    return 440 * 2 ** ((midi - 69) / 12)

def nejblizsi_ton(frekvence):
    if frekvence <= 0:
        return "—", 0

    midi = round(69 + 12 * math.log2(frekvence / 440))
    idealni = frekvence_tonu(midi)
    odchylka = 1200 * math.log2(frekvence / idealni)

    return nazev_tonu(midi), odchylka

#-----------------------------------------------------------
# Vlna jako perioda z PCM hodnot
#-----------------------------------------------------------

def vytvor_vlnu(pocet, hloubka, tvar):
    maximum = 2 ** hloubka - 1
    hodnoty = []

    for i in range(pocet):
        faze = i / pocet

        if tvar == "Sinusová":
            amplituda = math.sin(2 * math.pi * faze)

        elif tvar == "Obdélníková":
            amplituda = 1.0 if faze < 0.5 else -1.0

        elif tvar == "Trojúhelníková":
            amplituda = (
                2 / math.pi
                * math.asin(math.sin(2 * math.pi * faze))
            )

        elif tvar == "Pilová":
            amplituda = 2 * faze - 1

        else:
            raise ValueError("Neznámý tvar vlny.")

        hodnota = round((amplituda + 1) * maximum / 2)
        hodnoty.append(max(0, min(maximum, hodnota)))

    return hodnoty

