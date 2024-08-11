from users.forms import UserEditForm, TeacherEditForm, ChangePwdForm


class UserDataProcessor:
    def get_user_data(self, request):
        if request.user.is_authenticated:
            pwd_form = ChangePwdForm()
            user_form = UserEditForm(instance=request.user)
            if hasattr(request.user, 'teacher'):
                formTeacher = TeacherEditForm(instance=request.user.teacher)
                return {'user_form': user_form, 'pwd_form': pwd_form,  'formTeacher': formTeacher}
            return {'user_form': user_form, 'pwd_form': pwd_form, 'formTeacher': None}
        return {'user_form': None, 'pwd_form': None, 'formTeacher': None}


def user_data_processor(request):
    user_data_processor = UserDataProcessor()
    return user_data_processor.get_user_data(request)
