from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from operations.models import *
from organizations.models import Org


class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_display', 'title', 'display_actions')
    fields = ('image', 'title', 'url', )

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


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['course', ]
    fields = ['user', 'course']
    fields_limited = ['course', ]  # 限制用户字段

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user.id)

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.fields
        return self.fields_limited


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['notice', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user.id)


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['OrgOrCourse', 'fav_type', ]

    def OrgOrCourse(self, obj):
        if obj.fav_type == 1:  # 收藏类型为课程机构
            course_org = Org.objects.filter(id=obj.fav_id).first()
            if course_org:
                return course_org.name
        elif obj.fav_type == 2:  # 收藏类型为课程
            course = Course.objects.filter(id=obj.fav_id).first()
            if course:
                return course.name
        return '-'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(Banner, BannerAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
