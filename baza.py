# le zadeve, povezane z grajenjem in iskanjem po bazi
import json
import pafy
from youtubesearchpython import searchYoutube
'''  TODO
>fajli z os (brezveze, dokler ne začnem delat z bottle, ker bom šel takrat delat s piškotki)
> enostavni iskalnik je počasen. Če je blo do sedaj dovolj gesel ničelnih, itak veš, da pesmi ne bo noter
'''


def enostavni_iskalnik(kandidat, geslo):
    '''
    Pogleda, koliko besed iz gelsa se skriva v kandidatu. 
    Če uporabnik ne dela slovničnih napak, dokaj efektiven pristop.
    Vrne približno oceno ustreznosti me TODO
    >>> enostavni_iskalnik(["TooDamnFilthy", "pink", "guy", "sax"],["Filthy", "Frank"])
    2
    '''
    # vrednost pove, koliko je kandidat po tem enostavnem kriteriju podoben geslu
    vrednost = 0
    for i in geslo:
        for j in kandidat:
            if i == j:
                vrednost += 5
            elif i in j:
                vrednost += 2
            elif j in i:
                vrednost += 1
    return vrednost


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

    def isci_po_bazi(self, iskano_geslo, pi=10):
        '''
        Išče skladbe, ki imajo podoben naslov ali avtorja, kot geslo.
        Vrne seznam parov, kjer je prvi element slovar pesmi, drugi pa vrednost.
        IDEJA:
        > najprej predpostavi, da uporabnik zna pisat
        > nato dela kkšnega levensteina, s tem da mu je vseeno, če spusti druge besede
        > potem pa https://pythonspot.com/nltk-stemming/  in nimaš več volje do življenja

        '''
        rezultati = []
        geslo = iskano_geslo.lower().split()
        for pesem in self.baza:
            kandidat = pesem['naslov'].lower().split() + \
                pesem['avtor'].lower().split()
            
            vrednost = enostavni_iskalnik(kandidat, geslo)

            if vrednost != 0:
                rezultati.append((pesem, vrednost))
            # if len(rezultati) < pi: # uporabi boljšo verzijo iskanja

        return sorted(rezultati, key=lambda x: x[1], reverse=True)


    def isci_po_youtubu(self, geslo, pi=10):
        '''
        Uporabi modul *, in vrne prvih pi rezultatov iskanja v tabeli razredov.
        '''
        print("beta verzija")
        #tabela z rezultati
        rezultati = json.loads(searchYoutube(geslo, 1, "json").result())["search_result"]
        # standrdiziranje imen. TODO ? svoja verzija modula za rezultate?
        for i in rezultati:
            i['url'] = i.pop('link')
            i['naslov'] = i.pop('title')
            i['avtor'] = i.pop('channel')
            i['dolzina'] = i.pop('duration')
        return rezultati

