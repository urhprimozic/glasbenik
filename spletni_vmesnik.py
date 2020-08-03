import bottle
import baza
import model
import re
# vsako zdravilo za raka je rak

# BAZA
server = model.Server()

# VLC PREDVAJALNIk
domaci_server = False  # spremeni to za vlc predvajalnik
vlc = model.Predvajalnik()

SKRIVNOST = "42x69eq420"  # zastonj priložnost za jazjaz


def id():
    '''
    Vrne id uporabnikove seje, ali pa ustvari novo sejo in vrnje njen id.

    Parameters
    ----------
    None

    Returns
    -------
    ans : int
        Id seje trenuntnega uporabnika.
    '''
    try:
        ans = int(bottle.request.get_cookie('id_seje', secret=SKRIVNOST))
    except:
        ans = server.nova_seja()
        bottle.response.set_cookie(
            'id_seje', str(ans), secret=SKRIVNOST, path='/')
    if ans is None:
        ans = server.nova_seja()
        bottle.response.set_cookie(
            'id_seje', str(ans), secret=SKRIVNOST, path='/')
    return ans


def pridobi_sejo():
    '''
    Vrne sejo trenuntnega uporabnika.

    Parameters
    ----------
    None

    Returns
    -------
    ans : baza.Seja
        Seja trenuntega uporabnika
    '''
    ans = server.seje.get(id())
    if ans is None:
        index = server.nova_seja()
        bottle.response.set_cookie('id_seje', str(
            index), secret=SKRIVNOST, path='/')
        ans = server.seje[index]

    return ans


def predvajaj(pesem: dict, seja):
    '''
    Predvaja pesem.

    Parameters
    ----------
    pesem : dict
        Slovar pesmi

    seja : baza.Seja
        Uporabnikova seja

    Returns
    -------
    None
    '''
    if domaci_server:
        try:
            vlc.predvajaj_url(pesem['url'])
        except:
            vlc.predvajaj_url(
                'https://www.youtube.com/watch?v=hom9faSBUHQ')  # bolana šala
    else:
        seja.nov_id_predvajane(pesem.get('id'))
        seja.nov_naslov_predvajane(pesem.get('naslov'))
        if seja.id_trenunte_skladbe() is None:
            # ta šala ful kašla pa slabo ji je
            seja.nov_id_predvajane('hom9faSBUHQ')

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


@bottle.get('/')
def index():
    '''
    Naslovna stran
    '''
    seja = pridobi_sejo()
    return bottle.template('predvajalnik.html',  get_url=bottle.url, rezultati=seja.rezultati(), id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())


@bottle.get('/isci/')
def isci_get():
    seja = pridobi_sejo()
    # spucamo glasbe na serverju. Za malo uporabnikov je to ok način, to stoji tukaj izkljkučno, ker sem tako napisal
    model.izprazni_mapo('skladbe/')
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
    ime_datoteke = re.sub('[^a-zA-ZčšžćđČŠŽĆĐß$€0123456789]+',
                          '-', seja.rezultati()[index_skladbe]['naslov'])
    vlc.nalozi(seja.rezultati()[index_skladbe]['url'], ime_datoteke)
    bottle.redirect('/skladbe/' + ime_datoteke + '.mp3')


@bottle.post('/zgodovina/')
def zgodovina_post():
    seja = pridobi_sejo()
    index_skladbe = int(list(bottle.request.forms.keys())[0].split('.')[0])
    predvajaj(seja.zgodovina_predvajanih()[index_skladbe], seja)
    bottle.redirect('/domov/')


@bottle.post('/predvajaj/')
def predvajaj_get():
    seja = pridobi_sejo()
    index_skladbe = int(list(bottle.request.forms.keys())[0].split('.')[0])
    seja.dodaj_v_zgodovino(seja.rezultati()[index_skladbe])
    predvajaj(seja.rezultati()[index_skladbe], seja)
    bottle.redirect('/')


@bottle.get('/domov/')
def domov_get():
    seja = pridobi_sejo()
    return bottle.template('domov.html',  get_url=bottle.url, zgodovina=seja.zgodovina_predvajanih(), id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())


@bottle.post('/nalozi_vec_skladb/')
def nalozi_vec_post():
    seja = pridobi_sejo()
    # več iz baze
    if list(bottle.request.forms.keys())[0] == 'nalozi_vec':
        seja.isci_po_bazi(
            seja.geslo(), iskalni_prostor=seja.iskanje(), pi=seja.pi() + 10)
    else:
        seja.isci_po_youtubu(seja.geslo())
        seja.posodobi_bazo_na_nasilen_nacin()
        seja.isci_po_bazi(
            seja.geslo(), iskalni_prostor=seja.iskanje(), pi=seja.pi())
    bottle.redirect('/')


@bottle.post('/nakljucno/')  # copy paste code go brrrrrrrrrrrrrrrrrrrr
def nakljucno_post():
    seja = pridobi_sejo()
    pesem = seja.nakljucna_pesem()
    predvajaj(pesem, seja)
    seja.dodaj_v_zgodovino(pesem)
    bottle.redirect('/domov/')


@bottle.get('/kolofon/')
def kolofon_post():
    seja = pridobi_sejo()
    return bottle.template('kolofon.html', get_url=bottle.url, id_skladbe=seja.id_trenunte_skladbe(), naslov_skladbe=seja.naslov_trenutne_skladbe())


# konec
# bottle.run(debug=True, reloader=True, host='localhost') # DEV opcije
# POZOR! embed youtube teži, če je host IP address! Trik za domači server je uporaba localhosta.
bottle.run(host='localhost')
# na resnem serveju bo verjetno delalo tudi , če bo host="0.0.0.0", samo, da uporabnik do njega dostopa preko imena domene (baje)
#  vir: https://stackoverflow.com/questions/51969269/embedded-youtube-video-doesnt-work-on-local-server
