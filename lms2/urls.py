from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from lms2 import settings
from courses.views import *
from operations.views import *
from organizations.views import *
from users.views import *

urlpatterns = [
      path('admin/', admin.site.urls),
      # 首页
      path('', Index.as_view(), name='index'),
      # 用户：
      path('login/', LoginView.as_view(), name='login'),
      path('logout/', LogoutView.as_view(), name='logout'),
      path('register/', RegisterView.as_view(), name='register'),
      path('userEdit/', UserEditView.as_view(), name='userEdit'),
      path('TeacherEdit/', TeacherEditView.as_view(), name='teacherEdit'),
      path('changPWD/', ChangePasswordView.as_view(), name='CPW'),
      path('userFav/', UserFav.as_view(), name='userFav'),
      path('deleteFav/<int:fav_id>/', DeleteFav.as_view(), name='deleteFav'),
      path('userCourses/', UserCourses.as_view(), name='userCourses'),
      path('delete_course/<int:cid>/', Delete_course.as_view(), name='delete_course'),
      path('Message/', Message.as_view(), name='Message'),
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
      path('CourseDetail_home/<int:course_id>/', CourseDetail_home.as_view(), name='CourseDetail_home'),
      path('CourseDetail_desc/<int:course_id>/', CourseDetail_descView.as_view(), name='CourseDetail_desc'),
      path('CourseDetail_teacher/<int:course_id>/', CourseDetail_teacherView.as_view(),
           name='CourseDetail_teacher'),
      path('CourseDetail_start/<int:course_id>/', CourseDetail_startView.as_view(),
           name='CourseDetail_start'),
      path('Course_learn/<int:tid>/', Course_learn.as_view(), name='Course_learn'),

      # 教师课程
      path('teacherZoom/', TeacherZoom.as_view(), name='teacherZoom'),
      path('teacherZoom/Course_edit/<int:course_id>/', Course_edit.as_view(), name='Course_edit'),
      path('teacherZoom/Course_edit/<int:course_id>/desc/', Course_edit_desc.as_view(),
           name='Course_edit_desc'),
      path('teacherZoom/Course_edit/<int:course_id>/home/', Course_edite_home.as_view(),
           name='Course_edite_home'),
      path('teacherZoom/Course_edit/<int:course_id>/add_notice/', Add_notice.as_view(),
           name='add_notice'),
      path('teacherZoom/Course_edit/<int:course_id>/add_lesson/', Add_lesson.as_view(),
           name='add_lesson'),
      path('teacherZoom/Lesson_edit/<int:lid>/', Lesson_edit.as_view(), name='Lesson_edit'),
      path('teacherZoom/Content_edit/<int:tid>/', Content_edit.as_view(), name='Content_edit'),
      # 操作
      path('Content_delete/<int:tid>/', Content_delete.as_view(), name='Content_delete'),
      path('delete_lesson/<int:lid>/', Delete_lesson.as_view(), name='delete_lesson'),
      path('undisplay_course/<int:cid>/', unDisplay_course.as_view(), name='undisplay_course'),
      path('display_course/<int:cid>/', display_course.as_view(), name='display_course'),
      path('score/<int:task_id>/', Score.as_view(), name='score'),

      path('fav_org/<int:oid>/', Fav_org.as_view(), name='fav_org'),
      path('fav_course/<int:cid>/', Fav_course.as_view(), name='fav_course'),

      path('readMessage/<int:nid>/', ReadMessage.as_view(), name='readMessage'),
      path('task/<int:tid>/', task.as_view(), name='task'),
      path('edittask/<int:tid>/', editTask.as_view(), name='editTask'),

      path('uploadfile/<int:tid>/', Uploadfile.as_view(), name='uploadfile'),
      path('postdetail/<int:cid>/', Post_detail.as_view(), name='pD'),


      path('_nested_admin/', include('nested_admin.urls')),
      path('ueditor/', include('DjangoUeditor.urls')),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
