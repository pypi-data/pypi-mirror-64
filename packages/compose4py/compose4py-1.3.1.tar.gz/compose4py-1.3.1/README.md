# Compose4py

Onion Model in Python.
Pyton 洋葱模型

```
pip install compose4py
```

## Installation

## Usage

Import `compose4py`:

```
from compose4py import Compose
```

All the usual function composition you know and love:

```
    def mw_1(ctx, loader_context):
        print("mw_1: %s" % ctx)
        print("mw_1 loader_context: %s" % loader_context)
        ctx += ":mw1"
        # call the next middleware and waiting the new ctx
        ctx = yield ctx
        # use the latest ctx and process more logic
        ctx += ":post_mw1"
        return ctx

    def mw_2(ctx):
        print("mw_2: %s" % ctx)
        ctx += ":mw2"
        ctx = yield ctx
        ctx += ":post_mw2"
        return ctx

    def mw_3(ctx):
        print("mw_3: %s" % ctx)
        ctx += ":mw3"
        return ctx

    compose = Compose(mw_1, mw_2, mw_3, loader_context = {"foo": "bar"})
    result = compose("foo")
    print("final: %s" % result)
    # final: foo:mw1:mw2:mw3:post_mw2:post_mw1
```

## Give credits to

[scrapy](https://github.com/scrapy/scrapy)

## 开源许可协议

Copyright (2018-2020) <a href="https://www.chatopera.com/" target="_blank">北京华夏春松科技有限公司</a>

[Apache License Version 2.0](https://github.com/chatopera/cosin/blob/master/LICENSE)

[![chatoper banner][co-banner-image]][co-url]

[co-banner-image]: https://user-images.githubusercontent.com/3538629/42383104-da925942-8168-11e8-8195-868d5fcec170.png
[co-url]: https://www.chatopera.com
