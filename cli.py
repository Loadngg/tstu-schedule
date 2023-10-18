from typing import List

import click
import re
import os

from core.generator import Generator
from core.parser import Parser
from core.recording import Recording
from core.utils import find_in_list


@click.command()
@click.argument("directory")
@click.argument("filters", nargs=-1)
@click.option("--single-file", "-s", is_flag=True,
              help="Единый файл, вместо создания файла под каждый фильтр.")
@click.option("--grouping", "-g", is_flag=True, help="Объединение групп.")
@click.option("--out-path", "-o", type=click.Path(), default="./",
              help="Путь до папки с результатами.")
def main(filters, directory, **kwargs):
    """
    Парсинг ТГТУ расписаний

    Примеры использования:\n
    python3 cli.py ./excel Фамилия1 Фамилия2\n
    python3 cli.py -s -g -o ./results ./excel Фамилия1 Фамилия2
    """

    parser = Parser()

    split_filters = re.split(r"([a-zA-Zа-яА-ЯёЁ]+)", ' '.join(filters))
    search_filters = find_in_list(r"([a-zA-Zа-яА-ЯёЁ]+)", split_filters)

    formatted_results: List[List[Recording]] = []
    not_founded_filters: List[str] = []
    excel_files: List[str] = []

    if search_filters.__len__() == 0:
        print("Вы не ввели фильтр для поиска")
        return

    directory = directory if directory[-1] == "/" else directory + "/"
    if not os.path.isdir(directory):
        print("Данная папка не существует")
        return

    for item in os.listdir(directory):
        if item.endswith('.xls') or item.endswith(".xlsx"):
            excel_files.append(os.path.abspath(directory + item))

    if excel_files.__len__() == 0:
        print("В данной папке нет файлов с расширением .xls или .xlsx")
        return

    parser.load_files(excel_files)

    output_directory = kwargs["out_path"] if kwargs["out_path"][-1] == "/" else kwargs["out_path"] + "/"
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    for search_filter in search_filters:
        temp_results: List[Recording] = []
        parser_results = parser.search(search_filter)
        if parser_results.__len__() == 0:
            not_founded_filters.append(search_filter)
        else:
            for item in parser.search(search_filter):
                temp_results.append(Recording(item))

            formatted_results.append(temp_results)

    if not_founded_filters.__len__() != 0:
        print(f"Не найдено записей для преподавателей: {', '.join(not_founded_filters)}")

    search_filters = [x for x in search_filters if x not in not_founded_filters]

    generator = Generator()
    generator.generate(formatted_results, search_filters, general_file=kwargs["single_file"], group=kwargs["grouping"],
                       output_directory=output_directory)


if __name__ == "__main__":
    main()
