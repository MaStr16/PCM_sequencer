"""Export skutečných bajtů výsledného nekomprimovaného WAV jako bitů 0 a 1.

Modul nemění způsob generování WAV ani data v editorech.
"""

from tkinter import filedialog, messagebox


class ExportTXTMixin:
    def exportovat_txt(self):
        """Uloží všechny bajty WAV jako souvislou řadu bitů v pořadí bajtů souboru."""
        cesta = filedialog.asksaveasfilename(
            title="Exportovat bitový proud do TXT",
            defaultextension=".txt",
            filetypes=[("Textové soubory", "*.txt")],
        )
        if not cesta:
            return

        try:
            # Používá stejnou metodu jako tlačítko „Uložit WAV“.
            wav_data = self.vytvor_wav_data()
            pocet_bitu = len(wav_data) * 8
            velikost_mb = pocet_bitu / 1_000_000

            # Textový výpis zabere zhruba osmkrát více místa než WAV.
            if velikost_mb >= 10:
                souhlas = messagebox.askyesno(
                    "Velký textový soubor",
                    f"TXT bude mít přibližně {velikost_mb:.1f} MB "
                    f"({pocet_bitu:,} bitů).\n\nPokračovat?",
                )
                if not souhlas:
                    return

            # Zapisujeme po blocích, aby se nevytvářel obří řetězec v paměti.
            with open(cesta, "w", encoding="ascii", newline="") as soubor:
                for zacatek in range(0, len(wav_data), 8192):
                    blok = wav_data[zacatek:zacatek + 8192]
                    soubor.write("".join(f"{bajt:08b}" for bajt in blok))

            messagebox.showinfo(
                "Export dokončen",
                f"Uloženo {pocet_bitu:,} bitů.\n"
                "TXT obsahuje hlavičku WAV i nekomprimovaná zvuková data.",
            )
        except (ValueError, OSError) as chyba:
            messagebox.showerror("Chyba exportu TXT", str(chyba))
