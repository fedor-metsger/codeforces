
from django.contrib import admin
from django.urls import path

from crontab import manager
from problems.views import index_view, ProblemListView, TagListView, TagDetailView

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', index_view, name='index'),
    path('problem/', ProblemListView.as_view(), name='problem_list'),
    path('tag/', TagListView.as_view(), name='tag_list'),
    path('tag/<int:pk>', TagDetailView.as_view(), name='tag_detail'),
    path('scan/', manager.scan_codeforces, name='scan'),
    path('distribute/', manager.distribute, name='distribute'),
    path('crontab/', manager.switch_crontab, name='switch_crontab')
]
