
# PCM sekvencer – binární hudba

Výuková aplikace v Pythonu pro tvorbu, přehrávání, analýzu a export digitálního zvuku pomocí binárně zapsaných PCM vzorků.

Program názorně ukazuje principy **vzorkování, kvantování, bitové hloubky, vzorkovací frekvence a digitální reprezentace zvuku**. Uživatel může přímo upravovat binární hodnoty jednotlivých vzorků a sledovat jejich vliv na výsledný zvuk a grafický průběh.

## 1. Požadavky a spuštění

- Python 3
- Windows pro přehrávání pomocí modulu `winsound`

Program nevyžaduje žádné externí knihovny instalované přes `pip`.

Spuštění z kořenové složky projektu:

```bash
python main.py
```

Na jiných operačních systémech může fungovat tvorba grafů a export souborů, přehrávání přes `winsound` je však dostupné pouze ve Windows.

## 2. Struktura projektu

```text
Audio_01_create/
├── main.py
├── README.md
├── GUI/
│   ├── __init__.py
│   ├── interface.py
│   ├── sequencer_gui.py
│   ├── waveform_gui.py
│   └── calculator.py
├── Logic/
│   ├── __init__.py
│   ├── input_logic.py
│   ├── calculator_logic.py
│   └── pcm.py
└── Audio/
    ├── __init__.py
    ├── sound.py
    └── export_txt.py
```

### Popis modulů

| Soubor | Funkce |
|---|---|
| `main.py` | Spuštění aplikace, inicializace a propojení jejích částí |
| `GUI/interface.py` | Hlavní rozhraní, společná nastavení a výchozí skladba |
| `GUI/sequencer_gui.py` | Správa zvukových úseků, binárních editorů a ovládacích tlačítek |
| `GUI/waveform_gui.py` | Vykreslování průběhu zvuku, kvantizační sítě a ovládání grafů |
| `GUI/calculator.py` | Kalkulačka tónů a živá analýza zvukových úseků |
| `Logic/input_logic.py` | Kontrola a dekódování zadaných hodnot |
| `Logic/calculator_logic.py` | Výpočty frekvencí, délek a binárních zápisů tónů |
| `Logic/pcm.py` | Základní konstanty, hudební tóny a generování průběhů |
| `Audio/sound.py` | Přehrávání a export zvuku do WAV |
| `Audio/export_txt.py` | Export nekomprimovaného WAV souboru jako textové posloupnosti bitů |

## 3. Ovládání programu

### Společná nastavení

V horní části aplikace lze nastavit:

- **Bitovou hloubku:** 1, 2, 3, 4, 8 nebo 16 bitů.
- **Vzorkovací frekvenci:** počet vzorků za sekundu (1–44 100 Hz).
- **Opakování celé skladby:** kolikrát se přehraje posloupnost všech zvukových úseků.

Změna bitové hloubky sama o sobě nepřevádí ani nepřeskupuje již zapsané binární vzorky. Pokud jejich délka neodpovídá novému nastavení, program oznámí neplatný zápis.

### Zvukové úseky

Každý úsek obsahuje:

1. Editor binárních vzorků.
2. Počet opakování posloupnosti.
3. Graf průběhu zvuku.
4. Tlačítko pro odstranění úseku.

Nový úsek lze přidat tlačítkem **+ Přidat úsek**.

Binární vzorky se zapisují jako skupiny nul a jedniček oddělené mezerami nebo odřádkováním.

Příklad pro 8bitovou hloubku:

```text
00000000 01000000 10000000 11000000 11111111
```

Každá osmibitová skupina představuje jeden vzorek.

### Přehrávání

Tlačítko **Přehrát** vytvoří výsledný zvuk ze všech úseků a přehraje jej.

Tlačítko **Zastavit** ukončí přehrávání.

Výsledný zvuk vzniká postupným spojením úseků, jejich opakováním a následným opakováním celé skladby.

## 4. Grafy zvukových úseků

Vedle každého editoru se nachází graf odpovídající zadaným PCM vzorkům.

Graf zobrazuje:

