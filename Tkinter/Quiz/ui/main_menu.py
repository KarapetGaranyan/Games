import tkinter as tk
from tkinter import ttk


class MainMenuScreen(tk.Frame):
    def __init__(self, master, start_game_callback, show_profile_callback, exit_callback):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.start_game_callback = start_game_callback
        self.show_profile_callback = show_profile_callback
        self.exit_callback = exit_callback

        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        title_frame = tk.Frame(self, bg="#f0f0f0")
        title_frame.pack(pady=50)

        title_label = tk.Label(
            title_frame,
            text="ИНТЕЛЛЕКТУАЛЬНАЯ ВИКТОРИНА",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack()

        # Кнопки меню
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Create a style for the buttons
        style = ttk.Style()
        style.configure("Game.TButton", font=("Arial", 12))

        play_button = ttk.Button(
            button_frame,
            text="Начать игру",
            command=self.start_game_callback,
            width=20,
            style="Game.TButton"
        )
        play_button.pack(pady=10)

        profile_button = ttk.Button(
            button_frame,
            text="Профиль",
            command=self.show_profile_callback,
            width=20,
            style="Game.TButton"
        )
        profile_button.pack(pady=10)

        # Admin button for managing categories and questions
        admin_button = ttk.Button(
            button_frame,
            text="Администрирование",
            command=self.open_admin_panel,
            width=20,
            style="Game.TButton"
        )
        admin_button.pack(pady=10)

        exit_button = ttk.Button(
            button_frame,
            text="Выход",
            command=self.exit_callback,
            width=20,
            style="Game.TButton"
        )
        exit_button.pack(pady=10)

        # Нижний текст
        footer_frame = tk.Frame(self, bg="#f0f0f0")
        footer_frame.pack(side=tk.BOTTOM, pady=20)

        footer_text = tk.Label(
            footer_frame,
            text="© 2025 Интеллектуальная викторина",
            font=("Arial", 8),
            bg="#f0f0f0"
        )
        footer_text.pack()

    def open_admin_panel(self):
        """Open the admin panel for managing categories and questions"""
        try:
            from ui.admin_panel import AdminPanel
            admin_panel = AdminPanel(self.master)
            admin_panel.grab_set()  # Make window modal
        except Exception as e:
            print(f"Ошибка при открытии панели администратора: {e}")