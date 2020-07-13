# le zadeve, povezane z grajenjem in iskanjem po bazi
import json
import pafy
import youtube_dl
from youtubesearchpython import searchYoutube
'''  TODO
>fajli z os (brezveze, dokler ne začnem delat z bottle, ker bom šel takrat delat s piškotki)
> enostavni iskalnik je počasen. Če je blo do sedaj dovolj gesel ničelnih, itak veš, da pesmi ne bo noter
'''

# TODO : a je bolš da premakneš to v bazo in rečeš @staticmethod ?
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

    # TODO : kaj je hitrejš
    for i in geslo:
        for j in kandidat:
            # TODO : kk python izbede  __eq__() na strignih? Ker če je o(n^2), je to shit
            if i == j:
                vrednost += 5
            # načeloma bo dovolj gledat sam perfect match, zarad levhensteina
            # elif i in j:
            #    vrednost += 1
    return vrednost

def levenshtein(a, b):
    '''
    Vrne Levenshteinovo razdaljo med nizom a in nizom b.
    >>> evenshtein('riba', 'miza')
    2
    Več: https://en.wikipedia.org/wiki/Levenshtein_distance
    '''
    # Ix2 matrika, dinnamično programiranje
    I = len(a)
    J = len(b)
    memo = [[0] * (I + 1), [0] * (I + 1)]  # lepše kot rekurzija
    current = 1
    for j in range(J + 1):  # b
        for i in range(I + 1):  # a
            if i == 0 or j == 0:
                memo[current][i] = max(i, j)
                continue
            dodatek = 1
            if(a[i - 1] == b[j - 1]):
                dodatek = 0
            memo[current][i] = min(
                memo[current][i - 1] + 1, memo[not current][i - 1] + dodatek, memo[not current][i] + 1)

        current = not current  # "zamenjamo vrstici"

    return memo[not current][I]

def zapleteni_iskalnik(kandidat, geslo):
    '''
    Vrne minimum od Levenshteinove razdalje med geslom in besedam v kandidatu.
    TODO: kkšne meje, to bo počasno
    '''
    return min([levenshtein(j, i) for i in kandidat for j in geslo])

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
        self.zadnji_rezultati = []

    def dodaj_url(self, url):
        '''Doda pesem, ki se nahaja na spletnem naslovu url, v bazo seje, če je tam še ni.
        Vrne True, če je bila pesem uspešno dodana, drugače vrne False'''
        try:
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
            #thumbnail
            try:
                slovar['slika'] = posnetek.bigthumb
            except:
                print("Slika ni dostopna")
                slovar['slika'] = '/media/default.png'
            # google ne mara preveč requestov po kategoriji
            try:
                slovar['kategorija'] = posnetek.category,
            except:
                print(
                    "Napaka pri prepoznavanju kategorije skladbe.\nSkladba dodana brez kategorije")

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
        except youtube_dl.utils.ExtractorError:
            print("   Napaka: pesem ni dosegljiva")
            return False
        else:
            print("Neznana napaka pri klicu na pesem")
            return False

    def posodobi_bazo_na_nasilen_nacin(self):
        '''
        Lokalno bazo nadomesti z bazo trenutne seje.
        Nasilen, a hiter pristop.
        '''
        with open(self.lokacija_lokalne_baze, 'w') as txt:
            txt.write(json.dumps(self.baza))
            print("(zloben smeh) hahaha. vaši stari podatki so izgubljeni.")

    def uvozi(self, datoteka):
        '''
        V bazo seje doda pesmi iz datoteke z urlji, ločeni z novimi vrsticami.
        '''
        with open(datoteka) as txt:
            for pesem in txt.readlines():
                self.dodaj_url(pesem)

    def isci_po_bazi(self, iskano_geslo, iskalni_prostor=None, pi=10):
        '''
        Išče skladbe, ki imajo podoben naslov ali avtorja, kot geslo.
        Vrne seznam pesmi (slovarjev), 
        pi je število rezultatov
        iskalni_prostor je tabela, kjer i-ti element pove, ali naj i-to pesem izpustim iz iskanja.
        '''
        if iskalni_prostor is None:
            iskalni_prostor = [1]*len(self.baza)
        if len(iskalni_prostor) != len(self.baza):
            raise Exception(
                'iskalni_prostor mora biti enakih dimenzij kot baza')

        rezultati_enostavno = []
        rezultati_zapleteno = []
        geslo = iskano_geslo.lower().split()

        # enostavno iskanje
        for i in range(len(iskalni_prostor)):
            # iščemo samo po določenih pesmih
            if iskalni_prostor[i] == False:
                continue
            pesem = self.baza[i]
            kandidat = pesem['naslov'].lower().split() + \
                pesem['avtor'].lower().split()

            vrednost = enostavni_iskalnik(kandidat, geslo)

            if vrednost != 0:
                rezultati_enostavno.append((pesem, vrednost))
                iskalni_prostor[i] == 0  # za to pesem ni potrebno levenhsteina
            # potrebujemo le pi rezultatov
            if len(rezultati_enostavno) >= pi:
                break

        # levhenstein - hočeš čim manjšega
        for i in range(len(iskalni_prostor)):
            pesem = self.baza[i]
            kandidat = pesem['naslov'].lower().split() + \
                pesem['avtor'].lower().split()
            # potrebujemo le pi rezultatov
            if len(rezultati_enostavno) + len(rezultati_zapleteno) >= pi:
                break
            rezultati_zapleteno.append(
                (pesem, zapleteni_iskalnik(kandidat, geslo)))
        # Posortiram in vrnem prečiščeno
        # prava paša za oči
        self.zadnji_rezultati = [i[0] for i in sorted(rezultati_enostavno, key=lambda x: x[1], reverse=True)] + [j[0] for j in sorted(rezultati_zapleteno, key=lambda x: x[1])]
        return self.zadnji_rezultati

    def isci_po_youtubu(self, geslo, dodaj_v_bazo=True):
        '''
        Uporabi modul *, in vrne prvih pi rezultatov iskanja v tabeli razredov.
        '''
        print("beta verzija")
        try:
            # tabela z rezultati
            rezultati = json.loads(searchYoutube(geslo, 1, "json").result())[
                "search_result"]
            # standrdiziranje imen. TODO ? svoja verzija modula za rezultate?
            for i in rezultati:
                i['url'] = i.pop('link')
                i['naslov'] = i.pop('title')
                i['avtor'] = i.pop('channel')
                i['dolzina'] = i.pop('duration')
                if dodaj_v_bazo:
                    self.dodaj_url(i['url'])
            return rezultati
        except:
            print("napaka med klicom na pesem")

    def izvozi(self, datoteka='knjiznica.txt'):
        '''
        V datoteko izvozi spletne naslove pesmi v bazi, ločene z novo vrstico.
        '''
        with open(datoteka, 'a') as txt:
            for i in self.baza:
                txt.write(i['url'])

# s = Seja()
# for pesem in s.baza:
#     try:
#         p = pafy.new(pesem['url'])
#     except:
#         pesem['slika'] = '/media/default.png'
#         continue
#     try:
#         pesem['slika'] = p.bigthumb
#     except:
#         print("Slika ni dostopna")
#         pesem['slika'] = '/media/default.png'
# s.posodobi_bazo_na_nasilen_nacin()