from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedStackedInline

from courses.models import Course
from organizations.models import *


class TeacherInline(admin.StackedInline):
    model = Teacher
    list_display = 'name'
    fields = ['name']
    extra = 0


class CourseOrgAdmin(admin.ModelAdmin):
    inlines = [TeacherInline]
    fields = ['image', 'name', 'city', 'category', ]
    list_display = ('image_display', 'name', 'city', 'display_actions')
    search_fields = ('name', 'city')

    def image_display(self, obj):
        return format_html('<img src="{}" width="150" height="100" alt="Image">', obj.image.url)

    image_display.short_description = '机构封面'

    def display_actions(self, obj):
        edit_url = reverse('admin:organizations_courseorg_change', args=[obj.pk])
        delete_url = reverse('admin:organizations_courseorg_delete', args=[obj.pk])

        edit_button = format_html('<a href="{}" class="admin-edit-button">编辑</a>', edit_url)
        delete_button = format_html('<a href="{}" class="admin-delete-button">删除</a>', delete_url)

        return format_html('{}  {}', edit_button, delete_button)

    display_actions.short_description = '操作'


class CityAdmin(admin.ModelAdmin):
    fields = ['name']


class CourseInline(admin.StackedInline):
    model = Course
    # fields = ['image', 'org', 'name', 'desc', 'category', 'tag', 'youneed_know', 'detail']
    fields = ['name', 'image', 'org']
    extra = 0


class TeacherAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('name', 'org',)
    fields = ['name', 'org', 'user']
    search_fields = ['name', 'user']
    # raw_id_fields = ['user']
    autocomplete_fields = ['user']  # 这个需要在user的admin中添加搜索功能


admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Teacher, TeacherAdmin)

admin.site.site_header = '学习管理后台'
admin.site.index_title = '后台管理'
admin.site.site_title = '学习管理后台'
