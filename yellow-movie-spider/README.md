# yellow-movie-spider

#### 项目介绍

* 依赖：
```
^python3.5
scrapy 最新版.  pip install scrapy （如果pip版本低升级一下pip，自行百度升级命令）
requests 库  pip install requests 就ok 
```

* 设置
```

yellow/settings.py  FILES_STORE=xxxx 小电影存储目录，这个目录要自己创一下，程序里不清楚没建会不会自动创建，win平台目录例如C:/Users/XXXX/Downloads/yellowhaha

```

* 主要代码

```

yellow/spiders/video.py 爬虫 和 yellow/pipelines.py 下载器

```

* 运行

```
scrapy crawl videos

```

