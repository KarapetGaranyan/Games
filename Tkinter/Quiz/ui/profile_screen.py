import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import shutil
from db_manager import get_user_info, update_user_profile, get_user_statistics


class ProfileScreen(tk.Frame):
    def __init__(self, master, user_id=None, is_creation=False, save_callback=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.user_id = user_id
        self.is_creation = is_creation
        self.save_callback = save_callback

        # Директория для аватарок
        self.avatar_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "avatars")
        os.makedirs(self.avatar_dir, exist_ok=True)

        # Инициализация данных пользователя
        self.username = ""
        self.avatar_path = ""

        # Загрузить данные, если это не создание нового профиля
        if not is_creation and user_id:
            user_info = get_user_info(user_id)
            if user_info:
                self.user_id, self.username, self.avatar_path, _ = user_info

        # Настройка интерфейса
        self.setup_ui()

        # Если это не создание профиля, загрузить статистику
        if not is_creation and user_id:
            self.load_statistics()

    def setup_ui(self):
        # Основной контейнер
        main_container = tk.Frame(self, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Заголовок
        title_text = "Создание профиля" if self.is_creation else "Профиль пользователя"
        title_label = tk.Label(
            main_container,
            text=title_text,
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))

        # Фрейм для профиля
        profile_frame = tk.Frame(main_container, bg="#f0f0f0")
        profile_frame.pack(fill=tk.X, pady=10)

        # Контейнер для аватара
        avatar_frame = tk.Frame(profile_frame, bg="#f0f0f0")
        avatar_frame.pack(side=tk.LEFT, padx=20)

        # Изображение аватара
        self.avatar_image = self.load_avatar_image()
        self.avatar_label = tk.Label(
            avatar_frame,
            image=self.avatar_image,
            bg="#f0f0f0",
            width=150,
            height=150
        )
        self.avatar_label.pack()

        # Кнопка для изменения аватара
        change_avatar_button = tk.Button(
            avatar_frame,
            text="Изменить аватар",
            font=("Arial", 10),
            command=self.change_avatar
        )
        change_avatar_button.pack(pady=10)

        # Фрейм для информации
        info_frame = tk.Frame(profile_frame, bg="#f0f0f0")
        info_frame.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)

        # Имя пользователя
        username_label = tk.Label(
            info_frame,
            text="Имя пользователя:",
            font=("Arial", 12),
            bg="#f0f0f0",
            anchor=tk.W
        )
        username_label.pack(fill=tk.X, pady=(0, 5))

        self.username_entry = ttk.Entry(
            info_frame,
            font=("Arial", 12)
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.insert(0, self.username)

        # Кнопки
        button_frame = tk.Frame(info_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X)

        # Create a style for buttons
        style = ttk.Style()
        style.configure("Profile.TButton", font=("Arial", 11))

        save_button = ttk.Button(
            button_frame,
            text="Сохранить",
            style="Profile.TButton",
            command=self.save_profile
        )
        save_button.pack(side=tk.LEFT, padx=5)

        if not self.is_creation:
            back_button = ttk.Button(
                button_frame,
                text="Назад",
                style="Profile.TButton",
                command=self.master.show_main_menu
            )
            back_button.pack(side=tk.LEFT, padx=5)

        # Если это не создание профиля, добавить вкладки статистики
        if not self.is_creation:
            # Фрейм для статистики
            self.stats_frame = tk.Frame(main_container, bg="#f0f0f0")
            self.stats_frame.pack(fill=tk.BOTH, expand=True, pady=20)

            # Создаем вкладки для статистики
            self.stats_notebook = ttk.Notebook(self.stats_frame)
            self.stats_notebook.pack(fill=tk.BOTH, expand=True)

            # Вкладка общей статистики
            self.general_stats_frame = tk.Frame(self.stats_notebook, bg="#f0f0f0")
            self.stats_notebook.add(self.general_stats_frame, text="Общая статистика")

            # Вкладка статистики по категориям
            self.category_stats_frame = tk.Frame(self.stats_notebook, bg="#f0f0f0")
            self.stats_notebook.add(self.category_stats_frame, text="По категориям")

            # Вкладка последних игр
            self.recent_games_frame = tk.Frame(self.stats_notebook, bg="#f0f0f0")
            self.stats_notebook.add(self.recent_games_frame, text="Последние игры")

    def load_avatar_image(self):
        """Загружает изображение аватара или изображение по умолчанию"""
        try:
            if self.avatar_path and os.path.exists(self.avatar_path):
                img = Image.open(self.avatar_path)
                img = img.resize((150, 150), Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                # Изображение по умолчанию
                default_avatar = Image.new('RGB', (150, 150), color='gray')
                return ImageTk.PhotoImage(default_avatar)
        except Exception as e:
            print(f"Ошибка при загрузке аватара: {e}")
            # Изображение по умолчанию в случае ошибки
            default_avatar = Image.new('RGB', (150, 150), color='gray')
            return ImageTk.PhotoImage(default_avatar)

    def change_avatar(self):
        """Открывает диалог выбора изображения для аватара"""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение для аватара",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif")]
        )

        if file_path:
            try:
                # Копируем изображение в папку аватаров
                avatar_filename = f"avatar_{self.user_id if self.user_id else 'new'}.png"
                self.avatar_path = os.path.join(self.avatar_dir, avatar_filename)

                # Открываем и сохраняем изображение (с изменением размера)
                img = Image.open(file_path)
                img = img.resize((150, 150), Image.LANCZOS)
                img.save(self.avatar_path)

                # Обновляем отображение
                self.avatar_image = ImageTk.PhotoImage(img)
                self.avatar_label.config(image=self.avatar_image)
            except Exception as e:
                print(f"Ошибка при изменении аватара: {e}")

    def save_profile(self):
        """Сохраняет профиль пользователя"""
        username = self.username_entry.get().strip()

        if not username:
            # Показать сообщение об ошибке
            return

        if self.save_callback:
            self.save_callback(username, self.avatar_path)

    def load_statistics(self):
        """Загружает и отображает статистику пользователя"""
        try:
            stats = get_user_statistics(self.user_id)

            # Проверяем, получены ли статистические данные
            if not stats or 'general' not in stats:
                # Если статистики нет, показываем заглушку
                self.show_no_statistics_message()
                return

            # Заполнение вкладки общей статистики
            self.fill_general_stats(stats['general'])

            # Заполнение вкладки статистики по категориям
            if 'categories' in stats:
                self.fill_category_stats(stats['categories'])

            # Заполнение вкладки последних игр
            if 'recent_games' in stats:
                self.fill_recent_games(stats['recent_games'])
        except Exception as e:
            print(f"Ошибка при загрузке статистики: {e}")
            self.show_no_statistics_message()

    def show_no_statistics_message(self):
        """Отображает сообщение об отсутствии статистики"""
        # Очищаем все вкладки
        for frame in [self.general_stats_frame, self.category_stats_frame, self.recent_games_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        # Показываем сообщение на вкладке общей статистики
        no_data_label = tk.Label(
            self.general_stats_frame,
            text="Нет данных о играх\nСыграйте как минимум одну игру, чтобы увидеть статистику",
            font=("Arial", 12),
            bg="#f0f0f0",
            justify=tk.CENTER
        )
        no_data_label.pack(pady=50)

        # Сообщения на других вкладках
        no_cat_data = tk.Label(
            self.category_stats_frame,
            text="Нет данных о категориях",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        no_cat_data.pack(pady=50)

        no_games_data = tk.Label(
            self.recent_games_frame,
            text="Нет данных о последних играх",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        no_games_data.pack(pady=50)

    def fill_general_stats(self, general_stats):
        """Заполняет вкладку общей статистики"""
        if not general_stats:
            no_data_label = tk.Label(
                self.general_stats_frame,
                text="Нет данных о играх",
                font=("Arial", 12),
                bg="#f0f0f0"
            )
            no_data_label.pack(pady=50)
            return

        # Очищаем содержимое фрейма
        for widget in self.general_stats_frame.winfo_children():
            widget.destroy()

        total_games, total_points, total_correct, total_questions, best_score = general_stats

        # Проверяем все значения на None и заменяем их нулями
        total_games = total_games or 0
        total_points = total_points or 0
        total_correct = total_correct or 0
        total_questions = total_questions or 0
        best_score = best_score or 0

        stats_container = tk.Frame(self.general_stats_frame, bg="#f0f0f0")
        stats_container.pack(pady=20)

        # Всего игр
        games_label = tk.Label(
            stats_container,
            text=f"Всего игр: {total_games}",
            font=("Arial", 14),
            bg="#f0f0f0",
            anchor=tk.W
        )
        games_label.pack(fill=tk.X, pady=5)

        # Всего очков
        points_label = tk.Label(
            stats_container,
            text=f"Всего очков: {total_points}",
            font=("Arial", 14),
            bg="#f0f0f0",
            anchor=tk.W
        )
        points_label.pack(fill=tk.X, pady=5)

        # Лучший результат
        best_label = tk.Label(
            stats_container,
            text=f"Лучший результат: {best_score}",
            font=("Arial", 14),
            bg="#f0f0f0",
            anchor=tk.W
        )
        best_label.pack(fill=tk.X, pady=5)

        # Процент правильных ответов
        if total_questions > 0:
            accuracy = (total_correct / total_questions) * 100
            accuracy_label = tk.Label(
                stats_container,
                text=f"Точность ответов: {accuracy:.1f}%",
                font=("Arial", 14),
                bg="#f0f0f0",
                anchor=tk.W
            )
            accuracy_label.pack(fill=tk.X, pady=5)
        else:
            accuracy_label = tk.Label(
                stats_container,
                text="Точность ответов: -",
                font=("Arial", 14),
                bg="#f0f0f0",
                anchor=tk.W
            )
            accuracy_label.pack(fill=tk.X, pady=5)

    def fill_category_stats(self, category_stats):
        """Заполняет вкладку статистики по категориям"""
        # Очищаем содержимое фрейма
        for widget in self.category_stats_frame.winfo_children():
            widget.destroy()

        if not category_stats:
            no_data_label = tk.Label(
                self.category_stats_frame,
                text="Нет данных о категориях",
                font=("Arial", 12),
                bg="#f0f0f0"
            )
            no_data_label.pack(pady=50)
            return

        # Создаем таблицу с данными по категориям
        table_frame = tk.Frame(self.category_stats_frame, bg="#f0f0f0")
        table_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Заголовки таблицы
        headers = ["Категория", "Игр", "Очков", "Правильных", "Процент"]

        for col, header in enumerate(headers):
            header_label = tk.Label(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg="#e0e0e0",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            header_label.grid(row=0, column=col, sticky=tk.NSEW)

        # Данные по категориям
        for row, (name, games, points, correct, questions) in enumerate(category_stats, start=1):
            # Обработка возможных None значений
            games = games or 0
            points = points or 0
            correct = correct or 0
            questions = questions or 0

            # Категория
            category_label = tk.Label(
                table_frame,
                text=name,
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5,
                anchor=tk.W
            )
            category_label.grid(row=row, column=0, sticky=tk.NSEW)

            # Игр
            games_label = tk.Label(
                table_frame,
                text=str(games),
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            games_label.grid(row=row, column=1, sticky=tk.NSEW)

            # Очков
            points_label = tk.Label(
                table_frame,
                text=str(points),
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            points_label.grid(row=row, column=2, sticky=tk.NSEW)

            # Правильных
            correct_label = tk.Label(
                table_frame,
                text=f"{correct}/{questions}",
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            correct_label.grid(row=row, column=3, sticky=tk.NSEW)

            # Процент
            percentage = (correct / questions * 100) if questions > 0 else 0
            percentage_label = tk.Label(
                table_frame,
                text=f"{percentage:.1f}%",
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            percentage_label.grid(row=row, column=4, sticky=tk.NSEW)

        # Настройка растяжения таблицы
        for i in range(5):
            table_frame.columnconfigure(i, weight=1)

    def fill_recent_games(self, recent_games):
        """Заполняет вкладку последних игр"""
        # Очищаем содержимое фрейма
        for widget in self.recent_games_frame.winfo_children():
            widget.destroy()

        if not recent_games:
            no_data_label = tk.Label(
                self.recent_games_frame,
                text="Нет данных о последних играх",
                font=("Arial", 12),
                bg="#f0f0f0"
            )
            no_data_label.pack(pady=50)
            return

        # Создаем таблицу с данными о последних играх
        table_frame = tk.Frame(self.recent_games_frame, bg="#f0f0f0")
        table_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Заголовки таблицы
        headers = ["Дата", "Категория", "Очки", "Результат"]

        for col, header in enumerate(headers):
            header_label = tk.Label(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg="#e0e0e0",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            header_label.grid(row=0, column=col, sticky=tk.NSEW)

        # Данные о последних играх
        for row, (game_id, category, points, correct, questions, date) in enumerate(recent_games, start=1):
            # Обработка возможных None значений
            points = points or 0
            correct = correct or 0
            questions = questions or 0

            # Дата
            date_str = date[:19] if date else "-"  # Обрезаем до секунд
            date_label = tk.Label(
                table_frame,
                text=date_str,
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            date_label.grid(row=row, column=0, sticky=tk.NSEW)

            # Категория
            category_label = tk.Label(
                table_frame,
                text=category if category else "-",
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            category_label.grid(row=row, column=1, sticky=tk.NSEW)

            # Очки
            points_label = tk.Label(
                table_frame,
                text=str(points),
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            points_label.grid(row=row, column=2, sticky=tk.NSEW)

            # Результат
            result_text = f"{correct}/{questions} ({correct / questions * 100:.1f}%)" if questions > 0 else "-"
            result_label = tk.Label(
                table_frame,
                text=result_text,
                font=("Arial", 12),
                bg="#f5f5f5",
                relief=tk.RIDGE,
                padx=10,
                pady=5
            )
            result_label.grid(row=row, column=3, sticky=tk.NSEW)

        # Настройка растяжения таблицы
        for i in range(4):
            table_frame.columnconfigure(i, weight=1)