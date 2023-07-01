import customtkinter
import tkinter.filedialog as fd
from CTkMessagebox import CTkMessagebox
from generator import *
from parser import *
from recording import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class Application(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Парсинг расписания")
        self.geometry(f"{500}x{400}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.search_frame = customtkinter.CTkFrame(self, width=140, height=150, corner_radius=0)
        self.search_frame.grid(row=0, column=0, sticky="nsew")
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_rowconfigure(1, weight=1)

        self.search_label = customtkinter.CTkLabel(self.search_frame, text="Поиск по:", anchor="e")
        self.search_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.search_label.configure(font=('', 14))

        self.search_filter = customtkinter.CTkTextbox(self.search_frame, width=20, height=40, wrap="none")
        self.search_filter.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ew")
        self.search_filter.bind('<Return>', lambda event: 'break')
        self.search_filter.configure(font=('', 16))

        self.info_label = customtkinter.CTkLabel(self.search_frame, text="Готовность", anchor="w")
        self.info_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nw")
        self.info_label.configure(font=('', 12), justify="left", compound="left")

        self.general_file_checkbox = customtkinter.CTkCheckBox(self, text="Вывод в общий файл",
                                                               command=self.set_general_file_flag)
        self.general_file_checkbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.group_checkbox = customtkinter.CTkCheckBox(self, text="Объединять группы", command=self.set_group_flag)
        self.group_checkbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.load_button = customtkinter.CTkButton(self, text="Загрузить", command=self.load_button_event)
        self.load_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.search_button = customtkinter.CTkButton(self, text="Поиск", command=self.parse_button_event,
                                                     state="disabled")
        self.search_button.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.clear_files_button = customtkinter.CTkButton(self, text="Очистить файлы",
                                                          command=self.clear_files_button_event, state="disabled")
        self.clear_files_button.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

        self.parser = Parser(self.info_label)
        self.general_file_flag: bool = False
        self.group_flag: bool = False

    def clear_files_button_event(self) -> None:
        self.parser.clear_books()
        self.info_label.configure(text="Файлы успешно удалены")
        self.search_button.configure(state="disabled")
        self.clear_files_button.configure(state="disabled")

    def set_general_file_flag(self) -> None:
        self.general_file_flag = not self.general_file_flag

    def set_group_flag(self) -> None:
        self.group_flag = not self.group_flag

    def load_button_event(self) -> None:
        files = fd.askopenfilenames()
        if files.__len__() == 0:
            return

        self.parser.load_files(files)

        self.search_button.configure(state="normal")
        self.clear_files_button.configure(state="normal")

    def parse_button_event(self) -> None:
        search_filters = self.search_filter.get("0.0", "end").split("\n")[0].split(", ")
        formatted_results: List[List[Recording]] = []
        not_founded_filters: List[str] = []

        if search_filters[0].__len__() == 0:
            CTkMessagebox(title="Ошибка", message="Вы не ввели фильтр для поиска", icon="cancel")
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
        generator = Generator(self.info_label)
        generator.generate(formatted_results, search_filters, self.general_file_flag, self.group_flag)

        if not_founded_filters.__len__() != 0:
            self.info_label.configure(text=f"Не найдено записей для преподавателей: {', '.join(not_founded_filters)}\n"
                                           f"{self.info_label.cget('text')}")


if __name__ == '__main__':
    application = Application()
    application.mainloop()
