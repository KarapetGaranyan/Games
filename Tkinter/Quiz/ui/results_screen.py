import tkinter as tk
from tkinter import ttk


class ResultsScreen(tk.Frame):
    def __init__(self, master, total_points, correct_answers, total_questions, category_name,
                 return_to_menu_callback, play_again_callback):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.total_points = total_points
        self.correct_answers = correct_answers
        self.total_questions = total_questions
        self.category_name = category_name
        self.return_to_menu_callback = return_to_menu_callback
        self.play_again_callback = play_again_callback

        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self,
            text="Результаты игры",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=30)

        # Основной контейнер для результатов
        results_container = tk.Frame(self, bg="#ffffff", padx=30, pady=30)
        results_container.pack(padx=50, pady=20)

        # Категория
        category_label = tk.Label(
            results_container,
            text=f"Категория: {self.category_name}",
            font=("Arial", 14),
            bg="#ffffff",
            anchor=tk.W
        )
        category_label.pack(fill=tk.X, pady=5)

        # Разделительная линия
        separator = ttk.Separator(results_container, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=15)

        # Количество баллов
        points_label = tk.Label(
            results_container,
            text=f"Набрано баллов: {self.total_points}",
            font=("Arial", 18, "bold"),
            bg="#ffffff",
            fg="#4CAF50"
        )
        points_label.pack(pady=10)

        # Количество правильных ответов
        answers_label = tk.Label(
            results_container,
            text=f"Правильных ответов: {self.correct_answers} из {self.total_questions}",
            font=("Arial", 14),
            bg="#ffffff"
        )
        answers_label.pack(pady=5)

        # Процент правильных ответов
        percentage = (self.correct_answers / self.total_questions) * 100 if self.total_questions > 0 else 0
        percentage_label = tk.Label(
            results_container,
            text=f"Точность: {percentage:.1f}%",
            font=("Arial", 14),
            bg="#ffffff"
        )
        percentage_label.pack(pady=5)

        # Оценка результата
        evaluation = self.evaluate_result(percentage)
        evaluation_label = tk.Label(
            results_container,
            text=evaluation,
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg=self.get_evaluation_color(percentage)
        )
        evaluation_label.pack(pady=15)

        # Контейнер для кнопок
        buttons_container = tk.Frame(self, bg="#f0f0f0")
        buttons_container.pack(pady=30)

        # Кнопка "Играть снова"
        play_again_button = ttk.Button(
            buttons_container,
            text="Играть снова",
            command=self.play_again_callback
        )
        play_again_button.pack(side=tk.LEFT, padx=10)

        # Кнопка "Главное меню"
        menu_button = ttk.Button(
            buttons_container,
            text="Главное меню",
            command=self.return_to_menu_callback
        )
        menu_button.pack(side=tk.LEFT, padx=10)

    def evaluate_result(self, percentage):
        """Возвращает текстовую оценку результата на основе процента правильных ответов"""
        if percentage >= 90:
            return "Отлично! Вы настоящий эрудит!"
        elif percentage >= 70:
            return "Хороший результат!"
        elif percentage >= 50:
            return "Неплохо, но есть куда расти."
        else:
            return "Попробуйте еще раз. Практика - путь к совершенству!"

    def get_evaluation_color(self, percentage):
        """Возвращает цвет для оценки результата"""
        if percentage >= 90:
            return "#4CAF50"  # Зеленый
        elif percentage >= 70:
            return "#2196F3"  # Синий
        elif percentage >= 50:
            return "#FF9800"  # Оранжевый
        else:
            return "#F44336"  # Красный