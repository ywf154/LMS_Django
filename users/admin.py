from django.contrib import admin
from django.utils.html import format_html
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedStackedInline
from django.urls import reverse
from .models import UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ('image_display', 'id', 'username', 'display_actions')
    exclude = ('password', 'last_login', 'date_joined',)

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
