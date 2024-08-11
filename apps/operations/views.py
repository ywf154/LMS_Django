from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from courses.models import Content, Lesson, Course
from operations.forms import TaskForm, TaskGradeForm

from operations.models import UserFavorite, Task, Banner, UserMessage, UserCourse
from organizations.models import Org


class Fav_org(View):
    def get(self, request, oid, *args, **kwargs):
        if oid:
            fav = UserFavorite.objects.filter(fav_id=oid, fav_type=1, user=request.user).first()
            org = Org.objects.get(id=oid)
            if fav:
                fav.delete()
                org.fav_nums -= 1
                org.save()
                messages.success(request,'Favorite removed')
                return redirect('OrgDetail', oid)
            else:
                fav = UserFavorite(user_id=request.user.id, fav_id=oid, fav_type=1)
                fav.save()
                org.fav_nums += 1
                org.save()
                messages.success(request, 'Favorite added')
                return redirect('OrgDetail', oid)
        return JsonResponse({'status': 'error', 'msg': 'Invalid request.'})


class Fav_course(View):
    def get(self, request, cid, *args, **kwargs):
        if cid:
            fav = UserFavorite.objects.filter(fav_id=cid, fav_type=2, user=request.user).first()
            course = Course.objects.get(id=cid)
            if fav:
                fav.delete()
                course.fav_nums -= 1
                course.save()
                messages.success(request,'Favorite removed')
                return redirect('CourseDetail', cid)
            else:
                fav = UserFavorite(user_id=request.user.id, fav_id=cid, fav_type=2)
                fav.save()
                course.fav_nums += 1
                course.save()
                messages.success(request,'Favorite added')
                return redirect('CourseDetail',cid)
        return JsonResponse({'status': 'error', 'msg': 'Invalid request.'})


class task(View):
    def post(self, request, tid, *args, **kwargs):
        form_task = TaskForm(request.POST)
        if form_task.is_valid():
            detail = form_task.cleaned_data['detail']
            task = Task(content_id=tid, detail=detail, user_id=request.user.id)
            task.save()
            messages.success(request, 'ok')
            return redirect('Course_learn', tid)


class editTask(View):
    def post(self, request, tid, *args, **kwargs):
        form = TaskForm(request.POST)
        task_in = Task.objects.filter(content_id=tid, user_id=request.user.id).first()
        if form.is_valid():
            detail = form.cleaned_data['detail']
            task_in.detail = detail
            task_in.save()
            messages.success(request, 'ok')
            return redirect('Course_learn', tid)


class Index(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()
        recommend_orgs = Org.objects.order_by("students")[0:9]
        recommend_courses = Course.objects.order_by("students")
        fav_courses = UserFavorite.objects.filter(user_id=request.user.id, fav_type=2).all()
        favIds = [favCourse.id for favCourse in fav_courses]
        my_fav_courses = Course.objects.filter(id__in=favIds)[0:6]
        courses = UserCourse.objects.filter(user_id=request.user.id)
        courseIds = [course.id for course in courses]
        my_courses = Course.objects.filter(id__in=courseIds)[0:6]

        course_count = UserCourse.objects.filter(user_id=request.user.id).count()
        fav_course_count = UserFavorite.objects.filter(user_id=request.user.id, fav_type=2).count()
        return render(request, 'index.html', locals())


class Message(View):
    def get(self, request, *args, **kwargs):
        userMsgs = UserMessage.objects.filter(user=request.user, has_read=False)
        userMsgs_has_read = UserMessage.objects.filter(user=request.user, has_read=True)
        return render(request, 'message.html', locals())


class ReadMessage(View):
    def get(self, request, nid, *args, **kwargs):
        if nid:
            message = UserMessage.objects.filter(notice_id=nid, user=request.user)[0]
            if message is None:
                return JsonResponse({'status': 'error', 'msg': '未找到该条消息'})
            message.has_read = True
            message.save()
            return redirect('Message')
        return JsonResponse({'status': 'error', 'msg': '失败'})


class Score(View):
    def get(self, request, task_id, *args, **kwargs):
        score = request.GET.get('score')
        task = Task.objects.get(id=task_id)
        if task is None:
            messages.error(request, 'not found')
            return JsonResponse({'not found'})
        task.grade = int(score)
        task.save()
        messages.success(request, 'ok')
        return redirect('Content_edit', task.content_id)
