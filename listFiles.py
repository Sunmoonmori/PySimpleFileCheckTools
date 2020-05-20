import os


def dfs(path, f):
    count_f = 0
    count_d = 0
    try:
        dirs = os.listdir(path)
        for i in dirs:
            tmp = os.path.join(path, i)
            if os.path.isdir(tmp):
                rtf, rtd = dfs(tmp, f)
                count_f += rtf
                count_d += rtd + 1
            elif os.path.isfile(tmp):
                f.write(tmp + ',' + str(os.path.getsize(tmp)) + '\n')
                count_f += 1
            else:
                print('[unknown error]', tmp)
                f.write(tmp + ',' + str(os.path.getsize(tmp)) + '\n')
                count_f += 1
    except PermissionError:
        print('[PermissionError]', path)
    return count_f, count_d


if __name__ == '__main__':
    _f = open('listFiles.csv', 'w', encoding='utf-8')
    _rtf, _rtd = dfs('./', _f)
    print('\nfile number:', str(_rtf) + '\ndir number:', str(_rtd))
    _f.close()
