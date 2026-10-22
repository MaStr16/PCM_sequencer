import tkinter as tk
from GUI.interface import RozhraniMixin
from GUI.calculator import KalkulackaMixin
from Audio.sound import ZvukMixin


class PCMSequencer(RozhraniMixin, KalkulackaMixin, ZvukMixin):
    def __init__(self, root):
        self.root = root
        self.root.title("PCM sekvencer – binární hudba")
        self.root.geometry("1500x850")
        self.root.minsize(1050, 620)
    
        self.bity = tk.IntVar(value=8)
        self.frekvence = tk.StringVar(value="21000")
        self.opakovani_vsech = tk.StringVar(value="1")
    
        self.delka_tonu = tk.StringVar(value="0.5")
        self.tvar_vlny = tk.StringVar(value="Sinusová")
    
        self.useky = []
        self._aktualizace_id = None

        self.vytvor_gui()
    
        for promenna in (
            self.frekvence,
            self.opakovani_vsech,
            self.delka_tonu,
            self.tvar_vlny
        ):
            promenna.trace_add(
                "write", self.naplanovat_aktualizaci
            )
    
        self.root.protocol("WM_DELETE_WINDOW", self.zavrit)
        self.aktualizuj_vse()


if __name__ == "__main__":
    root = tk.Tk()
    app = PCMSequencer(root)
    root.mainloop()
