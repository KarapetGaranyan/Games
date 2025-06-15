import tkinter as tk
from tkinter import messagebox, ttk
import random


class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Переменные для хранения состояния игры
        self.current_player = "X"
        self.player_choice = "X"
        self.buttons = []
        self.game_active = True
        self.score_x = 0
        self.score_o = 0
        self.games_to_win = 3
        self.games_played = 0

        # Создание интерфейса
        self.create_choice_frame()
        self.create_score_frame()
        self.create_game_frame()
        self.create_control_frame()

    def create_choice_frame(self):
        """Создает фрейм для выбора символа игрока"""
        choice_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        choice_frame.pack(fill="x")

        choice_label = tk.Label(
            choice_frame,
            text="Выберите символ:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        choice_label.pack(side="left", padx=10)

        self.player_var = tk.StringVar(value="X")

        x_button = tk.Radiobutton(
            choice_frame,
            text="X",
            variable=self.player_var,
            value="X",
            font=("Arial", 12),
            bg="#f0f0f0",
            command=self.update_player_choice
        )
        x_button.pack(side="left", padx=10)

        o_button = tk.Radiobutton(
            choice_frame,
            text="O",
            variable=self.player_var,
            value="O",
            font=("Arial", 12),
            bg="#f0f0f0",
            command=self.update_player_choice
        )
        o_button.pack(side="left", padx=10)

    def create_score_frame(self):
        """Создает фрейм для отображения счета"""
        score_frame = tk.Frame(self.root, bg="#f0f0f0", pady=5)
        score_frame.pack(fill="x")

        # Метка для отображения текущего игрока
        self.player_label = tk.Label(
            score_frame,
            text="Сейчас ходит: X",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.player_label.pack(pady=5)

        # Метки для отображения счета
        score_label = tk.Label(
            score_frame,
            text=f"Счет (до {self.games_to_win} побед):",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        score_label.pack(pady=5)

        score_info_frame = tk.Frame(score_frame, bg="#f0f0f0")
        score_info_frame.pack()

        self.x_score_label = tk.Label(
            score_info_frame,
            text=f"X: {self.score_x}",
            font=("Arial", 12),
            bg="#e6f0ff",
            width=10,
            padx=10,
            pady=5,
            relief="ridge"
        )
        self.x_score_label.pack(side="left", padx=5)

        self.o_score_label = tk.Label(
            score_info_frame,
            text=f"O: {self.score_o}",
            font=("Arial", 12),
            bg="#ffe6e6",
            width=10,
            padx=10,
            pady=5,
            relief="ridge"
        )
        self.o_score_label.pack(side="left", padx=5)

    def create_game_frame(self):
        """Создает игровое поле"""
        game_frame = tk.Frame(self.root, bg="#d9d9d9", padx=10, pady=10)
        game_frame.pack(pady=10)

        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    game_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=3,
                    height=1,
                    bd=2,
                    relief="raised",
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                row.append(btn)
            self.buttons.append(row)

    def create_control_frame(self):
        """Создает фрейм с кнопками управления"""
        control_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        control_frame.pack(fill="x")

        reset_button = tk.Button(
            control_frame,
            text="Сбросить игру",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.reset_game
        )
        reset_button.pack(side="left", padx=10)

        new_match_button = tk.Button(
            control_frame,
            text="Новый матч",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
            command=self.new_match
        )
        new_match_button.pack(side="right", padx=10)

    def update_player_choice(self):
        """Обновляет выбор символа игрока"""
        self.player_choice = self.player_var.get()
        self.reset_game()

    def on_click(self, row, col):
        """Обрабатывает клик по ячейке игрового поля"""
        # Проверяем, активна ли игра и пуста ли ячейка
        if not self.game_active or self.buttons[row][col]['text'] != "":
            return

        # Устанавливаем символ текущего игрока
        self.buttons[row][col]['text'] = self.current_player

        # Устанавливаем цвет символа
        if self.current_player == "X":
            self.buttons[row][col]['fg'] = "#3366ff"  # Синий для X
        else:
            self.buttons[row][col]['fg'] = "#ff3333"  # Красный для O

        # Проверяем, выиграл ли кто-то
        if self.check_winner():
            self.game_active = False

            # Обновляем счет
            if self.current_player == "X":
                self.score_x += 1
                self.x_score_label['text'] = f"X: {self.score_x}"
            else:
                self.score_o += 1
                self.o_score_label['text'] = f"O: {self.score_o}"

            self.games_played += 1

            # Проверяем, достиг ли кто-то нужного количества побед
            if self.score_x >= self.games_to_win or self.score_o >= self.games_to_win:
                winner = "X" if self.score_x >= self.games_to_win else "O"
                messagebox.showinfo("Матч окончен", f"Игрок {winner} выиграл матч!")
                self.new_match()
            else:
                messagebox.showinfo("Игра окончена", f"Игрок {self.current_player} победил!")

        # Проверяем на ничью
        elif self.check_draw():
            self.game_active = False
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.games_played += 1
        else:
            # Меняем игрока
            self.current_player = "O" if self.current_player == "X" else "X"
            self.player_label['text'] = f"Сейчас ходит: {self.current_player}"

    def check_winner(self):
        """Проверяет, выиграл ли кто-то"""
        # Проверка по горизонтали
        for i in range(3):
            if (self.buttons[i][0]['text'] == self.buttons[i][1]['text'] ==
                    self.buttons[i][2]['text'] != ""):
                # Подсвечиваем выигрышную линию
                for j in range(3):
                    self.buttons[i][j]['bg'] = "#c8e6c9"  # Светло-зеленый
                return True

        # Проверка по вертикали
        for i in range(3):
            if (self.buttons[0][i]['text'] == self.buttons[1][i]['text'] ==
                    self.buttons[2][i]['text'] != ""):
                # Подсвечиваем выигрышную линию
                for j in range(3):
                    self.buttons[j][i]['bg'] = "#c8e6c9"
                return True

        # Проверка по диагонали (сверху слева - вниз справа)
        if (self.buttons[0][0]['text'] == self.buttons[1][1]['text'] ==
                self.buttons[2][2]['text'] != ""):
            # Подсвечиваем выигрышную линию
            self.buttons[0][0]['bg'] = "#c8e6c9"
            self.buttons[1][1]['bg'] = "#c8e6c9"
            self.buttons[2][2]['bg'] = "#c8e6c9"
            return True

        # Проверка по диагонали (сверху справа - вниз слева)
        if (self.buttons[0][2]['text'] == self.buttons[1][1]['text'] ==
                self.buttons[2][0]['text'] != ""):
            # Подсвечиваем выигрышную линию
            self.buttons[0][2]['bg'] = "#c8e6c9"
            self.buttons[1][1]['bg'] = "#c8e6c9"
            self.buttons[2][0]['bg'] = "#c8e6c9"
            return True

        return False

    def check_draw(self):
        """Проверяет, наступила ли ничья"""
        for row in self.buttons:
            for button in row:
                if button['text'] == "":
                    return False
        return True

    def reset_game(self):
        """Сбрасывает текущую игру"""
        # Возвращаем игрока в начальное состояние
        self.current_player = self.player_choice
        self.player_label['text'] = f"Сейчас ходит: {self.current_player}"

        # Очищаем игровое поле
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ""
                self.buttons[i][j]['bg'] = "SystemButtonFace"

        # Активируем игру
        self.game_active = True

    def new_match(self):
        """Начинает новый матч"""
        # Сбрасываем счет
        self.score_x = 0
        self.score_o = 0
        self.games_played = 0

        # Обновляем метки счета
        self.x_score_label['text'] = f"X: {self.score_x}"
        self.o_score_label['text'] = f"O: {self.score_o}"

        # Сбрасываем игру
        self.reset_game()


def main():
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()