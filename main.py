import customtkinter
import tkinter.filedialog as fd
from parser import *
import generator

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class Application(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.parser = Parser()

        self.title("Парсинг заочников")
        self.geometry(f"{500}x{250}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.search_frame = customtkinter.CTkFrame(self, width=140, height=50, corner_radius=0)
        self.search_frame.grid(row=0, column=0, sticky="nsew")
        self.search_frame.grid_columnconfigure(1, weight=1)

        self.search_label = customtkinter.CTkLabel(self.search_frame, text="Поиск по:", anchor="e")
        self.search_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.search_filter = customtkinter.CTkTextbox(self.search_frame, width=20, height=20, wrap="word")
        self.search_filter.grid(row=0, column=1, padx=(20, 10), pady=20, sticky="ew")

        self.buttons_frame = customtkinter.CTkFrame(self, width=140, height=100, corner_radius=0)
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.load_button = customtkinter.CTkButton(self.buttons_frame, text="Загрузить", command=self.load_button_event)
        self.load_button.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.search_button = customtkinter.CTkButton(self.buttons_frame, text="Поиск", command=self.parse_button_event,
                                                     state="disabled")
        self.search_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    def load_button_event(self) -> None:
        files = fd.askopenfilenames()
        if files.__len__() == 0:
            return

        self.parser.load_files(files)

        self.search_button.configure(state="normal")

    def parse_button_event(self) -> None:
        search_filter = self.search_filter.get("0.0", "end").split("\n")[0]

        result = self.parser.search(search_filter)
        generator.generate(result, search_filter)


if __name__ == '__main__':
    application = Application()
    application.mainloop()
