# 项目名称

[![GitHub](https://img.shields.io/github/license/username/repo)](https://github.com/username/repo/blob/main/LICENSE)
[![Build Status](https://img.shields.io/travis/username/repo/master)](https://travis-ci.org/username/repo)
[![Code Coverage](https://img.shields.io/codecov/c/github/username/repo)](https://codecov.io/gh/username/repo)

## 目录

- [简介](#简介)
- [功能](#功能)
- [技术栈](#技术栈)
- [安装](#安装)
- [使用](#使用)
- [贡献](#贡献)
- [许可证](#许可证)
- [联系](#联系)
- [致谢](#致谢)

## 简介
基于python的优必选舵机控制器，使用串口链接优必选总线舵机


## 功能

- 特性1：多个舵机分别控制，包括时间，角度，名称（不同id）
- 特性2：可以在打印界面中查看舵机的执行代码（可以直接复制到Arduino IDE中执行）
- 特性3：多个预设保存，点击记录可以记录当前的所有舵机信息，发送按钮一键发送
- 特性4：可以设置舵机的初始位置，在初始化时，舵机会自动回到初始位置
- 特性5：可以点击并发按钮一键发送当前所有舵机的信息
- 特性6：预设即使关掉软件也会保存，只有再次覆盖才会消失
- 特性7：可以个性化ui界面

## 技术栈

- 主要编程语言：Python
- 框架/库：PyQt, serial (用于串口通信)，servo(用于控制舵机)


## 安装

### 前置条件

- Python 3.x
- pip (Python包管理器)
- PyQt5 (用于GUI（5.12.3）)

### 步骤

1. 克隆仓库：
<pre>
git clone https://github.com/yourusername/yourproject.git
</pre>

2. 进入项目目录：
<pre>
cd yourproject
</pre>
3. 在此之前，请确保你已经安装了Python和pip，并且安装了必要的库
<pre>
pip install PyQt5
pip install serial
pip install .......
</pre>
4. 开始使用：
<pre>
python main.py   
</pre>  
## 使用

### 或者下载仓库后打开   *src-serial\build\exe.win-amd64-3.10\main.exe*的文件直接双击执行

## 贡献

欢迎贡献者！如果你想要为这个项目做出贡献，请遵循以下步骤：

1. 叉子(Fork)这个项目。
2. 创建一个新的分支来实现你的功能或修复错误。
3. 提交更改并推送到你的仓库。
4. 发起一个拉取请求(Pull Request)。

## 许可证

这个项目遵循MIT许可证。详情见[LICENSE](LICENSE)文件。

## 联系

如果有任何问题或建议，请通过以下方式联系我们：

- 邮箱：uf4hp@foxmail.com
- GitHub：@UF4OVER


## 致谢

感谢以下项目和人员对本项目的支持和启发：

- 1455067237@qq.com（王先生）：用于建议的提出与内测
