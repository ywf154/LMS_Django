from django import forms

from DjangoUeditor.widgets import UEditorWidget
from operations.models import UserFavorite, CourseComments, Task
from DjangoUeditor.forms import UEditorField, UEditorModelForm


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comments"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["detail"]
