from django import forms


class TaskForm(forms.Form):
    name = forms.CharField(max_length=200,
                           min_length=3,
                           required=True,
                           error_messages={"required": "username can not be empty"})

    description = forms.CharField(max_length=2000,
                                  min_length=1,
                                  required=True,
                                  error_messages={"required": "password can not be empty"})


class TaskInterfaceForm(forms.Form):
    task_id = forms.IntegerField(required=True)
    interface_id = forms.IntegerField(required=True)