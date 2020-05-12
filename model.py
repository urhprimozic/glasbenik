# PAZI:
# Model ne sme vedet za vmesnik
# slovenske spremenljivke
import vlc
import pafy


# TO DO: Združi te razrede!??
class Predvajalnik:
    """
    Poskrbi za magijo z moduloma vlc in pafy, da predvaja glasbo iz spletnega naslova.
    Trenutno zna:
        > Nič
    """
    def __init__(self):
        pass #bomo jutr

#Ali potrebujem poseben razred za predlaganje glasbe? Po mojem ne
class Lokalni_iskalnik:
    """
    Glede na geslo zna iskati po lokalni bazi, mogoče tudi predlaga glasbo.
    """
    def __init__(self):
        super().__init__()

class Spletni_iskalnik:
    """
    Glede na geslo zna iskati po spletni platformi youtube.
    """
    def __init__(self):
        pass

# Trenutno stanje: Znaš predvajat muzko (predvajalnik) in znaš iskat po obeh bazah (predpostavimo, da lokalni tud predlaga stvari)