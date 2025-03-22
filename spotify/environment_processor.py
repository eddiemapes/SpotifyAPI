from django.contrib.auth.models import User
from core.models import Profile

def environment_processor(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile': profile}
    return {}
