# Blog

*A blue blog.*




## Installation

```
$ git clone https://github.com/greyli/bluelog.git
$ cd bluelog
$ pipenv install --dev
$ pipenv shell
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```

Test account:

* username: `admin`
* password: `helloflask`




如果执行`pipenv install`命令安装依赖耗时太长，你可以考虑使用国内的PyPI镜像源，比如：
```
$ pipenv install --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
