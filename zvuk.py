import io
import os
import struct
import tempfile
import wave
from tkinter import filedialog, messagebox
from pcm import OUTPUT_RATE, MAX_SECONDS
try:
    import winsound
except ImportError:
    winsound = None

class ZvukMixin:

    def vytvor_wav_data(self):
        fs = self.nacti_fs()

        casti = []
        celkem_vzorku = 0

        for i, usek in enumerate(self.useky, 1):
            try:
                hodnoty = self.nacti_vzorky(usek["editor"])
                opakovani = self.nacti_opakovani(usek)

            except ValueError as e:
                raise ValueError(f"Chyba v úseku {i}: {e}")

            casti.append((hodnoty, opakovani))
            celkem_vzorku += len(hodnoty) * opakovani

        opakovani_vsech = self.nacti_opakovani_vsech()

        celkem = celkem_vzorku * opakovani_vsech
        delka = celkem / fs

        if delka > MAX_SECONDS:
            raise ValueError(
                f"Výsledný zvuk trvá {delka:.2f} s. "
                f"Maximum je {MAX_SECONDS} sekund."
            )

        # Sestavení všech úseků do jedné posloupnosti
        vsechny_vzorky = []

        for hodnoty, opakovani in casti:
            vsechny_vzorky.extend(hodnoty * opakovani)

        # Opakování celé skladby
        vsechny_vzorky *= opakovani_vsech

        # Převzorkování na výstupních 44 100 Hz
        pocet_vystupnich = round(
            len(vsechny_vzorky) * OUTPUT_RATE / fs
        )

        data = bytearray()

        for i in range(pocet_vystupnich):
            index = i * fs // OUTPUT_RATE
            index = min(index, len(vsechny_vzorky) - 1)

            amplituda = vsechny_vzorky[index]

            pcm = round(
                max(-1.0, min(1.0, amplituda)) * 32767
            )

            data.extend(struct.pack("<h", pcm))

        buffer = io.BytesIO()

        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(OUTPUT_RATE)
            wav.writeframes(data)

        return buffer.getvalue()


    def prehrat(self):
            if winsound is None:
                messagebox.showerror(
                    "Nepodporovaný systém",
                    "Přehrávání přes winsound funguje "
                    "pouze ve Windows."
                )
                return
    
            try:
                self.zastavit()
                data = self.vytvor_wav_data()
    
                cesta = os.path.join(
                    tempfile.gettempdir(),
                    "pcm_sekvencer_prehravani.wav"
                )
    
                with open(cesta, "wb") as soubor:
                    soubor.write(data)
    
                winsound.PlaySound(
                    cesta,
                    winsound.SND_FILENAME
                    | winsound.SND_ASYNC
                )
    
            except Exception as e:
                messagebox.showerror(
                    "Chyba přehrávání", str(e)
                )

    def zastavit(self):
            if winsound is not None:
                winsound.PlaySound(None, 0)

    def ulozit(self):
            cesta = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV soubory", "*.wav")]
            )
    
            if not cesta:
                return
    
            try:
                data = self.vytvor_wav_data()
    
                with open(cesta, "wb") as soubor:
                    soubor.write(data)
    
                messagebox.showinfo(
                    "Hotovo",
                    "Zvuk byl úspěšně uložen."
                )
    
            except Exception as e:
                messagebox.showerror(
                    "Chyba ukládání", str(e)
                )

    def zavrit(self):
            if self._aktualizace_id is not None:
                self.root.after_cancel(
                    self._aktualizace_id
                )
    
            self.zastavit()
            self.root.destroy()
