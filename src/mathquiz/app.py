import toga
import threading
import time
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from random import randint, choice, sample
from math import isclose


class Quiz(toga.App):
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.top_box = toga.Box(style=Pack(direction=ROW))
        self.bottom_box = toga.Box(style=Pack(direction=ROW))
        self.bottom_box_left = toga.Box(style=Pack(flex=1, direction=COLUMN))
        self.bottom_box_right = toga.Box(style=Pack(flex=1, direction=COLUMN))

        self.myscore = toga.TextInput(readonly=True, style=Pack(flex=4), value="0")
        self.mytime = toga.TextInput(readonly=True, style=Pack(flex=1), value="0")

        self.timer_label = toga.Label("Timer:", style=Pack(color="brown"))
        self.score_label = toga.Label("Score:", style=Pack(color="brown"))

        self.questions = toga.MultilineTextInput(readonly=True,style=Pack(flex=1, font_size=15, alignment='center'))

        self.optionA = toga.Button(text="??", style=Pack(flex=1, background_color='white', color='grey'))
        self.optionB = toga.Button(text="??", style=Pack(flex=1, background_color='white', color='grey'))
        self.optionC = toga.Button(text="??", style=Pack(flex=1, background_color='white', color='grey'))
        self.optionD = toga.Button(text="??", style=Pack(flex=1, background_color='white', color='grey'))

        self.bottom_box_left.add(toga.Label("(A)", style=Pack(color="green")))
        self.bottom_box_left.add(self.optionA)
        self.bottom_box_left.add(toga.Label("(B)", style=Pack(color="green")))
        self.bottom_box_left.add(self.optionB)
        self.bottom_box_right.add(toga.Label("(C)", style=Pack(color="green")))
        self.bottom_box_right.add(self.optionC)
        self.bottom_box_right.add(toga.Label("(D)", style=Pack(color="green")))
        self.bottom_box_right.add(self.optionD)

        self.top_box.add(self.timer_label)
        self.top_box.add(self.mytime)
        self.top_box.add(self.score_label)
        self.top_box.add(self.myscore)

        self.bottom_box.add(self.bottom_box_left)
        self.bottom_box.add(self.bottom_box_right)

        self.main_box.add(self.top_box)
        self.main_box.add(self.questions)   
        self.main_box.add(self.bottom_box)

        self.main_window = toga.MainWindow(title=self.formal_name, size=(600, 600))
        self.main_window.content = self.main_box
        self.main_window.show()

        self.optionA.on_press = self.answer
        self.optionB.on_press = self.answer
        self.optionC.on_press = self.answer
        self.optionD.on_press = self.answer

        self.start_game()

    def start_game(self):
        self.lives = 3
        self.content()
        self.questions.value = f"\n\n\n\n\n\n\t\tWhat is the output of this expression ?\n\n\n\t\t\t\t{str(self.operator1) + str(self.operand) + str(self.operator2)}"
        self.optionA.text = str(self.options[0])
        self.optionB.text = str(self.options[1])
        self.optionC.text = str(self.options[2])
        self.optionD.text = str(self.options[3])
        #self.timer_thread = threading.Thread(target=self.timer_countdown, daemon=True)
    
    def timer_countdown(self):
        time_left = 60
        while time_left >= 0:
            print(f"Time remaining: {time_left} seconds {self.mytime.value}")
            time.sleep(1)
            time_left -= 1

    def content(self):
        self.operator1 = randint(1, 100)
        self.operand = choice(["+", "-", "*", "/"])
        self.operator2 = randint(1, 100)
        self.options = sample(self.get_answer_options(), 4)
        self.correctanswer = self.calculate_answer()

    def calculate_answer(self):
        result = eval(f"{self.operator1} {self.operand} {self.operator2}")
        return round(result, 2) if isclose(result, round(result, 2)) else result

    def get_answer_options(self):
        if self.operand == "/":
            return [
                eval(f"{self.operator1} {self.operand} {self.operator2}"),
                eval(f"{self.operator1} {self.operand} {self.operator2 + 1}"),
                eval(f"{self.operator1} {self.operand} {self.operator2 - 1}"),
                eval(f"{self.operator1} {self.operand} {self.operator2 + 2}"),
            ]
        else:
            return [
                eval(f"{self.operator1} {self.operand} {self.operator2}"),
                eval(f"{self.operator1} {self.operand} {self.operator2 + 1}"),
                eval(f"{self.operator1} {self.operand} {self.operator2 - 1}"),
                eval(f"{self.operator1} {self.operand} {self.operator2 + 2}"),
            ]

    def answer(self, widget):
        widget.style.color = "blue"
        widget.style.background_color = "blue"
        
        #self.timer_thread.start()

        if str(widget.text) == str(self.correctanswer):
            self.main_window.info_dialog("Correct Answer", "Get Ready for the Next")
            self.myscore.value = str(int(self.myscore.value) + 10)
            widget.style.color = "grey"
            widget.style.background_color = "white"
            self.start_game()
        else:
            self.lives -= 1
            widget.style.color = "grey"
            widget.style.background_color = "white"
            if self.lives > 0:
                self.main_window.info_dialog("Wrong Answer", "Try Again!!!\nYou have {} chance(s)".format(self.lives))
                if self.myscore.value and int(self.myscore.value) > 0:
                    self.myscore.value = str(int(self.myscore.value) - 5)
                else:
                    self.myscore.value = "0"
            else:
                self.main_window.info_dialog("GAME OVER!", "You ran out of lives, GAME OVER!!!")
                self.exit()


def main():
    app = Quiz()
    app.main_loop()


if __name__ == '__main__':
    main() 