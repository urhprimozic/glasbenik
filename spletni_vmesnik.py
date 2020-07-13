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
    rezultati = seja.isci_po_bazi(geslo)
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=rezultati)

@bottle.post('/predvajaj/')
def predvajaj_get():
    index_skladbe = int(list(bottle.request.forms.keys())[0].split('.')[0])
    vlc.predvajaj_url(seja.zadnji_rezultati[index_skladbe]['url'])
    bottle.redirect('/')

# konec
bottle.run(debug=True, reloader=True)
