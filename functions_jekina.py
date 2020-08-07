import os 
import re
import argparse
import json
import time
import path_convertor as pc
import pyperclip
import shutil

powershell_path = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
explorer_path = "/mnt/c/Windows/explorer.exe"

def search_articles(site_base_path: str, site_post_path: str, search_string: str) -> list:
    post_urls= []
    for root, ___, files in os.walk(site_base_path + site_post_path):
        for filename in files:
            post_urls.append(os.path.join(root, filename)[(len(site_base_path) - 1):])
    regex = ".*" + search_string + ".*"
    regex_c = re.compile(regex)
    find_urls = []
    for url in post_urls:
        if regex_c.match(url):
            print(url)
            find_urls.append(url)
    return find_urls

def parse_argument():
    # 解析命令行参数
    desc =  'Move files to your jekyll hub, and provide the url you need for your site (print & clipboard)'
    argument_parser = argparse.ArgumentParser(description=desc)
    argument_parser.add_argument('-c','--disable-copy-path', dest='disable_copy_path', action='store_true',
                                help='do not copy jekyll paths to the clipboard')
    argument_parser.add_argument('-r','--disable-rename', dest='disable_rename', action='store_true',
                                help='do not rename the file')
    argument_parser.add_argument('-a','--add-path', dest='add_path_mode', action='store_true',
                                help='add custom paths')                      
    args = argument_parser.parse_args()
    return args

def add_custom_path(settings: dict) -> dict:
    add_path_id = input("\033[1;36;40mPlease input the name of the path: \033[0m\n")
    add_path_wsl = input("\033[1;36;40mEnter your wsl base path of \"" + add_path_id + "\": \033[0m \n")
    add_path_jek = input("\033[1;36;40mEnter your jekyll base path of \"" + add_path_id + "\": \033[0m \n")
    # 尾部修正
    if not add_path_wsl.endswith("/"):
        add_path_wsl += "/"
    if not add_path_jek.endswith("/"):
        add_path_jek += "/"        
    # 写入设置字典
    if not "custom_paths" in settings.keys():
        settings["custom_paths"]  = {}
    settings["custom_paths"][add_path_id] = (add_path_wsl, add_path_jek)
    # 写入配置文件
    with open('settings.json', 'w', encoding='utf-8') as settings_file:
        json.dump(settings, settings_file, indent=4, ensure_ascii=False)
    return settings

def initialize() -> dict:

    # 初始化配置文件
    settings = {}
    
    print("\033[1;31;40mNo setting file detected.\033[0m")
    print("\033[1;31;40mPlease complete your settings by following the guide.\033[0m ")
    settings["target_path_default"] = input("\033[1;36;40mThe base path to save your file (absolute linux path):\033[0m \ne.g. /mnt/c/Users/Reina/OneDrive/Chirpy/assets/images/\n")
    settings["jekyll_path_default"] = input("\033[1;36;40mThe base path to write in your jekyll article (web path):\033[0m \ne.g /assets/images/\n")
    settings["site_base_path"] = input("\033[1;36;40mThe absolute path of your site: (absolute linux path):\033[0m \ne.g. /mnt/c/Users/Reina/OneDrive/Chirpy/_site/\n")
    settings["site_post_path"] = input("\033[1;36;40mThe relative path you store your post pages: (relative linux path):\033[0m \ne.g. posts/\n")
    # 末尾纠正
    for key in settings.keys():
        if not settings[key].endswith("/"):
             settings[key] += "/"
    
    while True:
        choice = input("\033[1;36;40mDo you want to put the file in a subfolder with a formatted date? (yes/no):\033[0m ").lower()
        if choice in ['yes', 'ye', 'y', 'yeah']:
            settings["enable_date_subfolder"] = True
            break
        elif choice in ['no', 'n', 'not']:
            settings["enable_date_subfolder"] = False
            break
        else:
            pass
    with open('settings.json', 'w', encoding='utf-8') as settings_file:
        json.dump(settings, settings_file, indent=4, ensure_ascii=False)
    return settings

