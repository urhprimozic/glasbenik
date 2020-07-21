**Vsa sumljiva koda v projektu je zgolj naključje. Ustvarjalec z vsem srcem spoštuje [vse svete knjige](https://developers.google.com/youtube/terms/api-services-terms-of-service)!**
# Glasbenik – projekt pri predmetu UVP na FMF
Glasbenik je `python`ov `bottle` strežnik, ki išče in predvaja glasbo iz spletne platforme [youtube](https://www.youtube.com/).
## Inštalacija 
TODO
## Uporaba
### Iskanje
Iskalnik se nahaja v desnem zgornjem kotu. Če vam rezultati ne zadoščajo, jih lahko izpišete več (gumb **NALOŽI VEČ**) ali pa pobrskate po youtubu.

![Iskanje pesmi *Chuck Berry*](https://github.com/urhprimozic/glasbenik/blob/master/README_data/iskanje.png)

### Nalaganje pesmi
V tabeli z iskanjem se na desni strani nahaja gumb za nalaganje skladb na lokalni računalnik. ![gumb download](https://github.com/urhprimozic/glasbenik/blob/master/README_data/download.png)

### Zgodovina predvajanja
Na zavihtku **DOMOV** (zgoraj levo na orodni vrstici) se nam izriše zadnjih 50 skladb, ki smo jih poslušali. Seveda jih lahko tudi predvajamo.

![Zgodovina predvajanih pesmi](https://github.com/urhprimozic/glasbenik/blob/master/README_data/zgodovina.png)

### Predvajanje glasbe na strežniku (DEV - za hekerje)
Če se očitno spremenljivko nekje v kodi nastavi na `True`, se bo glasba predvajala na strežniku s pomočjo `vlc` in `pafy`.

### Predvajanje glasbe
Če kjerkoli pritisneš na naslovno sliko skladbe, se ta predvaja


## Izvedba
### Baza
Baza vsakega uporabnika je `json` seznam slovarjev s podatki (spletni naslov, id, kanal, naslov, dolžina in slika) o posamezni pesmi.

### Iskanje po bazi
`Seja.iskanje_po_bazi(self, geslo` iz naslovov, avtorjev in iskanega gesla počisti čudne znake in jih razdeli na besede, nato pa med seboj primerja posamezne besede. Za podobnost med besedama uporablja [Levenshteinovo razdaljo](https://en.wikipedia.org/wiki/Levenshtein_distance), implementirano z bottom-up DP.

### Iskanje po youtubu
`Seja.siaknje_po_youtubu(geslo)` uporablja knjižnico `youtube-search-python`, ki na silo pridobi podatke o rezultatih, nato pa rezultate doda v bazo in požene `Seja.iskanje_po_bazi(geslo)` po posodobljeni bazi.

### Nalaganje pesmi
Glasbenik pesem naloži na strežnik v(modul `pafy`), potem pa uporabnika pošlje na naloženo pesem. Pesmi na strežniku se brišejo ob vsakem iskanju.

### Izgled
Ves CSS je moj, večinoma povzet iz *w3schools*, osnovni design pa je klasičen (kot na drugih platformah z glasbo). Efekti (animacija med čakanjem) so spisani v JavaScriptu.

### Predvajanje na strežniku (DEV)
Le uporaba modulov `vlc` in `pafy`.

### Več uporabnikov
Piškotki, sistem deluje tudi ob resetu strežnika. Storitev nagaja, če jo večkrat odpreš v istem brskalniku (recimo v dveh različnih zavihtkih), saj je to isti piškotek, in to je uporabnikova napaka.

### Predvajanje glasbe
Trenunto: embled youtube predvajalnik.

**Problema**: [nagaja, če dostopaš do strežnika preko IP-ja.](https://stackoverflow.com/questions/51969269/embedded-youtube-video-doesnt-work-on-local-server) in na mobilnih napravah se med zaklepom glasba (verjetno? - nisem potstiral) ustavi.

Ostale možnosti:
1. Vsako pesem se najprej naloži na bazo, nato pa se jo od tam doda v HTML. Predvajalnik (gumbe) pa se napiše v javascriptu. **Problem**: Časovno in prostorsko požrešna rešitev. (skrbi me predvsem čas).
2. [Predvajanje iz youtuba s pomočjo JavaScripta](https://stackoverflow.com/questions/8690255/how-to-play-only-the-audio-of-a-youtube-video-using-html-5). **Še nisem potestiral**. 
3. Pafyjev stream s pomočjo kakšne knjižnice serviram spletni strani (recimo **pjamas**?). **Še nisem potestiral. Problem:** Veliko dela, ki ni več v pythonu. Na tem mestu bi se že bolj splačalo vse narediti v JavaScriptu.
4. Neka python scripta na uporabnikovem koncu, ki komunicira s strežnikom in predvaja glasbo. **Problem:** Počasno in absolutno grdo ter narobe in odpade na mobilnih napravah.

*Poleg tega vse rešitve razen (4) ne omogočajo, da navigacija po spletni strani ne bi prekinila glasbe. (grda rešitev bi bila, da si zapolnimo, kje smo končali s predvajanjem, vendar imaš potem vmes zamike). Lepa rešitev tega bi bila Javascript namesto Bottle, kar ni legalno. Res pa je, da bo uporabnik zelo verjetno ob predvajanju stran pustil pri miru, zato je ta pomanjkljivost irelevanta. * 



## Znane napake:
1. Kdaj pride do `BrokenPipeError` (ne obremeni uporabniške izkušnje)
2. Kakšni linki ne delajo, ali pa so posnetki na youtubu čudne narave (poskrbljeno, da se program ne sesuje)
3. *predvajanje s pomočjo embled youtube:* Če do strežnika dostopaš preko IP-ja namesto imena domene, ti youtube velikokrat [ne pusti emblad](https://stackoverflow.com/questions/51424578/embed-youtube-code-is-not-working-in-html). **(blazno omeji uporabniško izkušnjo)*

##TODO: (pa kodo je treba sčistit)
0. Dobro predvajanje glasbe!!
1. Prijava, najljubše pesmi, seznami predvajanja, naključna izbira
2. Nastavitve (če bo na voljo več različnih načinov za predvajanje glasbe)
3. Info o projektu
4. AWS strežnik
5. AI za sortiranje


.

.

.

old readme:
### Rešitev za glasbene navdušence brez denarja.
Glasbenik predvaja glasbo, ki jo najde na posnetkih [platforme youtube](https://www.youtube.com/). Predvaja samo glasbo, brez oglasov in filozofskih video vsebin. Prav tako gradi svojo bazo skladb in vam predlaga naslednji hit po njegovem izboru.

## Uporaba
Trenutno si lažem, da bo uporabniški vmesnik berljiv.

### Inštalacija
Enostavno vse, kar potrebujete naložite z:
```
pip3 install youtube-search-python
pip3 install pafy
pip3 install python-vlc
```   

TODO: `setup.py` ali kaj podobnega, ki pripravi okolje.

Sicer pa potrebuješ:
* [modul pafy](https://pypi.org/project/pafy/)
* [modul vlc](https://pypi.org/project/python-vlc/)
* [modul youtube-search-python](https://github.com/alexmercerind/youtube-search-python) - modul je še v izdelavi
* **bottle** (*bo verjetno že dodan*)

## Ideja
Na čase v svojem življenju čutim potrebo po specifični glasbi (politično nekorekten rap in death metal, ki ga poslušam na treningih mogoče ni najboljša glasbena izbira za babico, ki jo peljem po nakupih). Radio postaje imajo po večini preveč širok spekter žanrov in ponavljajoče skladbe za mojo rabo. Prav tako mi ne ustrezajo domače baze skladb, saj so premajhne in imam večen problem z dodajanjem novih vsebin. Vse moje želje sicer izpolnjeno novodobne aplikacije za predvajanje glasbe (Google Music, Spotify), ki pa so zaradi cene neugodne za ubogega študenta matematike.

Klasična rešitev je predvajanje glasbe iz youtuba, ki pa ima svoje težave.
1. Med posameznimi skladbami nas motijo dolgi oglasi.
2. Ker je youtubov algoritem prilagojen posnetkom, in ne glasbi, so njegovi glasbeni predlogi ponavljajoči, ne relevantni oziroma sploh niso skladbe, ampak učne ure igre Fortnite.
3. Youtubov vmesnik ni prilagojen predvajanju skladb.

Rešitev teh težav bi bil sistem, ki bi za glasbeno bazo jemal youtube, vendar imel izboljšane funkcije (1-3).

## Funkcije
Glavna funckija je predvajanje glasbe iz youtuba v živo. Za to bo uporabljal modula **pafy** in **vlc**, mogoče pa *celo s funckijami brskalnika since HTML5*

### Lokalna baza
Sistem bi gradil lokalno bazo skladb (le spletnih naslovov, brez dejanskih datotek), po kateri bi iskal hitreje in na kateri bi uporabljal bolše algoritme za predlaganje naslednje skladbe.

### Iskanje po celotni platformi youtube
Če iskane skladbe ne bi bilo v lokalni bazi, bi s pomočjo sortiranja youtubovih posnetkov glede na žanre, glasbenik iskal po youtubu.

### Algoritem predlaganja novih skladb
Glasbenik bo predlagal skladbe bolj efektivno kot youtubov algoritem.

## Nadgradnja – glasbenica
Isto kot **glasbenik**, vendar ima posluh. Umetna inteligenca, ki bi predlagala glasbo z upoštevanjem oblike skladbe. (To se da, recimo soundcloud zna.)