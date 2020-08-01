import re

FOLDER_MODE = 0
FILE_MODE = 1

def abs_wsl2win(abs_linux_path: str, mode: int):
    
    # WSL共享目录的正则表达式
    # 另: 合法Linux路径的正则表达式为 ^\/(\w+\/?)+$
    wsl_re = r'^/mnt/([a-z])/([^/]+/)*[^/]+/?$'

    # 路径中盘符右边的部分
    # 如对于'mnt/c/workspace/python/', 右边的部分是'/workspace/python/'
    wsl_re_right = r'/([^/]+)'
    
    # 编译后的正则表达式
    wsl_re_c = re.compile(wsl_re)
    wsl_re_right_c = re.compile(wsl_re_right)

    # 判断是否为合法的Linux路径
    if not wsl_re_c.match(abs_linux_path):
        print("ERROR: illegal absolute WSL share path")
        return None, None

    else:

        # 使用match & group提取盘符
        drive_letter = wsl_re_c.match(abs_linux_path).group(1)
        win_path = drive_letter.upper() + ':'

        # 使用findall捕获盘符下目录层次
        # 如对于'/mnt/c/workspace/python/', 捕获到的是['workspace','python']
        result_right = wsl_re_right_c.findall(abs_linux_path[6:])

        if mode == FOLDER_MODE:
            
            # 文件夹模式
            for node in result_right:
                win_path += ('\\' + node)

            # 结尾与输入保持一致
            if abs_linux_path.endswith('/'):
                win_path += '\\'
            return win_path, None

        elif mode == FILE_MODE:
            
            # 文件模式
            # 将文件名排除路径
            for node in result_right[:-1]:
                win_path += ('\\' + node)

            # 结尾为'\'
            win_path += '\\'

            # 提取文件名
            filename = result_right[-1]
            return win_path, filename

        else:

            # 模式错误
            return None, None

def abs_win2wsl(abs_win_path: str, mode: int):
    
    # windows本地磁盘驱动器合法路径的正则表达式
    win_re = r'^([a-zA-Z]):\\([^\\/:*?"<>|\r\n]+\\?)*$'
    win_re_right = r'([^\\/:*?"<>|\r\n]+)\\?'
    
    # 将正则表达式进行编译
    win_re_c = re.compile(win_re)
    win_re_right_c = re.compile(win_re_right)

    # 判断是否为合法的windows本地路径
    if not win_re_c.match(abs_win_path):
        print("ERROR: illegal windows absolute path")
        return None, None

    else:
        
        # 获取盘符
        driver_letter = win_re_c.match(abs_win_path).group(1)
        # 初始化WSL路径
        wsl_path = '/mnt/' + driver_letter.lower()
        
        # 使用findall捕获盘符下目录层次
        # 如对于'C:\workspace\python\', 捕获到的是['workspace','python']
        result_right = win_re_right_c.findall(abs_win_path[3:])
        
        if mode == FOLDER_MODE:
            
            # 文件夹模式
            for node in result_right:
                wsl_path += ('/' + node)

            # 结尾与输入保持一致
            if abs_win_path.endswith('\\'):
                wsl_path += '/'
            return wsl_path, None

        elif mode == FILE_MODE:

            # 文件模式
            # 将文件名排除路径
            for node in result_right[:-1]:
                wsl_path += ('/' + node)

            # 以'/'结尾
            wsl_path += '/'

            # 提取文件名
            filename = result_right[-1]
            return wsl_path, filename
        
        else:
            
            # 模式错误
            return None, None
