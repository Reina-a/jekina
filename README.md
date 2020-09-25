# jekina (on wsl)
## 一、 简介

tututuutuutu

不使用图床的情况下, 不妨使用jekina在本地保存博客中的图片

冲突!!!


功能介绍视频请前往[我的博客](http://reina.link/posts/jekina-readme/index.html)

## 二、 安装

当前jekina只有WSL(Windows Subsystem for Linux)版本, 后续会开发Windows版本

WSL版本需要的准备工作:

- Windows应用商店中任意版本的Ubuntu(WSL)
- WSL下的Python3环境
- 安装pyperclip模块: `pip3 install pipyerclip`

准备好环境后, 将仓库的所有文件下载到任意文件夹中即可

## 三、 配置

切换到jekina所在的文件夹下, 直接运行脚本`./jekina.py`即可

初次运行会生成`settings.json`配置文件, 请根据引导完成配置

配置文件对于jekina来说至关重要, 请确保配置文件中路径的正确性

下面是一个样例:

```json
{
    "jekyll_home": "/mnt/c/Users/Reina/OneDrive/Chirpy/",
    "asset_paths": {
        "image": "assets/images/",
        "file": "assets/files/",
        "audio": "assets/audio/",
        "video": "assets/video/"
    },
    "site_home": "_site/",
    "post_path": "posts/"
}
```

- `jekyll_home`保存了jekyll项目的绝对路径(是后面相对路径的基础)
- `asset_paths`保存了各个路径的信息, 文章所需的图片(文件)就保存在这些路径中
- `site_home`保存了生成网站的目录(关于`jekyll_home`的相对路径)
- `post_path`保存了网站中文章页面的保存路径(关于`site_home`的相对路径)

默认生成`image`的路径, 其他路径通过选用命令行参数`-a`, 根据提示添加

## 四、 使用

jekina支持命令行参数, 可以使用`./jekina.py -h`即可查看帮助信息

可以使用的命令行参数有:

- -h/--help: 显示帮助信息并退出
- -c/--disable-copy-path: 生成的路径不拷贝到剪切板
- -r/--disable-rename: 跳过重命名步骤
- -a/--add-path: 添加一个路径

正常进入程序后会出现jekina的命令行提示符

![prompt](http://reina.link/assets/images/2020-08-08/0808-125433.png)

可以使用的命令有:

- {Windows路径}: 实现拖动添加文件的功能(拖动文件可以自动输入其Windows路径)
- "clip": 从剪切板中添加图片
- "cd {路径名称}": 切换至指定路径
- "ls" : 查看当前路径下的文件
- "rm {需要删除的内容}" : 删除当前目录下指定文件(支持通配符)
- "pwd": 查看当前路径 
- "oie": 在Windows资源管理器中打开当前路径(open in explorer)
- "find {关键词}": 根据关键词查找已有文章(查找文件名), 生成文章所需的url 
- "sps" : 查看所有可用路径
- "quit": 退出程序


## 五、 功能完善计划

- 添加路径选择, 增强归档能力(已实现)
- 添加文章搜索功能, 快速获取站内文章链接(已实现)
- Windows版本开发
- ...

## 六、 联系作者

如果您有好的想法或者建议, 欢迎在`Issues`中与我交流

邮箱当然也可以: reinaxxxa@gmail.com