- **Modrou čáru:** spojnice jednotlivých vzorků.
- **Oranžovou čáru:** schodovitý průběh PCM.
- **Svislé čáry:** hranice vzorkovacích intervalů.
- **Vodorovné čáry:** kvantizační hladiny.

Graf standardně zobrazuje maximálně prvních **60 vzorků**.

### Jednotné měřítko

Všechny grafy používají při 100% přiblížení stejnou vodorovnou vzdálenost mezi vzorky.

Díky tomu lze porovnávat různé frekvence. Například tón A4 má při stejné vzorkovací frekvenci kratší periodu než C3.

### Přiblížení

Grafy podporují:

- `+` – přiblížení os X a Y.
- `−` – oddálení.
- `100 %` – obnovení výchozího měřítka.
- Vodorovný a svislý posuvník.

Při najetí myší na graf lze zobrazit binární zápis vzorku, jeho desetinnou hodnotu a amplitudu.

## 5. Vzorkování a kvantování

### Vzorkovací frekvence

Vzorkovací frekvence určuje, kolik vzorků připadá na jednu sekundu zvuku.

Například při frekvenci 20 000 Hz představuje jeden vzorek časový interval:

```text
1 / 20 000 = 0,00005 s
```

Pokud jeden úsek představuje právě jednu periodu a obsahuje 40 vzorků, výsledná frekvence tónu je:

```text
20 000 / 40 = 500 Hz
```

Program při analýze předpokládá, že zadaná posloupnost představuje jednu periodu tónu.

### Bitová hloubka

Bitová hloubka určuje počet možných kvantizačních hladin:

```text
Počet hladin = 2 ^ bitová_hloubka
```

| Bitová hloubka | Počet hladin |
|---|---:|
| 1 bit | 2 |
| 2 bity | 4 |
| 3 bity | 8 |
| 4 bity | 16 |
| 8 bitů | 256 |
| 16 bitů | 65 536 |

Čím vyšší je bitová hloubka, tím jemněji lze reprezentovat amplitudu zvuku.

### Převod binárního vzorku na amplitudu

Program používá neznaménkové hodnoty vzorků a převádí je na amplitudu v intervalu od −1 do +1.

```python
maximum = 2 ** hloubka - 1
amplituda = 2 * cislo / maximum - 1
```

Pro 8bitový zápis například platí:

| Binární zápis | Desetinná hodnota | Amplituda |
|---|---:|---:|
| `00000000` | 0 | −1 |
| `01000000` | 64 | přibližně −0,498 |
| `10000000` | 128 | přibližně +0,004 |
| `11000000` | 192 | přibližně +0,506 |
| `11111111` | 255 | +1 |

U sudého počtu kvantizačních hladin není nulová amplituda reprezentována přesně.

## 6. Kalkulačka hudebních tónů

Kalkulačka umožňuje:

1. Vybrat hudební tón.
2. Zvolit tvar vlny.
3. Nastavit požadovanou délku.
4. Vypočítat binární zápis jedné periody.
5. Zkopírovat zápis do zvukového úseku.

Podporované tvary vln:

- Sinusová
- Obdélníková
- Trojúhelníková
- Pilová

Program vypočítá také skutečnou frekvenci, odchylku od ideálního tónu v centech, počet vzorků a doporučený počet opakování.

Protože perioda obsahuje celočíselný počet vzorků, výsledná frekvence nemusí přesně odpovídat ideální frekvenci hudebního tónu.

## 7. Živá analýza

Program průběžně analyzuje jednotlivé zvukové úseky.

Zobrazuje:

- Počet vzorků v úseku.
- Frekvenci odpovídající jedné periodě.
- Nejbližší hudební tón.
- Délku úseku.
- Celkovou délku skladby.

Při změně vzorků, frekvence nebo počtu opakování se výsledky automaticky aktualizují.

## 8. Export WAV

Tlačítko **Uložit WAV** vytvoří zvukový soubor ve formátu WAV.

Parametry výstupu:

| Parametr | Hodnota |
|---|---|
| Formát | Nekomprimované PCM |
| Kanály | 1 (mono) |
| Bitová hloubka | 16 bitů |
| Vzorkovací frekvence | 44 100 Hz |
| Maximální délka | 120 sekund |

