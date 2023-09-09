
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from crontab.manager import ScraperManager
from problems.models import Problem, Tag


# Create your views here.
def index_view(request):
    problems = Problem.objects.count()
    tags = Tag.objects.count()

    crontab_status = "Запущен" if ScraperManager.crontab_status else "Остановлен"
    context = {
        "problems": problems,
        "tags": tags,
        "crontab_status": crontab_status
    }
    return render(request, "problems/index.html", context=context)


class ProblemListView(ListView):
    model = Problem
    extra_context = {
        'title': 'Задачи'
    }
    paginate_by = 10


class TagListView(ListView):
    model = Tag
    extra_context = {
        'title': 'Теги'
    }
    paginate_by = 3


class TagDetailView(DetailView):
    model = Tag
    extra_context = {
        'title': 'Тег'
    }
    paginate_by = 3
