from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from organizations.models import *


class CourseOrgAdmin(admin.ModelAdmin):
    fields = ['image', 'name', 'city', 'category', ]
    list_display = ('image_display', 'name', 'city', 'display_actions')
    search_fields = ('name', 'city')

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


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'org', 'image', 'work_years', 'course_nums')


admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)

admin.site.site_header = '学习管理后台'
admin.site.index_title = '后台管理'
admin.site.site_title = '学习管理后台'
