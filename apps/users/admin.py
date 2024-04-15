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
    list_display = ('image_display', 'id', 'username', 'teacher_name',)
    search_fields = ['username', ]
    fields = ['username', 'image', 'email', 'mobile', 'first_name', 'last_name', 'is_active', 'is_staff',
              'is_superuser', 'groups']
    exclude = ('password', 'last_login', 'date_joined',)
    fields_limited = ('username', 'gender', 'mobile', 'image', 'email')  # 限制用户字段
    filter_horizontal = ('groups',)

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

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.fields
        return self.fields_limited



admin.site.register(UserProfile, UserAdmin)
