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


def common_respone(success, data, error_code, error_message):
    response = {
        "data": data,
        "success": success,
        "error": {
            "code": error_code,
            "message": error_message
        }
    }
    return JsonResponse(response, safe=False)


def response_success(data={}):
    return common_respone(True, data, "", "")


def response_failed(code=ErrorCode, message="参数错误", data={}):
    return common_respone(False, data, "", "")