Zadané vzorky jsou před exportem převedeny na 16bitové PCM a na výstupní vzorkovací frekvenci.

Převzorkování využívá metodu **zero-order hold**, při níž se opakuje hodnota nejbližšího předchozího vstupního vzorku.

Výstupní parametry WAV jsou pevné a nemusí odpovídat bitové hloubce ani vzorkovací frekvenci zvolené v editoru.

## 9. Export TXT

Tlačítko **Export TXT** vytvoří textový soubor obsahující posloupnost nul a jedniček odpovídající celému exportovanému WAV souboru.

Export zahrnuje:

- Hlavičku WAV.
- Zvuková data všech úseků.
- Opakování jednotlivých úseků.
- Opakování celé skladby.

Každý bajt výsledného souboru je převeden na osm znaků `0` nebo `1`.

Výsledkem je souvislý bitový zápis bez mezer a odřádkování.

Například začátek souboru WAV odpovídá znakům `RIFF`, které mají následující binární reprezentaci:

```text
01010010010010010100011001000110
```

TXT obsahuje skutečné pořadí bajtů exportovaného WAV souboru. Jde o textovou reprezentaci dat, nikoliv o fyzikální simulaci přenosového signálu.

Protože se každý bit zapisuje jako samostatný textový znak, je TXT přibližně osmkrát větší než odpovídající WAV soubor.

## 10. Hlavička WAV

Aplikace obsahuje výukové zobrazení vybraných parametrů WAV v binární podobě.

Vícebajtová číselná pole WAV se ukládají v pořadí **little-endian**, tedy od nejméně významného bajtu.

Například vzorkovací frekvence 20 000 Hz je reprezentována čtyřmi bajty:

```text
00100000 01001110 00000000 00000000
```

Bitová hloubka 8 bitů je ve dvoubajtovém poli reprezentována takto:

```text
00001000 00000000
```

Zobrazení těchto parametrů je výukové. Skutečně exportovaný WAV má vždy 16 bitů a 44 100 Hz.

## 11. Výchozí skladba

Program po spuštění načítá ukázkovou melodii inspirovanou skladbou **Concerning Hobbits**.

Melodie je složena ze sedmi zvukových úseků s přednastavenými binárními hodnotami a počty opakování.

Uživatel může všechny hodnoty upravovat, přidávat další úseky nebo původní úseky odstraňovat.

## 12. Omezení programu

- Frekvence vypočítaná z délky posloupnosti předpokládá jednu periodu v úseku.
- Program neprovádí automatické překvantování při změně bitové hloubky.
- Výstupní WAV má pevně nastavené parametry 16 bitů a 44 100 Hz.
- Převzorkování metodou zero-order hold není určeno pro vysoce kvalitní zvukové zpracování.
- Graf zobrazuje maximálně prvních 60 vzorků každého úseku.
- Přehrávání pomocí `winsound` funguje pouze ve Windows.
- TXT export představuje binární zápis WAV souboru, nikoliv skutečný elektrický nebo rádiový signál.

## 13. Výukové využití

Program je určen zejména pro výuku informatiky a digitální reprezentace informace.

Možné úkoly pro studenty:

1. Porovnat binární zápisy stejného tónu při různých bitových hloubkách.
2. Pozorovat změny kvantizační sítě.
3. Zjistit, jak počet vzorků v periodě ovlivňuje frekvenci tónu.
4. Porovnat průběhy tónů C3, C4 a A4.
5. Vytvořit jednoduchou melodii z binárních vzorků.
6. Porovnat sinusovou, obdélníkovou, trojúhelníkovou a pilovou vlnu.
7. Analyzovat hlavičku WAV v binární podobě.
8. Porovnat velikost souborů WAV a TXT.
9. Vysvětlit rozdíl mezi vzorkovací frekvencí a bitovou hloubkou.
10. Zkoumat vliv změny PCM hodnot na amplitudu a výsledný zvuk.

---

**Technologie:** Python, Tkinter, PCM, WAV

**Účel:** Výuková demonstrace digitálního zpracování a binárního kódování zvuku.
