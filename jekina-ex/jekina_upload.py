#!/usr/bin/env python3


from datetime import datetime, date, timedelta
from ssh_reina import SSHDialog
import os

# def get_formated_time(year, mon, day):
#     return "{:0}-{:1>2d}-{:2>2d}".format(year, mon, day)
def dayback(count):
    return date.today() + timedelta(days=-count)



def action(date_back=3):
    print("\033[1;36;40muploading jekyll, please wait for a moment...:\033[0m")
    # 设定回溯天数
    date_back = 3
    # 设定本地路径起始目录
    base_local = '/mnt/c/Users/Reina/OneDrive/Chirpy/_site/'
    # 设定服务器路径起始目录
    base_remote = '/var/www/html'
    # 得到上传的date_pack
    date_pack = []
    for i in range(date_back):
        date_pack.append(str(dayback(i)))

    # 确定上传文件夹/路径 (相对路径)
    uploads = []
    uploads.append('index.html')
    uploads.append('sitemap.xml')
    uploads.append('feed.xml')
    uploads.append('posts/')

    filenames = os.listdir(base_local)
    for filename in filenames:
        if (os.path.isdir(os.path.join(base_local, filename)) and filename.startswith("page")):
            uploads.append(filename + '/')

    # images
    img_base = 'assets/images/'
    file_base = 'assets/files/'

    for date in date_pack:
        uploads.append(img_base + date + '/')
        uploads.append(file_base + date + '/')

    dialog = SSHDialog("root", "reina.link", '/home/reina/.ssh/id_rsa')

    for relative_path in uploads:
        local_absolute_path = os.path.join(base_local, relative_path)
        remote_absolute_path = os.path.join(base_remote, relative_path)
        if(os.path.isdir(local_absolute_path)):
            dialog.send_folder(local_absolute_path, remote_absolute_path)
        else:
            dialog.send_file(local_absolute_path, remote_absolute_path)
    print("\033[1;36;40muploaded:\033[0m")



if __name__ == "__main__":
    action()