def save_from_clip(tar_wslpath_base: str, jekpath_base: str, args):
    # 检查剪切板
    check_command = r"echo .\\\\clipboard.ps1 -c | " + powershell_path +  r" >> /dev/null"
    ret = os.system(check_command)
    
    # 如果powershell脚本正常返回 (剪切板上有图片)
    if ret == 0:
        # 为路径补充文件名 (根据命令行参数选择重命名或不重命名)
        if args.disable_rename:
            filename = time.strftime('%m%d-%H%M%S', time.localtime()) + '.png'
            tar_wslpath = tar_wslpath_base + filename
            jekpath =  jekpath_base + filename
        else:
            new_filename = input("New filename: ")
            tar_wslpath = tar_wslpath_base + new_filename    
            jekpath = jekpath_base + new_filename
        
        # 获得保存截图所需的windows路径
        tar_winpath, filename = pc.abs_wsl2win(tar_wslpath, pc.FILE_MODE)
        tar_winpath += filename

        # 调用WSL命令, 以调用PowerShell脚本(从剪切板中获取并保存图片)
        command_url = tar_winpath.replace('\\','\\\\\\\\')
        command_save = r'echo .\\\\clipboard.ps1 -s ' + command_url + r' | ' + powershell_path + r' >> /dev/null'
        os.system(command_save)
        print("\033[1;32;40mPicture on the clipboard has been saved!\033[0m")

        # 打印jekyll的路径
        print(jekpath)
        
        if not args.disable_copy_path:
            # 把jekyll的路径复制到剪切板
            pyperclip.copy(jekpath)
            print("\033[1;32;40mJekyll path has been copied to the clipboard!\033[0m\n")
    else:
        print("\033[1;31;40mError occurred, please check your clipboard (Image Supported Only)\033[0m\n")

def save_from_winpath(tar_wslpath_base: str, jekpath_base: str, args, winpath: str):
    src_winpath = winpath
    # 将得到的windows路径转化为相应的wsl路径
    src_wslpath, filename = pc.abs_win2wsl(src_winpath, pc.FILE_MODE)

    # 如果路径错误, 进入下个循环 (path_convertor内置报错)
    if not src_wslpath:
        print("")
        return

    src_wslpath += filename

    # 检查文件是否存在, 不存在则报错
    if not os.path.exists(src_wslpath):
        print("\033[1;31;40mFile not exists, please check your input. \033[0m")
        print("\033[1;31;40mIt is re    commended to drag the file into the terminal directly. \033[0m\n")
        return

    # 为路径补充文件名
    if args.disable_rename:
        tar_wslpath = tar_wslpath_base + filename
        jekpath =  jekpath_base + filename
    else:
        new_filename = input("New filename: ")
        tar_wslpath = tar_wslpath_base + new_filename    
        jekpath = jekpath_base + new_filename

    # 打印jekyll所需的路径
    print(jekpath)
    
    if not args.disable_copy_path:
        # 把jekyll所需的路径复制到剪切板
        pyperclip.copy(jekpath)
        print("\033[1;32;40mJekyll path has been copied to the clipboard! \033[0m")

    # 复制文件到目标路径
    if not os.path.exists(tar_wslpath_base):
        os.makedirs(tar_wslpath_base)
    shutil.copy(src_wslpath, tar_wslpath)
    print("\033[1;32;40mFile has been copied! \033[0m\n")

def open_in_explorer(tar_wslpath_base: str):
    tar_winpath_oie, ___ = pc.abs_wsl2win(tar_wslpath_base, pc.FOLDER_MODE)
    tar_winpath_oie = tar_winpath_oie.replace('\\','\\\\') 
    if tar_winpath_oie:
        command_oie = explorer_path + " " + tar_winpath_oie 
        os.system(command_oie)

def change_directory(user_input_split: list, settings: dict):
    custom_paths = {}
    
    tar_wslpath_base = None
    jekpath_base = None
    curr_path_name = None

    if "custom_paths" in settings.keys():
        custom_paths = settings["custom_paths"]
    for path_name in custom_paths.keys():
        if path_name == user_input_split[1]:
            # 更改路径
            tar_wslpath_base = custom_paths[path_name][0]
            jekpath_base = custom_paths[path_name][1]
            curr_path_name = path_name
            # 按照日期归档 (可选功能)
            if settings["enable_date_subfolder"]:
                # 获取当前日期并格式化
                formated_time = time.strftime("%Y-%m-%d", time.localtime())
                # 根据格式化的日期完善路径
                tar_wslpath_base += (formated_time + '/')
                jekpath_base += (formated_time + '/')
            # 进入下一个输入
            break
    if user_input_split[1] == "default":
        tar_wslpath_base = settings["target_path_default"]
        jekpath_base = settings["jekyll_path_default"]
        curr_path_name = "default"
        if settings["enable_date_subfolder"]:
            # 获取当前日期并格式化
            formated_time = time.strftime("%Y-%m-%d", time.localtime())
            # 根据格式化的日期完善路径
            tar_wslpath_base += (formated_time + '/')
            jekpath_base += (formated_time + '/')

    return tar_wslpath_base, jekpath_base, curr_path_name