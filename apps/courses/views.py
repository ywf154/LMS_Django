from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from courses.forms import *
from courses.models import *
from operations.forms import TaskForm
from operations.models import *


class CourseView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.filter(status=1)
        categs = CourseCategory.objects.all()
        categ = request.GET.get('categ', '')
        if categ:
            all_courses = all_courses.filter(category_id=int(categ))
        search = request.GET.get('search', '')
        if search:
            all_courses = all_courses.filter(name__contains=search)
        # 排序
        sort = request.GET.get('sort', '')
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "fav_nums":
            all_courses = all_courses.order_by("-fav_nums")
        course_list = Paginator(all_courses, 4)
        pages = request.GET.get('page')
        try:
            courses = course_list.page(pages)
        except EmptyPage:
            courses = course_list.page(course_list.num_pages)
        except PageNotAnInteger:
            courses = course_list.page(1)
        return render(request, 'course_list.html', locals())


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=course_id, fav_type=2, user=request.user)
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        return render(request, "course_detail_base.html", {'course': course, 'fav': fav})


class CourseDetail_home(View):
    def get(self, request, course_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=course_id, fav_type=2, user=request.user)
        course = Course.objects.get(id=course_id)
        return render(request, "course-detail-homepage.html", {'course': course, 'fav': fav})


class CourseDetail_descView(View):
    def get(self, request, course_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=course_id, fav_type=2, user=request.user)
        course = Course.objects.get(id=course_id)
        return render(request, "course-detail-desc.html", {'course': course, 'fav': fav})


class CourseDetail_teacherView(View):
    def get(self, request, course_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=course_id, fav_type=2, user=request.user)
        course = Course.objects.get(id=course_id)
        return render(request, "course-detail-teacher.html", {'course': course, 'fav': fav})


