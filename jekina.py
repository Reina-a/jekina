#!/usr/bin/env python3

import os
import time
import shutil
# pip3 install pyperclip
import pyperclip
# 此模块地址: https://github.com/Reina-a/develop-tools-python/blob/master/path_convertor.py
import path_convertor as pc
import json
import functions_jekina as func

# 解析命令行参数                     
args = func.parse_argument()

# 加载配置
settings = {}
if os.path.exists('./settings.json'):
    with open('settings.json','r', encoding='utf-8') as settings_file:
        settings = json.load(settings_file)
else:
    settings = func.initialize()
formated_time = time.strftime("%Y-%m-%d", time.localtime())

# 添加路径
if args.add_path_mode:
    settings = func.add_custom_path(settings)
    exit(0)

# 提取配置
jekyll_home = settings["jekyll_home"]
asset_paths = settings["asset_paths"]
site_home = settings["site_home"]
post_path = settings["post_path"]

# 初始化路径信息
curr_path = jekyll_home + asset_paths["image"] + formated_time + '/'
jek_path = '/' + asset_paths["image"] + formated_time + '/'
curr_path_id = "image"


# 循环输入
while True:
    # 提示符
    prompt = "\033[1;36;40mJekina \033[0m" + "\033[1;44m " + curr_path_id + " \033[0m >> "
    user_input = input(prompt)
    user_input_split = user_input.split()
    # 处理空输入
    if len(user_input_split) == 0:
        continue

    # 程序出口
    if user_input_split[0] == 'quit':
        break
    
    # 查看当前路径
    elif user_input_split[0] == 'pwd':
        print("\033[1;32mwsl path:\033[0m\t" + curr_path)
        print("\033[1;32mjekyll path:\033[0m\t" +  jek_path + '\n')
    
    # 在Windows资源管理器中打开当前文件夹
    elif user_input_split[0] == 'oie':
        # debug
        print(curr_path)
        func.open_in_explorer(curr_path)
    
    # 查看当前目录下的文件
    elif user_input_split[0] == 'ls':
        if not os.path.exists(curr_path):
            os.makedirs(curr_path)
        os.system("ls -hs1 " + curr_path)

    # 从剪切板保存
    elif user_input_split[0] == 'clip':
        func.save_from_clip(curr_path_id, settings, args, formated_time)
    
    # 切换目录
    elif user_input_split[0] == "cd": 
        if len(user_input_split) == 2:
            ret = func.change_directory(user_input_split, settings)
            if ret:
                curr_path_id = ret
                curr_path = jekyll_home + asset_paths[curr_path_id] + formated_time + "/"
                jek_path = "/" + asset_paths[curr_path_id] + formated_time + "/"

    # 当前目录下删除文件
    elif user_input_split[0] == "rm":
        if len(user_input_split) == 2: 
            command_rm = "rm " + curr_path + user_input_split[1]
            os.system(command_rm)

    # 查找文章
    elif user_input_split[0] == "find":
        search_string = user_input_split[1]
        if len(user_input_split) == 2:
            func.search_articles(settings, search_string)

    # 查看所有路径
    elif user_input_split[0] == "sps":
        for path_id in asset_paths.keys():
            print("\033[1;32m" + path_id + ":\033[0m\t" + asset_paths[path_id])

    # 从Windows路径保存
    else:
        func.save_from_winpath(user_input, curr_path_id, settings, args, formated_time)