import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from interface_app.libs.respone import response_success
from interface_app.models.task import RunTask


def _create_task_report_dir(task_id):
    task_reports_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id))
    if os.path.exists(task_reports_path):
        return
    os.makedirs(task_reports_path)


def _add_task_to_run_model(task_id):
    RunTask.objects.all().delete()
    RunTask.objects.create(task_id=task_id)


def _run_py_test(task_id):
    now = datetime.datetime.now()
    run_task_path = os.path.join(settings.BASE_DIR, "task_test", "run_task.py")
    report_name = "{}.html".format(now.strftime("%Y-%m-%d-%H_%M_%S"))
    # report_date = now.strftime("%Y-%m-%d")
    report_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id), report_name)
    command = "pytest {file_path} --html={report_path}".format(file_path=run_task_path, report_path=report_path)
    os.system(command)


@require_http_methods(["GET"])
def run_task(request, task_id):
    _create_task_report_dir(task_id)
    _add_task_to_run_model(task_id)
    _run_py_test(task_id)
    return HttpResponse()


@require_http_methods(["GET"])
def get_task_report_list(request, task_id):
    task_reports_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id))
    ret = []
    for root, dirs, files in task_reports_path:
        for file in files:
            if os.path.splitext(file)[1] == ".html":
                ret.append(file)
    return response_success(ret)


@require_http_methods(["GET"])
def get_task_report_detail(request, task_id, report_name):
    task_reports_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id), report_name)
    if not os.path.exists(task_reports_path):
        return " "
    return HttpResponse()