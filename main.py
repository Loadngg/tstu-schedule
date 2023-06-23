import customtkinter
from CTkMessagebox import CTkMessagebox
import tkinter.filedialog as fd
from generator import *
from parser import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class Application(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.parser = Parser()
        self.general_file_flag: bool = False

        self.title("Парсинг расписания")
        self.geometry(f"{500}x{250}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.search_frame = customtkinter.CTkFrame(self, width=140, height=70, corner_radius=0)
        self.search_frame.grid(row=0, column=0, sticky="nsew")
        self.search_frame.grid_columnconfigure(1, weight=1)

        self.search_label = customtkinter.CTkLabel(self.search_frame, text="Поиск по:", anchor="e")
        self.search_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.search_filter = customtkinter.CTkTextbox(self.search_frame, width=20, height=40, wrap="none")
        self.search_filter.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ew")
        self.search_filter.bind('<Return>', lambda event: 'break')
        self.search_filter.configure(font=('', 16))

        self.general_file_checkbox = customtkinter.CTkCheckBox(self, text="Вывод в общий файл",
                                                               command=self.set_general_file_flag)
        self.general_file_checkbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.load_button = customtkinter.CTkButton(self, text="Загрузить", command=self.load_button_event)
        self.load_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.search_button = customtkinter.CTkButton(self, text="Поиск", command=self.parse_button_event,
                                                     state="disabled")
        self.search_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

    def set_general_file_flag(self) -> None:
        self.general_file_flag = not self.general_file_flag

    def load_button_event(self) -> None:
        files = fd.askopenfilenames()
        if files.__len__() == 0:
            return

        self.parser.load_files(files)

        self.search_button.configure(state="normal")

    def parse_button_event(self) -> None:
        search_filters = self.search_filter.get("0.0", "end").split("\n")[0].split(", ")
        general_result = []

        if search_filters[0].__len__() == 0:
            CTkMessagebox(title="Ошибка", message="Вы не ввели фильтр для поиска", icon="cancel")
            return

        for search_filter in search_filters:
            general_result.append(self.parser.search(search_filter))

        generator = Generator()
        generator.generate(general_result, search_filters, self.general_file_flag)


if __name__ == '__main__':
    application = Application()
    application.mainloop()
