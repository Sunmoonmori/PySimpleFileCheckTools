import os
import zipfile
import rarfile


def dfs(path):
    count_f = 0
    count_z = 0
    count_r = 0
    count_p = 0
    dirs = os.listdir(path)
    for i in dirs:
        tmp = os.path.join(path, i)
        try:
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
                        info_list = z.infolist()
                    for item in info_list:
                        if item.flag_bits & 0x01:
                            print('!!! "' + tmp + '"')
                            count_p += 1
                            break
                elif tmp[-4:] == '.rar':
                    count_r += 1
                    try:
                        with rarfile.RarFile(tmp) as r:
                            if r.needs_password():
                                print('!!! "' + tmp + '"')
                                count_p += 1
                    except rarfile.NeedFirstVolume:
                        print('??? "' + tmp + '"')
            else:
                count_f += 1
                print('[unknown type]', tmp)
        except PermissionError:
            print('[PermissionError]', tmp)
        except FileNotFoundError:
            print('[FileNotFoundError]', tmp)
    return count_f, count_z, count_r, count_p


if __name__ == '__main__':
    file_number, zip_number, rar_number, password_number = dfs('.' + os.sep)
    print('\n"!!!" means the file needs password.')
    print('"???" means this file is not the first volume.')
    print('"[unknown type]" and "[FileNotFoundError]" may be because the directory name is too long.')
    print('\nfile number: %d\nzip number: %d\nrar number: %d\nneed password number: %d'
          % (file_number, zip_number, rar_number, password_number))
