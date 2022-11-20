import sys
import random
import sqlite3
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/main.ui', self)
        self.setWindowTitle('Камень-ножницы-бумага и неполезные программки')

        self.button_start.setStyleSheet("background-color : green")
        self.button_break.setStyleSheet("background-color : red")

        self.button_break.clicked.connect(self.exit)
        self.button_start.clicked.connect(self.open_games_and_tools)

    def exit(self):
        app.quit()

    def open_games_and_tools(self):
        uic.loadUi('windows/games_and_tools.ui', self)
        self.setWindowTitle('Выберите активность')

        self.label_picture_morse.setStyleSheet("border-image : url(pics/SOS.png)")
        self.label_picture_ceasar.setStyleSheet("border-image : url(pics/ceasar.png)")
        self.label_picture_rps.setStyleSheet("border-image : url(pics/Rock-paper-scissors.png)")

        self.button_open_morse.clicked.connect(self.open_window_morse)
        self.button_open_ceasar.clicked.connect(self.open_window_ceasar)
        self.button_open_rps.clicked.connect(self.open_window_rps)

    def open_window_morse(self):
        self.window_morse = Morse()
        self.window_morse.show()

    def open_window_ceasar(self):
        self.window_ceasar = Ceasar()
        self.window_ceasar.show()

    def open_window_rps(self):
        self.window_rps = RockPaperScissors()
        self.window_rps.show()


