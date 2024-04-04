from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from courses.models import Content, Lesson, Course
from operations.forms import TaskForm, TaskGradeForm

from operations.models import UserFavorite, Task, UserCourse, Banner, UserMessage
from organizations.models import Teacher


class User_fav(View):
    def get(self, request):
        fav_id = request.GET.get('fav_id')
        fav_type = request.GET.get('fav_type')
        if fav_id and fav_type:
            fav = UserFavorite.objects.filter(fav_id=fav_id, fav_type=fav_type, user=request.user)
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


class Index(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()
        user_courses = UserCourse.objects.filter(user_id=request.user.id)
        course_ids = user_courses.values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=course_ids)
        notice_list = [course.notice_set.order_by('-add_time').all() for course in courses]
        for notices in notice_list:
            for notice in notices:
                notice_exist = UserMessage.objects.filter(notice=notice)
                if not notice_exist:
                    my_notice = UserMessage(notice=notice, user=request.user)
                    my_notice.save()
        my_notices = UserMessage.objects.filter(has_read=0)
        notice_count = len(my_notices)
        # 处理老师和学生：老师看的界面是所授课程，学生看的是我的课程
        teacher = Teacher.objects.filter(user_id=request.user.id).first()
        return render(request, 'index.html', locals())


class Message(View):
    def get(self, request, *args, **kwargs):
        user_courses = UserCourse.objects.filter(user=request.user)
        course_ids = user_courses.values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=course_ids)
        notice_list = [course.notice_set.order_by('-add_time').all() for course in courses]
        for notices in notice_list:
            for notice in notices:
                notice_exist = UserMessage.objects.filter(notice=notice)
                if not notice_exist:
                    my_notice = UserMessage(notice=notice, user=request.user)
                    my_notice.save()
        my_notices = UserMessage.objects.filter(has_read=0)
        my_notices_has_read = UserMessage.objects.filter(has_read=1)
        notice_list = [my_notice.notice for my_notice in my_notices]
        notice_list_has_read = [my_notice.notice for my_notice in my_notices_has_read]
        return render(request, 'message.html', locals())


class ReadMessage(View):
    def get(self, request, nid, *args, **kwargs):
        if nid:
            message = UserMessage.objects.filter(notice_id=nid).first()
            message.has_read = True
            message.save()
            return redirect('Message')
        return JsonResponse({'status': 'error', 'msg': '失败'})


class ShowTask(View):
    def get(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        form = TaskGradeForm(instance=task)
        return render(request, 'showTask.html', locals())

    def post(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        form = TaskGradeForm(request.POST, instance=task)
        if form.is_valid():
            task.grade = form.cleaned_data['grade']
            task.save()
            return redirect('Lesson_edit', task.content.lesson.id)
        return render(request, 'showTask.html', locals())
