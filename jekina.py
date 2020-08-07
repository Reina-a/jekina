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

# 添加路径
if args.add_path_mode:
    settings = func.add_custom_path(settings)

# 提取配置
tar_wslpath_base_default = settings["target_path_default"]
jekpath_base_default = settings["jekyll_path_default"]
enable_date_subfolder = settings["enable_date_subfolder"]
site_base_path = settings["site_base_path"]
site_post_path = settings["site_post_path"]

# 初始化路径信息
tar_wslpath_base = tar_wslpath_base_default
jekpath_base = jekpath_base_default
curr_path_name = "default"

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


# 循环输入
while True:
    # 提示符
    prompt = "\033[1;36;40mJekina \033[0m" + "\033[1;44m " + curr_path_name + " \033[0m >> "
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
        print("\033[1;32mwsl path:\t\033[0m" + tar_wslpath_base)
        print("\033[1;32mjekyll path:\t\033[0m" + jekpath_base + '\n')
    
    # 在Windows资源管理器中打开当前文件夹
    elif user_input_split[0] == 'oie':
        func.open_in_explorer(tar_wslpath_base)
    
    # 查看当前目录下的文件
    elif user_input_split[0] == 'ls':
        os.system("ls -hs1 " + tar_wslpath_base)

    # 从剪切板保存
    elif user_input_split[0] == 'clip':
        func.save_from_clip(tar_wslpath_base, jekpath_base, args)
    
    # 切换目录
    elif user_input_split[0] == "cd": 
        if len(user_input_split) == 2:
            r1, r2, r3 = func.change_directory(user_input_split, settings)
            if r1 and r2 and r3:
                tar_wslpath_base, jekpath_base, curr_path_name = r1, r2, r3

    # 当前目录下删除文件
    elif user_input_split[0] == "rm":
        if len(user_input_split) == 2: 
            command_rm = "rm " + tar_wslpath_base + user_input_split[1]
            os.system(command_rm)

    # 查找文章
    elif user_input_split[0] == "find":
        if len(user_input_split) == 2:
            func.search_articles(site_base_path, site_post_path, user_input_split[1])

    # 从Windows路径保存
    else:
        func.save_from_winpath(tar_wslpath_base, jekpath_base, args, user_input)