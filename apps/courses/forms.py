from django import forms
from django.forms import inlineformset_factory

from courses.models import *
from operations.models import CourseComments


class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category', 'desc']


class CourseBaseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image', 'name', 'category', 'desc', 'tag', 'youneed_know', 'detail']


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


class ContentSpqaceForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'learning_space']


class CourseCommentsForms(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['comments']


class CourseResourceForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['name', 'file']
