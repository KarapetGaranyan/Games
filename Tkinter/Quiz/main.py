import tkinter as tk
from tkinter import ttk

from ui.main_menu import MainMenuScreen
from ui.profile_screen import ProfileScreen
from ui.category_select import CategorySelectScreen
from ui.question_screen import QuestionScreen
from ui.results_screen import ResultsScreen
from db_manager import initialize_database, check_user_exists, create_user


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Интеллектуальная викторина")
        self.geometry("800x600")
        self.resizable(True, True)

        # Инициализация базы данных
        initialize_database()

        # Глобальные данные приложения
        self.current_user_id = None
        self.current_screen = None

        # Проверка наличия пользователя при запуске
        self.check_user_on_startup()

    def check_user_on_startup(self):
        # Если пользователь существует, загрузить его профиль и показать главное меню
        # Иначе показать экран создания профиля
        if check_user_exists():
            self.current_user_id = 1  # Упрощенно, в реальности получаем ID пользователя
            self.show_main_menu()
        else:
            self.show_create_profile()

    def show_create_profile(self):
        # Очищаем предыдущий экран, если он был
        if self.current_screen:
            self.current_screen.pack_forget()

        # Создаем и отображаем экран создания профиля
        self.current_screen = ProfileScreen(self, is_creation=True, save_callback=self.on_profile_created)
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def on_profile_created(self, username, avatar_path):
        # Создаем пользователя и переходим в главное меню
        self.current_user_id = create_user(username, avatar_path)
        self.show_main_menu()

    def show_main_menu(self):
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = MainMenuScreen(
            self,
            start_game_callback=self.show_category_select,
            show_profile_callback=self.show_profile,
            exit_callback=self.quit
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def show_profile(self):
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = ProfileScreen(
            self,
            user_id=self.current_user_id,
            is_creation=False,
            save_callback=self.on_profile_updated
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def on_profile_updated(self, username, avatar_path):
        # Обновить профиль и вернуться в главное меню
        # обновление профиля из db_manager
        self.show_main_menu()

    def show_category_select(self):
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = CategorySelectScreen(
            self,
            start_game_callback=self.start_game
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def start_game(self, category_id, category_name):
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = QuestionScreen(
            self,
            category_id,
            category_name,
            finish_game_callback=self.show_results
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def show_results(self, total_points, correct_answers, total_questions, category_name):
        if self.current_screen:
            self.current_screen.pack_forget()

        self.current_screen = ResultsScreen(
            self,
            total_points,
            correct_answers,
            total_questions,
            category_name,
            return_to_menu_callback=self.show_main_menu,
            play_again_callback=self.show_category_select
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()