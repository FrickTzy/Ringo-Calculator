from tkinter import Button, Frame, StringVar, Tk, Entry, TOP, RIGHT


class InputManager:
    expression: str = ""

    def __init__(self, lyrics: list[str]):
        self.input_text = StringVar()
        self.__lyrics = lyrics
        self.__current_index = 0

    def click(self, item):
        self.expression += str(item)
        self.input_text.set(self.expression)

    def clear(self):
        self.expression = ""
        self.input_text.set("")

    def evaluate(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except SyntaxError:
            self.input_text.set("Error")
            self.expression = ""

    def set_lyrics(self):
        self.input_text.set(f"{self.__lyrics[self.__current_index]}")
        self.expression = ""
        self.__current_index += 1

    def check_if_set_lyrics(self, event):
        if event.keysym == 'a':
            self.set_lyrics()


class CalculatorButton(Button):
    def __init__(self, *args, input_manager: InputManager = None, **kwargs):
        self.__input_manager = input_manager
        if kwargs.get("command") is None:
            kwargs["command"] = lambda: self.__input_manager.click(item=kwargs["text"])
        super().__init__(*args, **kwargs)


class Calculator:
    def __init__(self, window, lyrics):
        self.__window = window
        self.__lyrics = lyrics
        self.__window.title("Ringo Calculator")
        self.__set_position()
        self.__window.resizable(0, 0)
        self.__input_manager = InputManager(lyrics=self.__lyrics)
        self.__window.bind('<KeyPress>', self.__input_manager.check_if_set_lyrics)
        self.__window.bind()
        self.__button_frame = Frame(self.__window, width=800, height=1200, bg="grey")
        self.__create_widgets()

    def __set_position(self):
        screen_width, screen_height = self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()
        window_width, window_height = 500, 700
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.__window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def __create_widgets(self):
        self.__create_input_field()
        self.__create_buttons()
        self.__button_frame.pack()

    def __create_input_field(self):
        input_frame = Frame(self.__window, width=800, height=100, bd=0, highlightbackground="black",
                            highlightcolor="black", highlightthickness=1)
        input_frame.pack(side=TOP)

        input_field = Entry(input_frame, font=('arial', 26, 'bold'), textvariable=self.__input_manager.input_text,
                            width=100, bg="#eee", bd=0, justify=RIGHT)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=30)

    def __create_buttons(self):
        button_list = [["C", "C", "%", "/"],
                       ["7", "8", "9", "*"],
                       ["4", "5", "6", "-"],
                       ["1", "2", "3", "+"],
                       ["0", "0", ".", "="]]
        fg, bg = "black", "#fff"
        height = 6
        bd = 0
        cursor = "hand2"

        for row_index, row in enumerate(button_list):
            last_text = ""
            for column_index, column in enumerate(row):
                current_text = str(column)
                column_span = 1
                width = 17
                command = None
                bg = "#fff" if current_text.isdigit() else "#eee"
                if last_text == current_text:
                    continue
                else:
                    last_text = current_text
                for next_text in row[column_index + 1: len(row)]:
                    if next_text == current_text:
                        column_span += 1
                    else:
                        break
                if current_text == "C":
                    width = 35
                    command = self.__input_manager.clear
                elif current_text == "0":
                    width = 35
                elif current_text == "=":
                    command = self.__input_manager.set_lyrics
                else:
                    width = 17
                self.__create_button(current_text, fg, width, height, bd, bg, cursor, row_index, column_span,
                                     column_index, command)

    def __create_button(self, text, fg, width, height, bd, bg, cursor, row_index, column_span, column_index, command):
        button = CalculatorButton(self.__button_frame, text=text, fg=fg, width=width, height=height, bd=bd, bg=bg,
                                  cursor=cursor, command=command, input_manager=self.__input_manager)
        button.grid(row=row_index, columnspan=column_span, column=column_index, padx=1, pady=1)


def _get_lyrics(song_name: str):
    with open(f'lyrics/{song_name}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return [line.strip() for line in lines]


if __name__ == "__main__":
    root_window = Tk()
    calculator = Calculator(root_window, lyrics=_get_lyrics("mahiwagang_usok"))
    root_window.mainloop()
