# -*- coding: utf-8 -*-

# Pomožne funckije za vnos


def napaka(niz, p=True, naslov='Napaka: '):
    '''
    V linuxovih bashih pobarva besedilo z rdečo.
    p=False ne izpiše napake
    '''
    if p:
        print('\033[91m'+'\033[1m'+ naslov + '\033[0m' + niz)
    return '\033[91m'+'\033[1m'+ naslov + '\033[0m' + niz
