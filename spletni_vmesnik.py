#trenutno podpiramo enega uporabnika. TODO: več uporabnikov
import bottle
import baza
import model
import re
import json
# vsako zdravilo za raka je rak
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL) 
# BAZA
server = model.Server()

# VLC PREDVAJALNIk
domaci_server = False # spremeni to za vlc predvajalnik
vlc = model.Predvajalnik()

SKRIVNOST = "42x69eq420" # zastonj priložnost za jazjaz

def id():
    '''
    Vrne id uporabnikove seje, ali pa ustvari novo sejo in vrnje njen id.
    '''
    try:
        ans = int(bottle.request.get_cookie('id_seje', secret=SKRIVNOST))
    except:
        ans = server.nova_seja()
        bottle.response.set_cookie('id_seje', str(ans), secret=SKRIVNOST, path='/')
    if ans is None:
        ans = server.nova_seja()
        bottle.response.set_cookie('id_seje', str(ans), secret=SKRIVNOST, path='/')
    return ans

def pridobi_sejo():
    ans = server.seje.get(id())
    if ans is None:
        index = server.nova_seja()
        bottle.response.set_cookie('id_seje', str(index), secret=SKRIVNOST, path='/')
        ans = server.seje[index]
        
    return ans

# poti do map
@bottle.route('/static/<filename>', name='static')
def server_static(filename):
    return bottle.static_file(filename, root='static')
@bottle.route('/media/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='media')
@bottle.route('/skladbe/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='skladbe')

# vlc + bottle je ABSOLUTNO slaba rešitev (vlc je na serverju)
# TODO: rešitev
# > javascript (vse znova)
# > embled audio in html + zapolneš se kje si ostal (počasno in nagaja)
# > python plugin za uporabnika, ki predvaja musko

@bottle.get('/')
def index():
    # model.izprazni_mapo('skladbe/') # TODO le, ko zaženeš nov session ?
    seja = pridobi_sejo()
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=seja.rezultati(), id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())

@bottle.get('/isci/')
def isci_get():
    seja = pridobi_sejo()
    model.izprazni_mapo('skladbe/') # TODO le, ko zaženeš nov session ?
    geslo = bottle.request.query.getunicode('iskalno_okno')
    if geslo is None or geslo == '':
        return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=None, id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())
    rezultati = seja.isci_po_bazi(geslo, pi=11)
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=rezultati, id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())

@bottle.post('/nalozi/')
def nalozi_post():
    '''
    Naloži pesem na server in uporabnika pošlje na datoteko, da si jo ta lahko naloži
    '''
    seja = pridobi_sejo()
    index_skladbe = int(list(bottle.request.forms.keys())[0])
    ime_datoteke = re.sub('[^a-zA-ZčšžćđČŠŽĆĐß$€0123456789]+', '-', seja.rezultati()[index_skladbe]['naslov'])
    vlc.nalozi(seja.rezultati()[index_skladbe]['url'], ime_datoteke)
    bottle.redirect('/skladbe/' + ime_datoteke + '.mp3')


@bottle.post('/zgodovina/')
def zgodovina_post():
    seja = pridobi_sejo()
    index_skladbe = int(list(bottle.request.forms.keys())[0].split('.')[0])
    if domaci_server:
        try:
            vlc.predvajaj_url(seja.zgodovina_predvajanih()[index_skladbe]['url'])
        except:
            vlc.predvajaj_url('https://www.youtube.com/watch?v=hom9faSBUHQ') # bolana šala
    else:
        seja.nov_id_predvajane(seja.zgodovina_predvajanih()[index_skladbe].get('id'))
        seja.nov_naslov_predvajane(seja.zgodovina_predvajanih()[index_skladbe].get('naslov'))
        if seja.id_trenunte_skladbe() is None:
            seja.nov_id_predvajane('hom9faSBUHQ') # ta šala ful kašla pa slabo ji je
    bottle.redirect('/domov/')


@bottle.post('/predvajaj/')
def predvajaj_get():
    seja = pridobi_sejo()
    index_skladbe = int(list(bottle.request.forms.keys())[0].split('.')[0])
    seja.dodaj_v_zgodovino(seja.rezultati()[index_skladbe])
    if domaci_server:
        try:
            vlc.predvajaj_url(seja.rezultati()[index_skladbe]['url'])
        except:
            vlc.predvajaj_url('https://www.youtube.com/watch?v=hom9faSBUHQ') # šla je na ustnega brez maske
    else:
        seja.nov_id_predvajane(seja.rezultati()[index_skladbe].get('id'))
        seja.nov_naslov_predvajane(seja.rezultati()[index_skladbe].get('naslov'))
        if seja.id_trenunte_skladbe() is None:
            seja.nov_id_predvajane('hom9faSBUHQ') # ta šala ima aids in tuberkulozo
        print(seja.id_trenunte_skladbe())
        print("https://www.youtube.com/embed/" + seja.id_trenunte_skladbe() + "?autoplay=1")
    bottle.redirect('/')

@bottle.get('/domov/')
def domov_get():
    seja = pridobi_sejo()
    # TODO: posebna stran za domov - predlogi itd
    return bottle.template('domov.html',  get_url=bottle.url, zgodovina=seja.zgodovina_predvajanih(), id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())

@bottle.post('/nalozi_vec_skladb/')
def nalozi_vec_post():
    seja = pridobi_sejo()
    # več iz baze
    if list(bottle.request.forms.keys())[0] == 'nalozi_vec':
        seja.isci_po_bazi(seja.geslo(), iskalni_prostor=seja.iskanje(), pi=seja.pi() + 10)
    else:
        seja.isci_po_youtubu(seja.geslo())
        # TODO: ne bit tko nasilen
        seja.posodobi_bazo_na_nasilen_nacin()
        seja.isci_po_bazi(seja.geslo(), iskalni_prostor=seja.iskanje(), pi=seja.pi())
        # zdaj najprej zlovfdamo, nato pa iščemo  z našim algoritmom..
        # return bottle.template('predvajalnik.html',  get_url=bottle.url,  rezultati=seja.isci_po_bazi(seja.geslo()), id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())
    bottle.redirect('/')
    
@bottle.get('/kolofon/')
def kolofon_post():
    seja = pridobi_sejo()
    return bottle.template('kolofon.html', get_url=bottle.url, id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())
# konec
bottle.run(debug=True, reloader=True, host='localhost')
