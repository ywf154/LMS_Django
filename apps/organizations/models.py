from django.db import models

from DjangoUeditor.models import UEditorField

from users.models import BaseModel


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name=u"城市名")
    desc = models.CharField(max_length=200, verbose_name=u"描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrgCategory(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"机构类别名")
    class Meta:
        verbose_name = "机构类别"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Org(BaseModel):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")
    desc = UEditorField(verbose_name='描述', default='', blank=True, imagePath='org_desc/', toolbars="full",
                        filePath="org_desc_files/", )
    category = models.ForeignKey(OrgCategory, on_delete=models.CASCADE, verbose_name="机构类别")

    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    students = models.IntegerField(default=0, verbose_name="学习人数")

    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="机构地址")

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_num(self):
        return self.course_set.count()



from users.models import UserProfile


class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", default="teacher_img_default.jpg")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()
