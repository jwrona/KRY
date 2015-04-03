#!/usr/bin/env python3
#author: Jan Wrona
#email: xwrona00@stud.fit.vutbr.cz

import sys
from Encryption import Encryption as en
import unicodedata as ud

#constants
################################################################################
dict_file = 'dictionaries/pspad/dict.txt'

c1 = '07403f4c794843407b017d66285926404027427b226b2431314061315a642c5c39076e6b4e7d5b5c334f5972524f0f7b3a5c6f3f282f024f377c1e5b6825236e03702b3f31686975343a7455573c72312578527f350268792d4c2c21554d74572953732b477f3b6d476e6f642269327c2c4704577065164553537469650817746053492e7a756655662b2e26404372442201787e737a713c5017'
c2 = '1b4a6903685f02496b4d2e6d6d4727514171543e3a3f6b2135406f3a597c2459250b3e7807785c4c691f403950450c322c5e2a6538394d1f357052116064377e41613d3b797d6b60352063585a7528782a390a3e2d52777d364721215f18275668503f314b743a640a236f6635673a2811454c48706502590050776a2143762762585e3877792a077a3a2e2c454e72432457707e6d69683e5d5e'

#c1 = '160a0d001a0000' #neconic
#c2 = '19070105171c10' #ahojcus

################################################################################

#functions
################################################################################
def strip_accents(s):
    return ''.join(c for c in ud.normalize('NFD', s) if ud.category(c) != 'Mn')

def xor_ciphers(c1, c2):
    c1_ordlist = en.hexListToIntList(en.stringToHexList(c1)[::2])
    c2_ordlist = en.hexListToIntList(en.stringToHexList(c2)[::2])
    return en.listXOR(c1_ordlist, c2_ordlist)

def create_word_list(dict_file):
    word_list = []
    with open(dict_file, 'r') as f:
        word_list = f.read().splitlines()
    return [strip_accents(word).lower() for word in word_list]
################################################################################

if __name__ == "__main__":
    ciphers_xor = xor_ciphers(c1, c2)
    word_set = frozenset(create_word_list(dict_file))
    word_list = sorted(list(word_set), key = len, reverse = True)

    counter = 0
    for word in word_list:
        #counter = counter + 1
        #if not (counter % 1000):
        #    print(counter, word)

        test_word = en.stringToOrdList(word)
        for i in range(len(ciphers_xor) - len(test_word) + 1):
            m_xor = en.ordListToString(en.listXOR(test_word, ciphers_xor[i:]))
            if m_xor.isprintable() and (m_xor.lower() in word_set):
                print(word, m_xor)
