
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

    # def get_queryset(self):
    #     if "manager" in [i.name for i in self.request.user.groups.all()]:
    #         return super().get_queryset()
    #     return super().get_queryset().filter(owner=self.request.user).order_by('pk')
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
    #     return context_data


class TagListView(ListView):
    model = Tag
    extra_context = {
        'title': 'Теги'
    }
    paginate_by = 3

    # def get_queryset(self):
    #     if "manager" in [i.name for i in self.request.user.groups.all()]:
    #         return super().get_queryset()
    #     return super().get_queryset().filter(owner=self.request.user).order_by('pk')
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
    #     return context_data


class TagDetailView(DetailView):
    model = Tag
    extra_context = {
        'title': 'Тег'
    }
    paginate_by = 3

    # def get_queryset(self):
    #     if "manager" in [i.name for i in self.request.user.groups.all()]:
    #         return super().get_queryset()
    #     return super().get_queryset().filter(owner=self.request.user).order_by('pk')
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data["not_manager"] = "manager" not in [i.name for i in self.request.user.groups.all()]
    #     return context_data
