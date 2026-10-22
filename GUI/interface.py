from tkinter import ttk
from sequencer_gui import SekvencerMixin
from Logic.input_logic import VstupyMixin
from Logic.pcm import OUTPUT_RATE

class RozhraniMixin(SekvencerMixin, VstupyMixin):
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

        # Defaultní zvuk (Concerning hobbits)
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

        # -----------------------------------------------------------
        # Výběr bitové hloubky
        # -----------------------------------------------------------

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


        # -----------------------------------------------------------
        # Vzorkovací frekvence
        # -----------------------------------------------------------

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

        # -----------------------------------------------------------
        # Opakování skladby
        # -----------------------------------------------------------

        ttk.Entry(
            ramecek,
            textvariable=self.opakovani_vsech,
            width=10
        ).grid(row=0, column=5, padx=5)

        # -----------------------------------------------------------
        # Doplňková informace o výstupním formátu
        # -----------------------------------------------------------
        ttk.Label(
            ramecek,
            text="Výstupní WAV: mono, 16 bitů, 44 100 Hz"
        ).grid(
            row=1, column=0, columnspan=6,
            sticky="w", pady=(10, 0)
        )
