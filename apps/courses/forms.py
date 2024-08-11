from django import forms

from courses.models import *
from operations.models import CourseComments


class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category', 'desc']


class CourseBaseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image', 'name', 'category', 'desc']


class CourseDetailForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['detail']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name']


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name']


class Content_upload_Form(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['file']


class ContentSpqaceForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'learning_space']


class CourseCommentsForms(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['comments']
