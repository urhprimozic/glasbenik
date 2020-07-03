# PAZI:
# Model ne sme vedet za vmesnik
# slovenske spremenljivke
import pafy
import vlc

class Predvajalnik:
    '''
    Poskrbi za magijo z moduloma vlc in pafy, da predvaja glasbo iz spletnega naslova.
    Trenutno zna:
        > predvajaj_url(url)
    '''

    def __init__(self):
        self.trenutna_pesem = None

        # zažene vlc
        # Običaj za poimenovanje te spremenljivkle je instance, prevod bi bil čuden
        self.vlc_instance = vlc.Instance()
        self.vlc_predvajalnik = self.vlc_instance.media_player_new()

    def predvajaj_url(self, url):
        '''
        Predvaja glasbo iz posnetka, ki se nahaja na spletnem naslovu url.
        TODO: Trenutno odpre okno
        Preveri internetno povezavo, preveri url
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

