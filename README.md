# LanZouCloud
蓝奏云批量上传
    介绍：
              利用Python上传文件到蓝奏云，easygui实现gui选择文件，然后批量上传到自己的蓝奏云盘，生成下载直链，复制到迅雷或者其他下载器进行下载（直链有效期只有30多分钟）。
使用方法：
              下载文件，编辑config.ini，填入用户名和密码（不要用单引号或者双引号），再打开exe会出现文件选择框（可以多选文件）就可以上传了，然后出现生成的下载直链，保存在download_links.txt里，注意每次上传都会刷新这个文件（只保留当前直链信息）。
               允许上传类型:
                            doc,docx,zip,rar,apk,ipa,txt,exe,7z,e,z,ct,ke,cetrainer,db,tar,pdf,w3x
                            epub,mobi,azw,azw3,osk,osz,xpa,cpk,lua,jar,dmg,ppt,pptx,xls,xlsx,mp3
                            ipa,iso,img,gho,ttf,ttc,txf,dwg,bat,dll
已知bug：
              1.虽然能上传带中文名的文件，但会改成UrlEncode编码，因为不能上传带中文名的文件所以该成非中文的文件名，建议修改成英文名上传。
缺陷：              
              1.没有因网络问题上传失败而进行重新上传。
暂时就写到这里 ，以后有时间慢慢完善，欢迎star和pull。

