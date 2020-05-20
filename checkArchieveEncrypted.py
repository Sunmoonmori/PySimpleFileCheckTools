import os
import zipfile
import rarfile


def dfs(path):
    count_f = 0
    count_z = 0
    count_r = 0
    count_p = 0
    try:
        dirs = os.listdir(path)
        for i in dirs:
            tmp = os.path.join(path, i)
            if os.path.isdir(tmp):
                rtf, rtz, rtr, rtp = dfs(tmp)
                count_f += rtf
                count_z += rtz
                count_r += rtr
                count_p += rtp
            elif os.path.isfile(tmp):
                count_f += 1
                if tmp[-4:] == '.zip':
                    count_z += 1
                    with zipfile.ZipFile(tmp) as z:
                        for item in z.infolist():
                            if item.flag_bits & 0x01:
                                print('!!! "' + tmp + '"')
                                count_p += 1
                                break
                elif tmp[-4:] == '.rar':
                    count_r += 1
                    try:
                        with rarfile.RarFile(tmp) as z:
                            if z.needs_password():
                                print('!!! "' + tmp + '"')
                                count_p += 1
                    except rarfile.NeedFirstVolume:
                        print('??? "' + tmp + '"')
            else:
                print('[unknown error]', tmp)
                count_f += 1
    except PermissionError:
        print('[PermissionError]', path)
    return count_f, count_z, count_r, count_p


if __name__ == '__main__':
    print('start')
    _rtf, _rtz, _rtr, _rtp = dfs('./')
    print('\n"!!!" means the file needs password.\n"???" means this file is not the first volume.')
    print('\nfile number:', str(_rtf) + '\nzip number:', str(_rtz) + '\nrar number:', str(_rtr)
          + '\nneed password number:', str(_rtp))
