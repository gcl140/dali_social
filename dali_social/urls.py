# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('members.urls')),
#     path('posts/', include('posts.urls')),
#     path('connections/', include('connections.urls')),
#     path('api/', include('members.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from members import views as member_views
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create router for API
router = DefaultRouter()
router.register(r'members', member_views.MemberViewSet)
handler404 = 'yuzzaz.views.custom_404_view'

def logout_then_google(request):
    logout(request)
    return redirect('/oauth/login/google-oauth2/?next=/profile/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),  # HTML views
    path('', include('posts.urls')),
    path('connections/', include('connections.urls')),
    path('accounts/', include('yuzzaz.urls')),  # HTML views
    path('api/', include(router.urls)),  # API endpoints

    path('oauth/', include('social_django.urls', namespace='social')),
    path('oauth/login/google/', logout_then_google, name='logout-then-google'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)