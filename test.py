# Ti testi niso ignorirani
# TO DO: Dol iz finalne verzije
import model
import baza

seja_baze = baza.Seja()
with open('glasbena-knjiznica.txt') as txt:
    for pesem in txt.readlines():
        seja_baze.dodaj_url(pesem)
seja_baze.posodobi_bazo_na_nasilen_nacin()

# predvajalnik = model.Predvajalnik()
# predvajalnik.predvajaj_url('https://www.youtube.com/watch?v=r7gFNaGYEs8')
# predvajalnik.predvajaj_url('https://youtu.be/SJfUYTfdoR4?t=44')
