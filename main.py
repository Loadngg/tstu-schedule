import re
import sys

from typing import List

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from core.generator import Generator
from core.parser import Parser
from core.recording import Recording
from core.utils import find_in_list, show_message
from design.design import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    general_file_flag: bool = False
    group_flag: bool = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.qss_file = open("res/dark.qss").read()
        self.setStyleSheet(self.qss_file)

        self.init_ui()

        self.parser = Parser(self.infoLabel)

    def init_ui(self):
        self.generalFileCheckbox.clicked.connect(self.set_general_file_flag)
        self.groupCheckbox.clicked.connect(self.set_group_flag)
        self.loadButton.clicked.connect(self.load_button_event)
        self.searchButton.clicked.connect(self.search_button_event)
        self.clearFilesButton.clicked.connect(self.clear_files_button_event)

    def clear_files_button_event(self) -> None:
        self.parser.clear_books()
        self.infoLabel.setText("Файлы успешно удалены")
        self.searchButton.setEnabled(False)
        self.clearFilesButton.setEnabled(False)

    def set_general_file_flag(self) -> None:
        self.general_file_flag = not self.general_file_flag

    def set_group_flag(self) -> None:
        self.group_flag = not self.group_flag

    def load_button_event(self) -> None:
        try:
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
            dialog.setNameFilter("Excel (*.xls *.xlsx)")
            dialog.setViewMode(QFileDialog.Detail)

            if dialog.exec_():
                self.parser.load_files(dialog.selectedFiles())

                self.searchButton.setEnabled(True)
                self.clearFilesButton.setEnabled(True)
        except Exception:
            show_message(self, "Непредвиденная ошибка при загрузке файлов", "Ошибка", QMessageBox.Warning)

    def search_button_event(self) -> None:
        split_filters = re.split(r"([a-zA-Zа-яА-ЯёЁ]+)", self.searchFilter.text())
        search_filters = find_in_list(r"([a-zA-Zа-яА-ЯёЁ]+)", split_filters)

        formatted_results: List[List[Recording]] = []
        not_founded_filters: List[str] = []

        if search_filters.__len__() == 0:
            show_message(self, "Вы не ввели фильтр для поиска", "Ошибка", QMessageBox.Warning)
            return

        for search_filter in search_filters:
            temp_results: List[Recording] = []
            parser_results = self.parser.search(search_filter)
            if parser_results.__len__() == 0:
                not_founded_filters.append(search_filter)
            else:
                for item in self.parser.search(search_filter):
                    temp_results.append(Recording(item))

                formatted_results.append(temp_results)

        search_filters = [x for x in search_filters if x not in not_founded_filters]
        generator = Generator(self.infoLabel)
        generator.generate(formatted_results, search_filters, self.general_file_flag, self.group_flag)

        if not_founded_filters.__len__() != 0:
            self.infoLabel.setText(f"Не найдено записей для преподавателей: {', '.join(not_founded_filters)}\n"
                                   f"{self.infoLabel.text()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
