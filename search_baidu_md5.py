import urllib.request
import urllib.parse
import json

BDUSS = ''
STOKEN = ''
APPID = ''
DIR = ''


def install():
    opener = urllib.request.build_opener()
    opener.addheaders = [('Cookie', 'BDUSS=%s; STOKEN=%s;' % (BDUSS, STOKEN))]
    urllib.request.install_opener(opener)


def get_file_list(rdir):
    file_list = []
    list_url = 'https://pan.baidu.com/api/list?dir=%s' % (urllib.parse.quote(rdir), )
    with urllib.request.urlopen(list_url) as list_req:
        list_page = list_req.read()
    page_json = json.loads(str(list_page, encoding='unicode_escape'))
    for i in page_json['list']:
        if i['isdir'] == 0:
            file_list.append(i)
        elif i['isdir'] == 1:
            file_list += get_file_list(i['path'])
        else:
            print('[unknown error1]', i['path'])
    return file_list


def get_md5(file_o):
    file = urllib.parse.quote(file_o)
    url = 'http://pcs.baidu.com/rest/2.0/pcs/file?app_id=%s&method=download&path=%s' % (APPID, file)
    with urllib.request.urlopen(url) as req:
        return req.headers['Content-Length'], req.headers['Content-MD5']


if __name__ == '__main__':
    install()
    fl = get_file_list(DIR)
    fs = 0
    for f in fl:
        content_length, content_md5 = get_md5(f['path'])
        if int(content_length) != f['size']:
            print('[unknown error2]', f['path'])
        else:
            fs += f['size']
            print('path:', f['path'])
            print('size:', f['size'])
            print('md5 :', content_md5)
            print()
    print(len(fl), 'file(s) in total |', fs, 'byte(s) in total')
