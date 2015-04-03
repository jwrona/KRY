#!/usr/bin/env python3
#author: Jan Wrona
#email: xwrona00@stud.fit.vutbr.cz

from Encryption import Encryption as en
import unicodedata as ud
import re

#constants
################################################################################
dict_file = 'dictionaries/pspad/dict.txt'
#ciphers = [
#'160f7b4a70430250614c7b23784122505c6e117c247b61317d4f6d35562a085228437b7d427e1615521f46785500057334562f3f27384b452069103b', 
#'07403f4c794843407b017d66285926404027427b226b2431314061315a642c5c39076e6b4e7d5b5c334f5972524f0f7b3a5c6f3f282f024f377c1e5b6825236e03702b3f31686975343a7455573c72312578527f350268792d4c2c21554d74572953732b477f3b6d476e6f642269327c2c4704577065164553537469650817746053492e7a756655662b2e26404372442201787e737a713c5017', 
#'1b4a6903685f02496b4d2e6d6d4727514171543e3a3f6b2135406f3a597c2459250b3e7807785c4c691f403950450c322c5e2a6538394d1f357052116064377e41613d3b797d6b60352063585a7528782a390a3e2d52777d364721215f18275668503f314b743a640a236f6635673a2811454c48706502590050776a2143762762585e3877792a077a3a2e2c454e72432457707e6d69683e5d5e', 
#'1c4b66593b4c47576b4d2e67670d3057496d543271656132295477744b6f655f2307747c4f7c185e665116494c4f02323c402a3f2934491f36684b45637c722b3564247a7c672873282b26464c253167213c43727028', 
#'1f5a6a563a1a495667426b6f690d2e565a6c503e3f7e242932466f3d4b7e2c172d076b71467d5d59721f466b5b5341643957363f2d275b5c6b0f', 
#'034e7403755b4f047b4a6f79285e354c4262116c247c61637d747731186720533a427a39547a184f724f597450450d3225452c753875415a376b5b116c253e7f13643c3678646d252f2267404c752470263d4a772a0c12', 
#'1c5d7e4f744c4c4d6d4a6f23724c354c44665d7f716c6837354c3b351879355820427d7742335347725353394441177b38462f767d314d1f296b5b5f686d222b14673d2f626728647b2a6940473428782831067a314f6d363d4264204e5b3b45311f303050763a78536c45', 
#'045b7e51621a51416a4d6f68284b22514975583e3e3f773438583b2741642a41250774705d33555b7c57533948591160374526737175485e2e2550502d6b2861416f2a3e7f7d606a7b2a685515252c74323d427b7e417d7a200d292e505d20562313733250716f6a5f262a343d6522282f4f404a7a2d0f00444d7e257a0244737359456134716653683a6222515961083d526d317678713e5a17', 
#'1c4e7203685f02527c556076370d0d4243685f7b323f77277d466f355066241722463e76547255507f4616781e4f11672547267124754f50266452116c25387141762a7a7c77726c7b3d7049583c7e7f2d3342677e4c7d63324c3e2e56597a39', 
#'034e3f507e1a4b4c60446a237d572751497158723033242331503b3f5c733f173f4e3e734e334e5a795e5d394e52007e7649223f27304c4a6925545066252f720d6a6f297d7b6a6035212a104527316525304a3e3550797a79422623535b3159641f232a5e6e20724f6235713e65356065474148352a105241557f70201047666659496d6771325e25712369474570446701633b23637c3d1354', 
#'034e74463b404b507c402e706d0d21564c62423e3c767062395a79265d246545294c723977764c473365576a5b000b61335e636b347556502d6a1e596261236e41753d337f777b69756e56425c3b3d743e36473e3c5b38643849256f4c5d3056245e7f785e7e247d4e623b7b707a256d655a4b477d241a490c037a6965435869325d456d7a7925076734302c5e4c37082a4239286664753b1347', 
#'1c4b66593b5e4d566f5b676f610163485a665d3e227a24343859763d187024452d43716f467f1854334d537252002f6b385a636a27755156656a5a1179602f6e416b2a3864767d2535276d544c7530782778566c3f5636360a48286f511824412151303d4b742a284b623d713b6076432a485d486c65090056517a6b6908176d6158596d7a71664968353426474937082558773723667d3f464d', 
#'034e72036b5556566b4d2e71675d3650416a116d3d767e2730156820597826583a5e3e76447a1854334f57721e4d1432245c336a3e3d571f376a44457f6c3e7f08696f3531716d69346226514f752d74642a49642e506b7d354c64215b18205a3b5630785a753a7b41376f75707f2269374f47046365145500517a6b7543416e7652406d60712d076330312750007149204e393567716b3b1d3d', 
#'034a7157741a464b7b476f6f240d39460871427b32776a3b7d5b7a24596e2b5e275e3e76436159517a131678524541622456306b3275515a656b5b5a626924604167233b797d7e7c38262640473c30723178493e2a4776363242313c5f5374432754262b587620240a23237170613f7b31450457353512494e407e7f6e0c422b3244402c62792a4e2927273a504c705d6b527c7e797d7a334758', 
#'13407d517e1a5045604e22236a5f22504126116427706823315a3b205d692d173f426d6d07585958635e5d3953411577765d2272342747512a3a1e6562253e6a0c6c6f34746461683e602642503e3278642c4f3e2a5071362a40313b545d7452684c273d4b753969462b6f67392c386965595445612b05004342687c2e69', 
#'160f7d46615f4e046d407d2f2847224808654868303f6e27355a3b2e4e732e52210b3e77426648477c4c587c1e4141703349636a2e2143512c2b34', 
#'194a75506f5b5057674c7b236a5f22575a684777716d6d293c597274686f31456c576b6d48655959334c407c4a450c3e7652393f373046512a6d5111696b282b11772629747e2861346e6e5c4037317a2130493e3d476a783c452b6f565d2752641f382c54682a655f62217132753a6765414b4a76204e2a', 
#'1c4b66593b57474078446a23785f2a504d6b117f2b3f6f62335c767818793556284b7f3954335650791f5b7c5a5604763f13286a2730025e65764a5061253d7904616f34787f6125303c67435b2c7e7c312206687e496a773542323c515d39133b5e273d1f10', 
#'035d6a4b775b50047d442e737d5e374a44275571717b6d2e3c157a744a6f3f5620077f394561574060565a395f000a67225a2f337d34581f28605211676029650e6d207a757c6d253321725f432c7e62302d4a3054', 
#'16437a03765f0251740160666a4c354a0865486a716561202f54783f577f643d', 
#'194a7c4b7a56024c6101676b6648270358755868346c706227156d31426f2b5e6007686a4233554033494f6951560476335f637e7d25565e29254d542d6d22274166207a736b28683e2226465a3f3f7a2b2e4f3e2b4e776c305964355b18205632542a785a753a7b4f29611e', 
#'1d4a7103685f024a6f01636d6d0d334c4c6e477b3b3e2430385e77744b67304322423013', 
#'014a654e721a514d2e5577236e4c394c446c4832717c6b622e503b2259782c173a076c7c4977545c784a18394e5208613a5c63697d3a464f2a735b55230f', 
#'1c5d7e4f3b504b04785b6f6f240d2d464b6f5072716d6b38395077354c2a35583e467a775e33575d765116781e53007f76466371383f02493c66555061296d6f0e6e3a3e317c6d763321745559347e7f2578566c3f41703853', 
#'04406b557a1a51412e4561776343364f086d547a71756128345673744a7e301b6c5d7f7a467f1845664c597b57544173765c2d7e7d37474565615b5265706d7b0061233b3179287f3e236f1e3f', 
#'1d4a7b4d74524d046a4f6b2f2846275a5227476722737d6227543b274e73285e6c5d7f75426951417c4c4274570c4173344a636c3875491f33605d547f706d7100762a7a6760697132227f10513a33646878487f2d4e6136295f212b1a4e26523c542a785e7e3f67492b3975242c2667214352517d2a044e454b7425701756647956006d7f64235570712c2c575977082a4f707e7978773e5217', 
#'075d7650775502566f4f6123690d300360685f643e6a243138593b3a592a29583a076c6045724a15721f5a76484502323e5f2a7b3c39025b30681e502d6a2f7815643d3b677364253127625c5a7b54', 
#'16437a03705e5b5e2e517c6a7b4122034362116d25706837711575314e70245b2d076d700772565c334c596c4d540e323713297a3375524d2473575d6c25036a122522337d7d7b7132387f106534303d6433527b2c5b387b374864391a4c31133e5a293111602e6b422d39753c2c267a2c0a5e4d632a144500426125640c17737743436d7778304e65386e69584e7e0829536327237e61214558'
#]
ciphers = [
'07403f4c794843407b017d66285926404027427b226b2431314061315a642c5c39076e6b4e7d5b5c334f5972524f0f7b3a5c6f3f282f024f377c1e5b6825236e03702b3f31686975343a7455573c72312578527f350268792d4c2c21554d74572953732b477f3b6d476e6f642269327c2c4704577065164553537469650817746053492e7a756655662b2e26404372442201787e737a713c5017', 
'1b4a6903685f02496b4d2e6d6d4727514171543e3a3f6b2135406f3a597c2459250b3e7807785c4c691f403950450c322c5e2a6538394d1f357052116064377e41613d3b797d6b60352063585a7528782a390a3e2d52777d364721215f18275668503f314b743a640a236f6635673a2811454c48706502590050776a2143762762585e3877792a077a3a2e2c454e72432457707e6d69683e5d5e', 
'045b7e51621a51416a4d6f68284b22514975583e3e3f773438583b2741642a41250774705d33555b7c57533948591160374526737175485e2e2550502d6b2861416f2a3e7f7d606a7b2a685515252c74323d427b7e417d7a200d292e505d20562313733250716f6a5f262a343d6522282f4f404a7a2d0f00444d7e257a0244737359456134716653683a6222515961083d526d317678713e5a17', 
'034e3f507e1a4b4c60446a237d572751497158723033242331503b3f5c733f173f4e3e734e334e5a795e5d394e52007e7649223f27304c4a6925545066252f720d6a6f297d7b6a6035212a104527316525304a3e3550797a79422623535b3159641f232a5e6e20724f6235713e65356065474148352a105241557f70201047666659496d6771325e25712369474570446701633b23637c3d1354', 
'034e74463b404b507c402e706d0d21564c62423e3c767062395a79265d246545294c723977764c473365576a5b000b61335e636b347556502d6a1e596261236e41753d337f777b69756e56425c3b3d743e36473e3c5b38643849256f4c5d3056245e7f785e7e247d4e623b7b707a256d655a4b477d241a490c037a6965435869325d456d7a7925076734302c5e4c37082a4239286664753b1347', 
'1c4b66593b5e4d566f5b676f610163485a665d3e227a24343859763d187024452d43716f467f1854334d537252002f6b385a636a27755156656a5a1179602f6e416b2a3864767d2535276d544c7530782778566c3f5636360a48286f511824412151303d4b742a284b623d713b6076432a485d486c65090056517a6b6908176d6158596d7a71664968353426474937082558773723667d3f464d', 
'034e72036b5556566b4d2e71675d3650416a116d3d767e2730156820597826583a5e3e76447a1854334f57721e4d1432245c336a3e3d571f376a44457f6c3e7f08696f3531716d69346226514f752d74642a49642e506b7d354c64215b18205a3b5630785a753a7b41376f75707f2269374f47046365145500517a6b7543416e7652406d60712d076330312750007149204e393567716b3b1d3d', 
'034a7157741a464b7b476f6f240d39460871427b32776a3b7d5b7a24596e2b5e275e3e76436159517a131678524541622456306b3275515a656b5b5a626924604167233b797d7e7c38262640473c30723178493e2a4776363242313c5f5374432754262b587620240a23237170613f7b31450457353512494e407e7f6e0c422b3244402c62792a4e2927273a504c705d6b527c7e797d7a334758', 
'1d4a7b4d74524d046a4f6b2f2846275a5227476722737d6227543b274e73285e6c5d7f75426951417c4c4274570c4173344a636c3875491f33605d547f706d7100762a7a6760697132227f10513a33646878487f2d4e6136295f212b1a4e26523c542a785e7e3f67492b3975242c2667214352517d2a044e454b7425701756647956006d7f64235570712c2c575977082a4f707e7978773e5217', 
'16437a03705e5b5e2e517c6a7b4122034362116d25706837711575314e70245b2d076d700772565c334c596c4d540e323713297a3375524d2473575d6c25036a122522337d7d7b7132387f106534303d6433527b2c5b387b374864391a4c31133e5a293111602e6b422d39753c2c267a2c0a5e4d632a144500426125640c17737743436d7778304e65386e69584e7e0829536327237e61214558'
]

