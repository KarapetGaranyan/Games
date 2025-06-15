import tkinter as tk
from tkinter import ttk
from db_manager import get_questions_for_category, get_answers_for_question, save_game_results


class QuestionScreen(tk.Frame):
    def __init__(self, master, category_id, category_name, finish_game_callback):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.category_id = category_id
        self.category_name = category_name
        self.finish_game_callback = finish_game_callback

        # Получение вопросов для выбранной категории
        self.questions = get_questions_for_category(category_id, 10)

        # Инициализация переменных для игры
        self.current_question_index = 0
        self.correct_answers = 0
        self.total_points = 0
        self.timer_id = None
        self.answers = []
        self.time_left = 0

        # Настройка интерфейса
        self.setup_ui()

        # Загрузка первого вопроса
        self.load_question()

    def setup_ui(self):
        # Create styles for buttons
        self.style = ttk.Style()
        self.style.configure("Default.TButton", font=("Arial", 12))
        self.style.configure("Correct.TButton", background="#32CD32", font=("Arial", 12))
        self.style.configure("Incorrect.TButton", background="#FF6347", font=("Arial", 12))

        # Верхний информационный блок
        self.info_frame = tk.Frame(self, bg="#e0e0e0", height=40)
        self.info_frame.pack(fill=tk.X)

        # Категория
        self.category_label = tk.Label(
            self.info_frame,
            text=f"Категория: {self.category_name}",
            font=("Arial", 12),
            bg="#e0e0e0"
        )
        self.category_label.pack(side=tk.LEFT, padx=15, pady=10)

        # Прогресс
        self.progress_label = tk.Label(
            self.info_frame,
            text="",
            font=("Arial", 12),
            bg="#e0e0e0"
        )
        self.progress_label.pack(side=tk.RIGHT, padx=15, pady=10)

        # Блок с таймером
        self.timer_frame = tk.Frame(self, bg="#f0f0f0")
        self.timer_frame.pack(fill=tk.X, pady=5)

        self.timer_label = tk.Label(
            self.timer_frame,
            text="Время: 30 сек",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.timer_label.pack(side=tk.LEFT, padx=15)

        self.timer_bar = ttk.Progressbar(
            self.timer_frame,
            orient=tk.HORIZONTAL,
            length=500,
            mode='determinate'
        )
        self.timer_bar.pack(side=tk.RIGHT, padx=15, fill=tk.X, expand=True)

        # Блок с вопросом
        self.question_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        self.question_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.question_text = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 16),
            wraplength=700,
            justify=tk.LEFT,
            bg="#f5f5f5"
        )
        self.question_text.pack(anchor=tk.W, pady=20)

        # Блок с вариантами ответов
        self.answers_frame = tk.Frame(self, bg="#f0f0f0")
        self.answers_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Using standard tk.Button instead of ttk.Button for easier styling
        self.answer_buttons = []
        for i in range(4):
            button = tk.Button(
                self.answers_frame,
                text="",
                font=("Arial", 12),
                bg="#f0f0f0",
                activebackground="#e0e0e0",
                width=50,
                height=2,
                command=lambda idx=i: self.check_answer(idx)
            )
            button.pack(fill=tk.X, pady=5, ipady=5)
            self.answer_buttons.append(button)

        # Кнопка для пропуска вопроса
        self.skip_button = tk.Button(
            self,
            text="Пропустить",
            font=("Arial", 12),
            bg="#f0f0f0",
            activebackground="#e0e0e0",
            command=self.skip_question
        )
        self.skip_button.pack(side=tk.BOTTOM, pady=15)

    def load_question(self):
        """Загружает текущий вопрос и варианты ответов"""
        if self.current_question_index >= len(self.questions):
            self.finish_game()
            return

        # Очистка предыдущего таймера, если есть
        if self.timer_id:
            self.after_cancel(self.timer_id)

        # Обновляем индикатор прогресса
        self.progress_label.config(
            text=f"Вопрос {self.current_question_index + 1} из {len(self.questions)}"
        )

        # Получаем данные текущего вопроса
        question_data = self.questions[self.current_question_index]
        question_id, _, question_text, time_limit, difficulty = question_data

        # Обновляем текст вопроса
        self.question_text.config(text=question_text)

        # Получаем варианты ответов для текущего вопроса
        self.answers = get_answers_for_question(question_id)

        # Перемешиваем варианты ответов и обновляем кнопки
        for i, (answer_id, _, answer_text, _) in enumerate(self.answers):
            self.answer_buttons[i].config(
                text=answer_text,
                state=tk.NORMAL,
                bg="#f0f0f0"
            )

        # Запускаем таймер
        self.time_left = time_limit
        self.timer_bar.config(maximum=time_limit, value=time_limit)
        self.update_timer()

    def update_timer(self):
        """Обновляет отображение таймера и проверяет, не истекло ли время"""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Время: {self.time_left} сек")
            self.timer_bar.config(value=self.time_left)
            self.timer_id = self.after(1000, self.update_timer)
        else:
            # Время истекло
            self.timer_label.config(text="Время истекло!")
            self.disable_answer_buttons()
            self.after(1500, self.next_question)

    def check_answer(self, answer_index):
        """Проверяет правильность выбранного ответа"""
        # Останавливаем таймер
        if self.timer_id:
            self.after_cancel(self.timer_id)

        # Деактивируем все кнопки ответов
        self.disable_answer_buttons()

        # Получаем выбранный ответ
        _, _, _, is_correct = self.answers[answer_index]

        # Выделяем выбранный ответ
        self.answer_buttons[answer_index].config(
            bg="#32CD32" if is_correct else "#FF6347"
        )

        # Показываем также правильный ответ, если выбран неправильный
        if not is_correct:
            for i, (_, _, _, correct) in enumerate(self.answers):
                if correct:
                    self.answer_buttons[i].config(bg="#32CD32")

        # Если ответ правильный, увеличиваем счетчики
        if is_correct:
            self.correct_answers += 1

            # Расчет очков: базовые очки + бонус за скорость + множитель сложности
            question_difficulty = self.questions[self.current_question_index][4]
            base_points = 100
            time_bonus = int((self.time_left / self.questions[self.current_question_index][3]) * 50)
            points = int((base_points + time_bonus) * question_difficulty)

            self.total_points += points

        # Переход к следующему вопросу через небольшую паузу
        self.after(1500, self.next_question)

    def disable_answer_buttons(self):
        """Деактивирует все кнопки ответов"""
        for button in self.answer_buttons:
            button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)

    def skip_question(self):
        """Пропускает текущий вопрос"""
        # Останавливаем таймер
        if self.timer_id:
            self.after_cancel(self.timer_id)

        # Деактивируем кнопки
        self.disable_answer_buttons()

        # Показываем правильный ответ
        for i, (_, _, _, is_correct) in enumerate(self.answers):
            if is_correct:
                self.answer_buttons[i].config(bg="#32CD32")

        # Переход к следующему вопросу
        self.after(1500, self.next_question)

    def next_question(self):
        """Переходит к следующему вопросу"""
        self.current_question_index += 1

        # Восстанавливаем исходное состояние кнопок
        for button in self.answer_buttons:
            button.config(state=tk.NORMAL, bg="#f0f0f0")
        self.skip_button.config(state=tk.NORMAL)

        # Загружаем следующий вопрос
        self.load_question()

    def finish_game(self):
        """Завершает игру и переходит к экрану результатов"""
        # Сохраняем результаты в БД
        try:
            save_game_results(
                self.master.current_user_id,
                self.category_id,
                self.total_points,
                self.correct_answers,
                len(self.questions)
            )
        except Exception as e:
            print(f"Ошибка при сохранении результатов: {e}")

        # Вызываем callback для отображения результатов
        self.finish_game_callback(
            self.total_points,
            self.correct_answers,
            len(self.questions),
            self.category_name
        )