

## Дипломная работа на тему






### Результаты тестов

Команда запуска тестов: `coverage run --source='.' manage.py test`

Результат:
```
(venv) fedor@fedor-Z68P-DS3:~/CODE/SkyPro/codeforces$ coverage run --source='.' manage.py test
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.110s

OK
Destroying test database for alias 'default'...
(venv) fedor@fedor-Z68P-DS3:~/CODE/SkyPro/codeforces$
```

Команда вывода отчёта по покрытию тестами: `coverage report`
```
(venv) fedor@fedor-Z68P-DS3:~/CODE/SkyPro/codeforces$ coverage report
Name                                                                           Stmts   Miss  Cover
--------------------------------------------------------------------------------------------------
config/__init__.py                                                                 0      0   100%
config/asgi.py                                                                     4      4     0%
config/settings.py                                                                23      0   100%
config/urls.py                                                                     5      0   100%
config/wsgi.py                                                                     4      4     0%
crontab/__init__.py                                                                0      0   100%
crontab/manager.py                                                                65     19    71%
crontab/tests.py                                                                  45      0   100%
manage.py                                                                         12      2    83%
problems/__init__.py                                                               0      0   100%
problems/admin.py                                                                  8      0   100%
problems/apps.py                                                                   4      0   100%
problems/migrations/0001_initial.py                                                5      0   100%
problems/migrations/0002_alter_problem_number.py                                   4      0   100%
problems/migrations/0003_alter_tag_name.py                                         4      0   100%
problems/migrations/0004_alter_problem_difficulty_alter_problem_solutions.py       4      0   100%
problems/migrations/0005_belonging.py                                              5      0   100%
problems/migrations/__init__.py                                                    0      0   100%
problems/models.py                                                                27      3    89%
problems/tests.py                                                                  1      0   100%
problems/views.py                                                                 22      5    77%
scraper/__init__.py                                                                0      0   100%
scraper/scraper.py                                                                49     12    76%
scraper/tests.py                                                                  12      0   100%
--------------------------------------------------------------------------------------------------
TOTAL                                                                            303     49    84%
(venv) fedor@fedor-Z68P-DS3:~/CODE/SkyPro/codeforces$
```