import re
import json


def haha(vtext, cidtext):

    ciddict_file = 'ciddict.json'

    with open(ciddict_file) as json_file:
        ciddict = json.load(json_file)

    # print(ciddict)

    print('-------')
    cidtext = cidtext.replace('(cid:', '')
    cids = cidtext.rsplit(')')[:-1]
    # ciddict = dict()
    for i, cid in enumerate(cids):
        ciddict['(cid:' + cid + ')'] = vtext[i]

    with open(ciddict_file, 'w') as outfile:
        json.dump(ciddict, outfile)

    print(ciddict)
    return 'haha'


if __name__ == '__main__':
    vtext = ('ỵ')
    cidtext = ('(cid:1271)')
    haha(vtext, cidtext)
