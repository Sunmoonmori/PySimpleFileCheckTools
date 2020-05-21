import os


def dfs(path, f):
    count_f = 0
    count_d = 0
    total_size = 0
    dirs = os.listdir(path)
    for i in dirs:
        tmp = os.path.join(path, i)
        try:
            if os.path.isdir(tmp):
                rtf, rtd, rts = dfs(tmp, f)
                count_f += rtf
                count_d += rtd + 1
                total_size += rts
            elif os.path.isfile(tmp):
                file_size = os.path.getsize(tmp)
                f.write('%s,%d\n' % (tmp, file_size))
                count_f += 1
                total_size += file_size
            else:
                print('[unknown type]', tmp)
                file_size = os.path.getsize(tmp)
                f.write('%s,%d\n' % (tmp, file_size))
                count_f += 1
                total_size += file_size
        except PermissionError:
            print('[PermissionError]', tmp)
        except FileNotFoundError:
            print('[FileNotFoundError]', tmp)
    return count_f, count_d, total_size


if __name__ == '__main__':
    with open('list_files.csv', 'w', encoding='utf-8') as file:
        file_number, dir_number, size = dfs('.' + os.sep, file)
    print('\n"[unknown type]" and "[FileNotFoundError]" may be because the directory name is too long.')
    print('\nfile number: %d\ndir number: %d\n%.2f GB (%d Bytes) in total (with list_file)'
          % (file_number, dir_number, size / 1024 / 1024 / 1024, size))
    print('filename and filesize were written in "list_files.csv"')
