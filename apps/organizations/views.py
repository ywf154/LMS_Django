from django.shortcuts import render, redirect
from django.views.generic import View
from organizations.models import Org, City, Teacher, OrgCategory
# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operations.models import UserFavorite
from courses.models import Course


class OrganizationsView(View):
    def get(self, request, *args, **kwargs):
        categs = OrgCategory.objects.all()
        # 总的机构
        all_orgs = Org.objects.all()
        # 总的城市
        all_citys = City.objects.all()

        # 对课程类别进行筛选
        categ = request.GET.get('categ', '')
        if categ:
            all_orgs = all_orgs.filter(category_id=int(categ))

        # 对进行城市筛选
        search = request.GET.get('search', '')
        if search:
            all_orgs = all_orgs.filter(city_id=int(search))

        # 排序
        sort = request.GET.get('sort', '')
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "fav_nums":
            all_orgs = all_orgs.order_by("-fav_nums")

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
        fav = UserFavorite.objects.filter(fav_id=int(org_id), fav_type=1, user=request.user)
        if org_id:
            org = Org.objects.filter(id=org_id)[0]
            org.click_nums += 1
            org.save()
        return render(request, "org_detail_base.html", locals())


class OrgDetail_home(View):
    def get(self, request, org_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=int(org_id), fav_type=1, user=request.user)
        if org_id:
            org = Org.objects.filter(id=org_id)[0]
            org_course_set_all = org.course_set.filter(status=1)
        return render(request, "org-detail-homepage.html", locals())


class OrgDetail_descView(View):
    def get(self, request, org_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=int(org_id), fav_type=1, user=request.user)
        if org_id:
            org = Org.objects.filter(id=org_id)[0]
        return render(request, "org-detail-desc.html", locals())


class OrgDetail_teacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=int(org_id), fav_type=1, user=request.user)
        if org_id:
            org = Org.objects.filter(id=org_id)[0]
        return render(request, "org-detail-teacher.html", locals())


class OrgDetail_courseView(View):
    def get(self, request, org_id, *args, **kwargs):
        fav = UserFavorite.objects.filter(fav_id=int(org_id), fav_type=1, user=request.user)
        if org_id:
            org = Org.objects.filter(id=org_id)[0]
            org_course_set_all = org.course_set.filter(status=1)
        return render(request, "org-detail-course.html", locals())


class TeacherZoom(View):
    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.filter(user=request.user).first()
        if not teacher:
            return redirect('index')
        courses = Course.objects.filter(teacher=teacher).all()
        return render(request, "teacher.html", locals())
