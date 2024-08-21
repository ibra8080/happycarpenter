from rest_framework.decorators import api_view
from rest_framework.response import Response
from dj_rest_auth.views import UserDetailsView
from .serializers import CurrentUserSerializer

@api_view()
def root_route(request):
    return Response({"message": "Welcome to Happy Carpenter API!"})

class CustomUserDetailsView(UserDetailsView):
    serializer_class = CurrentUserSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            profile_data = CurrentUserSerializer(request.user).data.get('profile')
            response.data['profile'] = profile_data
        return response