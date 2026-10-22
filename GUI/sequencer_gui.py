import tkinter as tk
from tkinter import ttk, messagebox
from GUI.waveform_gui import WaveformMixin


class SekvencerMixin(WaveformMixin):
    def vytvor_sekvencer(self, rodic):
        ttk.Label(
            rodic,
            text="Zvukové úseky",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(5, 8))

        # -----------------------------------------------------------
        # Oblast pro vkládání kontejnerů
        # -----------------------------------------------------------
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

        # -----------------------------------------------------------
        # Vložení kontejneru do Canvas
        # -----------------------------------------------------------
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

        # -----------------------------------------------------------
        # Ovládací tlačítka
        # -----------------------------------------------------------
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

    # -----------------------------------------------------------
    # Přidání úseku
    # -----------------------------------------------------------
    def pridej_usek(self, text=None, opakovani="1"):
        cislo = len(self.useky) + 1

        ramecek = ttk.LabelFrame(
            self.kontejner,
            text=f"Úsek {cislo}",
            padding=10
        )
        ramecek.pack(fill="x", pady=5)

        # Editor vlevo a graf vlny vpravo v jednom úseku.
        obsah = ttk.Frame(ramecek)
        obsah.pack(fill="both", expand=True)
        leva_cast = ttk.Frame(obsah)
        leva_cast.pack(side="left", fill="both", expand=True)

        ttk.Label(
            leva_cast, text="Binární vzorky:"
        ).pack(anchor="w")

        editor = tk.Text(
            leva_cast,
            height=4,
            width=35,
            font=("Consolas", 8),
            wrap="word"
        )
        editor.pack(fill="both", expand=True, pady=5)

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

        # -----------------------------------------------------------
        # Uložení úseku do datové struktury
        # -----------------------------------------------------------
        usek = {
            "ramecek": ramecek,
            "editor": editor,
            "opakovani": pocet
        }

        self.useky.append(usek)
        self.vytvor_graf_useku(obsah, usek)
        self.aktualizuj_graf_useku(usek)

        ttk.Button(
            dolni,
            text="Odstranit úsek",
            command=lambda: self.odstran_usek(usek)
        ).pack(side="right")

        # -----------------------------------------------------------
        # Sledování změn
        # -----------------------------------------------------------
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

    # -----------------------------------------------------------
    # Reakce na změnu textu
    # -----------------------------------------------------------
    def zmena_textu(self, event):
        editor = event.widget

        if editor.edit_modified():
            editor.edit_modified(False)
            self.naplanovat_aktualizaci()
