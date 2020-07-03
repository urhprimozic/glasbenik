# le zadeve, povezane z grajenjem in iskanjem po bazi
import json
import pafy

'''  TODO
>fajli z os (brezveze, dokler ne začnem delat z bottle, ker bom šel takrat delat s piškotki)
'''


class Seja:
    ''' Skrbi za bazo trenutne seje.
    self.baza je (pythonova) kopija lokalne baze.
    Struktura:
     [{ Slovar o pesmi} ] <-- seznam pesmi
    '''

    def __init__(self, lokacija='baza.json'):
        self.lokacija_lokalne_baze = lokacija
        with open(lokacija, 'r') as lokalna_baza:
            self.baza = json.load(lokalna_baza)

    def dodaj_url(self, url):
        '''Doda pesem, ki se nahaja na spletnem naslovu url, v bazo seje, če je tam še ni.
        Vrne True, če je bila pesem uspešno dodana, drugače vrne False'''

        posnetek = pafy.new(url)
        slovar = {
            'url': url,
            'avtor': posnetek.author,
            # googlu to ni všeč
            # 'kategorija' : posnetek.category,
            # 'kljucne_besede' : posnetek.keywords
            'dolzina': posnetek.duration,
            'naslov': posnetek.title,
        }
        # preveri, če je pesem že v bazi
        for pesem in self.baza:
            if pesem['url'] == url:
                print('\033[91m'+'Pesem je že v bazi.'+'\033[0m')  # log
                return False
        # če pesmi še ni, jo dodamo
        self.baza.append(slovar)
        print('\033[92m'+'Pesem uspešno dodana.' +
              '\033[0m'+' \nNaslov: ' + slovar['naslov'])
        return True

    def posodobi_bazo_na_nasilen_nacin(self):
        '''
        Lokalno bazo nadomesti z bazo trenutne seje.
        Nasilen, a hiter pristop.
        '''
        with open(self.lokacija_lokalne_baze, 'w') as txt:
            txt.write(json.dumps(self.baza))
            print("(zloben smeh) hahaha. vaši stari podatki so izgubljeni.")

    def dodaj_urlje(self, datoteka):
        '''
        V bazo seje doda pesmi iz datoteke z urlji, ločeni z novimi vrsticami.
        '''
        with open(datoteka) as txt:
            for pesem in txt.readlines():
                self.dodaj_url(pesem)