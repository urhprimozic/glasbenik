#trenutno podpiramo enega uporabnika. TODO: več uporabnikov
import bottle
import baza
import model
# BAZA
seja = baza.Seja()
#VLC PREDVAJALNIk
vlc = model.Predvajalnik()


# styles
@bottle.route('/static/<filename>', name='static')
def server_static(filename):
    return bottle.static_file(filename, root='static')
@bottle.route('/media/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='media')

# vlc + bottle je slaba rešitev, javascript bi bla boljša

@bottle.get('/')
def index():
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=seja.zadnji_rezultati)

@bottle.get('/isci/')
def isci_get():
    geslo = bottle.request.query.getunicode('iskalno_okno')
    if geslo is None or geslo == '':
        return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=None)
    rezultati = seja.isci_po_bazi(geslo, pi=11)
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=rezultati)

@bottle.post('/nalozi/')
def nalozi_post():
    index_skladbe = int(list(bottle.request.forms.keys())[0])
    vlc.nalozi(seja.zadnji_rezultati[index_skladbe]['url'])
    bottle.redirect('/')


@bottle.post('/predvajaj/')
def predvajaj_get():
    index_skladbe = int(list(bottle.request.forms.keys())[0].split('.')[0])
    # print(seja.zadnji_rezultati)
    vlc.predvajaj_url(seja.zadnji_rezultati[index_skladbe]['url'])
    bottle.redirect('/')

@bottle.get('/domov/')
def domov_get():
    # TODO: posebna stran za domov - predlogi itd
    return bottle.template('domov.html',  get_url=bottle.url)

@bottle.post('/nalozi_vec_skladb/')
def nalozi_vec_post():
    # več iz baze
    if list(bottle.request.forms.keys())[0] == 'nalozi_vec':
        seja.isci_po_bazi(seja.zadnje_geslo, iskalni_prostor=seja.zadnje_iskanje, pi=seja.zadnji_pi + 10)
    else:
        seja.isci_po_youtubu(seja.zadnje_geslo)
        # TODO: ne bit tko nasilen
        seja.posodobi_bazo_na_nasilen_nacin()
        # zdaj najprej zlovfdamo, nato pa iščemo  z našim algoritmom..
        return bottle.template('predvajalnik.html',  get_url=bottle.url,  rezultati=seja.isci_po_bazi(seja.zadnje_geslo))
    bottle.redirect('/')
    

# konec
bottle.run(debug=True, reloader=True)
