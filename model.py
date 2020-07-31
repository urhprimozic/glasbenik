import pafy
import vlc
import youtube_dl 
import os
import shutil
import baza


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
        '''
        # pafy poišče najbolšo kvaliteto za prenos v živo
        kvaliteten_url = pafy.new(url).getbestaudio().url

        # vlc magija
        media = self.vlc_instance.media_new(kvaliteten_url)
        media.get_mrl()
        self.vlc_predvajalnik.set_media(media)

        # predvajaj
        self.vlc_predvajalnik.play()

    def pavza(self):
        self.vlc_predvajalnik.pause()

    def predvajaj(self):
        self.vlc_predvajalnik.play()

    def nalozi(self, url, ime_datoteke, mesto='skladbe/'):
        '''
        Naloži glasbo iz url-ja v zapisu mp3.
        '''
        try:
            # pafy nima možnosti za manualen filename
            ydl_opts = {'outtmpl': mesto + ime_datoteke + '.%(ext)s',
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                return ydl.download([url])
        except:
            return False


def izprazni_mapo(rel):
    shutil.rmtree(rel)
    os.makedirs(rel)


class Server:
    def __init__(self):
        self.seje = {}  # slovar

    # povzeto po vislicah.
    def prost_id_seje(self):
        if len(self.seje) == 0:
            return 0
        else:
            return max(self.seje.keys()) + 1

    def nova_seja(self, glavna_baza='baza.json'):
        # vsak dobi SVOJO bazo
        id = self.prost_id_seje()
        ime_baze = str(id) + '.json'
        # če ime_baze obstaja, ga shutil NE ohrani
        shutil.copyfile(glavna_baza, ime_baze)
        seja = baza.Seja(lokacija=ime_baze)
        self.seje[id] = seja
        return id