class Morse(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/morse.ui', self)
        self.setWindowTitle('Азбука Морзе')

        self.button_convert.clicked.connect(self.convert_text)

    def convert_text(self):
        input_text = self.edit_input.toPlainText()
        converted_text = ''

        connection = sqlite3.connect("project.db")
        cur = connection.cursor()

        if self.radio_lang_rus.isChecked():
            morse = {
                key: value for key, value in
                cur.execute("SELECT * FROM rus_morse").fetchall()
            }
        else:
            morse = {
                key: value for key, value in
                cur.execute("SELECT * FROM eng_morse").fetchall()
            }
        symbol_morse = {
            key: value for key, value in
            cur.execute("SELECT * FROM morse").fetchall()
        }
        connection.close()

        if self.radio_to_morse.isChecked():
            try:
                for letter in input_text:
                    if letter.lower() in morse:
                        converted_text += (morse[letter.lower()] + ' ')
                    else:
                        converted_text += (symbol_morse[letter.lower()] + ' ')
                converted_text += symbol_morse['end']
            except Exception:
                converted_text = 'ОШИБКА'
            
        else:
            try:
                words = input_text.split('   ')
                for word in words:
                    letters = word.split(' ')
                    for letter in letters:
                        if letter in morse:
                            converted_text += morse[letter]
                        else:
                            converted_text += symbol_morse[letter]
                    converted_text += ' '
            except Exception:
                converted_text = 'ОШИБКА'

        self.text_converted.setPlainText(converted_text)


class Ceasar(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/ceasar.ui', self)
        self.setWindowTitle('Шифр Цезаря')

        self.shift = 0
        self.last_mode = ""

        self.slider_shift.valueChanged.connect(self.shift_change)
        self.button_convert.clicked.connect(self.code_text)
        self.button_save_to_file.clicked.connect(self.save_to_file)

    def shift_change(self):
        self.label_shift_value.setText(str(self.slider_shift.value()))

    def code_text(self):
        self.shift = self.slider_shift.value()
        input_text = self.edit_input.toPlainText()
        converted_text = ''

        rus_letter_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        rus_letter_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        eng_letter_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_letter_lower = 'abcdefghijklmnopqrstuvwxyz'
        symbols_letter = ',.-?!:;\'[]\{\}_+=\\/()*% $#'

        for letter in input_text:
            if letter in rus_letter_upper:
                dictionary = rus_letter_upper
            elif letter in rus_letter_lower:
                dictionary = rus_letter_lower
            elif letter in eng_letter_upper:
                dictionary = eng_letter_upper
            elif letter in eng_letter_lower:
                dictionary = eng_letter_lower
            elif letter in symbols_letter:
                dictionary = symbols_letter

            if self.radio_encode.isChecked():
                self.last_mode = "encode"
                index = (dictionary.index(letter) + self.shift) % len(dictionary)
            else:
                self.last_mode = "decode"
                index = (dictionary.index(letter) - self.shift) % len(dictionary)
            converted_text += dictionary[index]

        self.text_converted.setPlainText(converted_text)

    def save_to_file(self):
        coded_text = self.text_converted.toPlainText()
        message = 'ошибка'
        if coded_text != '' and self.last_mode == "encode":
            connection = sqlite3.connect("project.db")
            cur = connection.cursor()
            count, = cur.execute(
                "SELECT count FROM statistics WHERE program = 'ceasar_to_file'"
            ).fetchone()

            count += 1

            message = f'message-{count} code {self.shift}.txt'
            with open(message, 'w', encoding="utf-8") as code_file:
                code_file.write(coded_text)

            cur.execute(
                f"UPDATE statistics SET count = {count} WHERE program = 'ceasar_to_file'"
            )
            connection.commit()
            connection.close()
        QMessageBox.about(self, "Сохранение в файл", message)


class RockPaperScissors(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/rock_paper_scissors.ui', self)
        self.setWindowTitle('Камень-ножницы-бумага')

        self.label_rock.setStyleSheet("border-image : url(pics/rock.png)")
        self.label_scissors.setStyleSheet("border-image : url(pics/scissors.png)")
        self.label_paper.setStyleSheet("border-image : url(pics/paper.png)")
        self.label_computer_picture.setStyleSheet("border: 1px solid black")

        self.button_rock.clicked.connect(self.choose_rock)
        self.button_scissors.clicked.connect(self.choose_scissors)
        self.button_paper.clicked.connect(self.choose_paper)

        self.button_statistics.clicked.connect(self.open_window_statistics)

    def choose_rock(self):
        self.button_rock.setStyleSheet("background-color : gray")
        self.button_scissors.setStyleSheet("background-color : none")
        self.button_paper.setStyleSheet("background-color : none")
        self.play('Камень')

    def choose_scissors(self):
        self.button_scissors.setStyleSheet("background-color : gray")
        self.button_rock.setStyleSheet("background-color : none")
        self.button_paper.setStyleSheet("background-color : none")
        self.play('Ножницы')

    def choose_paper(self):
        self.button_paper.setStyleSheet("background-color : gray")
        self.button_rock.setStyleSheet("background-color : none")
        self.button_scissors.setStyleSheet("background-color : none")
        self.play('Бумага')

    def play(self, player_choice):
        computer = random.randint(1, 3)
        if computer == 1:
            self.label_computer_picture.setStyleSheet("border-image : url(pics/rock.png)")
            self.label_computer_choice.setText('Компьютер: Камень')
            computer_choice = 'Камень'
        elif computer == 2:
            self.label_computer_picture.setStyleSheet("border-image : url(pics/scissors.png)")
            self.label_computer_choice.setText('Компьютер: Ножницы')
            computer_choice = 'Ножницы'
        elif computer == 3:
            self.label_computer_picture.setStyleSheet("border-image : url(pics/paper.png)")
            self.label_computer_choice.setText('Компьютер: Бумага')
            computer_choice = 'Бумага'

        if player_choice == computer_choice:
            self.label_result.setText('Результат: Ничья')
            self.label_result.setStyleSheet("background-color : yellow")
            self.save_statistics(player_choice, computer_choice, 'Ничья')
        elif (
            player_choice == 'Камень' and computer_choice == 'Ножницы' or
            player_choice == 'Ножницы' and computer_choice == 'Бумага' or
            player_choice == 'Бумага' and computer_choice == 'Камень'
        ):
            self.label_result.setText('Результат: Победа')
            self.label_result.setStyleSheet("background-color : green")
            self.save_statistics(player_choice, computer_choice, 'Игрок победил')
        else:
            self.label_result.setText('Результат: Проигрыш')
            self.label_result.setStyleSheet("background-color : red")
            self.save_statistics(player_choice, computer_choice, 'Игрок проиграл')

    def save_statistics(self, player_choice, computer_choice, result):
        connection = sqlite3.connect("project.db")
        cur = connection.cursor()
        cur.execute(
            "UPDATE statistics SET count = (count+1) WHERE program = 'rock_paper_scissors'"
        )
        cur.execute(
            f"INSERT INTO rock_paper_scissors VALUES (?, ?, ?, ?)",
            (datetime.now(), player_choice, computer_choice, result)
        )
        connection.commit()
        connection.close()

    def open_window_statistics(self):
        self.window_statistics = Statistics()
        self.window_statistics.show()


class Statistics(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/statistics.ui', self)
        self.setWindowTitle('Статистика')

        connection = sqlite3.connect("project.db")
        cur = connection.cursor()
        count, = cur.execute(
            "SELECT count FROM statistics WHERE program = 'rock_paper_scissors'"
        ).fetchone()
        statistics = cur.execute("SELECT * FROM rock_paper_scissors").fetchall()
        connection.close()

        self.label_count.setText(f"Всего игр: {count}")

        self.table_widget_statistics.setRowCount(count)
        self.table_widget_statistics.setColumnCount(4)
        self.table_widget_statistics.setHorizontalHeaderLabels(
            ["Время", "Игрок", "Компьютер", "Результат"]
        )
        self.table_widget_statistics.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        for i in range(len(statistics)):
            row = statistics[i]
            for j in range(len(row)):
                self.table_widget_statistics.setItem(
                    i, j, QTableWidgetItem(row[j])
                ) 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
