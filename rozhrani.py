
import math
import tkinter as tk
from tkinter import ttk, messagebox
from pcm import OUTPUT_RATE


class RozhraniMixin:

    def vytvor_gui(self):
        hlavni = ttk.Frame(self.root, padding=12)
        hlavni.pack(fill="both", expand=True)

        ttk.Label(
            hlavni,
            text="PCM sekvencer",
            font=("Arial", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            hlavni,
            text=(
                "Vytvářej zvuk z binárních PCM vzorků. "
                "Vpravo zjistíš, jak zapsat konkrétní hudební tón."
            )
        ).pack(anchor="w", pady=(4, 10))

        self.vytvor_nastaveni(hlavni)

        panely = ttk.PanedWindow(
            hlavni, orient="horizontal"
        )
        panely.pack(fill="both", expand=True, pady=(10, 0))

        levy = ttk.Frame(panely)
        pravy = ttk.Frame(panely)

        panely.add(levy, weight=3)
        panely.add(pravy, weight=2)

        self.vytvor_sekvencer(levy)
        self.vytvor_kalkulacku(pravy)

        self.pridej_usek(
            "10000000 10011010 10110011 11001010 11011110 11101110 11111001 11111110 11111110"
            " 11111001 11101110 11011110 11001010 10110011 10011010 10000000 01100101 01001100"
            " 00110101 00100001 00010001 00000110 00000001 00000001 00000110 00010001 00100001"
            " 00110101 01001100 01100101 ",
            "100"
        )

        self.pridej_usek(
            "10000000 10011101 10111001 11010001 11100110 11110101 11111101 11111111 11111010"
            " 11101110 11011100 11000110 10101011 10001110 01110001 01010100 00111001 00100011"
            " 00010001 00000101 00000000 00000010 00001010 00011001 00101110 01000110 01100010",
            "100"
        )

        self.pridej_usek(
            "10000000 10100000 10111111 11011010 11101110 11111011 11111111 11111011 11101110 11011010"
            " 10111111 10100000 10000000 01011111 01000000 00100101 00010001 00000100 00000000"
            " 00000100 00010001 00100101 01000000 01011111",
            "200"
        )

        self.pridej_usek(
            "10000000 10100111 11001010 11100111 11111001 11111111 11111001 11100111 11001010 10100111"
            " 10000000 01011000 00110101 00011000 00000110 00000000 00000110 00011000 00110101 01011000",
            "200"
        )

        self.pridej_usek(
            "10000000 10100000 10111111 11011010 11101110 11111011 11111111 11111011 11101110 11011010"
            " 10111111 10100000 10000000 01011111 01000000 00100101 00010001 00000100 00000000"
            " 00000100 00010001 00100101 01000000 01011111",
            "200"
        )

        self.pridej_usek(
            "10000000 10011101 10111001 11010001 11100110 11110101 11111101 11111111 11111010"
            " 11101110 11011100 11000110 10101011 10001110 01110001 01010100 00111001 00100011"
            " 00010001 00000101 00000000 00000010 00001010 00011001 00101110 01000110 01100010",
            "200"
        )

        self.pridej_usek(
            "10000000 10011010 10110011 11001010 11011110 11101110 11111001 11111110 11111110"
            " 11111001 11101110 11011110 11001010 10110011 10011010 10000000 01100101 01001100"
            " 00110101 00100001 00010001 00000110 00000001 00000001 00000110 00010001 00100001"
            " 00110101 01001100 01100101 ",
            "200"
        )


    def vytvor_nastaveni(self, rodic):
        ramecek = ttk.LabelFrame(
            rodic, text="Společná nastavení", padding=10
        )
        ramecek.pack(fill="x")

        ttk.Label(
            ramecek, text="Bitová hloubka:"
        ).grid(row=0, column=0, padx=5, sticky="w")

        ttk.Combobox(
            ramecek,
            textvariable=self.bity,
            values=[1, 2, 3, 4, 8, 16],
            state="readonly",
            width=7
        ).grid(row=0, column=1, padx=5)

        ttk.Label(
            ramecek, text="Vzorkovací frekvence:"
        ).grid(row=0, column=2, padx=(20, 5))

        ttk.Spinbox(
            ramecek,
            from_=1,
            to=OUTPUT_RATE,
            textvariable=self.frekvence,
            width=12
        ).grid(row=0, column=3, padx=5)

        ttk.Label(
            ramecek, text="Opakování celé skladby:"
        ).grid(row=0, column=4, padx=(20, 5))

        ttk.Entry(
            ramecek,
            textvariable=self.opakovani_vsech,
            width=10
        ).grid(row=0, column=5, padx=5)

        ttk.Label(
            ramecek,
            text="Výstupní WAV: mono, 16 bitů, 44 100 Hz"
        ).grid(
            row=1, column=0, columnspan=6,
            sticky="w", pady=(10, 0)
        )

    def vytvor_sekvencer(self, rodic):
        ttk.Label(
            rodic,
            text="Zvukové úseky",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(5, 8))

        oblast = ttk.Frame(rodic)
        oblast.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            oblast, highlightthickness=0
        )
        self.canvas.pack(
            side="left", fill="both", expand=True
        )

        scrollbar = ttk.Scrollbar(
            oblast,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.kontejner = ttk.Frame(self.canvas)

        self.okno = self.canvas.create_window(
            (0, 0),
            window=self.kontejner,
            anchor="nw"
        )

        self.kontejner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(
                self.okno, width=e.width
            )
        )

        tlacitka = ttk.Frame(rodic)
        tlacitka.pack(fill="x", pady=10)

        ttk.Button(
            tlacitka,
            text="+ Přidat úsek",
            command=self.pridej_usek
        ).pack(side="left", padx=3)

        ttk.Button(
            tlacitka,
            text="▶ Přehrát",
            command=self.prehrat
        ).pack(side="left", padx=3)

        ttk.Button(
            tlacitka,
            text="■ Zastavit",
            command=self.zastavit
        ).pack(side="left", padx=3)

        ttk.Button(
            tlacitka,
            text="Uložit WAV",
            command=self.ulozit
        ).pack(side="left", padx=3)

        self.info = ttk.Label(
            rodic, text="", wraplength=650
        )
        self.info.pack(anchor="w", pady=5)

    def pridej_usek(self, text=None, opakovani="1"):
        cislo = len(self.useky) + 1

        ramecek = ttk.LabelFrame(
            self.kontejner,
            text=f"Úsek {cislo}",
            padding=10
        )
        ramecek.pack(fill="x", pady=5)

        ttk.Label(
            ramecek, text="Binární vzorky:"
        ).pack(anchor="w")

        editor = tk.Text(
            ramecek,
            height=4,
            font=("Consolas", 11),
            wrap="word"
        )
        editor.pack(fill="x", pady=5)

        if text is None:
            text = "0" * self.bity.get()

        editor.insert("1.0", text)

        dolni = ttk.Frame(ramecek)
        dolni.pack(fill="x")

        ttk.Label(
            dolni, text="Počet opakování:"
        ).pack(side="left")

        pocet = tk.StringVar(value=str(opakovani))

        ttk.Entry(
            dolni,
            textvariable=pocet,
            width=12
        ).pack(side="left", padx=8)

        usek = {
            "ramecek": ramecek,
            "editor": editor,
            "opakovani": pocet
        }

        self.useky.append(usek)

        ttk.Button(
            dolni,
            text="Odstranit úsek",
            command=lambda: self.odstran_usek(usek)
        ).pack(side="right")

        editor.bind(
            "<<Modified>>", self.zmena_textu
        )
        editor.edit_modified(False)

        pocet.trace_add(
            "write", self.naplanovat_aktualizaci
        )

        self.naplanovat_aktualizaci()

    def odstran_usek(self, usek):
        if len(self.useky) <= 1:
            messagebox.showwarning(
                "Upozornění",
                "Musí zůstat alespoň jeden úsek."
            )
            return

        usek["ramecek"].destroy()
        self.useky.remove(usek)

        for i, polozka in enumerate(self.useky, 1):
            polozka["ramecek"].configure(
                text=f"Úsek {i}"
            )

        self.naplanovat_aktualizaci()

    def zmena_textu(self, event):
        editor = event.widget

        if editor.edit_modified():
            editor.edit_modified(False)
            self.naplanovat_aktualizaci()

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
