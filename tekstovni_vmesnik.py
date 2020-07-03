# Pomožne funckije za vnos
import model
import baza


seja = baza.Seja()
predvajalnik = model.Predvajalnik()

#ojoj ne globalne spremenljivke groza ne
def predvajanje():
    global predvajalnik
    while(True):
        i = input('(1) za pavzo\n (2) za predvajaj\n(3) za stop')
        if i == '1':
            predvajalnik.pavza()
        if i == '2':
            predvajalnik.predvajaj()
        if i == '3':
            return True

print("\033[93m Dobrodošli v shitty tekstovnem vmesniku, ki ga jutri ne bo več \033[0m")

while(True):
    ukaz = str(input(
        "\n\nTrenutno lahko: \n(1) poiščeš glasbo v lokalni bazi\n(2)poiščeš glasbo na spletu\n(3)Predvajaš glasbo\n(4) nasilno posodobiš bazo\n>"))
    if ukaz == '1':
        geslo = str(input('Iskano geslo:\n>'))
        rezultati = seja.isci_po_bazi(geslo)
        for i in range(min(len(rezultati), 5)):
            print('(' + str(i) + ')  ' + str(rezultati[i]['naslov']))#( '(' + str(i) + ')' + str(rezultati[i]['avtor']) + ': \033[93m' + + str(rezultati[i]['naslov']) + ' \033[0m')
        
        pesem = int(input())
        predvajalnik.predvajaj_url(rezultati[pesem]['url'])
        predvajanje()
    if ukaz == '2':
        geslo = str(input('Iskano geslo:\n>'))
        rezultati = seja.isci_po_youtubu(geslo)
        for i in range(min(len(rezultati), 5)):
            print('(' + str(i) + ')  ' + str(rezultati[i]['naslov']))
        
        pesem = int(input())
        predvajalnik.predvajaj_url(rezultati[pesem]['url'])
        predvajanje()
        

    if ukaz == '3':
        print("Ja veš, morš najprej povedat kero musko bi!")
    if ukaz == '4':
        seja.posodobi_bazo_na_nasilen_nacin()