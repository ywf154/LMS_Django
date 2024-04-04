from django.shortcuts import render, redirect
from django.views.generic import View
from organizations.models import CourseOrg, City, Teacher
# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operations.models import UserFavorite
from courses.models import Course

def get_org_data(org_id, user):
    if user.is_authenticated:
        org = CourseOrg.objects.filter(id=int(org_id))[0]
        fav = UserFavorite.objects.filter(fav_id=int(org_id), fav_type=1, user=user)
        fav_count = UserFavorite.objects.filter(fav_type=1, fav_id=org_id).count()
        course_count = org.course_set.count()
        return org, fav, fav_count, course_count


class OrganizationsView(View):
    def get(self, request, *args, **kwargs):
        # 总的机构
        all_orgs = CourseOrg.objects.all()
        # 总的城市
        all_citys = City.objects.all()

        # 对课程类别进行筛选
        categ = request.GET.get('categ', '')
        if categ:
            all_orgs = all_orgs.filter(category=categ)

        # 对进行城市筛选
        cityid = request.GET.get('cityid', '')
        if cityid:
            all_orgs = all_orgs.filter(city_id=int(cityid))

        # 排序
        sort = request.GET.get('sort', '')
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "course_nums":
            all_orgs = all_orgs.order_by("-course_nums")

        # 此时的 all_orgs 是经过  课程类别筛选、城市筛选、学习人数/课程数  三重url的平接
        # ?categ={{ categ }}&cityid={{ cityid }}&sort={{ sort }}"

        # 分页
        orgs_list = Paginator(all_orgs, 4)
        pages = request.GET.get('page')
        try:
            orgs = orgs_list.page(pages)
        except EmptyPage:
            orgs = orgs_list.page(orgs_list.num_pages)
        except PageNotAnInteger:
            orgs = orgs_list.page(1)
        # 每页5条数据
        return render(request, 'org_list.html', locals())


class OrgDetailView(View):
    def get(self, request, org_id, *args, **kwargs):
        if org_id:
            org, fav, fav_count, course_count = get_org_data(org_id, request.user)
            org.click_nums += 1
            org.save()
        return render(request, "org_detail_base.html", locals())


class OrgDetail_home(View):
    def get(self, request, org_id, *args, **kwargs):
        if org_id:
            org, fav, fav_count, course_count = get_org_data(org_id, request.user)
        return render(request, "org-detail-homepage.html", locals())


class OrgDetail_descView(View):
    def get(self, request, org_id, *args, **kwargs):
        if org_id:
            org, fav, fav_count, course_count = get_org_data(org_id, request.user)
        return render(request, "org-detail-desc.html", locals())


class OrgDetail_teacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        if org_id:
            org, fav, fav_count, course_count = get_org_data(org_id, request.user)
        return render(request, "org-detail-teacher.html", locals())


class OrgDetail_courseView(View):
    def get(self, request, org_id, *args, **kwargs):
        if org_id:
            org, fav, fav_count, course_count = get_org_data(org_id, request.user)
        return render(request, "org-detail-course.html", locals())


class TeacherZoom(View):
    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.filter(user_id=request.user.id).first()
        if not teacher:
            return redirect('index')
        name = teacher.name
        courses = Course.objects.filter(teacher_id=teacher.id).all()

        return render(request, "teacher.html", locals())
