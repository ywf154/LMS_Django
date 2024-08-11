from django import forms

from operations.models import UserFavorite, CourseComments, Task


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


class TaskGradeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["grade"]
