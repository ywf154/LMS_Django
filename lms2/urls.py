from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from lms2 import settings
from courses.views import CourseView, CourseDetailView, CourseDetail_descView, CourseDetail_teacherView, \
    CourseDetail_startView, Course_learn
from operations.views import User_fav, task, EditTask
from organizations.views import OrganizationsView, OrgDetailView, OrgDetail_descView, OrgDetail_teacherView, \
    OrgDetail_courseView, OrgDetail_home
from users.views import LoginView, LogoutView, UserEditView, UserCenterView, RegisterView, ChangePasswordView, \
      UserCourses, Delete_course, UserFav, DeleteFav

urlpatterns = [
      path('admin/', admin.site.urls),
      # 首页
      path('', TemplateView.as_view(template_name='index.html'), name='index'),
      # 用户：
      path('login/', LoginView.as_view(), name='login'),
      path('logout/', LogoutView.as_view(), name='logout'),
      path('register/', RegisterView.as_view(), name='register'),
      path('userEdit/', UserEditView.as_view(), name='userEdit'),
      path('UserCenter/', UserCenterView.as_view(), name='UserCenter'),
      path('changPWD/', ChangePasswordView.as_view(), name='ChangePassword'),
      path('userFav/', UserFav.as_view(), name='userFav'),
      path('delete_course/<int:fav_id>/', DeleteFav.as_view(), name='deleteFav'),
      path('userCourses/', UserCourses.as_view(), name='userCourses'),
      path('delete_course/<int:cid>/', Delete_course.as_view(), name='delete_course'),
      # 机构：
      path('OrgList/', OrganizationsView.as_view(), name='OrganizationsView'),
      path('OrgDetail/<int:org_id>/', OrgDetailView.as_view(), name='OrgDetail'),
      path('OrgDetail_home/<int:org_id>/', OrgDetail_home.as_view(), name='OrgDetail_home'),
      path('OrgDetail_desc/<int:org_id>/', OrgDetail_descView.as_view(), name='OrgDetail_desc'),
      path('OrgDetail_teacher/<int:org_id>/', OrgDetail_teacherView.as_view(), name='OrgDetail_teacher'),
      path('OrgDetail_course/<int:org_id>/', OrgDetail_courseView.as_view(), name='OrgDetail_course'),
      # 课程
      path('CourseList/', CourseView.as_view(), name='CourseList'),
      path('CourseDetail/<int:course_id>/', CourseDetailView.as_view(), name='CourseDetail'),
      path('CourseDetail_desc/<int:course_id>/', CourseDetail_descView.as_view(), name='CourseDetail_desc'),
      path('CourseDetail_teacher/<int:course_id>/', CourseDetail_teacherView.as_view(),
           name='CourseDetail_teacher'),
      path('CourseDetail_start/<int:course_id>/', CourseDetail_startView.as_view(),
           name='CourseDetail_start'),
      path('Course_learn/<int:cid>/<int:lid>/<int:tid>/', Course_learn.as_view(), name='Course_learn'),

      # 操作
      re_path(r'user_fav/$', User_fav.as_view(), name='user_fav'),

      # 作业
      path('task/<int:cid>/<int:lid>/<int:tid>/', task.as_view(), name='task'),
      path('EditTask/<int:task_id>/', EditTask.as_view(), name='EditTask'),

      path('_nested_admin/', include('nested_admin.urls')),
      path('ueditor/', include('DjangoUeditor.urls')),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
