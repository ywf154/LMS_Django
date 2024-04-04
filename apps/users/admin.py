from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from organizations.models import Teacher
from .models import UserProfile


class TeacherInline(admin.StackedInline):
    model = Teacher
    fields = ['name', 'org']


class UserAdmin(admin.ModelAdmin):
    inlines = [TeacherInline]
    list_display = ('image_display', 'id', 'username', 'teacher_name', 'display_actions',)
    exclude = ('password', 'last_login', 'date_joined',)

    def teacher_name(self, obj):
        if obj.teacher:
            return obj.teacher.name

    teacher_name.short_description = '教师名'

    def image_display(self, obj):
        return format_html('<img src="{}" width="50" height="50" alt="Image">', obj.image.url)

    image_display.short_description = '头像'

    def display_actions(self, obj):
        edit_url = reverse('admin:users_userprofile_change', args=[obj.pk])
        delete_url = reverse('admin:users_userprofile_delete', args=[obj.pk])
        edit_button = format_html('<a href="{}" class="admin-edit-button">编辑</a>', edit_url)
        delete_button = format_html('<a href="{}" class="admin-delete-button">删除</a>', delete_url)

        return format_html('{}  {}', edit_button, delete_button)

    display_actions.short_description = '操作'


admin.site.register(UserProfile, UserAdmin)
