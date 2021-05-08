from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='search'),
                  path('result/', views.result,name='result'),
                  # path('detail/', views.detail,name='detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

