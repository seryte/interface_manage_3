import json

from django.forms import model_to_dict

from interface_app.forms.task_form import TaskInterfaceForm
from interface_app.libs.respone import ErrorCode, response_success, response_failed
from interface_app.models.interface import Interface
from interface_app.models.task import TaskInterface
from interface_app.views.base.base_list import MyBaseListView


class TaskInterfaceListView(MyBaseListView):
    model = TaskInterface
    form = TaskInterfaceForm
    code = ErrorCode.task_interface

    def get(self, request, *args, **kwargs):
        task_id = request.GET.get("task_id", "")  # 从url里边获取task_id
        task_interfaces = TaskInterface.objects.filter(task_id=task_id)
        ret = []
        for s in task_interfaces:
            interface = Interface.objects.filter(id=s.interface_id).first()
            t = model_to_dict(interface)
            t["context"] = json.loads(t["context"], encoding="utf-8")
            t["task_id"] = task_id
            t["task_interface_id"] = s.id
            ret.append(t)
        return response_success(ret)

    def post(self, request, *args, **kwargs):
        body = request.body
        data = json.loads(body, encoding="utf-8")

        if not isinstance(data, list):
            return response_failed(data)

        for item in data:
            form = self.form(data)
            if not form.is_valid():
                return response_failed(form)
            service = self.model.objects.create(**form.cleaned_data)
            if not service:
                return response_failed(code=self.code, message='创建数据失败')

        return response_success()
