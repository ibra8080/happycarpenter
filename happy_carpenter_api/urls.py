from django.contrib import admin
from django.urls import path, include
from .views import root_route, CustomUserDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', root_route),
    path('', include('profiles.urls')),
    path('', include('posts.urls')),
    path('', include('likes.urls')),
    path('', include('follows.urls')),
    path('', include('professionals.urls')),
    path('', include('authentication.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/user/', CustomUserDetailsView.as_view(), name='rest_user_details'),
]
