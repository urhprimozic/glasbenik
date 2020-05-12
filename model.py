# -*- coding: utf-8 -*-
# $ Z $ označim komentarji, ki morajo stran PRED ZADNJO VERZIJO
# $PAZI:
# $Model ne sme vedet za vmesnik
# $slovenske spremenljivke
import vlc
import pafy


# $TODO: Združi te razrede!??
class Predvajalnik:
    '''
    Poskrbi za magijo z moduloma vlc in pafy, da predvaja glasbo iz spletnega naslova.
    Trenutno zna:
        > Nič
    '''

    def __init__(self):
        self.trenutna_pesem = None

        #zažene vlc
        self.vlc_instance = vlc.Instance() # Običaj za poimenovanje te spremenljivkle je instance, prevod bi bil čuden
        self.vlc_predvajalnik = self.vlc_instance.media_player_new()
        

    def predvajaj_url(self, url):
        '''
        Predvaja glasbo iz posnetka, ki se nahaja na spletnem naslovu url.
        TODO: Preveri internetno povezavo, preveri url
        '''
        # pafy poišče najbolšo kvaliteto za prenos v živo
        kvaliteten_url = pafy.new(url).getbest().url
        
        # vlc magija
        media = self.vlc_instance.media_new(kvaliteten_url)
        media.get_mrl()
        self.vlc_predvajalnik.set_media(media)

        # predvajaj
        self.vlc_predvajalnik.play()




class Lokalni_iskalnik:
    '''
    Glede na geslo zna iskati po lokalni bazi, mogoče tudi predlaga glasbo.
    '''

    def __init__(self):
        super().__init__()


class Spletni_iskalnik:
    '''
    Glede na geslo zna iskati po spletni platformi youtube.
    '''

    def __init__(self):
        pass

# $Trenutno stanje: Znaš predvajat muzko (predvajalnik) in znaš iskat po obeh bazah (predpostavimo, da lokalni tud predlaga stvari)
