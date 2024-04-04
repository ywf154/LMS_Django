from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from operations.models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_display', 'title', 'display_actions')
    fields = ('image', 'title', 'url','index')

    def image_display(self, obj):
        return format_html('<img src="{}" width="200" height="100" alt="Image">', obj.image.url)

    image_display.short_description = '轮播图'

    def display_actions(self, obj):
        edit_url = reverse('admin:courses_course_change', args=[obj.pk])
        delete_url = reverse('admin:courses_course_delete', args=[obj.pk])
        edit_button = format_html('<a href="{}" class="admin-edit-button">编辑</a>', edit_url)
        delete_button = format_html('<a href="{}" class="admin-delete-button">删除</a>', delete_url)

        return format_html('{}  {}', edit_button, delete_button)

    display_actions.short_description = '操作'


admin.site.register(Banner, BannerAdmin)
