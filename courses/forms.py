from django.forms import ModelForm

from courses.models import Course


class CourseAdminForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'org', 'teacher', 'category', 'image']

