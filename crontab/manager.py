
from datetime import datetime
import os

from django.shortcuts import redirect

from problems.models import Tag, Problem, Belonging
from scraper.scraper import LOG_FILE_NAME, log_to_file, scrape_api


class ScraperManager():
    crontab_status = False


def switch_crontab(request):
    if ScraperManager.crontab_status:
        log_to_file(f'-------------------------------\nCrontab disbled at {datetime.utcnow().time()}\n')
        os.system(f'./manage.py crontab remove >> {LOG_FILE_NAME}')
    else:
        log_to_file(f'-------------------------------\nCrontab enbled at {datetime.utcnow().time()}\n')
        os.system(f'./manage.py crontab add >> {LOG_FILE_NAME}')
    ScraperManager.crontab_status = not ScraperManager.crontab_status
    return redirect('index')


def scan() -> int:
    # problems = scrape_data()
    problems = scrape_api()

    if problems:
        for n, p in problems.items():
            if Problem.objects.filter(number=n).exists():
                prob = Problem.objects.get(number=n)
            else:
                prob = Problem.objects.create(
                    number=n,
                    name=p["name"],
                    solutions=p["solutions"],
                    difficulty=p["difficulty"]
                )
            for t in p["tags"]:
                if Tag.objects.filter(name=t).exists():
                    tag = Tag.objects.get(name=t)
                else:
                    tag = Tag.objects.create(name=t)
                prob.tags.add(tag)
            prob.save()
    return len(problems)


def scan_codeforces(request):
    log_to_file(f'-------------------------------\nРучной запуск загрузки в {datetime.utcnow().time()}\n')
    num = scan()
    log_to_file(f'Загружено {num} задач\n')
    return redirect('index')


def distrib():
    log_to_file(f'-------------------------------\n'
                f'Запуск распределения задач по тэгам в {datetime.utcnow().time()}\n')
    problems = Problem.objects.order_by('difficulty')

    tags = {}
    for p in problems:

        least_count = None
        least_name = None
        for t in p.tags.all():
            if t.name not in tags:
                tags[t.name] = []
            if least_name is None or len(tags[t.name]) < least_count:
                least_name = t.name
                least_count = len(tags[t.name])
        if least_name in tags:
            tags[least_name].append([p.number, p.id])

    for k in tags:
        log_to_file(f'{k} = {str(tags[k])}\n')
        # print(f'{k} = ', tags[k])
        tag = Tag.objects.filter(name=k).get()
        Belonging.objects.filter(tag=tag.id).delete()
        for p in tags[k]:
            b = Belonging.objects.create(tag=tag, problem_id=p[1])
            b.save()
    log_to_file(f'Запуск распределения задач по тэгам завершён в {datetime.utcnow().time()}\n')


def distribute(request):
    distrib()
    return redirect('index')


def load_problems():
    log_to_file(f'-------------------------------\nStarting at {datetime.utcnow().time()}\n')
    num = scan()
    log_to_file(f'Loaded {num} problems\n')
    distrib()
