# on-chain

此项目的目的是为了获取链上数据，调用以太坊上（或BSC等）的合约

## 项目开发

### 环境设置

```shell
## 创建虚拟环境
python3.8 -m venv venv

# 使用当前项目的虚拟环境
source venv/bin/activate

# 回到默认环境
deactivate
```

### 安装依赖，指定文件`requirements.txt`

```shell
pip3.8 install -r requirements.txt
```

### 如果依赖有更新，更新`requirements.txt`

```shell
pip3.8 freeze > requirements.txt
```

### 测试是否能够启动成功，此命令只限于开发环境

```shell
# 使用默认端口
python manage.py runserver --settings "onchain.settings.local"

# 使用8080端口
python manage.py runserver 8080
```

## Django命令记录

### Creating a project

```shell
django-admin startproject project_name
```

### Creating the app

```shell
python manage.py startapp app_name
```

为了在我们的工程中包含这个应用，我们需要在配置类 INSTALLED_APPS 中添加设置。因为 PollsConfig 类写在文件 polls/apps.py 中，所以它的点式路径是 '
polls.apps.PollsConfig'。在文件 mysite/settings.py 中 INSTALLED_APPS 子项添加点式路径后，它看起来像这样：

```python
INSTALLED_APPS = [
  'polls.apps.PollsConfig',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]
```

通过运行 makemigrations 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为一次 迁移。

```shell
python manage.py makemigrations evm_chain --settings "onchain.settings.local"
```

sqlmigrate 命令接收一个迁移的名称，然后返回对应的 SQL：

```shell
python manage.py sqlmigrate evm_chain 0001 --settings "onchain.settings.local"
```

现在，再次运行 migrate 命令，在数据库里创建新定义的模型的数据表：

```shell
# 指定本地环境
python manage.py migrate --settings "onchain.settings.local"

# 指定开发环境
python manage.py migrate --settings "onchain.settings.dev"

```

这个 migrate 命令选中所有还没有执行过的迁移（Django 通过在数据库中创建一个特殊的表 django_migrations 来跟踪执行过哪些迁移）并应用在数据库上 - 也就是将你对模型的更改同步到数据库结构上。

### 使用Django进行单元测试

```shell
python manage.py test evm_chain
```

### 使用gunicorn启动项目

```shell
# 在当前项目的主目录下执行命令：
gunicorn crypto.wsgi

# -D 后台运行
gunicorn crypto.wsgi -D
```
