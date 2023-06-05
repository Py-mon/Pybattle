import json

import requests
from bs4 import BeautifulSoup


def main():
    URL = "https://www.fileformat.info/info/charset/UTF-8/list.htm"

    chars = {}
    max_ = 100000

    def add(url, start=0):
        response = requests.get(url + f"?start={start}")

        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"class": "table table-bordered table-striped"})

        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if cols:
                # x += 1
                # pb.update(x)
                character = cols[0].text.strip()

                if character == "More...":
                    start += 1024

                    if start > max_:
                        break

                    print(f"Working... {start}/{max_}")
                    add(URL, start)
                else:
                    title: str = cols[1].text.strip()

                    if (
                        not title[:-10].isupper()  # not chinese symbols
                        or title[:6]
                        == title[8:-1]  # not chinese symbols (duped U+code)
                    ):
                        continue

                    chars[title] = character

    add(URL)

    with open("chars/chars.json", "w", encoding="utf-8") as f:
        json.dump(chars, f, ensure_ascii=False, indent=4)


main()
