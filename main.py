from tkinter import Button, Frame, StringVar, Tk, Entry, TOP, RIGHT
from threading import Thread
from time import sleep, time

lyrics_lines = [("Suki yo", 0.0, 0.09, False, True),
("Ima anata ni ", 0.9923076629638672, 0.11, False, True),
("omoi ", 2.880147933959961, 0.09, False, False),
("nosete", 3.676890277862549, 0.09, False, False),
("Hora, ", 4.8688966274261475, 0.10, False, True),
("sunao ni ", 5.856818914413452, 0.11, False, False),
("naru ", 7.249434947967529, 0.11, False, False),
("no watashi", 8.10, 0.09, False, False),
("Kono saki ", 9.569412469863892, 0.09, False, True),
("motto", 10.70, 0.12, False, False),
("soba ni ite mo ", 11.937920570373535, 0.11, False, True),
("ii ka na?", 13.74186954498291, 0.11, False, False),
("Koi to ", 15.161859035491943, 0.10, False, True),
("koi ga ", 16.05, 0.10, False, False),
("kasa", 16.87440962927246, 0.09, False, False),
("natte", 17.553884983062744, 0.12, False, False),
("Suki yo", 18.682809306549072, 0.09, False, True)]


class InputManager:
    expression: str = ""

    def __init__(self, lyrics: list[str], window):
        self.input_text = StringVar()
        self.__lyrics = lyrics
        self.__current_index = 0
        self.__window = window
        self.__printed_lyric = ""

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

    def set_lyrics_automatically(self):
        start_time = time()
        for current_line in self.__lyrics:
            lyric, starting_time, character_delay, is_colored, next_line = current_line
            while time() - start_time < starting_time:
                sleep(0.01)
            self.__set_current_lyric(current_line=lyric, character_delay=character_delay, next_line=next_line)

    def __set_current_lyric(self, current_line: str, character_delay: float, next_line: bool):
        if next_line:
            self.__printed_lyric = ""
        for current_character in current_line:
            self.__printed_lyric += current_character
            self.input_text.set(self.__printed_lyric)
            self.__window.update()
            sleep(character_delay)

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
    __FONT_SIZE = 20
    __WIDTH, __HEIGHT = 500, 700
    __BG_COLOR = "grey"
    __TITLE = "Calculator  |  @kurikosancode"

    def __init__(self, window, lyrics):
        self.__window = window
        self.__lyrics = lyrics
        self.__window.title(self.__TITLE)
        self.__set_position()
        self.__window.resizable(0, 0)
        self.__input_manager = InputManager(lyrics=self.__lyrics, window=self.__window)
        self.__window.bind('<KeyPress>', self.__input_manager.check_if_set_lyrics)
        self.__button_frame = Frame(self.__window, width=self.__WIDTH, height=self.__HEIGHT, bg=self.__BG_COLOR)
        self.__create_widgets()

    def __set_position(self):
        screen_width, screen_height = self.__window.winfo_screenwidth(), self.__window.winfo_screenheight()
        position_x = (screen_width // 2) - (self.__WIDTH // 2)
        position_y = (screen_height // 2) - (self.__HEIGHT // 2)
        self.__window.geometry(f"{self.__WIDTH}x{self.__HEIGHT}+{position_x}+{position_y}")

    def __create_widgets(self):
        self.__create_input_field()
        self.__create_buttons()
        self.__button_frame.pack()

    def __create_input_field(self):
        input_frame = Frame(self.__window, width=800, height=100, bd=0, highlightbackground="black",
                            highlightcolor="black", highlightthickness=1)
        input_frame.pack(side=TOP)

        input_field = Entry(input_frame, font=('arial', self.__FONT_SIZE, 'bold'), textvariable=self.__input_manager.input_text,
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
                    command = Thread(target=self.__input_manager.set_lyrics_automatically, daemon=True).start
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
    calculator = Calculator(root_window, lyrics=lyrics_lines)
    root_window.mainloop()
