import json

from django.forms import model_to_dict
from django.views.generic import View

from interface_app.forms.service_form import ServiceForm
from interface_app.libs.respone import response_success, response_failed, ErrorCode
from interface_app.models.service import Service


class MyBaseListView(View):

    model = Service
    form = ServiceForm
    code = ErrorCode.common

    def get(self, request, *args, **kwargs):
        """
        获取列表
        :param args:
        :param kwargs:
        :return:
        """
        services = self.model.objects.all()
        ret = []
        for s in services:
            t = model_to_dict(s)
            ret.append(t)
        return response_success(model_to_dict(ret))

    def post(self, request, *args, **kwargs):
        """
        新增数据
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        data = json.loads(body, encoding="utf-8")

        form = self.form(data)
        if not form.is_valid():
            return response_failed(code=self.code)

        service = self.model.objects.create(**form.changed_data)

        if not service:
            return response_failed(code=ErrorCode.service)
        else:
            return response_success(model_to_dict(service))
