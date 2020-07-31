# le zadeve, povezane z grajenjem in iskanjem po bazi
import json
import re
import pafy
import youtube_dl
from youtubesearchpython import SearchVideos
import random

velikost_zgodovine = 50

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
        if i in kandidat:
            vrednost += 5
        # else:
        #    vrednost -= 2

    return max(0, vrednost)


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
    vrednost = 0
    for i in geslo:
        vrednost += min([levenshtein(i, j) for j in kandidat])
    return vrednost
    # return min([levenshtein(j, i) for i in kandidat for j in geslo])


def cistilec_nizov(niz):
    '''
    niz - str
    Vzame niz in vrne tabelo besed, pisanih z malimi črkami iz niza. Vse znake, ki niso črke, vrže ven.
    Simbola € in $ pusti, ker se večkrat pojavljata v glasbah,
    Simbol & pa ne, saj je po navadi uporabljen brez sosednjih presledkov.
    >>> cistilec_nizov("Elvis Jackson-Against The Gravity(Album)")
    ['Elvis', 'Jackson', 'Against', 'The', 'Gravity', 'Album']
    '''
    # verjetno je regex hitrejši, pa rad bi se ga naučil uporabljat
    return [i for i in re.sub("[^a-zA-ZčšžćđČŠŽĆĐß$€0123456789]+", " ", niz.lower()).split(" ") if i != '']


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
        self.zadnje_iskanje = []
        self.zadnje_geslo = "klemen klemen"
        self.zadnji_pi = 11
        # zgodovina[0] pove, kje je zadnji zapisani element
        self.zgodovina = [1]
        self.id_predvajane = "ApU-5Oot7cI"
        self.naslov_predvajane = "KEŠPIČKE $$$"

    def naslov_trenutne_skladbe(self):
        return self.naslov_predvajane

    def nov_naslov_predvajane(self, naslov: str):
        self.naslov_predvajane = naslov

    def id_trenunte_skladbe(self):
        return self.id_predvajane

    def nov_id_predvajane(self, id: str):
        self.id_predvajane = id

    def dodaj_v_zgodovino(self, pesem: dict):
        if len(self.zgodovina) <= velikost_zgodovine:
            self.zgodovina.append(pesem)
            self.zgodovina[0] = len(self.zgodovina) - 1
        else:
            if self.zgodovina[0] < len(self.zgodovina) - 1:
                self.zgodovina[0] += 1
            else:
                self.zgodovina[0] = 1
            self.zgodovina[self.zgodovina[0]] = pesem

    def zgodovina_predvajanih(self):
        '''
        Vrne seznam nazadnje predvajanih pesmi, kjer je prva pesem zadnja predvajana.
        '''
        j = self.zgodovina[0]
        ans = []
        for i in range(len(self.zgodovina) - 1):
            ans.append(self.zgodovina[j])
            j -= 1
            if j < 1:
                j = len(self.zgodovina) - 1
        return ans

    def rezultati(self):
        return self.zadnji_rezultati

    def iskanje(self):
        return self.zadnje_iskanje

    def geslo(self):
        return self.zadnje_geslo

    def pi(self):
        return self.zadnji_pi

    def dodaj_url(self, url):
        '''Doda pesem, ki se nahaja na spletnem naslovu url, v bazo seje, če je tam še ni.
        Vrne True, če je bila pesem uspešno dodana, drugače vrne False'''
        try:
            posnetek = pafy.new(url)
            slovar = {
                'url': url,
                'avtor': posnetek.author,
                'dolzina': posnetek.duration,
                'naslov': posnetek.title,
                'id': posnetek.videoid,
            }
            # thumbnail
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
                    return False
            # če pesmi še ni, jo dodamo
            self.baza.append(slovar)
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

    def nakljucna_pesem(self):
        return random.choice(self.baza)

    def uvozi(self, datoteka):
        '''
        V bazo seje doda pesmi iz datoteke z urlji, ločeni z novimi vrsticami.
        '''
        with open(datoteka) as txt:
            for pesem in txt.readlines():
                self.dodaj_url(pesem)

    def isci_po_bazi(self, iskano_geslo=None, iskalni_prostor=None, pi=11):
        '''
        Išče skladbe, ki imajo podoben naslov ali avtorja, kot geslo.
        Vrne seznam pesmi (slovarjev), 
        pi je število rezultatov
        iskalni_prostor je tabela, kjer i-ti element pove, ali naj i-to pesem izpustim iz iskanja.
        '''
        self.zadnji_pi = pi
        if iskano_geslo is None:
            iskano_geslo = self.zadnje_geslo
        else:
            self.zadnje_geslo = iskano_geslo
        vec_pesmi = True
        if iskalni_prostor is None:
            iskalni_prostor = [1] * len(self.baza)
            vec_pesmi = False

        rezultati_enostavno = []
        rezultati_zapleteno = []
        geslo = cistilec_nizov(iskano_geslo)

        # enostavno iskanje
        for i in range(len(iskalni_prostor)):
            # iščemo samo po določenih pesmih
            if iskalni_prostor[i] == False:
                continue
            pesem = self.baza[i]
            kandidat = cistilec_nizov(pesem['naslov'] + ' ' + pesem['avtor'])
            # kandidat = pesem['naslov'].lower().split() + \
            #    pesem['avtor'].lower().split()

            vrednost = enostavni_iskalnik(kandidat, geslo)

            if vrednost != 0:
                rezultati_enostavno.append((pesem, vrednost))
                # print("aa")
                iskalni_prostor[i] = 0  # za to pesem ni potrebno levenhsteina
        rezultati_enostavno = sorted(rezultati_enostavno, key=lambda x: x[1], reverse=True)[
            0:min(pi, len(rezultati_enostavno))]

        # levhenstein - hočeš čim manjšega
        for i in range(len(iskalni_prostor)):
            if iskalni_prostor[i] == 0:
                continue
            pesem = self.baza[i]
            kandidat = cistilec_nizov(pesem['naslov'] + ' ' + pesem['avtor'])
            # kandidat = pesem['naslov'].lower().split() + \
            #  pesem['avtor'].lower().split()
            # potrebujemo le pi rezultatov
           # if len(rezultati_enostavno) + len(rezultati_zapleteno) >= pi:
            #    break
            rezultati_zapleteno.append(
                (pesem, zapleteni_iskalnik(kandidat, geslo), i))
        # iskalni prostor
        rezultati_zapleteno = sorted(rezultati_zapleteno, key=lambda x: x[1])[
            0:pi-len(rezultati_enostavno)]
        for i in rezultati_zapleteno:
            iskalni_prostor[i[2]] = 0

        # for i in sorted(rezultati_enostavno, key=lambda x: x[1], reverse=True):
        #    print(i)

        ans = [i[0] for i in rezultati_enostavno] + [
            j[0] for j in rezultati_zapleteno]

        self.zadnje_iskanje = iskalni_prostor[:]
        # Posortiram in vrnem prečiščeno
        # prava paša za oči
        if vec_pesmi:
            self.zadnji_rezultati += ans
        else:
            self.zadnji_rezultati = ans
        return self.zadnji_rezultati

    def isci_po_youtubu(self, geslo, dodaj_v_bazo=True):
        '''
        Uporabi modul youtubesearchpython, in vrne prvih pi rezultatov iskanja v tabeli razredov.
        '''
        # tabela z rezultati
        rezultati = json.loads(SearchVideos(geslo, offset=1, mode="json", max_results=10).result())[
            "search_result"]
        for i in rezultati:
            self.dodaj_url(i['link'])
        return self.isci_po_bazi(iskano_geslo=geslo)

    def izvozi(self, datoteka='knjiznica.txt'):
        '''
        V datoteko izvozi spletne naslove pesmi v bazi, ločene z novo vrstico.
        '''
        with open(datoteka, 'a') as txt:
            for i in self.baza:
                txt.write(i['url'])
