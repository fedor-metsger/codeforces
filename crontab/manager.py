
from datetime import datetime
import os

from django.conf import settings
from django.shortcuts import redirect

from problems.models import Tag, Problem, Belonging
from scraper.scraper import scrape_data

LOG_FILE_NAME = "/tmp/scraper.log"


class ScraperManager():
    crontab_status = False


def run():
    with open(LOG_FILE_NAME, "a") as logfile:

        now_time = datetime.utcnow().time()
        logfile.write(f'-------------------------------\nStarting at {now_time}\n')

def switch_crontab(request):
    if ScraperManager.crontab_status:
        os.system("./manage.py crontab remove")
    else:
        os.system("./manage.py crontab add")
    ScraperManager.crontab_status = not ScraperManager.crontab_status
    return redirect('index')

def scan_codeforces(request):
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
    return redirect('index')

def distribute(request):

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
            if least_name == None or len(tags[t.name]) < least_count:
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

    return redirect('index')
