from operations.models import UserMessage
from organizations.models import Teacher


class NavbarDataProcessor:
    def navbar_data(self, request):
        try:
            notice_count = UserMessage.objects.filter(user=request.user, has_read=0).count()
            teacher = Teacher.objects.filter(user=request.user).first()
            return {'notice_count': notice_count, 'teacher': teacher}
        except:
            return {'notice_count': 0, 'teacher': None}


def navbar_data_processor(request):
    navbar_data_processor = NavbarDataProcessor()
    try:
        return navbar_data_processor.navbar_data(request)
    except:
        return {'notice_count': 0, 'teacher': None}
