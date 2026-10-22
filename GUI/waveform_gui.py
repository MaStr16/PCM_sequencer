"""Prvních 60 PCM vzorků ve společném měřítku pro všechny úseky."""
import tkinter as tk
from tkinter import ttk


MAX_ZOBRAZENYCH_VZORKU = 60
SIRKA_VZORKU = 12  # Stejné měřítko pro všechny úseky při 100 %


class WaveformMixin:
    def vytvor_graf_useku(self, rodic, usek):
        """Vytvoří graf, společné přiblížení obou os a posuvníky."""
        panel = ttk.LabelFrame(rodic, text="Vlna / PCM", padding=5)
        panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

        ovladani = ttk.Frame(panel)
        ovladani.pack(fill="x", pady=(0, 3))
        ttk.Button(ovladani, text="−", width=3,
                   command=lambda u=usek: self.zmen_priblizeni_grafu(u, 1 / 1.5)).pack(side="left")
        ttk.Button(ovladani, text="+", width=3,
                   command=lambda u=usek: self.zmen_priblizeni_grafu(u, 1.5)).pack(side="left", padx=(3, 0))
        ttk.Button(ovladani, text="100 %", width=7,
                   command=lambda u=usek: self.reset_priblizeni_grafu(u)).pack(side="left", padx=(5, 0))
        priblizeni = ttk.Label(ovladani, text="100 %", font=("Arial", 8))
        priblizeni.pack(side="left", padx=(7, 0))

        oblast = ttk.Frame(panel)
        oblast.pack(fill="both", expand=True)
        graf = tk.Canvas(oblast, height=125, bg="white", highlightthickness=1,
                         highlightbackground="#c5c5c5")
        graf.grid(row=0, column=0, sticky="nsew")
        svisly = ttk.Scrollbar(oblast, orient="vertical", command=graf.yview)
        svisly.grid(row=0, column=1, sticky="ns")
        vodorovny = ttk.Scrollbar(oblast, orient="horizontal", command=graf.xview)
        vodorovny.grid(row=1, column=0, sticky="ew")
        oblast.columnconfigure(0, weight=1)
        oblast.rowconfigure(0, weight=1)
        graf.configure(xscrollcommand=vodorovny.set, yscrollcommand=svisly.set)

        popisek = ttk.Label(panel, text="", font=("Arial", 8))
        popisek.pack(anchor="w", pady=(3, 0))

        usek["graf"] = graf
        usek["graf_popisek"] = popisek
        usek["graf_zoom"] = 1.0
        usek["graf_zoom_popisek"] = priblizeni
        graf.bind("<Configure>", lambda _event, u=usek: self.aktualizuj_graf_useku(u))
        graf.bind("<Motion>", lambda event, u=usek: self.popis_vzorku(event, u))
        graf.bind("<Leave>", lambda _event, u=usek: self.zakladni_popis_grafu(u))

    def zmen_priblizeni_grafu(self, usek, nasobek):
        """Přiblíží obě osy a zachová přibližně střed aktuálního výřezu."""
        graf = usek.get("graf")
        if graf is None or not graf.winfo_exists():
            return
        puvodni = usek.get("graf_zoom", 1.0)
        nove = max(1.0, min(16.0, puvodni * nasobek))
        if abs(nove - puvodni) < 0.0001:
            return
        w = max(graf.winfo_width(), 150)
        h = max(graf.winfo_height(), 90)
        # Střed viditelné oblasti v souřadnicích původního grafu.
        stred_x = (graf.canvasx(w / 2) - 28) / max(1, MAX_ZOBRAZENYCH_VZORKU * SIRKA_VZORKU * puvodni)
        stred_y = (graf.canvasy(h / 2) - h / 2) / puvodni
        usek["graf_zoom"] = nove
        self.aktualizuj_graf_useku(usek)
        sirka = max(w, 28 + MAX_ZOBRAZENYCH_VZORKU * SIRKA_VZORKU * nove + 10)
        vyska = max(h, (h - 33) * nove + 33)
        graf.xview_moveto(max(0.0, min(1.0, (28 + stred_x * MAX_ZOBRAZENYCH_VZORKU * SIRKA_VZORKU * nove - w / 2) / sirka)))
        graf.yview_moveto(max(0.0, min(1.0, (vyska / 2 + stred_y * nove - h / 2) / vyska)))

    def reset_priblizeni_grafu(self, usek):
        usek["graf_zoom"] = 1.0
        self.aktualizuj_graf_useku(usek)
        usek["graf"].xview_moveto(0)
        usek["graf"].yview_moveto(0)

    def zakladni_popis_grafu(self, usek):
        usek["graf_popisek"].configure(
            text=f"Modrá: vzorky | Oranžová: PCM | Kvantování: {2 ** self.bity.get()} hladin"
        )

    def popis_vzorku(self, event, usek):
        """Při najetí myší zobrazí kód vzorku i při přiblížení a posunutí."""
        try:
            skupiny = usek["editor"].get("1.0", "end").split()
            vzorky = self.nacti_vzorky(usek["editor"])[:MAX_ZOBRAZENYCH_VZORKU]
            graf = usek["graf"]
            w = max(graf.winfo_width(), 150)
            plot_w = MAX_ZOBRAZENYCH_VZORKU * SIRKA_VZORKU * usek.get("graf_zoom", 1.0)
            index = int((graf.canvasx(event.x) - 28) / plot_w * len(vzorky))
            if 0 <= index < len(vzorky):
                usek["graf_popisek"].configure(
                    text=f"Vzorek {index + 1}: {skupiny[index]} = {int(skupiny[index], 2)} "
                         f"| amplituda {vzorky[index]:+.3f} | hladina {int(skupiny[index], 2) + 1}/{2 ** self.bity.get()}"
                )
            else:
                self.zakladni_popis_grafu(usek)
        except (ValueError, tk.TclError, IndexError, ZeroDivisionError):
            pass

    def aktualizuj_grafy_useku(self):
        """Aktualizuje všechny grafy; volá se společně s analýzou."""
        for usek in self.useky:
            self.aktualizuj_graf_useku(usek)

    def aktualizuj_graf_useku(self, usek):
        """Zobrazí kvantované PCM schody a spojnice vzorků s přiblížením X/Y."""
        graf = usek.get("graf")
        if graf is None or not graf.winfo_exists():
            return
        graf.delete("all")
        w = max(graf.winfo_width(), 150)
        h = max(graf.winfo_height(), 90)
        left, right, top, bottom = 28, 10, 10, 23
        zoom = usek.get("graf_zoom", 1.0)
        plot_w = MAX_ZOBRAZENYCH_VZORKU * SIRKA_VZORKU * zoom
        plot_h = max(1, (h - top - bottom) * zoom)
        # Při zoomu zůstává nula amplitudy uprostřed rozšířené svislé oblasti.
        vyska = max(h, plot_h + top + bottom)
        mid = vyska / 2
        y_top = mid - plot_h / 2
        y_bottom = mid + plot_h / 2
        konec = left + plot_w
        graf.configure(scrollregion=(0, 0, konec + right, vyska))
        usek["graf_zoom_popisek"].configure(text=f"{zoom * 100:.0f} % (X/Y)")

        graf.create_line(left, mid, konec, mid, fill="#a0a0a0", dash=(3, 3))
        graf.create_line(left, y_top, left, y_bottom, fill="#777777")
        graf.create_text(left - 4, mid, text="0", anchor="e", font=("Arial", 7))

        try:
            vsechny_vzorky = self.nacti_vzorky(usek["editor"])
            vzorky = vsechny_vzorky[:MAX_ZOBRAZENYCH_VZORKU]
        except (ValueError, tk.TclError) as exc:
            usek["graf_popisek"].configure(text=f"Neplatné vzorky: {exc}")
            graf.create_text(left + plot_w / 2, mid, text="Oprav binární zápis", fill="#a33")
            return
        if not vzorky:
            return
        n = len(vzorky)
        dx = SIRKA_VZORKU * zoom

        # Kvantizační síť: každá vodorovná linka odpovídá dovolené
        # amplitudě dané bitovou hloubkou. Při 8/16 bitech je hladin
        # příliš mnoho, proto se pro přehlednost vykreslí jen část.
        hloubka = self.bity.get()
        pocet_hladin = 2 ** hloubka
        # Maximálně cca 45 viditelných linek (jemné síto při vyšší hloubce).
        krok = max(1, (pocet_hladin - 1 + 43) // 44)
        hladiny = list(range(0, pocet_hladin, krok))
        if hladiny[-1] != pocet_hladin - 1:
            hladiny.append(pocet_hladin - 1)
        for hodnota in hladiny:
            amplituda = 2 * hodnota / (pocet_hladin - 1) - 1
            yy = mid - amplituda * plot_h / 2
            graf.create_line(left, yy, konec, yy, fill="#e8d9bf", width=1)
            # U malého počtu hladin popíšeme všechny, jinak jen krajní.
            if pocet_hladin <= 16 or hodnota in (0, pocet_hladin - 1):
                graf.create_text(left - 4, yy, text=str(hodnota), anchor="e",
                                 fill="#a26a20", font=("Arial", 7))

        # Pevná šířka vzorku: C3 i A4 mají stejnou časovou osu.
        # Svislé čáry oddělují 60 stejných vzorkovacích intervalů.
        for i in range(MAX_ZOBRAZENYCH_VZORKU + 1):
            x = left + i * dx
            graf.create_line(x, y_top, x, y_bottom, fill="#dedede", width=1)

        def y(amplituda):
            return mid - amplituda * plot_h / 2

        schody = []
        for i, a in enumerate(vzorky):
            x0 = left + i * dx
            x1 = left + (i + 1) * dx
            if i == 0:
                schody.extend((x0, y(a)))
            else:
                schody.extend((x0, y(vzorky[i - 1]), x0, y(a)))
            schody.extend((x1, y(a)))
        graf.create_line(*schody, fill="#d47c18", width=2)

        if n > 1:
            body = []
            for i, a in enumerate(vzorky):
                body.extend((left + (i + 0.5) * dx, y(a)))
            graf.create_line(*body, fill="#1766b0", width=1.5)
        if dx >= 7:
            for i, a in enumerate(vzorky):
                x = left + (i + 0.5) * dx
                graf.create_oval(x - 2, y(a) - 2, x + 2, y(a) + 2,
                                 fill="#1766b0", outline="")
        graf.create_text(left, vyska - 8, text="0", anchor="w", font=("Arial", 7))
        popis_poctu = (f"Prvních {n} z {len(vsechny_vzorky)} vzorků"
                        if len(vsechny_vzorky) > n else f"{n} vzorků")
        graf.create_text(konec, vyska - 8, text=popis_poctu, anchor="e", font=("Arial", 7))
        self.zakladni_popis_grafu(usek)
