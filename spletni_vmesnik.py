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


#@bottle.get('/<ime>/')
#def pozdravi(ime):
#    return 'Živjo, {}!'.format(ime)


@bottle.get('/')
def index():
    #return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=None)
    geslo = bottle.request.query.getunicode('iskalno_okno')
    if geslo is None:
        return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=None)
    rezultati = seja.isci_po_bazi(geslo)
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=rezultati)

# iskanje


# @bottle.post('/isci_po_bazi/')
# def isci():
#     geslo = (bottle.request.forms.getunicode('iskalno_okno'))
#     rezultati = seja.isci_po_bazi(geslo)
#     bottle.redirect('/isci_po_bazi/')


# @bottle.get('/isci_po_bazi/')
# def index():
#     geslo = bottle.request.query.getunicode('iskalno_okno')
#     rezultati = seja.isci_po_bazi(geslo)
#     return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=rezultati)


# konec
bottle.run(debug=True, reloader=True)
