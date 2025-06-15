import tkinter as tk
from tkinter import ttk
from db_manager import get_all_categories


class CategorySelectScreen(tk.Frame):
    def __init__(self, master, start_game_callback):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.start_game_callback = start_game_callback

        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self,
            text="Выберите категорию",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=20)

        # Основной контейнер для категорий
        categories_container = tk.Frame(self, bg="#f0f0f0")
        categories_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Получение списка категорий из базы данных
        categories = get_all_categories()

        # Создание карточек для каждой категории
        for cat_id, name, description in categories:
            category_card = tk.Frame(
                categories_container,
                bg="#ffffff",
                relief=tk.RAISED,
                bd=1
            )
            category_card.pack(fill=tk.X, pady=10, ipady=10)

            # Название категории
            name_label = tk.Label(
                category_card,
                text=name,
                font=("Arial", 14, "bold"),
                bg="#ffffff"
            )
            name_label.pack(anchor=tk.W, padx=15, pady=(10, 5))

            # Описание категории
            description_label = tk.Label(
                category_card,
                text=description,
                font=("Arial", 12),
                bg="#ffffff",
                wraplength=600,
                justify=tk.LEFT
            )
            description_label.pack(anchor=tk.W, padx=15, pady=(0, 10))

            # Кнопка выбора категории
            select_button = ttk.Button(
                category_card,
                text="Выбрать",
                command=lambda cid=cat_id, cname=name: self.select_category(cid, cname)
            )
            select_button.pack(side=tk.RIGHT, padx=15, pady=10)

        # Кнопка "Назад"
        back_button = ttk.Button(
            self,
            text="Назад",
            command=self.master.show_main_menu
        )
        back_button.pack(pady=20)

    def select_category(self, category_id, category_name):
        """Обработчик выбора категории"""
        self.start_game_callback(category_id, category_name)