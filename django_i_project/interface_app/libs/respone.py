#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-04 21:26:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from django.http import JsonResponse


class ErrorCode:
    common = 10000
    auth = 10001
    service = 10002
    task = 10003
    interface = 10004
    task_interface = 10005


def common_respone(success, data, error_code, error_message, page=1, pagesize=10, count=0):
    response = {
        "page": page,
        "pageSize": pagesize,
        "count": count,
        "data": data,
        "success": success,
        "error": {
            "code": error_code,
            "message": error_message
        }

    }
    return JsonResponse(response, safe=False)


def response_success(data={}, page=1, pagesize=10, count=0):
    return common_respone(True, data, "", "", page=page, pagesize=pagesize, count=count)


def response_failed(code=ErrorCode.common, message="参数错误", data={}):
    return common_respone(False, data, code, message)
