**Vsa sumljiva koda v projektu je zgolj naključje. Ustvarjalec z vsem srcem spoštuje [vse svete knjige](https://developers.google.com/youtube/terms/api-services-terms-of-service)!**
# Glasbenik – projekt pri predmetu UVP na FMF
Glasbenik je `python`ov `bottle` strežnik, ki išče in predvaja glasbo iz spletne platforme [youtube](https://www.youtube.com/).

## Inštalacija
Glasbenik temelji na treh zunanjih modulih, ki jih potrebuje za [iskanje po youtubu](https://github.com/alexmercerind/youtube-search-python), [komunikacijo z youtubom](https://pypi.org/project/pafy/) in [predvajanje glasbe na lokalnem strežniku](https://pypi.org/project/python-vlc/).

Module preprosto inštalirate s spodnjimi ukazi:
```
pip3 install youtube-search-python
pip3 install pafy
pip3 install python-vlc
``` 
## Uporaba
Strežnik se nahaja v datoteki `spletni_vmesnik.py`, zaženemo pa ga lahko z ukazom `python3 -i spletni_vmesnik.py`.

### Iskanje
Iskalnik se nahaja v desnem zgornjem kotu. Če vam rezultati ne zadoščajo, jih lahko izpišete več (gumb **NALOŽI VEČ**) ali pa pobrskate po youtubu.

![Iskanje pesmi Chuck Berry](https://github.com/urhprimozic/glasbenik/blob/master/README_data/iskanje.png)

### Nalaganje pesmi
V tabeli z iskanjem se na desni strani nahaja gumb za nalaganje skladb na lokalni računalnik. ![gumb download](https://github.com/urhprimozic/glasbenik/blob/master/README_data/download.png)

### Zgodovina predvajanja
Na zavihtku **DOMOV** (zgoraj levo na orodni vrstici) se nam izriše zadnjih 50 skladb, ki smo jih poslušali. Seveda jih lahko tudi predvajamo.

![Zgodovina predvajanih pesmi](https://github.com/urhprimozic/glasbenik/blob/master/README_data/zgodovina.png)


### Predvajanje glasbe
Če kjerkoli pritisneš na naslovno sliko skladbe, se ta predvaja


## Izvedba
### Baza
Baza vsakega uporabnika je `json` seznam slovarjev s podatki (spletni naslov, id, kanal, naslov, dolžina in slika) o posamezni pesmi.

### Iskanje po bazi
Program iz naslovov, avtorjev in iskanega gesla počisti čudne znake in jih razdeli na besede, nato pa med seboj primerja posamezne besede. Za podobnost med besedama uporablja [Levenshteinovo razdaljo](https://en.wikipedia.org/wiki/Levenshtein_distance), implementirano z bottom-up DP.

### Iskanje po youtubu
Program uporablja knjižnico `youtube-search-python`, ki na silo pridobi podatke o rezultatih, nato pa rezultate doda v bazo.

### Nalaganje pesmi
Glasbenik pesem naloži na strežnik v(modul `pafy`), potem pa uporabnika pošlje na naloženo pesem. Pesmi na strežniku se brišejo ob vsakem iskanju.

### Dizajn
Ves CSS je moj, večinoma povzet iz *w3schools*, osnovni dizajn pa je klasičen (kot na drugih platformah z glasbo). Efekti (animacija med čakanjem) so spisani v JavaScriptu.



### Več uporabnikov
Piškotki, sistem deluje tudi ob resetu strežnika. Storitev nagaja, če jo večkrat odpreš v istem brskalniku (recimo v dveh različnih zavihtkih), saj je to isti piškotek, in to je uporabnikova napaka.

### Predvajanje glasbe
Glasba se predvaja s pomočjo embed youtube predvajalnika.

### Predvajanje glasbe na strežniku (DEV - za hekerje)
Če se očitno spremenljivko nekje v kodi nastavi na `True`, se bo glasba predvajala na strežniku s pomočjo `vlc` in `pafy`.