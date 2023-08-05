#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : test
# @Time         : 2020-03-21 17:15
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import uvicorn

from mi.app import mongo

app = mongo.app
uvicorn.run(app, host='0.0.0.0', port=8000, workers=1, debug=True)
