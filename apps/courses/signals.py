from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Notice
from operations.models import UserCourse, UserMessage


@receiver(post_save, sender=Notice)
def notice_saved(sender, instance, created, **kwargs):
    if created:
        in_course_users = UserCourse.objects.filter(course=instance.course)
        for in_course_user in in_course_users:
            userMessage = UserMessage.objects.create(user=in_course_user.user, notice=instance)
            userMessage.save()
    else:
        # 检查是否有已存在的 UserMessage 记录
        existing_messages = UserMessage.objects.filter(notice=instance)
        # 如果有已存在的记录,更新它们
        if existing_messages:
            for message in existing_messages:
                message.notice = instance
                message.has_read = False
                message.save()
        # 如果没有已存在的记录,创建新的 UserMessage 记录
        else:
            in_course_users = UserCourse.objects.filter(course=instance.course)
            for in_course_user in in_course_users:
                userMessage = UserMessage.objects.create(user=in_course_user.user, notice=instance)
                userMessage.save()