class CourseDetail_startView(View):
    def get(self, request, course_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=course_id, fav_type=2, user=request.user)
        course = Course.objects.get(id=course_id)
        lesson_list = course.lesson_set.all()
        notices = course.notice_set.all()
        courseComments = CourseComments.objects.filter(course=course).order_by('-add_time')
        form = CourseCommentsForms()
        return render(request, "course-detail-start.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        if course_id:
            form = CourseCommentsForms(request.POST)
            if form.is_valid():
                comments = form.cleaned_data['comments']
                comment = CourseComments(course_id=course_id, user=request.user, comments=comments)
                comment.save()
                messages.success(request,'Successfully Commented')
                return redirect('CourseDetail_start', course_id)


class Course_learn(View):
    def get(self, request, tid, *args, **kwargs):
        if tid:
            content = Content.objects.get(id=tid)
            # 纳入我的课程
            UserCourse_list = UserCourse.objects.filter(course_id=content.lesson.course_id, user_id=request.user.id).first()
            if not UserCourse_list:
                student = UserCourse(course_id=content.lesson.course_id, user_id=request.user.id)
                student.save()
            task = Task.objects.filter(content__id=tid, user_id=request.user.id).first()
            if task:
                form = TaskForm(instance=task)
            else:
                form = TaskForm()
            return render(request, "course_learn.html", locals())


class Course_edit(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
        return render(request, "Course_edit.html", locals())


class Course_edite_home(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
        return render(request, "course_edite_home.html", locals())


class Course_edit_desc(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
        form = CourseBaseForm(instance=course)
        DitailForm = CourseDetailForm(instance=course)
        undisplayed = request.GET.get('undisplayed', '')
        return render(request, "Course_edit_desc.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
        form = CourseBaseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('Course_edit_desc', course_id=course.id)
        errs = form.errors
        return render(request, "Course_edit_desc.html", locals())


class Post_detail(View):
    def post(self, request, cid, *args, **kwargs):
        if cid:
            course = Course.objects.get(id=cid)
        DitailForm = CourseDetailForm(request.POST, instance=course, files=request.FILES)
        if DitailForm.is_valid():
            DitailForm.save()
            # messages.success('Ok')
            return redirect('Course_edit_desc', course_id=course.id)
        # messages.success('Bad')
        return redirect('Course_edit_desc', course_id=course.id)


class Add_notice(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
        notices = Notice.objects.filter(course=course).all()
        form = NoticeForm()
        return render(request, "add_notice.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
        form = NoticeForm(request.POST, instance=course, files=request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            notice = Notice(title=title, content=content, course=course)
            notice.save()
        return redirect('add_notice', course_id=course_id)


class Add_lesson(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course = Course.objects.get(id=course_id)
            lesson_list = course.lesson_set.all()
            lesson_form = LessonForm()
            courseComments = CourseComments.objects.filter(course=course).order_by('-add_time')
            notices = Notice.objects.filter(course=course)
            return render(request, "add_lesson.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            name = lesson_form.cleaned_data['name']
            lesson = Lesson(name=name, course=course)
            lesson.save()
        return redirect('add_lesson', course_id=course_id)


class Lesson_edit(View):
    def get(self, request, lid, *args, **kwargs):
        lesson = Lesson.objects.get(id=lid)
        contents = Content.objects.filter(lesson=lesson).all()
        form = ContentForm()
        return render(request, "Lesson_edit.html", locals())

    def post(self, request, lid, *args, **kwargs):
        lesson = Lesson.objects.get(id=lid)
        form = ContentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = Content(name=name, lesson=lesson)
            content.save()
            return redirect('Lesson_edit', lid=lid)
        return render(request, "Lesson_edit.html", locals())


class Uploadfile(View):
    def post(self, request, tid, *args, **kwargs):
        file_form = Content_upload_Form(request.POST, files=request.FILES)
        if tid:
            content = Content.objects.get(id=tid)
            if file_form.is_valid():
                content.file = file_form.cleaned_data['file']
                content.save()
                messages.success(request, '上传成功！')
                return redirect('Content_edit', tid=tid)
        messages.error(request, '上传失败！')
        return redirect('Content_edit', tid=tid)


class Content_edit(View):
    def get(self, request, tid, *args, **kwargs):
        content = Content.objects.filter(id=tid).first()

        form = ContentSpqaceForm(instance=content)
        file_form = Content_upload_Form(instance=content)
        messages.get_messages(request)  # 触发消息存储的处理
        return render(request, "Content_edit.html", locals())

    def post(self, request, tid, *args, **kwargs):
        content = Content.objects.filter(id=tid).first()
        form = ContentSpqaceForm(request.POST, files=request.FILES, instance=content)
        if form.is_valid():
            content.learning_space = form.cleaned_data['learning_space']
            content.name = form.cleaned_data['name']
            content.save()
            messages.success(request, '修改成功！')
            return redirect('Content_edit', tid=content.id)
        messages.success(request, '修改失败！')
        return render(request, "Content_edit.html", locals())


class Content_delete(View):
    def get(self, request, tid, *args, **kwargs):
        if tid:
            content = Content.objects.filter(id=tid).first()
            lesson_id = content.lesson.id  # 保存要删除内容所属的课程ID
            content.delete()
            return redirect('Lesson_edit', lid=lesson_id)


class Delete_lesson(View):
    def get(self, request, lid, *args, **kwargs):
        lesson = Lesson.objects.get(id=lid)
        if lesson:
            course_id = lesson.course.id  # 保存要删除内容所属的课程ID
            lesson.delete()
            messages.success(request, 'ok')
            return redirect('add_lesson', course_id=course_id)
        return HttpResponse("删除操作被取消")  # 返回一个适当的响应对象


class unDisplay_course(View):
    def get(self, request, cid, *args, **kwargs):
        course = Course.objects.get(id=cid)
        course.status = False
        course.save()
        messages.add_message(request, messages.SUCCESS, '已关闭课程')
        return redirect('teacherZoom')


class display_course(View):
    def get(self, request, cid, *args, **kwargs):
        course = Course.objects.get(id=cid)
        course.status = True
        course.save()
        messages.add_message(request, messages.SUCCESS, '已开启课程')
        return redirect('teacherZoom')
