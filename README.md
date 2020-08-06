# jekina
## 一、 简介

jekina是以方便jekyll博客撰写为目的开发的实用脚本工具

当前支持的功能有:

- 拖动添加文件、生成文章所需链接
- 从剪切板快速添加图片、生成文章所需链接

## 二、 安装

当前jekina只有WSL(Windows Subsystem for Linux)版本, 后续会开发Windows版本

WSL版本需要的准备工作:

- Windows应用商店中任意版本的Ubuntu(WSL)
- WSL下的Python3环境
- 安装pyperclip模块: `pip3 install pipyerclip`

准备好环境后, 将仓库的所有文件下载到任意文件夹中即可

## 三、 使用

切换到jekina所在的文件夹下, 直接运行脚本`./jekina.py`即可

初次运行会生成`settings.json`配置文件, 请根据引导完成配置

![初始化配置](http://reina.link/assets/images/2020-08-06/init.png)

jekina支持命令行参数, 使用`./jekina.py -h`即可查看帮助信息, 例如: 

```
usage: jekina.py [-h] [-c] [-r]

Move files to your jekyll hub, and provide the url you need for your site
(print & clipboard)

optional arguments:
  -h, --help            show this help message and exit
  -c, --disable-copy-path
                        do not copy jekyll paths to the clipboard
  -r, --disable-rename  do not rename the file
```

在运行jekina后, 会根据用户的命令行选项显示当前的模式 

![显示模式](http://reina.link/assets/images/2020-08-06/0806-094946.png)

`User input`是最主要的输入, 它可以是以下几种情况

- "quit": 退出程序
- "clip": 实现从剪切板添加图片的功能
- Windows路径: 实现拖动添加文件的功能(拖动文件可以自动输入其Windows路径)


### 功能演示

README无法添加视频, 演示视频请移步[丽奈的技术栈-jekina文档](http://reina.link/posts/jekina-readme/)

## 三、 功能完善计划

- 添加路径选择, 增强归档能力
- 添加文章搜索功能, 快速获取站内文章链接
- 添加轻量上传功能, 轻松更新站点
- Windows版本开发
- ...

## 四、 联系作者

如果您有好的想法或者建议, 欢迎在`Issues`中与我交流

邮箱当然也可以: reinaxxxxa@gmail.com
