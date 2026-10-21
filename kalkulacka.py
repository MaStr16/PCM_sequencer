import math
import tkinter as tk
from tkinter import ttk, messagebox
from pcm import NAZVY_TONU, TVARY, nazev_tonu, frekvence_tonu, nejblizsi_ton, vytvor_vlnu

class KalkulackaMixin:

    def vytvor_kalkulacku(self, rodic):
            panel = ttk.Frame(rodic)
            panel.pack(fill="both", expand=True)
    
            # Horní část – živá analýza
    
            analyza = ttk.LabelFrame(
                panel,
                text="Živá analýza zadaných úseků",
                padding=10
            )
            analyza.pack(fill="x", pady=(0, 10))
    
            sloupce = (
                "usek", "vzorky", "frekvence",
                "ton", "delka"
            )
    
            self.tabulka_useku = ttk.Treeview(
                analyza,
                columns=sloupce,
                show="headings",
                height=5,
                selectmode="browse"
            )
    
            hlavicky = {
                "usek": "Úsek",
                "vzorky": "Vzorků",
                "frekvence": "Hz",
                "ton": "Tón",
                "delka": "Délka (s)"
            }
    
            for sloupec in sloupce:
                self.tabulka_useku.heading(
                    sloupec,
                    text=hlavicky[sloupec]
                )
                self.tabulka_useku.column(
                    sloupec,
                    width=75,
                    anchor="center",
                    stretch=True
                )
    
            self.tabulka_useku.pack(fill="x")
    
            self.tabulka_useku.bind(
                "<<TreeviewSelect>>",
                self.zobraz_detail_useku
            )
    
            self.detail_useku = ttk.Label(
                analyza, text="", wraplength=450
            )
            self.detail_useku.pack(
                anchor="w", pady=(7, 0)
            )
    
            self.info_skladby = ttk.Label(
                analyza,
                text="",
                font=("Arial", 10, "bold"),
                wraplength=450
            )
            self.info_skladby.pack(
                anchor="w", pady=(5, 0)
            )
    
            # Dolní část – kalkulačka binárního zápisu
    
            kalk = ttk.LabelFrame(
                panel,
                text="Kalkulačka binárního zápisu tónů",
                padding=10
            )
            kalk.pack(fill="both", expand=True)
    
            ttk.Label(
                kalk,
                text=(
                    "Vyber tón, tvar vlny a délku. "
                    "Kalkulačka zobrazí přesný binární zápis "
                    "jedné periody a počet opakování."
                ),
                wraplength=450
            ).pack(anchor="w", pady=(0, 8))
    
            # Výběr tónu
    
            vyber_ramecek = ttk.Frame(kalk)
            vyber_ramecek.pack(fill="x")
    
            ttk.Label(
                vyber_ramecek,
                text="Hudební tón:"
            ).grid(
                row=0, column=0,
                sticky="w", pady=4
            )
    
            self.vybrany_ton = tk.StringVar(
                value="C4"
            )
    
            self.tony_midi = {}
    
            nazvy = []
    
            for midi in range(48, 84):
                nazev = nazev_tonu(midi)
                self.tony_midi[nazev] = midi
                nazvy.append(nazev)
    
            self.vyber_tonu = ttk.Combobox(
                vyber_ramecek,
                textvariable=self.vybrany_ton,
                values=nazvy,
                state="readonly",
                width=15
            )
            self.vyber_tonu.grid(
                row=0, column=1,
                sticky="w", padx=8
            )
    
            self.vyber_tonu.bind(
                "<<ComboboxSelected>>",
                self.naplanovat_aktualizaci
            )
    
            ttk.Label(
                vyber_ramecek,
                text="Tvar vlny:"
            ).grid(
                row=1, column=0,
                sticky="w", pady=4
            )
    
            ttk.Combobox(
                vyber_ramecek,
                textvariable=self.tvar_vlny,
                values=TVARY,
                state="readonly",
                width=18
            ).grid(
                row=1, column=1,
                sticky="w", padx=8
            )
    
            ttk.Label(
                vyber_ramecek,
                text="Délka tónu (s):"
            ).grid(
                row=2, column=0,
                sticky="w", pady=4
            )
    
            ttk.Entry(
                vyber_ramecek,
                textvariable=self.delka_tonu,
                width=12
            ).grid(
                row=2, column=1,
                sticky="w", padx=8
            )
    
            # Výsledky výpočtu
    
            self.vysledek_tonu = ttk.Label(
                kalk,
                text="",
                justify="left",
                wraplength=450
            )
            self.vysledek_tonu.pack(
                anchor="w", pady=(10, 8)
            )
    
            ttk.Label(
                kalk,
                text="Binární zápis jedné periody:",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")
    
            oblast_textu = ttk.Frame(kalk)
            oblast_textu.pack(
                fill="both",
                expand=True,
                pady=5
            )
    
            self.binarni_vystup = tk.Text(
                oblast_textu,
                height=7,
                font=("Consolas", 10),
                wrap="word"
            )
            self.binarni_vystup.pack(
                side="left",
                fill="both",
                expand=True
            )
    
            posuvnik = ttk.Scrollbar(
                oblast_textu,
                orient="vertical",
                command=self.binarni_vystup.yview
            )
            posuvnik.pack(side="right", fill="y")
    
            self.binarni_vystup.configure(
                yscrollcommand=posuvnik.set,
                state="disabled"
            )
    
            ttk.Button(
                kalk,
                text="Kopírovat binární zápis",
                command=self.kopirovat_binarni_zapis
            ).pack(fill="x", pady=(6, 4))
    
            self.info_opakovani = ttk.Label(
                kalk,
                text="",
                font=("Arial", 10, "bold")
            )
            self.info_opakovani.pack(
                anchor="w", pady=(5, 0)
            )
    
            ttk.Label(
                kalk,
                text=(
                    "Zkopírované vzorky vlož do libovolného "
                    "úseku vlevo. Nastav počet opakování "
                    "podle vypočítané hodnoty."
                ),
                foreground="gray",
                wraplength=450
            ).pack(anchor="w", pady=(8, 0))

    def naplanovat_aktualizaci(self, *args):
            if self._aktualizace_id is not None:
                self.root.after_cancel(
                    self._aktualizace_id
                )
    
            self._aktualizace_id = self.root.after(
                150, self.aktualizuj_vse
            )

    def aktualizuj_vse(self):
            self._aktualizace_id = None
    
            self.aktualizuj_useky()
            self.aktualizuj_binarni_kalkulacku()

    def aktualizuj_useky(self):
            vyber = self.tabulka_useku.selection()
            predchozi = vyber[0] if vyber else "1"
    
            for polozka in self.tabulka_useku.get_children():
                self.tabulka_useku.delete(polozka)
    
            try:
                fs = self.nacti_fs()
                opakovani_vsech = (
                    self.nacti_opakovani_vsech()
                )
            except ValueError as e:
                self.info_skladby.configure(text=str(e))
                self.detail_useku.configure(text="")
                return
    
            celkem_vzorku = 0
            vse_platne = True
    
            for i, usek in enumerate(self.useky, 1):
                try:
                    hodnoty = self.nacti_vzorky(
                        usek["editor"]
                    )
                    opakovani = self.nacti_opakovani(usek)
    
                    n = len(hodnoty)
                    frekvence = fs / n
                    ton, _ = nejblizsi_ton(frekvence)
                    delka = n * opakovani / fs
    
                    celkem_vzorku += n * opakovani
    
                    self.tabulka_useku.insert(
                        "",
                        "end",
                        iid=str(i),
                        values=(
                            i,
                            n,
                            f"{frekvence:.2f}",
                            ton,
                            f"{delka:.3f}"
                        )
                    )
    
                except ValueError:
                    vse_platne = False
    
                    self.tabulka_useku.insert(
                        "",
                        "end",
                        iid=str(i),
                        values=(i, "Chyba", "—", "—", "—")
                    )
    
            if vse_platne:
                celkova_delka = (
                    celkem_vzorku * opakovani_vsech / fs
                )
    
                self.info_skladby.configure(
                    text=(
                        f"Celková délka skladby: "
                        f"{celkova_delka:.3f} s "
                        f"(opakování celé skladby: "
                        f"{opakovani_vsech}×)"
                    )
                )
            else:
                self.info_skladby.configure(
                    text="Některé úseky obsahují neplatné hodnoty."
                )
    
            self.info.configure(
                text=(
                    f"Počet úseků: {len(self.useky)} | "
                    f"Bitová hloubka: {self.bity.get()} bitů | "
                    f"Vzorkovací frekvence: {fs} Hz"
                )
            )
    
            if self.tabulka_useku.exists(predchozi):
                self.tabulka_useku.selection_set(predchozi)
            elif self.tabulka_useku.exists("1"):
                self.tabulka_useku.selection_set("1")
    
            self.zobraz_detail_useku()

    def zobraz_detail_useku(self, event=None):
            vyber = self.tabulka_useku.selection()
    
            if not vyber:
                self.detail_useku.configure(text="")
                return
    
            index = int(vyber[0]) - 1
    
            if index >= len(self.useky):
                return
    
            usek = self.useky[index]
    
            try:
                fs = self.nacti_fs()
                hodnoty = self.nacti_vzorky(
                    usek["editor"]
                )
                opakovani = self.nacti_opakovani(usek)
    
                n = len(hodnoty)
                frekvence = fs / n
                ton, odchylka = nejblizsi_ton(frekvence)
                delka = n * opakovani / fs
    
                self.detail_useku.configure(
                    text=(
                        f"Úsek {index + 1}: {n} vzorků, "
                        f"{frekvence:.2f} Hz, "
                        f"nejbližší tón {ton}, "
                        f"odchylka {odchylka:+.1f} centů, "
                        f"délka {delka:.3f} s."
                    )
                )
    
            except ValueError as e:
                self.detail_useku.configure(
                    text=f"Chyba: {e}"
                )

    def aktualizuj_binarni_kalkulacku(self):
            try:
                fs = self.nacti_fs()
                delka = self.nacti_delku()
    
                ton = self.vybrany_ton.get()
    
                if ton not in self.tony_midi:
                    raise ValueError(
                        "Vyber platný hudební tón."
                    )
    
                midi = self.tony_midi[ton]
                idealni = frekvence_tonu(midi)
    
                # Počet vzorků jedné periody
                n = max(1, round(fs / idealni))
    
                skutecna = fs / n
    
                odchylka = (
                    1200 * math.log2(skutecna / idealni)
                )
    
                # Opakování pro požadovanou délku
                opakovani = max(
                    1,
                    round(delka * fs / n)
                )
    
                skutecna_delka = opakovani * n / fs
    
                hloubka = self.bity.get()
                tvar = self.tvar_vlny.get()
    
                # Vytvoření jedné periody
                hodnoty = vytvor_vlnu(
                    n, hloubka, tvar
                )
    
                # Binární reprezentace všech vzorků
                binarni = [
                    format(hodnota, f"0{hloubka}b")
                    for hodnota in hodnoty
                ]
    
                zapis = " ".join(binarni)
    
                self.vysledek_tonu.configure(
                    text=(
                        f"Tón: {ton}\n"
                        f"Ideální frekvence: {idealni:.2f} Hz\n"
                        f"Výsledná frekvence: {skutecna:.2f} Hz\n"
                        f"Odchylka: {odchylka:+.1f} centů\n"
                        f"Počet vzorků v periodě: {n}\n"
                        f"Bitová hloubka: {hloubka} bitů\n"
                        f"Tvar vlny: {tvar}\n"
                        f"Skutečná délka: "
                        f"{skutecna_delka:.3f} s"
                    )
                )
    
                self.binarni_vystup.configure(
                    state="normal"
                )
                self.binarni_vystup.delete(
                    "1.0", "end"
                )
                self.binarni_vystup.insert(
                    "1.0", zapis
                )
                self.binarni_vystup.configure(
                    state="disabled"
                )
    
                self.info_opakovani.configure(
                    text=(
                        f"Počet opakování posloupnosti: "
                        f"{opakovani}×"
                    )
                )
    
            except ValueError as e:
                self.vysledek_tonu.configure(
                    text=str(e)
                )
    
                self.binarni_vystup.configure(
                    state="normal"
                )
                self.binarni_vystup.delete(
                    "1.0", "end"
                )
                self.binarni_vystup.configure(
                    state="disabled"
                )
    
                self.info_opakovani.configure(text="")

    def kopirovat_binarni_zapis(self):
            zapis = self.binarni_vystup.get(
                "1.0", "end"
            ).strip()
    
            if not zapis:
                messagebox.showwarning(
                    "Upozornění",
                    "Nejprve musí být vypočítán platný tón."
                )
                return
    
            self.root.clipboard_clear()
            self.root.clipboard_append(zapis)
            self.root.update()
