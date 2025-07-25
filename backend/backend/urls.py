from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from api.views import CreateUserView, MyTokenObtainPairView, GetUser, UserUpdate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name='register'),
    path("api/users/<int:id>/", GetUser.as_view(), name="get-user"),
    path('api/token/get/', MyTokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/user/update/', UserUpdate.as_view(), name='update-user'),
    path('api-auth/', include('rest_framework.urls')),
    path("api/", include('posts.urls')),
    path("api/", include('teams.urls')),
    path("api/", include('venue.urls')),
    path("api/", include('matches.urls'))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
