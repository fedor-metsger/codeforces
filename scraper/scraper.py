
import os
from datetime import datetime
import time
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup, Tag

from config.settings import BASE_DIR

PROBLEMSET_URL = "https://codeforces.com/problemset"
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME")


load_dotenv(BASE_DIR / '.env')

def log_to_file(msg):
    with open(LOG_FILE_NAME, "a") as logfile:
        logfile.write(msg)


def scrape_data() -> list:
    log_to_file(f'-------------------------------\nScraper started at {datetime.utcnow().time()}\n')
    res = []
    raw = None
    try:
        result = requests.get(PROBLEMSET_URL)
        if result.status_code != 200:
            print("Ошибка при запросе данных с сайта Codeforces: Status code ", result.status_code)
            log_to_file("Ошибка при запросе данных с сайта Codeforces: Status code " +
                        str(result.status_code) + '\n')
            return res

        soup = BeautifulSoup(result.content, 'html.parser')
        total_pages = None
        # try:
        total_pages = int(soup.find(
            'div', {"class": "pagination"}
        ).find_all("span", reqursive=False)[-1].find("a").text)

        # # except:
        # #     pass
        log_to_file(f"Всего найдено {total_pages} страниц\n")
        print(f"Всего найдено {total_pages} страниц")
        # for p in range(total_pages):
        for p in range(40):
            time.sleep(1)
            print(f"Загружается страница {p + 1}")
            params = {"page": p + 1}
            result = requests.get(f'{PROBLEMSET_URL}/page/{p + 1}')
            soup = BeautifulSoup(result.content, 'html.parser')
            table = soup.find_all("table", {"class":"problems"})
            for r in table[0].contents:
                raw = r
                if isinstance(r, Tag):
                    name = r.contents[3].text.split('\n\n\n')[0].strip()
                    if name != "Name":
                        number = r.contents[1].text.strip()
                        tags = [t.strip() for t in r.contents[3].text.split("\n\n\n")[1].split(',')]
                        solutions = 0
                        if r.contents[9].text.strip():
                            if r.contents[9].text.strip()[0] == 'x':
                                solutions = int(r.contents[9].text.strip()[1:])
                            else:
                                print(f'Странное содержимое поля "Количество решивших задачу":',
                                      {r.contents[9].text.strip()})
                        difficulty = int(r.contents[7].text.strip()) if r.contents[7].text.strip() else 0
                        # print(number, name, tags, solutions, difficulty)
                        res.append({
                            "name": name,
                            "number": number,
                            "tags": tags,
                            "solutions": solutions,
                            "difficulty": difficulty
                        })
        log_to_file(f'Loaded {len(res)} problems\n')
        print(f'Loaded {len(res)} problems')
        return res
    except Exception as e:
        log_to_file("Ошибка при запросе данных с сайта Codeforces:" + repr(e) + '\n')
        log_to_file("Обрабатываемая строка:" + str(raw) + '\n')
        print("Ошибка при запросе данных с сайта Codeforces:", repr(e))
        print("Обрабатываемая строка:", raw)
        return res

def main():
    res = scrape_data()

if __name__ == "__main__":
    main()