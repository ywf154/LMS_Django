from DjangoUeditor.models import UEditorField

from django.db import models

from users.models import BaseModel
from organizations.models import Teacher, CourseOrg


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="课程机构", default=None)
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300, null=True, blank=True)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10, null=True, blank=True)
    youneed_know = models.TextField(default="", max_length=300, verbose_name="课程须知", null=True, blank=True)
    detail = UEditorField(verbose_name="课程详情", default='', blank=True, imagePath='course_detail/', toolbars="full",
                          filePath="course_detail_files/", height=500, width=900)
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", default='course_images.jpg')
    is_banner = models.BooleanField(default=False, verbose_name="是否宣传")
    status = models.BooleanField(default=True, verbose_name="课程状态")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

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
    content = UEditorField(verbose_name="课程详情", default='', blank=True, imagePath='course_notice', toolbars="mini",
                           filePath="course_notice_files/", height=150, width=1000)

    class Meta:
        verbose_name = "课程通知"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Content(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="课程章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"小节名称", null=True)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    learning_space = UEditorField(verbose_name="学习空间", default='', blank=True, imagePath='course_content/',
                                  toolbars="full", filePath="course_content_files/", )
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="课件资料", max_length=200, null=True,
                            blank=True)

    class Meta:
        verbose_name = "课程小节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    content = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="内容", default='')
    name = models.CharField(max_length=100, verbose_name=u"名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200, null=True,
                            blank=True)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
