# le zadeve, povezane z grajenjem in iskanjem po bazi
import json
import pafy


def dodaj_url(url):
    '''Doda pesem, ki se nahaja na spletnem naslovu url, v bazo, če je tam še ni.'''
    posnetek = pafy.new(url)
    slovar = {
        "url": url,
        "avtor": posnetek.author,
        # googlu to ni všeč
        # "kategorija" : posnetek.category,
        "dolzina": posnetek.duration,
        "naslov": posnetek.title,
        # "kljucne_besede" : posnetek.keywords
    }
    # preveri, če je pesem že v bazi
  #  with open('baza.json', 'r') as txt:

    with open('baza.json', 'a') as txt:
        json.dump(slovar, txt)
