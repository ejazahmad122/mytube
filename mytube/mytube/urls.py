from django.contrib import admin
from django.urls import path, include
from media import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('api/videos', views.MediaView, basename='mytube')
router.register('api/comments', views.CommentView, basename='mytubecomment')
router.register('api/likes', views.LikeView, basename='mytubelike')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('user/', include('account.urls'))
]
