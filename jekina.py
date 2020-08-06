#!/usr/bin/env python3

import os
import time
import shutil
import argparse
# pip3 install pyperclip
import pyperclip
# 此模块地址: https://github.com/Reina-a/develop-tools-python/blob/master/path_convertor.py
import path_convertor as pc
import json



is_first_setting = False

if not os.path.exists('./settings.json'):
    is_first_setting = True


if not is_first_setting:
    with open('settings.json','r', encoding='utf-8') as settings_file:
        settings = json.load(settings_file)
else:
    # 初始化配置文件
    settings = {}
    
    print("\033[1;31;40mNo setting file detected.\033[0m")
    print("\033[1;31;40mPlease complete your settings by following the guide.\033[0m ")
    settings["target_path_default"] = input("\033[1;36;40mThe base path to save your file (absolute linux path):\033[0m \n")
    settings["jekyll_path_default"] = input("\033[1;36;40mThe base path to write in your jekyll article (web path):\033[0m \n") 
    if not settings["target_path_default"].endswith('/'):
        settings["target_path_default"] += '/'
    if not settings["jekyll_path_default"].endswith('/'):
        settings["jekyll_path_default"] += '/'
    
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

# 提取配置文件
tar_wslpath_base = settings["target_path_default"]
jekpath_base = settings["jekyll_path_default"]
enable_date_subfolder = settings["enable_date_subfolder"]
custom_paths = {}
if "custom_paths" in settings.keys():
    custom_paths = settings["custom_paths"]


# 按照日期归档 (可选功能)
if enable_date_subfolder:
    # 获取当前日期并格式化
    formated_time = time.strftime("%Y-%m-%d", time.localtime())
    # 根据格式化的日期完善路径
    tar_wslpath_base += (formated_time + '/')
    jekpath_base += (formated_time + '/')


# 检查目标路径是否存在, 若不存在则创建
if not os.path.exists(tar_wslpath_base):
    os.makedirs(tar_wslpath_base)

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

# 添加路径模式
if args.add_path_mode:
    add_path_id = input("Please input the name of the path: \n")
    add_path_wsl = input("Enter your wsl base path of \"" + add_path_id + "\": \n")
    add_path_jek = input("Enter your jekyll base path of \"" + add_path_id + "\": \n")
    # 尾部修正
    if not add_path_wsl.endswith("/"):
        add_path_wsl += "/"
    if not add_path_jek.endswith("/"):
        add_path_jek += "/"        
    # 写入设置字典
    custom_paths[add_path_id] = (add_path_wsl, add_path_jek)
    settings["custom_paths"] = custom_paths
    # 写入配置文件
    with open('settings.json', 'w', encoding='utf-8') as settings_file:
        json.dump(settings, settings_file, indent=4, ensure_ascii=False)


# 显示当前模式
if not args.disable_copy_path:
    print("- clipboard:\tenabled")
else:
    print("- clipboard:\tdisabled")

if not args.disable_rename:
    print("- rename:\tenabled")
else:
    print("- rename:\tdisabled")


# 循环输入
while True:
    user_input = input("User input: ")
    user_input_split = user_input.split()

    # 判断是否为自定义模式
    if len(user_input_split) == 2:
        for path_name in custom_paths.keys():
            if path_name == user_input_split[0]:
                # 更改路径
                tar_wslpath_base = custom_paths[path_name][0]
                jekpath_base = custom_paths[path_name][1]
                # 按照日期归档 (可选功能)
                if enable_date_subfolder:
                    # 获取当前日期并格式化
                    formated_time = time.strftime("%Y-%m-%d", time.localtime())
                    # 根据格式化的日期完善路径
                    tar_wslpath_base += (formated_time + '/')
                    jekpath_base += (formated_time + '/')
                # 修正输入
                user_input = user_input_split[1]
                
    # 程序出口
    if user_input == 'quit':
        break
    # 从剪切板保存
    elif user_input == 'clip':
        # 检查剪切板
        check_command = r"echo .\\\\clipboard.ps1 -c | /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe >> /dev/null"
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
            command_save = r'echo .\\\\clipboard.ps1 -s ' + command_url + r' | /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe >> /dev/null'
            os.system(command_save)
            print("\033[1;32;40mPicture on the clipboard has been saved!\033[0m")

            # 打印jekyll的路径
            print(jekpath)
            
            if not args.disable_copy_path:
                # 把jekyll的路径复制到剪切板
                pyperclip.copy(jekpath)
                print("\033[1;32;40mJekyll path has been copied to the clipboard!\033[0m\n")
                continue
        else:
            print("\033[1;31;40mError occurred, please check your clipboard (Image Supported Only)\033[0m\n")
            continue
    # 使用Windows路径
    else:
        src_winpath = user_input
        # 将得到的windows路径转化为相应的wsl路径
        src_wslpath, filename = pc.abs_win2wsl(src_winpath, pc.FILE_MODE)

        # 如果路径错误, 进入下个循环 (path_convertor内置报错)
        if not src_wslpath:
            print("")
            continue

        src_wslpath += filename

        # 检查文件是否存在, 不存在则报错
        if not os.path.exists(src_wslpath):
            print("\033[1;31;40mFile not exists, please check your input. \033[0m")
            print("\033[1;31;40mIt is re    commended to drag the file into the terminal directly. \033[0m\n")
            continue

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