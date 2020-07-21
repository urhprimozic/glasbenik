**Vsa sumljiva koda v projektu je zgolj naključje. Ustvarjalec z vsem srcem spoštuje [vse svete knjige](https://developers.google.com/youtube/terms/api-services-terms-of-service)!**
# Glasbenik – projekt pri predmetu UVP na FMF

## Uporaba
### Iskanje
Iskalnik se nahaja v desnem zgornjem kotu. Če vam rezultati ne zadoščajo, jih lahko izpišete več (gumb **NALOŽI VEČ**) ali pa pobrskate po youtubu.

![Iskanje pesmi *Chuck Berry*](https://github.com/urhprimozic/glasbenik/blob/master/README_data/iskanje.png)

### Zgodovina predvajanja
Na zavihtku **DOMOV** (zgoraj levo na orodni vrstici) se nam izriše zadnjih 50 skladb, ki smo jih poslušali. Seveda jih lahko tudi predvajamo.

![Zgodovina predvajanih pesmi](https://github.com/urhprimozic/glasbenik/blob/master/README_data/zgodovina.png)

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