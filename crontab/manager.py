
from datetime import datetime
import os

from django.shortcuts import redirect

from problems.models import Tag, Problem, Belonging
from scraper.scraper import scrape_data, LOG_FILE_NAME, log_to_file


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
    problems = scrape_data()
    if problems:
        for p in problems:
            if Problem.objects.filter(number=p["number"]).exists():
                prob = Problem.objects.get(number=p["number"])
            else:
                prob = Problem.objects.create(
                    number=p["number"],
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
    problems = Problem.objects.order_by('difficulty')

    tags = {}
    for p in problems:
        # print(p.number)

        least_count = None
        least_name = None
        for t in p.tags.all():
            # print(t.name)
            if t.name not in tags:
                tags[t.name] = []
                # print(f'counts["{t.name}"] => 0')
            if least_name is None or len(tags[t.name]) < least_count:
                least_name = t.name
                least_count = len(tags[t.name])
        tags[least_name].append([p.number, p.id])
        # print(f'tags["{least_name}"] =>', tags[least_name])

    for k in tags:
        print(f'{k} = ', tags[k])
        tag = Tag.objects.filter(name=k).get()
        Belonging.objects.filter(tag=tag.id).delete()
        for p in tags[k]:
            b = Belonging.objects.create(tag=tag, problem_id=p[1])
            b.save()


def distribute(request):
    distrib()
    return redirect('index')


def load_problems():
    log_to_file(f'-------------------------------\nStarting at {datetime.utcnow().time()}\n')
    num = scan()
    log_to_file(f'Loaded {num} problems\n')
    distrib()
