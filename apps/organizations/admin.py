from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group
from courses.models import Course
from organizations.models import *


class TeacherInline(admin.StackedInline):
    model = Teacher
    list_display = 'name'
    fields = ['name']
    extra = 0


class OrgAdmin(admin.ModelAdmin):
    inlines = [TeacherInline]
    fields = ['image', 'name', 'city', 'category','desc' ]
    list_display = ('image_display', 'name', 'city', 'display_actions')
    search_fields = ('name', 'city')

    def image_display(self, obj):
        return format_html('<img src="{}" width="150" height="100" alt="Image">', obj.image.url)

    image_display.short_description = '机构封面'

    def display_actions(self, obj):
        edit_url = reverse('admin:organizations_org_change', args=[obj.pk])
        delete_url = reverse('admin:organizations_org_delete', args=[obj.pk])

        edit_button = format_html('<a href="{}" class="admin-edit-button">update</a>', edit_url)
        delete_button = format_html('<a href="{}" class="admin-delete-button">delete</a>', delete_url)

        return format_html('{}  {}', edit_button, delete_button)

    display_actions.short_description = '操作'


class CityAdmin(admin.ModelAdmin):
    fields = ['name']


class CourseInline(admin.StackedInline):
    model = Course
    fields = ['name', 'image', 'org']
    extra = 0


class TeacherAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('name', 'org',)
    fields = ['name', 'org', 'user']
    search_fields = ['name', 'user']
    # raw_id_fields = ['user']
    autocomplete_fields = ['user']  # 这个需要在user的admin中添加搜索功能

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        user = obj.user
        # 将用户添加到 'Teachers' 用户组
        teachers_group, _ = Group.objects.get_or_create(name='Teachers')
        user.groups.add(teachers_group)
        user.is_staff = True
        user.save()


class OrgCategAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Org, OrgAdmin)
admin.site.register(OrgCategory, OrgCategAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Teacher, TeacherAdmin)

admin.site.site_header = '学习管理后台'
admin.site.index_title = '后台管理'
admin.site.site_title = '学习管理后台'
