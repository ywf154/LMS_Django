from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from courses.models import Content, Lesson, Course
from operations.forms import TaskForm

from operations.models import UserFavorite, Task, UserCourse


class User_fav(View):
    def get(self, request):
        fav_id = request.GET.get('fav_id')
        fav_type = request.GET.get('fav_type')
        if fav_id and fav_type:
            fav = UserFavorite.objects.filter(fav_id=int(fav_id), fav_type=int(fav_type), user=request.user)
            if fav:
                fav.delete()
                return JsonResponse({'status': 'ok', 'msg': 'Favorite removed.'})
            else:
                fav = UserFavorite()
                fav.user = request.user
                fav.fav_id = fav_id
                fav.fav_type = fav_type
                fav.save()
                return JsonResponse({'status': 'ok', 'msg': 'Favorite added.'})
        return JsonResponse({'status': 'error', 'msg': 'Invalid request.'})


class task(View):
    def get(self, request, cid, lid, tid, *args, **kwargs):
        task = Task.objects.filter(user_id=request.user.id, content_id=tid).first()
        if not task:
            form = TaskForm()
        # 是否已交：未交：form;已交：task
        return render(request, 'task.html', locals())

    def post(self, request, cid, lid, tid, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            detail = form.cleaned_data['detail']
            task = Task(detail=detail, user_id=request.user.id, content_id=tid)
            task.save()
            return redirect('task', cid, lid, tid)
        errors = form.errors
        return redirect(request, 'task.html', locals())


class EditTask(View):
    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.filter(id=task_id).first()
        tid = task.content_id
        lid = Content.objects.get(id=tid).lesson_id
        cid = Lesson.objects.get(id=lid).course_id
        form = TaskForm(request.POST)
        return render(request, 'editTask.html', locals())

    def post(self, request, task_id, *args, **kwargs):
        task = Task.objects.filter(id=task_id).first()
        tid = task.content_id
        lid = Content.objects.get(id=tid).lesson_id
        cid = Lesson.objects.get(id=lid).course_id
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            detail = form.cleaned_data['detail']
            task.detail = detail
            task.save()
            return redirect('task', cid, lid, tid)
        errors = form.errors
        return render(request, 'editTask.html', locals())



