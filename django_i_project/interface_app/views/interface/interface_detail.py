import json

from django.forms import model_to_dict

from interface_app.forms.interface_form import InterfaceForm
from interface_app.libs.respone import ErrorCode, response_success, response_failed
from interface_app.models.interface import Interface
from interface_app.views.base.base_detail import MyBaseDetailView


class InterfaceDetailView(MyBaseDetailView):
    model = Interface
    form = InterfaceForm
    code = ErrorCode.common

    def get(self, request, base_id, *args, **kwargs):
        interface = self.model.objects.filter(id=base_id).first()
        if not interface:
            return response_failed(code=self.code, message="数据不存在！")
        ret = model_to_dict(interface)
        ret["context"] = json.loads(ret["context"], encoding="utf-8")
        return response_success(ret)

    def put(self, request, base_id, *args, **kwargs):
        body = request.body
        data = json.loads(body, encoding="utf-8")
        if "context" not in data:
            return response_failed()
        data["context"] = json.dumps(data["context"], encoding="utf-8")

        form = self.form(data)
        if not form.is_valid():
            return response_failed()

        interface = self.model.objects.filter(id=base_id).first()
        if not interface:
            return response_failed(code=ErrorCode.interface, message="数据不存在！")

        self.model.objects.filter(id=base_id).update(**form.cleaned_data)  # 这里返回是id
        interface = self.model.objects.filter(id=base_id).first()
        return response_success(model_to_dict(interface))
