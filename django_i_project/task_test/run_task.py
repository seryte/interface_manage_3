import json

import pytest
import os
import sys
import django

# 不同进程使用django代码


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 定位到django的根目录
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))  # 把django目录放到环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_i_project.settings")
django.setup()  # django的初始化

from interface_app.models.interface import Interface
from interface_app.models.task import TaskInterface, RunTask
from task_test.http_request import HttpRequest

run_task = RunTask.objects.all().first()

if run_task is None:
    sys.exit(-1)
task_id = run_task.task_id
params_list = []
t = TaskInterface.objects.filter(task_id=task_id)

for i in t:
    interface = Interface.objects.filter(id=i.interface_id).first()
    context = json.loads(interface.context, encoding='utf-8')
    i_data = [
        interface.name,
        context.get("method", ""),
        context.get("url", {}),
        context.get("params", {}),
        context.get("asst", {}),
    ]
    params_list.append(i_data)


@pytest.mark.parametrize(("name", "method", "url", "params", "asst"), params_list)
def test_task(name, method, url, params, asst):
    response = HttpRequest.send_request(url, method, params)

    for text in asst:
        rule = asst[text]
        if not rule:
            continue
        if rule == 'include':
            assert str(text) in str(response)
        elif rule == 'exclude':
            assert str(text) not in str(response)
        else:
            continue
