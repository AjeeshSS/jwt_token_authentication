from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from myapp.views import*
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', RegisterUser.as_view(), name='register'),
    
    path('userlist/', UserListView.as_view(), name='userlist'),
    path('user/<id>', GetUser.as_view(), name='get_user'),
    path('edit/<id>', EditUser.as_view()),
    path('delete/<id>', DeleteUser.as_view()),
    path('searchuser/',SearchUserView.as_view()),
    
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('logout/blacklist/', BlacklistRefreshView.as_view(),name='blacklist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
