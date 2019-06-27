import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
import easygui
import os
import configparser
import urllib

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config.ini")
conf = configparser.ConfigParser()
conf.read(cfgpath, encoding="utf-8")
sections = conf.sections()
items = conf.items('user')
username = items[0][1]
userpassed  = items[1][1]

session = requests.session()

fileup_url = r'http://up.woozooo.com/fileup.php'
login_url = r'https://up.woozooo.com/account.php'
mydisk_url = r'https://up.woozooo.com/doupload.php'
url_api = 'http://1787005804808765.cn-shanghai.fc.aliyuncs.com/2016-08-15/proxy/lanzous/api/'

login_data = {
    "action": "login",
    "task": "login",
    "ref": "https://up.woozooo.com/",
    "formhash": "0af1aa15",
    "username": username,
    "password": userpassed,
}

mydisk_data = {
    "task": "5",
    "folder_id": "-1",
    "pg": "1",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

login_json = session.post(url=login_url, data=login_data, headers=headers).text
# mydisk_json = session.post(url=mydisk_url, data=mydisk_data, headers=headers).json()
# print(mydisk_json)

def fileup(file_path,filename):
    print("正在上传： "+filename)
    filename = urllib.parse.quote(filename)
    fileup_headers = {
        "Accept": "* / *",
        "Accept - Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Origin": "https://up.woozooo.com",
        "Referer": "https://up.woozooo.com/mydisk.php?item=files&action=index",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    multipart_encoder = MultipartEncoder(
        fields={
            "task": "1",
            "folder_id": "-1",
            "id": "WU_FILE_0",
            "name": filename,
            "type": "application/octet-stream",
            # "lastModifiedDate": "Thu Jun 27 2019 12:11:16 GMT 0800 (中国标准时间)",
            # "size": "185",
            'upload_file': (filename, open(file_path, 'rb'), 'application/octet-stream')
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    fileup_headers['Content-Type'] = multipart_encoder.content_type
    fileup_json = session.post(url = fileup_url, data=multipart_encoder, headers=fileup_headers).json()
    if fileup_json['zt'] == 1:
        print(filename+" 上传成功")
    return fileup_json
# , filetypes = ['apk','zip','rar','txt','7z','z','e','ct','doc','docx','exe','ke','tar','db','pdf','w3x']

def download_link(f_id):
    url = url_api+'?url=https://www.lanzous.com/'+str(f_id)
    session = requests.session()
    return session.get(url=url).json()



files_list = easygui.fileopenbox(multiple = True)

download_links = ''
for file in files_list:
    name = os.path.basename(file)
    res = fileup(file,name)
    # {'zt': 1, 'info': '上传成功', 'text': [
    #     {'icon': 'rar', 'id': '9691414', 'f_id': 'i4qowxe', 'name_all': '1.rar', 'name': '1.rar', 'size': '185.0 B',
    #      'time': '0 秒前', 'downs': '0', 'onof': '0', 'is_newd': 'https://www.lanzous.com'}]}
    if res['zt'] == 0:
        print("上传失败: %s" %res['info'])
    else:
        text = res['text'][0]
        icon = text['icon']
        id = text['id']
        f_id = text['f_id']
        name_all = text['name_all']
        name = text['name']
        size = text['size']
        downs = text['downs']
        onof = text['onof']
        is_newd = text['is_newd']
        download_data = download_link(f_id)
        if download_data['code'] ==200:
            download_links = download_links + download_data['data']['downUrl'] + '\n'
            with open('download_links.txt', 'a+', encoding='utf-8') as f:
                f.write(str(download_links))
                print('下载连接已保存在download_links.txt文件'+'\n')


easygui.textbox(msg="把下面的下载链接复制到迅雷或者其他下载器即可下载", title="123 ", text=download_links,
                codebox=False, callback=None, run=True)

