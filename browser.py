from bs4 import BeautifulSoup
import click
import requests
import re
import os
import time

# Очищение консоли. Вывод названия и строки с запросом URL.
os.system('cls||clear')
print("{:=^120}".format(""))
print("{: ^120}".format(" The Simplest Terminal Browser (c) 2020 "))
print("{:=^120}".format(""))

@click.command()
@click.option("--url", prompt="URL", help="Get URL and load the site.")

def site(url):
    # Разделение ввода от вывода знаками '=', имитация загрузки.
    print("{:=^120}".format(""))
    if url[:4:] != "http":
        url = "http://" + url
    click.echo(f"Loading...")
    time.sleep(1)
    print("{:=^120}".format(""))

    # Получение исходника сайта с помощью библиотеки Requests 
    page = requests.get(url)

    # Приведения кода в читаемый вид с помощью библиотеки BeautifulSoup
    soup = BeautifulSoup(page.text, "lxml")

    # Обработка полученного кода:
    # -- тег жирного <b>
    tag_b = soup.find_all("b")
    if tag_b != [] and tag_b[0].contents != []:
        for i in range(len(tag_b)):
            tag_b[i].contents[0].replace_with(f'\033[1m{tag_b[i].contents[0]}\033[0m')

    # -- тег жирного <strong>
    tag_strong = soup.find_all("strong")
    if tag_strong != [] and tag_strong[0].contents != []:
        for i in range(len(tag_strong)):
            tag_strong[i].contents[0].replace_with(f'\033[1m{tag_strong[i].contents[0]}\033[0m')
    
    # -- тег курсива <i>
    tag_i = soup.find_all("i")
    if tag_i != [] and tag_i[0].contents != []:
        for i in range(len(tag_i)):
            tag_i[i].contents[0].replace_with(f'\033[7m{tag_i[i].contents[0]}\033[0m')

    # -- тег курсива <em>
    tag_em = soup.find_all("em")
    if tag_em != [] and tag_em[0].contents != []:
        for i in range(len(tag_em)):
            tag_em[i].contents[0].replace_with(f'\033[7m{tag_em[i].contents[0]}\033[0m')

    # -- тег нумерованного списка <ol>
    list_ol = soup.find_all("ol")
    for i in range(len(list_ol)):
        for j in range(1, len(list_ol[i].contents)):
            if list_ol[i].contents[j] != "\n":
                var_for_list_content = list_ol[i].contents[j].get_text()
                list_ol[i].contents[j].replace_with(f'{j}.' + var_for_list_content)
                #list_ol[i].contents[0].replace_with('   ' + list_ol[i].contents[0])
                #print(list_ol[i].contents[j])
        list_ol[i].replace_with(list_ol[i].prettify(formatter="html"))

    # -- тег обычного списка <ul>
    list_ul = soup.find_all("ul")
    for i in range(len(list_ul)):
        for j in range(1, len(list_ul[i].contents)):
            if list_ul[i].contents[j] != "\n":
                var_for_list_content = list_ul[i].contents[j].get_text()
                list_ul[i].contents[j].replace_with('-- ' + var_for_list_content)
        list_ul[i].replace_with(list_ul[i].prettify(formatter="html"))

    # Извлечение текста из результата
    soup = soup.get_text()
    soup = re.sub(r'\<[^>]*\>', '', soup)
    soup = re.sub(r'&lt;/ol&gt;', '', soup)
    soup = re.sub(r'    &lt;ol&gt;', '', soup)

    # Вывод
    print(soup)

if __name__ == '__main__':
    site()
    input()