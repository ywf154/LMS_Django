from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from courses.forms import *
from courses.models import *
from operations.models import *
from organizations.models import Teacher


def get_course_data(course_id, user):
    if user.is_authenticated:
        course = Course.objects.filter(id=int(course_id))[0]
        fav = UserFavorite.objects.filter(fav_id=int(course_id), fav_type=2, user=user)
        fav_count = UserFavorite.objects.filter(fav_type=2, fav_id=course_id).count()
        content_count = Content.objects.filter(lesson__course=course).count()
        student_count = UserCourse.objects.filter(course_id=course_id, user=user).count()
        return course, fav, fav_count, content_count, student_count


class CourseView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.all().order_by('-add_time')
        categs = set([course.category for course in all_courses])
        categs = [categ for categ in categs]
        categ = request.GET.get('categ', '')
        if categ:
            all_courses = all_courses.filter(category=categ)
        tag = request.GET.get('tag', '')
        if tag:
            all_courses = all_courses.filter(name__contains=tag)
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
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            course.click_nums += 1
            course.save()
        return render(request, "course_detail_base.html", locals())


class CourseDetail_home(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
        return render(request, "course-detail-homepage.html", locals())


class CourseDetail_descView(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
        return render(request, "course-detail-desc.html", locals())


class CourseDetail_teacherView(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
        return render(request, "course-detail-teacher.html", locals())


class CourseDetail_startView(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
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
                comment = CourseComments(course_id=course_id, user_id=request.user.id, comments=comments)
                comment.save()
                return redirect('CourseDetail_start', course_id)


class Course_learn(View):
    def get(self, request, cid, lid, tid, *args, **kwargs):
        if cid:
            UserCourse_list = UserCourse.objects.filter(course_id=cid, user_id=request.user.id).first()
            if not UserCourse_list:
                student = UserCourse(course_id=cid, user_id=request.user.id)
                student.save()
            course = Course.objects.filter(id=cid).first()
            all_lessons = course.lesson_set.all()
            if lid:
                lesson = all_lessons.filter(id=lid).first()
                all_contents = lesson.content_set.all()
                if tid:
                    content = all_contents.filter(id=tid).first()

        return render(request, "course_learn.html", locals())


class Course_edit(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            lesson_list = course.lesson_set.all()
        return render(request, "Course_edit.html", locals())


class Course_edite_home(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            lesson_list = course.lesson_set.all()
        return render(request, "course_edite_home.html", locals())


class Course_edit_desc(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            lesson_list = course.lesson_set.all()
        form = CourseBaseForm(instance=course)
        return render(request, "Course_edit_desc.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            lesson_list = course.lesson_set.all()
        form = CourseBaseForm(request.POST, instance=course, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Course_edit_desc', course_id=course.id)
        errs = form.errors
        return render(request, "Course_edit_desc.html", locals())


class Add_notice(View):
    def get(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            lesson_list = course.lesson_set.all()
        notices = Notice.objects.filter(course=course).order_by('-add_time').all()
        form = NoticeForm()
        return render(request, "add_notice.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        if course_id:
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
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
            course, fav, fav_count, content_count, student_count = get_course_data(course_id, request.user)
            lesson_list = course.lesson_set.all()
        form = LessonForm()
        courseComments = CourseComments.objects.filter(course=course).order_by('-add_time')
        notices = Notice.objects.filter(course=course).order_by('-add_time')
        return render(request, "add_lesson.html", locals())

    def post(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        form = LessonForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            lesson = Lesson(name=name, course=course)
            lesson.save()
        return redirect('add_lesson', course_id=course_id)


class Lesson_edit(View):
    def get(self, request, lid, *args, **kwargs):
        lesson = Lesson.objects.filter(id=lid).first()
        contents = Content.objects.filter(lesson=lesson).all()
        form = ContentForm()
        return render(request, "Lesson_edit.html", locals())

    def post(self, request, lid, *args, **kwargs):
        lesson = Lesson.objects.filter(id=lid).first()
        form = ContentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = Content(name=name, lesson=lesson)
            content.save()
            return redirect('Lesson_edit', lid=lid)
        return render(request, "Lesson_edit.html", locals())


class Uploadfile(View):
    def get(self, request, tid, *args, **kwargs):
        form = CourseResourceForm(request.POST, request.FILES)
        return render(request, "uploadfile.html", locals())

    def post(self, request, tid, *args, **kwargs):
        form = CourseResourceForm(request.POST, files=request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['file']
            courseResource = CourseResource(content_id=tid, file=file, name=name)
            courseResource.save()
            return redirect('Content_edit', tid=tid)
        return render(request, "uploadfile.html", locals())


class Content_edit(View):
    def get(self, request, tid, *args, **kwargs):
        content = Content.objects.filter(id=tid).first()
        courseResources = CourseResource.objects.filter(content_id=tid).all()
        form = ContentSpqaceForm(instance=content)
        return render(request, "Content_edit.html", locals())

    def post(self, request, tid, *args, **kwargs):
        content = Content.objects.filter(id=tid).first()
        form = ContentSpqaceForm(request.POST, files=request.FILES, instance=content)
        if form.is_valid():
            content.learning_space = form.cleaned_data['learning_space']
            content.save()
            return redirect('Lesson_edit', lid=content.lesson.id)
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
        lesson = Lesson.objects.filter(id=lid).first()
        if lesson:
            course_id = lesson.course.id  # 保存要删除内容所属的课程ID
            lesson.delete()
            return redirect('add_lesson', course_id=course_id)
