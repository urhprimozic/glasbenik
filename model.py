import pafy
import vlc
import youtube_dl
import os
import shutil
import baza


class Predvajalnik:
    '''
    Predvaja glasbo s spletnega naslova v VCL predvajalniku.
    '''

    def __init__(self):
        self.trenutna_pesem = None
        self.vlc_instance = vlc.Instance()
        self.vlc_predvajalnik = self.vlc_instance.media_player_new()

    def predvajaj_url(self, url: str):
        '''
        Predvaja glasbo iz posnetka, ki se nahaja na spletnem naslovu url.

        Parameters
        ----------
        url : str
            spletni naslov posnetka

        Returns
        -------
        None
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

    def nalozi(self, url: str, ime_datoteke: str, mesto='skladbe/'):
        '''
        Naloži glasbo iz url-ja v zapisu mp3.

        Parameters
        ----------
        url : str
            Spletni naslov pesmi.

        ime_datoteke : str
            Ime datoteke, kamor naj shrani pesem

        mesto : str

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


def izprazni_mapo(rel: str):
    '''
    Izprazne mapo na lokaciji rel.
    Parameters
    ----------
    rel : str
        lokacija mape
    Returns
    -------
    None
    '''
    shutil.rmtree(rel)
    os.makedirs(rel)


class Server:
    '''
    Objekt, ki skrbi za serviranje zadev uporabnikom.
    '''

    def __init__(self):
        self.seje = {}  # slovar

    # povzeto po vislicah.
    def prost_id_seje(self):
        ''' 
        Vrne prost id seje.
        '''
        if len(self.seje) == 0:
            return 0
        else:
            return max(self.seje.keys()) + 1

    def nova_seja(self, glavna_baza='baza.json'):
        '''
        Ustvari novo sejo.

        Parameters
        ----------
        glavna_baza : str
            datoteka - baza, po kateri naj seja brska
        Returns
        -------
        id : int
            Id seje.
        '''
        # vsak dobi SVOJO bazo
        id = self.prost_id_seje()
        ime_baze = str(id) + '.json'
        # če ime_baze obstaja, ga shutil NE ohrani
        shutil.copyfile(glavna_baza, ime_baze)
        seja = baza.Seja(lokacija=ime_baze)
        self.seje[id] = seja
        return id
