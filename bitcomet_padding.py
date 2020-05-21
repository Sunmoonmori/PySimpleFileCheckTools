import os

index = 0
btorrent = bytes()


def bstring():
    global index
    s_len = 0
    while btorrent[index] != ord(':'):
        s_len = s_len * 10 + btorrent[index] - ord('0')
        index += 1
    index += 1
    try:
        s_ret = str(btorrent[index:index + s_len], encoding='utf-8')
    except UnicodeDecodeError:
        s_ret = btorrent[index:index + s_len]
    index += s_len
    return s_ret


def binteger():
    global index
    index += 1
    ret = 0
    while btorrent[index] != ord('e'):
        ret = ret * 10 + btorrent[index] - ord('0')
        index += 1
    index += 1
    return ret


def blist():
    global index
    index += 1
    ret = []
    while btorrent[index] != ord('e'):
        ret.append(belement())
    index += 1
    return ret


def bdictionary():
    global index
    index += 1
    ret = {}
    while btorrent[index] != ord('e'):
        k = belement()
        v = belement()
        ret[k] = v
    index += 1
    return ret


def belement():
    if ord('0') <= btorrent[index] <= ord('9'):
        return bstring()
    elif btorrent[index] == ord('i'):
        return binteger()
    elif btorrent[index] == ord('l'):
        return blist()
    elif btorrent[index] == ord('d'):
        return bdictionary()
    else:
        print('error')


def show_keys(a, tab=0):
    for k in a:
        print(('    ' * tab) + k)
        if type(a[k]) == dict:
            show_keys(a[k], tab + 1)


def get_bt(filename):
    global index
    index = 0
    global btorrent
    with open(filename, 'rb') as file:
        btorrent = file.read()
    return belement()


if __name__ == '__main__':
    try:
        f = open('torrentFileName', 'r')
        torrentFilenames = f.read().split('\n')
        f.close()
        for fn in torrentFilenames:
            if fn == '':
                continue
            print(fn)
            bt = get_bt(fn)
            pn = fn + '_padding_files'
            if not os.path.exists('.' + os.sep + pn):
                os.makedirs('.' + os.sep + pn)
            for i in bt['info']['files']:
                if '_____padding_file_' in i['path'][-1]:
                    f = open('.' + os.sep + pn + os.sep + i['path'][-1], 'wb')
                    f.write(bytes([0] * i['length']))
                    f.close()
    except FileNotFoundError:
        f = open('torrentFileName', 'w')
        f.close()
        print('please fill the file with torrent filename, each file a line')