word_list = ['byt', 'ten', 'ktery', 'mit', 'jeho', 'ale', 'svuj', 'jako', 'moci', 'rok', 'pro', 'tak', 'tento', 'kdyz', 'vsechen', 'jak', 'aby', 'nebo', 'rici', 'jeden', 'jen', 'muj', 'jenz', 'clovek', 'stat', 'muset', 'velky', 'chtit', 'take', 'nez', 'jeste', 'pri', 'jit', 'pak', 'pred', 'dva', 'vsak', 'ani', 'vedet', 'novy', 'hodne', 'podle', 'dalsi', 'cely', 'jiny', 'prvni', 'mezi', 'dat', 'tady', 'den', 'tam', 'kde', 'doba', 'kazdy', 'druhy', 'misto', 'dobry', 'takovy', 'strana', 'protoze', 'nic', 'zacit', 'neco', 'zivot', 'videt', 'rikat', 'zeme', 'dite', 'maly', 'sam', 'bez', 'ruka', 'svet', 'dostat', 'prace', 'nejaky', 'proto']

#c1 = '160a0d001a0000' #neconic
#c2 = '19070105171c10' #ahojcus

################################################################################

#functions
################################################################################
def strip_accents(s):
    return ''.join(c for c in ud.normalize('NFD', s) if ud.category(c) != 'Mn')

