import math
from pcm import OUTPUT_RATE


class VstupyMixin:
    # -----------------------------------------------------------
    # Přeskupení bitů na n-tice dle zvolené bitové hloubky
    # -----------------------------------------------------------
    def preskup_bity(self, *args):
        if self._meni_bity:
            return

        self._meni_bity = True

        try:
            hloubka = self.bity.get()

            for usek in self.useky:
                editor = usek["editor"]

                proud = "".join(
                    editor.get("1.0", "end").split()
                )

                if any(c not in "01" for c in proud):
                    continue

                skupiny = [
                    proud[i:i + hloubka]
                    for i in range(
                        0, len(proud), hloubka
                    )
                ]

                if skupiny:
                    skupiny[-1] = skupiny[-1].ljust(
                        hloubka, "0"
                    )

                editor.delete("1.0", "end")
                editor.insert(
                    "1.0", " ".join(skupiny)
                )

        finally:
            self._meni_bity = False

        self.naplanovat_aktualizaci()

    def nacti_fs(self):
        try:
            fs = int(self.frekvence.get())
        except ValueError:
            raise ValueError(
                "Vzorkovací frekvence musí být celé číslo."
            )

        if not 1 <= fs <= OUTPUT_RATE:
            raise ValueError(
                "Vzorkovací frekvence musí být "
                "1 až 44 100 Hz."
            )

        return fs

    def nacti_delku(self):
        try:
            delka = float(
                self.delka_tonu.get().replace(",", ".")
            )
        except ValueError:
            raise ValueError(
                "Délka tónu musí být číslo."
            )

        if not math.isfinite(delka) or delka <= 0:
            raise ValueError(
                "Délka tónu musí být kladné číslo."
            )

        return delka

    def nacti_opakovani(self, usek):
        try:
            pocet = int(usek["opakovani"].get())
        except ValueError:
            raise ValueError(
                "Počet opakování musí být celé číslo."
            )

        if pocet < 1:
            raise ValueError(
                "Počet opakování musí být alespoň 1."
            )

        return pocet

    def nacti_opakovani_vsech(self):
        try:
            pocet = int(self.opakovani_vsech.get())
        except ValueError:
            raise ValueError(
                "Opakování celé skladby musí být celé číslo."
            )

        if pocet < 1:
            raise ValueError(
                "Opakování celé skladby musí být alespoň 1."
            )

        return pocet

    def nacti_vzorky(self, editor):
        hloubka = self.bity.get()
        skupiny = editor.get("1.0", "end").split()

        if not skupiny:
            raise ValueError(
                "Úsek neobsahuje žádné vzorky."
            )

        maximum = 2 ** hloubka - 1
        hodnoty = []

        # -----------------------------------------------------------
        # Ověření platnosti úseku
        # -----------------------------------------------------------
        for skupina in skupiny:
            if (
                len(skupina) != hloubka
                or any(c not in "01" for c in skupina)
            ):
                raise ValueError(
                    f"Neplatný vzorek '{skupina}'. "
                    f"Je potřeba přesně {hloubka} bitů."
                )

            cislo = int(skupina, 2)
            amplituda = 2 * cislo / maximum - 1
            hodnoty.append(amplituda)

        return hodnoty
