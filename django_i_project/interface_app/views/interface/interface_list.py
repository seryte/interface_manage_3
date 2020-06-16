import json

from django.forms import model_to_dict

from interface_app.forms.interface_form import InterfaceForm
from interface_app.libs.respone import ErrorCode, response_success, response_failed
from interface_app.models.interface import Interface
from interface_app.models.service import Service
from interface_app.views.base.base_list import MyBaseListView


class InterfaceListView(MyBaseListView):
    model = Interface
    form = InterfaceForm
    code = ErrorCode.common

    def get(self, request, *args, **kwargs):
        """
        获取某个服务下的接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        service_id = request.GET.get("service_id", 0)
        ret = []
        if service_id == "0":
            interfaces_lists = self.model.objects.all()
            for s in interfaces_lists:
                t = {"id": s.id,
                     "name": s.name,
                     "description": s.description,
                     "service_id": s.service_id,
                     "service_name": Service.objects.filter(id=s.service_id).first().name,
                     "context": json.loads(s.context)
                     }
                ret.append(t)
        else:
            interfaces = self.model.objects.filter(service_id=service_id)
            service_name = Service.objects.filter(id=service_id).first().name

            for s in interfaces:
                t = {"id": s.id,
                     "name": s.name,
                     "description": s.description,
                     "service_id": s.service_id,
                     "service_name": service_name,
                     "context": json.loads(s.context)
                     }
                ret.append(t)
        return response_success(ret)

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        data = json.loads(body, encoding="utf-8")
        if "context" not in data:
            return response_failed()
        data["context"] = json.dumps(data["context"])
        form = self.form(data)
        if not form.is_valid():
            return response_failed(code=self.code)

        interface = self.model.objects.create(**form.cleaned_data)

        if not interface:
            return response_failed(code=ErrorCode.interface)
        else:
            ret = model_to_dict(interface)
            ret["context"] = json.loads(ret["context"])
            return response_success(ret)