def xor_ciphers(ciphers):
    ordlists = [en.hexListToIntList(en.stringToHexList(cip)[::2]) for cip in ciphers]
    return [en.listXOR(ordlists[0], ordlist) for ordlist in ordlists[1:]]

def create_word_list(dict_file):
    word_list = []
    with open(dict_file, 'r') as f:
        word_list = f.read().splitlines()
    return [strip_accents(word).lower() for word in word_list]
################################################################################

if __name__ == "__main__":
    xor_list = xor_ciphers(ciphers)
    shortest = min([len(i) for i in xor_list])

    word_set = frozenset(create_word_list(dict_file))
    word_list = sorted(list(word_set), key = len, reverse = True)

    print('{} ciphers, {} shortest'.format(len(xor_list), shortest))
    for word in word_list:
        word = ' ' + word + ' '
        word = en.stringToOrdList(word)
        for offset in range(shortest - len(word) + 1):
            printable = True
            for xor in xor_list:
                m_xor = en.ordListToString(en.listXOR(word, xor[offset:]))
                if not re.match(r'^[A-Z "\'.,?!]+$', m_xor, re.ASCII | re.IGNORECASE):
                #if not m_xor.isprintable():
                    printable = False
            if printable:
                print(word, offset)
                for xor in xor_list:
                    print('\t', en.ordListToString(en.listXOR(word, xor[offset:])))
