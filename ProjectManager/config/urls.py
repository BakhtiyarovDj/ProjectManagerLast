#urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings
from users.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acc-auth/', include('rest_framework.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('users/', include("users.urls")), 
    path('', include('announcements.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

