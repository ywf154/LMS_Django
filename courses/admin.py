from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from courses.models import *
from operations.models import Task


class CourseResourceInline(NestedStackedInline, SortableHiddenMixin):
    model = CourseResource
    fields = ['name', 'file']
    extra = 0


class ContentInline(NestedStackedInline, SortableHiddenMixin):
    model = Content
    fields = ['name', 'learning_space', 'file']
    extra = 0


class LessonInline(NestedStackedInline, SortableHiddenMixin):
    model = Lesson
    inlines = [ContentInline]
    fields = ['name']
    extra = 0


class CourseAdmin(NestedModelAdmin):
    inlines = [LessonInline, CourseResourceInline]
    extra = 0
    # 这里是多级内联编辑
    collapse_template = 'templates/admin/collapse_nested_inline.html'
    fields = ['name', 'org', 'teacher', 'category', 'image', 'detail', 'tag', 'desc']
    list_display = ('image_display', 'name', 'teacher', 'org', 'display_actions')
    search_fields = ['name', 'org', 'teacher', 'category']

    def image_display(self, obj):
        return format_html('<img src="{}" width="50" height="50" alt="Image">', obj.image.url)

    image_display.short_description = '课程封面'

    def display_actions(self, obj):
        edit_url = reverse('admin:courses_course_change', args=[obj.pk])
        delete_url = reverse('admin:courses_course_delete', args=[obj.pk])
        edit_button = format_html('<a href="{}" class="admin-edit-button">编辑</a>', edit_url)
        delete_button = format_html('<a href="{}" class="admin-delete-button">删除</a>', delete_url)

        return format_html('{}  {}', edit_button, delete_button)

    display_actions.short_description = '操作'


admin.site.register(Course, CourseAdmin)
admin.site.site_header = '学习管理后台'
admin.site.index_title = '后台管理'
admin.site.site_title = '学习管理后台'
