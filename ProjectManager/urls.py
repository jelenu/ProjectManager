from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from projects.views import CreateProjectAPIView, StatusPriorityAPIView
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('create_project/', CreateProjectAPIView.as_view(), name='create_project'),
    path('status_priority/', StatusPriorityAPIView.as_view(), name='status_priority'),


    path('auth/', include('djoser.urls')),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'), 
    path('auth/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

]
