
import requests
import time
import re
from bs4 import BeautifulSoup, Tag


PROBLEMSET_URL = "https://codeforces.com/problemset"


def scrape_data() -> list:
    res = []
    raw = None
    try:
        result = requests.get(PROBLEMSET_URL)
        if result.status_code != 200:
            print("Ошибка при запросе данных с сайта Codeforces: Status code ", result.status_code)
            return None

        soup = BeautifulSoup(result.content, 'html.parser')
        total_pages = None
        # try:
        total_pages = int(soup.find(
            'div', {"class": "pagination"}
        ).find_all("span", reqursive=False)[-1].find("a").text)

        # # except:
        # #     pass
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
        print(f'Loaded {len(res)} problems')
        return res
    except Exception as e:
        print("Ошибка при запросе данных с сайта Codeforces:", repr(e))
        print("Обрабатываемая строка:", raw)
        return res

def main():
    res = scrape_data()

if __name__ == "__main__":
    main()