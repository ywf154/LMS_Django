from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from operations.models import UserCourse


@receiver(post_save, sender=UserCourse)
def user_study_course(sender, instance, created, **kwargs):
    if created:
        instance.course.students += 1
        instance.course.org.students += 1
        instance.course.org.save()
        instance.course.save()


@receiver(post_delete, sender=UserCourse)
def user_stop_study_course(sender, instance, **kwargs):
    instance.course.students -= 1
    instance.course.org.students -= 1
    instance.course.org.save()
    instance.course.save()