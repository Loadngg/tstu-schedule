from typing import List
from utils import find_in_list, remove_substring_from_string, roman_to_int
import re


class Recording:
    def __init__(self, result: str) -> None:
        self.time_interval_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b-\b[0-2]?[0-9].[0-5][0-9]\b)"
        self.time_regex = r"(\b[0-2]?[0-9].[0-5][0-9]\b)"
        self.roman_regex = r"([MDCLXVI]+)"

        self.result = result

        self.data: str = ''
        self.time: str = ''
        self.pair_number: str = ''
        self.group: str = ''
        self.subject: str = ''
        self.auditorium: str = ''

        self.__formatting()

    def __find_field_by_regex(self, regex: str) -> str:
        split_string = re.split(regex, self.temp_str)
        field = find_in_list(regex, split_string)
        self.temp_str = remove_substring_from_string(field, self.temp_str)
        return field

    def __find_field_by_index(self, index: int) -> str:
        field = self.temp_str.split()[index]
        self.temp_str = remove_substring_from_string(field, self.temp_str)
        return field

    def __formatting(self) -> None:
        self.data = self.result[:5]  # дата - всегда первые 5 символов
        self.temp_str: str = remove_substring_from_string(self.data, self.result)

        # время
        if re.search(self.time_interval_regex, self.temp_str):
            self.time = self.__find_field_by_regex(self.time_interval_regex)
            self.time = self.time.split("-")[0]
        elif re.search(self.time_interval_regex, self.temp_str) is None and re.search(self.time_regex, self.temp_str):
            self.time = self.__find_field_by_regex(self.time_regex)

        self.time = self.time.replace(".", ":")

        # номер пары
        if re.search("пара", self.temp_str):
            self.pair_number = self.__find_field_by_regex(self.roman_regex)
            self.temp_str = remove_substring_from_string("пара", self.temp_str)
            self.pair_number = roman_to_int(self.pair_number)

        # аудитория, группа и дисциплина всегда остаются в середине, поэтому универсально
        self.auditorium = self.__find_field_by_index(-1)
        self.group = self.__find_field_by_index(0)
        self.subject = self.temp_str

    def get_record(self, flags: str = "/d/t/p/g/s/a") -> List[str]:
        flags_dict = {
            "d": self.data,
            "t": self.time,
            "p": f"({self.pair_number} пара)",
            "g": self.group,
            "s": self.subject,
            "a": self.auditorium
        }
        result: List[str] = []

        for flag in ''.join(flags.split()).split("/")[1:]:
            try:
                result.append(flags_dict[flag])
            except KeyError:
                raise ValueError(f"fВведён неверный флаг /{flag}")

        return result
