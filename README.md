# Glasbenik – projekt pri predmetu UVP na FMF
### Rešitev za glasbene navdušence brez denarja.
Glasbenik predvaja glasbo, ki jo najde na posnetkih [platforme youtube](https://www.youtube.com/). Predvaja samo glasbo, brez oglasov in filozofskih video vsebin. Prav tako gradi svojo bazo skladb in vam predlaga naslednji hit po njegovem izboru.

## Uporaba
Trenutno si lažem, da bo uporabniški vmesnik berljiv.

### Inštalacija
TODO: `setup.py` ali kaj podobnega, ki pripravi okolje.

Sicer pa potrebuješ:
* [modul pafy](https://pypi.org/project/pafy/)
* [modul vlc](https://pypi.org/project/python-vlc/)
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