# UPYUN Python SDK

[![pypi package](https://badge.fury.io/py/upyun.png)](http://badge.fury.io/py/upyun) [![Build
Status](https://travis-ci.org/upyun/python-sdk.svg)](https://travis-ci.org/upyun/python-sdk)

UPYUN Python SDK，集合 [UPYUN HTTP REST 接口](http://docs.upyun.com/api/rest_api/)，[UPYUN HTTP FORM 接口](http://docs.upyun.com/api/form_api/) 和 [视频处理接口](http://docs.upyun.com/api/av_pretreatment/)。

### 更新说明

1. 不再兼容 1.x 的版本，新版接口设计和实现更加 Pythonic，且代码风格完全符合 [pep8](https://pypi.python.org/pypi/pep8) 规范。
2. 2.2.0 及以上版本同时兼容了最新版本的 Python 2.6 / 2.7 / 3.3 / 3.4。
3. 2.3.0 及以上版本不再支持直接使用默认标准库 httplib，必须依赖 requests 这个第三方 HTTP Client 库。
4. 2.5.0 及以上版本更新了 REST API，FORM API 以及预处理接口的[签名算法](http://docs.upyun.com/api/authorization/#_2)，同时移除分块上传接口。

### 安装说明

> 安装第三方依赖库 [requests](https://github.com/kennethreitz/requests): HTTP for Humans!

```
pip install requests
```

> 安装 UPYUN SDK

```
pip install upyun
```

> 运行测试用例

```
export UPYUN_SERVICE=<service>
export UPYUN_USERNAME=<username>
export UPYUN_PASSWORD=<password>

make init test
```

## 基本函数接口

### 初始化 UpYun

```python
import upyun

up = upyun.UpYun('service', 'username', 'password', timeout=30, endpoint=upyun.ED_AUTO)
```

`service`，`username`，`password` 分别为服务名，授权操作员帐号，密码。`timeout` 为 HTTP 请求超时时间，默认 60 秒，可选。

由于直接在 SDK 中暴露密码可能存在安全隐患，因此对于安全性要求较高的用户，可使用如下远程签名方式：

```python
import upyun

up = upyun.UpYun('service', username='username', auth_server='http://localhost:8080')
```

[签名服务](#远程签名服务)示例代码见 [examples/auth\_server.py](./examples/auth_server.py)

> 远程签名方式暂不支持[缓存刷新](https://docs.upyun.com/api/purge/)功能

###### 初始化示例

```python
import upyun

up = upyun.UpYun('service', username='username', password='password')
```

以及，根据国内的网络情况，UPYUN API 目前提供了电信、联通网通、移动铁通三个接入点，在初始化时可由参数 `endpoint` 进行设置，其可选的值有：

```python
upyun.ED_AUTO     # 根据网络条件自动选择接入点，默认
upyun.ED_TELECOM  # 电信接入点
upyun.ED_CNC      # 联通网通接入点
upyun.ED_CTT      # 移动铁通接入点
```

默认设置为 `upyun.ED_AUTO` ，但是我们推荐根据服务器网络状况，手动设置合理的接入点以获取最佳的访问速度。同时，也可通过：

```python
up.<api>.endpoint = upyun.ED_TELECOM
```

在对象使用过程中更改，其中 `<api>` 为你所要调用接口，REST 为 `up_rest`，表单为 `up_form`，视频处理为 `av`。


### 上传文件

#### 直接传递文件内容的形式上传

```python
up.put('/upyun-python-sdk/ascii.txt', 'abcdefghijklmnopqrstuvwxyz\n')
```

其中，方法 `up.put` 默认自动创建相应目录。

#### 数据流方式上传，可降低内存占用

```python
headers = { 'x-gmkerl-rotate': '180' }

with open('unix.png', 'rb') as f:
    res = up.put('/upyun-python-sdk/xinu.png', f, checksum=True, headers=headers)
```

其中，参数 `checksum` 和 `headers` 可选，前者默认 False，表示不进行 MD5 校验; 后者可根据需求设置自定义 HTTP Header，例如作图参数 `x-gmkerl-*` ，具体请参考 [REST API 上传文件](http://docs.upyun.com/api/rest_api/#_4)。

上传成功，如果是图片类型文件，那么 `res` 返回的是一个包含图片长、宽、帧数和类型信息的 Python Dict 对象 ( 其他文件类型, 返回一个空的 Dict)：

```
{'frames': '1', 'width': '1280', 'file-type': 'PNG', 'height': '800'}
```

上传失败，则抛出相应异常。

#### 移动文件

```python
up.move('/upyun-python-sdk/move-from.txt', '/upyun-python-sdk/move-to.txt')
```

第一个参数是源文件地址， 第二个参数是目的文件地址

#### 拷贝文件

```python
up.copy('/upyun-python-sdk/copy-from.txt', '/upyun-python-sdk/copy-to.txt')
```

第一个参数是源文件地址， 第二个参数是目的文件地址

#### 断点续传

```python
with open('unix.png', 'rb') as f:
    res = up.put('/upyun-python-sdk/xinu.png', f, checksum=True, need_resume=True)
```

参数 `need_resume` 默认 False， 置为 True 后， 采用断点续传方式上传文件。

```python
from upyun import FileStore
from upyun import print_reporter

with open('unix.png', 'rb') as f:
    res = up.put('/upyun-python-sdk/xinu.png', f, checksum=True, need_resume=True, headers={'X-Upyun-Multi-Type': 'image/png'}, store=FileStore(), reporter=print_reporter)
```

参数 `store` 用来保存断点信息， 默认保存断点信息在内存中。 `FileStore()` 可以保存断点信息到文件， 注意文件夹的权限， 默认保存在 `~/.up-python-resume/`， 提供参数 `directory` 用于修改默认的文件夹路径。 也可以选择继承 `BaseStore` 实现自己的断点存储。

参数 `reporter` 用于报告上传进度, 默认忽略上传进度。 `print_reporter` 只是 `print` 上传进度, 有需要的请继承 `BaseReporter` 自行处理。

可以使用头部 `X-Upyun-Multi-Type` 来指定上传文件类型, 默认情况下根据文件名分析处理。

#### 并发上传
并发上传是把文件按照part_size切割后，并发上传，都上传完毕后调用`complete`结束上传。  
part_size取值1M(1024*1024)的整数倍，默认是1M。  
下面的示例是并发上传一个2.5M的文件，数据内容是随机生成的。其中的`upload`方法可以多线程并发调用
```python
uploder = up.init_multi_uploader(key) #初始化上传

#并发上传需要数据块
uploder.upload(2, os.urandom(512 * 1024))    
uploder.upload(0, os.urandom(1024 * 1024))
uploder.upload(1, os.urandom(1024 * 1024))
res = uploder.complete() #所有块都上传完毕后，调用结束
```
若在上传过程中不需要上传了，可以调用`uploader.cancel()`取消上传任务。取消的任务无法再继续上传。

#### 表单方式上传

用户可直接上传文件到 UPYUN，而不需要通过客户服务器进行中转。


```python
kwargs = { 'allow-file-type': 'jpg,jpeg,png',
           'notify-url': 'http://httpbin.org/post', }

with open('unix.png', 'rb') as f:
    res = up.put('/upyun-python-sdk/xinu.png', f, checksum=True, form=True, **kwargs)
```

其中，参数 `form` 表示是否使用表单上传方式，必选。

同时表单上传可携带许多额外的可选参数，可以组合成字典作为函数可选参数传入，例如表单参数 `allow-file-type` ，具体请参考 [表单 API 参数](http://docs.upyun.com/api/form_api/#api_1)。

表单上传还支持同步通知及异步通知机制，可以通过设置 `return-url` 和 `notify-url` 来指定 URL。具体请参考[通知规则](http://docs.upyun.com/api/form_api/#_2)。

上传成功，如果是图片类型文件，那么 `res` 返回的是一个包含图片长、宽、帧数、类型信息、图片上传地址、返回状态码、返回状态信息和 signature 的 Python Dict 对象 (其他文件类型，则返回信息不包括图片长、宽和帧数参数)：

```
{u'code': 200, u'image-height': 410, u'url': u'/upyun-python-sdk/xinu.png', u'image-frames': 1, u'sign': u'60e63662202e50bddedd01f8ca601ba5', u'image-type': u'PNG', u'time': 1450783577, u'message': u'ok', u'image-width': 1000}
```

### 下载文件

#### 直接读取文件内容

```python
res = up.get('/upyun-python-sdk/ascii.txt')
```

下载成功，返回文件内容; 失败则抛出相应异常。

#### 使用数据流模式下载，节省内存占用

```python
with open('xinu.png', 'wb') as f:
    up.get('/upyun-python-sdk/xinu.png', f)
```

下载成功，返回 Python `None` 对象; 失败则抛出相应异常。

### 创建目录

```python
up.mkdir('/upyun-python-sdk/temp/')
```

创建成功，返回 Python `None` 对象; 失败则抛出相应异常。

### 删除目录或文件

```python
up.delete('/upyun-python-sdk/xinu.png')
up.delete('/upyun-python-sdk/temp/')
```

删除成功，返回 Python `None` 对象; 失败则抛出相应异常。注意删除目录时，必须保证目录为空。

### 获取目录文件列表

```python
res = up.getlist('/upyun-python-sdk/')
```

获取成功，返回一个包含该目录下所有目录或文件条目信息的 Python List 对象：

```
[{'time': '1363247311', 'type': 'F', 'name': 'temp', 'size': '0'}, {'time': '1363247311', 'type': 'N', 'name': 'xinu.png', 'size': '477908'}]
```

其中每个条目信息是又是一个 Python Dict 对象：

```python
item = res[0]
print item['name'] # 文件名称
print item['type'] # 文件类型
print item['size'] # 文件大小
print item['time'] # 创建时间
```

获取失败，则抛出相应的异常。该方法默认获取根目录列表信息。


#### 分页功能

```python
res = up.getlist('/upyun-python-sdk/', limit=10, order='asc', begin='xxx')
```

三个分页参数，默认为空，具体含义请参见 [分页参数](http://docs.upyun.com/api/rest_api/#_25)

#### 分页获取文件

```
res = get_list_with_iter('/upyun-python-sdk/', limit=10, order='asc', begin='xxx')

{
	'files': [{
		'name': 'xxx.m4a',
		'type': 'N',
		'size': '332918',
		'time': '1449137388'
	}],
	'iter': 'xxxxx'
}
```

三个分页参数，默认为空，具体含义请参见 [分页参数](http://docs.upyun.com/api/rest_api/#_25)


#### 流式返回

```python
iter_items = up.iterlist('/upyun-python-sdk/', limit=10, order='asc', begin='xxx')
# the resulting iterator object
for item in iter_items:
    print(item['type'], item['name'], item['size'])
```

三个分页参数，默认为空，具体含义请参见 [分页参数](http://docs.upyun.com/api/rest_api/#_25)




### 获取文件信息

```python
res = up.getinfo('/upyun-python-sdk/xinu.png')
print res['file-type']
print res['file-size']
print res['file-date']
```

获取成功，返回一个 Python Dict 对象; 失败则抛出相应异常。

### 获取服务使用情况

```python
res = up.usage()
```

获取成功，始终返回该服务当前使用的总容量，单位 Bytes，值类型为 Python String 对象; 失败则抛出相应异常。

### 视频处理

用于处理已经上传到对应存储服务中的视频文件，进行转码、截图等操作。

```python
source = '/service/test.mp4'
tasks = [{'type': 'probe', }, {'type': 'hls', 'hls_time': '100'}]
notify_url = 'http://httpbin.org/post'
up.pretreat(tasks, source, notify_url)
```

`tasks` 为提交的任务数据，需将所有任务组成数组，若仅有一个任务，也应组成数组结构，必选。UPYUN 的视频处理服务目前支持四种类型的处理请求：

- 视频转码
- HLS 切割
- 视频截图
- 视频信息获取

具体请参考[视频处理参数](http://docs.upyun.com/api/av_pretreatment/#_8)

`notify_url` 为异步回调地址，在处理完成之后将会以 `HTTP POST` 请求进行异步通知，参考[回调参数](http://docs.upyun.com/api/av_pretreatment/#_11), 必选。`source` 为待处理源文件路径，需提供已上传文件的相对路径。

视频处理任务提交成功，则会针对提交的处理任务返回一组唯一的 `task_id`，可以根据这个 `task_id` 查询处理进度，如:

```
[
    '35f0148d414a688a275bf915ba7cebb2',
    '98adbaa52b2f63d6d7f327a0ff223348',
    ...
]
```

任务提交失败则会抛出相应异常。

### 视频处理进度查询

```python
ids = ['35f0148d414a688a275bf915ba7cebb2','98adbaa52b2f63d6d7f327a0ff223348', ...]
up.status(ids)
```
以视频处理接口返回的数组作为传入参数，需为 Python List 结构。

返回的数据示例如下:

```
{
    tasks: {
        35f0148d414a688a275bf915ba7cebb2: 100,
        98adbaa52b2f63d6d7f327a0ff223348: null,
        ...
    }
}
```

特别的，当值为 null 时，表示没有查询到相关的任务信息。同时，由于视频处理所用时间较长，当提交任务后立刻去查询进度，也有可能会返回 null。


### 异步任务提交

```
notify_url = 'http://httpbin.org/post'                          // 回调地址

compress_tasks = [
    {
        "sources": ["a/b/c/source/1.jpg","a/b/c/source/2.jpg"],
        "save_as": "/result/t.zip",
        "home_dir": "a/b/c"
    },
]

print up.put_tasks(compress_tasks, notify_url, 'compress')

depress_tasks = [
    {
        "sources": "/source/t.zip",              //UPYUN 存储服务中内文件路径
        "save_as": "/result/t/",                 //保存路径
    },
]

print up.put_tasks(depress_tasks, notify_url, 'depress')

fetch_tasks = [
    {
        'url': 'http://www.upyun.com/index.html',               // 需要拉取文件的 URL
        'random': False,                                        // 是否追加随机数, 默认 false
        'overwrite': True,                                      // 是否覆盖，默认 true
        'save_as': '/site/index.html',                          // 保存路径
    }
]

print up.put_tasks(fetch_tasks, notify_url, 'spiderman')
```

具体请参考 [压缩解压缩](http://docs.upyun.com/cloud/unzip/) 和 [异步文件拉取](http://docs.upyun.com/cloud/spider/)

### 异常处理

```python
try:
    res = up.usage()

    # do something else

except upyun.UpYunServiceException as se:
    print 'Except an UpYunServiceException ...'
    print 'Request Id: ' + se.request_id
    print 'HTTP Status Code: ' + str(se.status)
    print 'Error Message:    ' + se.msg + '\n'
except upyun.UpYunClientException as ce:
    print 'Except an UpYunClientException ...'
    print 'Error Message: ' + ce.msg + '\n'
```

其中， `UpYunServiceException` 主要是 UPYUN 端返回的错误信息，具体错误代码请参考 [标准 API 错误代码表](http://docs.upyun.com/api/errno/); 而 `UpYunClientException` 则主要是一些客户端环境的异常，例如客户端网络超时，或客户端参数不完整等。

## 高级特性

### 自定义数据流大小

```python
up = upyun.UpYun('service', 'username', 'password', chunksize=8192)
```

当通过数据流方式上传和下载文件时，`chunksize` 决定了每次读操作的缓存区大小，默认 8192 字节。

### 自定义文件上传和下载过程

> 例如，通过如下代码可以很容易实现上传下载的进度条显示：

```python
from progressbar import *

class ProgressBarHandler(object):
    def __init__(self, totalsize, params):
        widgets = [params, Percentage(), ' ',
                   Bar(marker='=', left='[', right=']'), ' ',
                   ETA(), ' ', FileTransferSpeed()]
        self.pbar = ProgressBar(widgets=widgets, maxval=totalsize).start()

    def update(self, readsofar):
        self.pbar.update(readsofar)

    def finish(self):
        self.pbar.finish()

with open('unix.png', 'rb') as f:
    res = up.put('xinu.png', f, handler=ProgressBarHandler, params='Uploading ')

with open('xinu.png', 'wb') as f:
    up.get('xinu.png', f, handler=ProgressBarHandler, params='Downloading ')
```

### 原图密钥保护

```python
with open('unix.png', 'rb') as f:
    res = up.put('xinu.png', f, secret="abc")
```

其中参数 `secret` 可指定具体密钥内容；默认 `None`，表示不设置密钥。特别地，该功能仅对配置了缩略图版本号的图片服务有效。

详见 [UPYUN HTTP REST API 接口](http://docs.upyun.com/api/rest_api/) 中关于原图密钥保护的说明。

## 缓存刷新

基于 [UPYUN 缓存刷新 API 接口](http://docs.upyun.com/api/purge/) 开发，方便对 CDN 服务缓存资源进行主动刷新。

特别地，云存储服务正常情况下，资源更新则不需要额外提交刷新请求，缓存系统会自动进行处理。

```python
>>> print up.purge('/upyun-python-sdk/xinu.png')
[]
```

```python
>>> print up.purge(['/unix.png', '/xinu.png'], domain='invalid.upyun.com')
['/unix.png', '/unix.png']
```

支持提交单个或一组 URI 到缓存刷新队列，其中 `domain` 参数可特别指定为该服务对应的绑定域名作为本次刷新的域，默认其值为 `None`，表示始终使用默认域名。

提交成功，返回一个 Python List 对象，包含本次提交中无效的 URI 列表；失败则抛出相应异常。

## 签名验证

如果在表单或异步任务提交接口使用了 `return-url` 或 `notify-url` 等通知方法后，回调结果信息头会包含 `Authorization` 字段，用于验证回调信息是否正确。

```python
import upyun

up = upyun.UpYun('service', 'username', 'password')

headers = {
    'Date': 'Fri, 20 Jan 2017 08:46:20 GMT',
    'Content-MD5': 'd36489794822f8d33fd28217d8a5bed4',
    'Authorization': 'UPYUN username:W738BergX15B+jso8fSPzKd0/zQ='
}

assert up.verify_signature(headers['Authorization'], '/api/v1/echo', headers)
```

## 远程签名服务

创建自己的远程签名服务以提供签名功能。实现 API 如下：

URL：任意合法 URL

HTTP 方法：POST

文档格式：JSON

请求参数：

参数名称        | 必选    | 类型
----------- | ----- | ------
username    | true  | string
method      | true  | string
uri         | true  | string
date        | true  | stirng
policy      | false | string
content_md5 | false | string

返回结果: `UPYUN: username:signature`

> 参数说明及签名算法见[签名算法](http://docs.upyun.com/api/authorization/#_2)
