from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model

from users.models import BaseModel
from courses.models import Course, Lesson, Content, Notice

UserProfile = get_user_model()


class Banner(BaseModel):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=200, verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments


class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=((2, "课程"), (1, "课程机构"), (3, "讲师")), default=1,
                                   verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, verbose_name="来自的通知", default=None)
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.notice.title


class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name


class Task(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="学生")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="所属章节")
    detail = UEditorField(verbose_name="课程编辑", default='', blank=True, imagePath='task/img/',toolbars="full", filePath='task/file/')
    grade = models.IntegerField(verbose_name="成绩", default=0)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.content) + '作业'
