from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from courses.forms import CourseModelForm
from courses.models import Course, CourseCategory
from operations.models import UserCourse, UserFavorite
from organizations.models import Org, Teacher
from .forms import RegistrationForm, UserEditForm, ChangePwdForm, TeacherEditForm


class UserEditView(View):
    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'You have updated information！')
            return redirect('index')
        messages.error(request, 'You have not updated any information')
        return redirect('index')


class TeacherEditView(View):
    def post(self, request, *args, **kwargs):
        formTeacher = TeacherEditForm(request.POST, instance=request.user.teacher, files=request.FILES)
        if request.user.is_authenticated and formTeacher.is_valid():
            formTeacher.save()
            messages.success(request, 'You have updated information！')
            return redirect('teacherZoom')
        messages.error(request, 'You have not updated any information')
        return redirect('teacherZoom')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if not username:
            return render(request, 'login.html', {'错误': '请输入用户名'})
        if not password:
            return render(request, 'login.html', {'错误': '请输入密码'})
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {'错误': '用户名或密码错误'})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'register.html', locals())

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'register.html', locals())


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            messages.success(request, 'You have changed your password！')
            return redirect('index')
        else:
            messages.error(request, 'You have not changed your password！')
            return redirect('index')


class UserCourses(View):
    def get(self, request, *args, **kwargs):
        uc_list = UserCourse.objects.filter(user=request.user)
        courses = [uc.course for uc in uc_list]
        return render(request, 'userCourses.html', locals())


class Delete_course(View):
    def get(self, request, cid, *args, **kwargs):
        if cid:
            UserCourse.objects.filter(course_id=cid, user=request.user).first().delete()
            return redirect('userCourses')
        return JsonResponse({'status': 'error', 'msg': '删除失败'})


class UserFav(View):
    def get(self, request, *args, **kwargs):
        fav_orgs = UserFavorite.objects.filter(user_id=request.user.id, fav_type=1)
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_orgs = [Org.objects.filter(id=CFav.fav_id).first() for CFav in fav_orgs]
        fav_courses = [Course.objects.filter(id=OFav.fav_id).first() for OFav in fav_courses]
        return render(request, 'userFav.html', locals())


class DeleteFav(View):
    def get(self, request, fav_id, *args, **kwargs):
        user_fav = get_object_or_404(UserFavorite, fav_id=fav_id, user_id=request.user.id)
        if user_fav:
            user_fav.delete()
            return redirect('userFav')
        return JsonResponse({'status': 'error', 'msg': '删除失败'})


class TeacherZoom(View):
    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.filter(user=request.user).first()
        if not teacher:
            return redirect('index')
        form = CourseModelForm()
        categs = CourseCategory.objects.all()

        all_courses = Course.objects.filter(teacher_id=teacher.id).order_by('-status', '-add_time').all()

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
        return render(request, "teacher_zoom.html", locals())

    def post(self, request, *args, **kwargs):
        teacher = Teacher.objects.filter(user_id=request.user.id).first()
        if not teacher:
            return redirect('index')
        form = CourseModelForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            desc = form.cleaned_data['desc']
            course = Course(name=name, category=category, teacher_id=teacher.id, org_id=teacher.org_id, desc=desc)
            course.save()
        return render(request, "teacher_zoom.html", locals())
