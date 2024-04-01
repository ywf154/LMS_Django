from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from courses.models import Course, Lesson, Content
from operations.models import UserFavorite, UserCourse, CourseComments


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
        categ = request.GET.get('categ', '')
        if categ:
            all_courses = all_courses.filter(category=categ)
        tag = request.GET.get('tag', '')
        if tag:
            all_courses = all_courses.filter(tag=tag)
        degree = request.GET.get('degree', '')
        if degree:
            all_courses = all_courses.filter(degree=degree)
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
        return render(request, "course-detail-start.html", locals())


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
