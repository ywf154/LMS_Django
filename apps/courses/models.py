from DjangoUeditor.models import UEditorField

from django.db import models

from users.models import BaseModel
from organizations.models import Teacher, Org


class CourseCategory(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程类别"
        verbose_name_plural = verbose_name



class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name="课程机构", default=None)
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300, null=True, blank=True)

    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")

    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, verbose_name="课程类别")
    detail = UEditorField(verbose_name="课程详情", default='', blank=True, imagePath='course_detail/', toolbars="full",
                          filePath="course_detail_files/", height=500, width=1200)
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", default='course_images.jpg')
    status = models.BooleanField(default=True, verbose_name="课程状态")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        sum = 0
        for lesson in self.lesson_set.all():
            sum += lesson.content_set.all().count()
        return sum

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))

    show_image.short_description = "图片"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))

    go_to.short_description = "跳转"


class Notice(BaseModel):
    title = models.CharField(verbose_name="通知标题", max_length=100)
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE, null=True)
    content = UEditorField(verbose_name="通知详情", default='', blank=True, imagePath='course_notice', toolbars="mini",
                           filePath="course_notice_files/", height=150, width=1000)

    class Meta:
        verbose_name = "课程通知"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Content(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="课程章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"小节名称", null=True)
    learning_space = UEditorField(verbose_name="学习空间", default='', blank=True, imagePath='course_content/',
                                  toolbars="full", filePath="course_content_files/", height=300, width=1340)
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="课件资料", null=True,
                            blank=True)

    class Meta:
        verbose_name = "课程小节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
