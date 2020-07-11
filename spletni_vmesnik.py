import bottle
import baza

#styles
@bottle.route('/static/<filename>', name='static')
def server_static(filename):
    return bottle.static_file(filename, root='static')

@bottle.get('/<ime>/')
def pozdravi(ime):
    return 'Živjo, {}!'.format(ime)

@bottle.get('/')
def main():
    return bottle.template('predvajalnik.html',  get_url=bottle.url)
bottle.run(debug=True, reloader=True)