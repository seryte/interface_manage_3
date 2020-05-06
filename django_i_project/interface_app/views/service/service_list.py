from interface_app.forms.service_form import ServiceForm
from interface_app.libs.respone import ErrorCode
from interface_app.models.service import Service
from interface_app.views.base.base_list import MyBaseListView


class ServiceListView(MyBaseListView):
    model = Service
    form = ServiceForm
    code = ErrorCode.common
