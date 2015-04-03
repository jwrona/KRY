#!/usr/bin/env python3

from Encryption import Encryption as en

m1_list = en.stringToOrdList('neconic')
m2_list = en.stringToOrdList('ahojcus')
k_list = en.stringToOrdList('xonotic')

c1_list = en.listXOR(m1_list, k_list)
c2_list = en.listXOR(m2_list, k_list)

print(en.intListToHexList(c1_list))
print(en.intListToHexList(c2_list))

c1_xor_c2_list = en.listXOR(c1_list, c2_list)
m1_xor_m2_list = en.listXOR(m1_list, m2_list)

test_word = en.stringToOrdList('ahoj')
for i in range(len(m1_xor_m2_list) - len(test_word) + 1):
    print(i)
    winning = en.listXOR(test_word, m1_xor_m2_list[i:])
    print(en.ordListToString(winning))
