from interface_app.forms.task_form import TaskForm
from interface_app.libs.respone import ErrorCode
from interface_app.models.task import Task
from interface_app.views.base.base_list import MyBaseListView


class TaskListView(MyBaseListView):
    model = Task
    form = TaskForm
    code = ErrorCode.task
