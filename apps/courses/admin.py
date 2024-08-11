from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from courses.models import *


class ContentInline(NestedStackedInline, SortableHiddenMixin):
    model = Content
    fields = ['name', 'learning_space', 'file']
    extra = 0


class LessonInline(NestedStackedInline, SortableHiddenMixin):
    model = Lesson
    inlines = [ContentInline]
    fields = ['name']
    extra = 0


class NoticeInline(NestedStackedInline, SortableHiddenMixin):
    model = Notice
    fields = ['title', 'content']
    extra = 0


class CourseAdmin(NestedModelAdmin):
    inlines = [NoticeInline, LessonInline]
    extra = 0
    # 这里是多级内联编辑
    collapse_template = 'templates/admin/collapse_nested_inline.html'
    fields = ['name', 'category', 'image', 'detail', 'desc', 'status', ]
    list_display = ('image_display', 'name', 'teacher', 'org', 'status', 'display_actions')
    list_per_page = 5
    list_filter = ['category', 'org', 'status']
    search_fields = ['name', ]
    save_on_top = True
    save_as = False

    def image_display(self, obj):
        return format_html('<img src="{}" width="150" height="100" alt="Image">', obj.image.url)

    image_display.short_description = '课程封面'

    def display_actions(self, obj):
        edit_url = reverse('admin:courses_course_change', args=[obj.pk])
        delete_url = reverse('admin:courses_course_delete', args=[obj.pk])
        detail_url = reverse('Course_edit', args=[obj.pk])
        edit_button = format_html('<a href="{}" class="admin-edit-button">编辑</a>', edit_url)
        delete_button = format_html('<a href="{}" class="admin-delete-button">删除</a>', delete_url)
        detail_button = format_html('<a href="{}" class="admin-edit-button">详情</a>', detail_url)
        return format_html('{}  {}  {}', edit_button, detail_button, delete_button)

    display_actions.short_description = '操作'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.teacher = request.user.teacher
            obj.org = request.user.teacher.org
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user.teacher)


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.site_header = '学习管理后台'
admin.site.index_title = '后台管理'
admin.site.site_title = '学习管理后台'
