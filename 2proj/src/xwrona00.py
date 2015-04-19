#!/usr/bin/env python2
#author: Jan Wrona
#email: xwrona00@stud.fit.vutbr.cz

import sys, os
from binascii import hexlify, unhexlify
from OracleModule import paddingOracle, genNewKey, setKey, encrypt

block_len = 16 #in words
word_len = 8 #in bits

def last_word_oracle(block):
    '''Return one or more last words of C^-1(block).

    Usually only last block of C^-1(block) is returned. May return more
    blocks if we are lucky and generated random numbers causes more blocks of
    valid PKCS#7 padding on plaintext.
    Arguments:
    block -- block to decrypt (binary, not hexadecimal)
    '''
    rand_block = bytearray(os.urandom(block_len))

    #Try all combinations of last word and ask oracle.
    for i in range(2 ** word_len):
        rand_block[-1] ^= i #alter
        if paddingOracle(hexlify(rand_block + block)):
            break
        else:
            rand_block[-1] ^= i #revert

    #Check if one or more words were decrypted by gradually altering words from
    #left to right. When oracle returns false, altered word represents position
    #of the leftmost decrypted word of C^-1(block).
    for i in range(block_len):
        rand_block[i] ^= 1 #alter
        oracle_res = paddingOracle(hexlify(rand_block + block))
        if not oracle_res:
            rand_block[i] ^= 1 #revert
            return bytearray([word ^ (block_len - i) for word in rand_block[i:]])


def next_word_oracle(block, known_suffix):
    '''Return next word of C^-1(block).

    Initial known_suffix is obtained by call to last_word_oracle(). Next word
    here means leftmost word of C^-1(block) not contained in known_suffix. If
    all words of C^-1(block) are contained in known_suffix, None is returned.
    Arguments:
    block -- block do decrypt (binary, not hexadecimal)
    known_suffix -- allready decrypted words from block
    '''
    if len(block) == len(known_suffix):
        return #nothing to decrypt

    new_padd_val = len(known_suffix) + 1 #new padding value == new padding length
    next_word_index = block_len - new_padd_val
    rand_block = bytearray(os.urandom(next_word_index + 1)) #random prefix
    rand_block += bytearray([i ^ new_padd_val for i in known_suffix])

    #Try all combinations of next word and ask oracle.
    for i in range(2 ** word_len):
        rand_block[next_word_index] ^= i #alter
        if paddingOracle(hexlify(rand_block + block)):
            return bytearray([rand_block[next_word_index] ^ new_padd_val])
        else:
            rand_block[next_word_index] ^= i #revert


def decode_ciphertext(ciphertext):
    '''Return decoded ciphertext as string.

    All data are internally handled as bytearrays.
    Arguments:
    ciphertext -- IV | ciphertext (hexadecimal representation)
    '''
    bin_c = bytearray(unhexlify(ciphertext))

    #argument validity checks
    if len(bin_c) == 0 or len(bin_c) % block_len != 0:
        print 'Bad ciphertext length or no ciphertext at all.'
        return
    elif len(bin_c) / block_len < 2:
        print 'Missing ciphertext, only IV present.'
        return

    #cut ciphertext into IV and individual blocks
    bin_block_list = [bin_c[i:i + block_len] for i in range(0, len(bin_c), block_len)]

    plain_int = []
    #Decode each block separately and store results in plain_int list.
    for block_idx, bin_block in enumerate(bin_block_list[1:]): #first is IV
        known_suffix = last_word_oracle(bin_block)
        while len(known_suffix) != block_len:
            known_suffix = next_word_oracle(bin_block, known_suffix) + known_suffix

        #On each decrypted word perform XOR with corresponding word of the previous
        #block (IV in case of first block) to decode C^-1(block) into plaintext.
        for word_idx, word in enumerate(known_suffix):
            plain_int.append(bin_block_list[block_idx][word_idx] ^ word)
 
    #Strip PKCS#7 padding and return plaintext in string representation.
    return ''.join(chr(i) for i in plain_int[:-plain_int[-1]])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ciphertext = sys.argv[1]
    else:
        ciphertext = 'fa485ab028cb239a39a9e52df1ebf4c30911b25d73f8906cc45b6bf87f7a693f47609094ccca42050ad609bb3cf979ac'

    print decode_ciphertext(ciphertext)
    sys.exit(0)
