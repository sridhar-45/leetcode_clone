from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/problems/', include('problems.urls')),
    path('api/submissions/', include('submissions.urls')),
    path('api/contests/', include('contests.urls')),
    path('api/groups/', include('groups.urls')),
    path('api/leaderboard/', include('leaderboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)