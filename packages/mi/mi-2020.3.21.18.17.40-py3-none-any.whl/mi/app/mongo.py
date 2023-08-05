#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : watchDog
# @Time         : 2020-03-06 09:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
""":arg
/app/mongo/{collection}/{attribute}：insert delete update find count(默认)
querypath+postdata+formdata+date
querypath：
可增加是否发邮件参数(需要润色html或者web或者sreamlit)
可增加一些额外信息：jobid jobtype
增加collection name判断
返回：可选操作前后的文档数、新增的doc、更新后的doc、耗时信息、抛错信息

"""
import re
import time
from datetime import datetime
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *
from collections import OrderedDict
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html
from collections import Iterable, Iterator
from bson import json_util

from ..db import Mongo

mongo = Mongo()

ROUTE = "/app"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get(f"{ROUTE}/demo.a")
async def report():
    return "xx"


@app.get("/app/mongo/{collection}/{attribute}")
async def report(request: Request, collection, attribute):
    """:arg
    查询功能
    """
    dic = OrderedDict()
    dic['querypath'] = dict(request.query_params)

    try:
        params = dic['querypath']
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

        if 'filter' in params:
            params['filter'] = eval(params['filter'])

        _ = mongo.db[collection].__getattribute__(attribute)(**params)
        # _ = list(_) if isinstance(_, Iterator) else _
        dic[f"{collection}.{attribute}"] = eval(json_util.dumps(_))

        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


@app.post("/app/mongo/post/{collection}/{attribute}")
async def report(request: Request, kwargs: dict, collection, attribute):
    """:arg
    /app/mongo/{collection}/{attribute}：insert delete update find count(默认)
    querypath+postdata+formdata+date
    querypath：
    可增加是否发邮件参数(需要润色html或者web或者sreamlit)
    可增加一些额外信息：jobid jobtype
    增加collection name判断
    返回：可选操作前后的文档数、新增的doc、更新后的doc、耗时信息、抛错信息
    """
    # print(dict(request))
    # print(request.path_params) # {'job_type': 'hive'}
    dic = OrderedDict()
    dic['post_data'] = kwargs
    dic['form_data'] = dict(await request.form())
    dic['querypath'] = dict(request.query_params)
    dic['date'] = datetime.now().__str__()
    try:
        params = dic['querypath']
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

        if 'filter' in params:
            params['filter'] = eval(params['filter'])

        _ = mongo.db[collection].__getattribute__(attribute)(**params)
        # _ = list(_) if isinstance(_, Iterator) else _
        dic[f"{collection}.{attribute}"] = eval(json_util.dumps(_))

        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

    except Exception  as e:
        dic['error'] = format_exc()
    return dic


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True)
