[pyenv](https://github.com/pyenv/pyenv) 能管理python解释器的版本和虚拟环境的版本

### 下载pyenv源码
找一个合适的目录，例如$HOME，即当前用户的家目录
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
下载完成后，输入ls查看当前目录的文件，是看不到pyenv的，因为.开头的目录被隐藏了，可以cd到.pyenv查看

### 配置环境变量
下载完成pyenv之后，要想在任意目录下都能使用pyenv命令，还需要配置环境变量
打开rc文件，例如.zshrc 或者.bashrc
在其中加入以下内容
```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```
添加完毕之后，在终端使用 ```source .bashrc``` 让上面的配置生效

### 验证是否安装成功
终端输入 ```pyenv --version```

显示 ```pyenv 2.3.36-3-gf9a2bb81``` 相似输出表示安装成功

### 使用pyenv管理python的版本
- 显示已有版本```pyenv versions``` 展示已有的python版本（不是由pyenv下载的不会显示）
- 下载新的python解释器 ```pyenv install --list``` 查看所有可下载的版本
- 下载指定的版本 ```pyenv install 3.10.10```

直接使用该命令下载，由于网络原因会很慢。

自己将源码包下载到正确的（pyenv能找到的目录）即可。

网络不好的只能从[Python版本大全导航页](https://www.python.org/downloads/source/)选择适合的版本下载，下载为tar.xz 放到.pyenv/cache中

放好之后再次执行 ```pyenv install 3.x.x``` 这里的3.x.x要和下载的版本号一致
若安装失败，可能是缺少python编译的 [依赖](https://github.com/pyenv/pyenv/wiki) ，ubuntu可如下

``` shell
sudo apt-get install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

```shell
pyenv versions
* system (set by /home/gyl/.pyenv/version)
  3.10.13
```

设定全局版本
```pyenv global 3.10.13```

### 虚拟环境管理插件安装

[pyenv virtualenv](https://github.com/pyenv/pyenv-virtualenv)

```
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

```
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```

重启shell 即可使用

### 创建虚拟环境

```
pyenv virtualenv 3.10.13 env_name
```
这个命令会在.pyenv/versions/下创建一个名为env_name的虚拟环境

使用 pyenv activate|deactivate激活 退出虚拟环境