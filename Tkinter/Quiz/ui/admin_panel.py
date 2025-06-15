import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import (get_all_categories, get_questions_for_category,
                        get_answers_for_question, add_category, update_category,
                        delete_category, add_question, update_question,
                        update_answer, delete_question)


class AdminPanel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Панель администратора")
        self.geometry("900x700")
        self.resizable(True, True)

        # Create notebook with tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for categories and questions
        self.categories_tab = ttk.Frame(self.notebook)
        self.questions_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.categories_tab, text="Рубрики")
        self.notebook.add(self.questions_tab, text="Вопросы")

        # Setup each tab
        self.setup_categories_tab()
        self.setup_questions_tab()

    def setup_categories_tab(self):
        # Split into two frames
        left_frame = ttk.Frame(self.categories_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_frame = ttk.Frame(self.categories_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create category list with scrollbar
        list_frame = ttk.LabelFrame(left_frame, text="Список рубрик")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.category_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
        self.category_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.category_listbox.yview)

        # Bind selection event
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)

        # Buttons for category actions
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Добавить рубрику", command=self.add_new_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить рубрику", command=self.delete_selected_category).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(button_frame, text="Обновить список", command=self.load_categories).pack(side=tk.LEFT, padx=5)

        # Category edit form
        edit_frame = ttk.LabelFrame(right_frame, text="Редактирование рубрики")
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(edit_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.category_name_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.category_name_var, width=40).grid(row=0, column=1, sticky=tk.W + tk.E,
                                                                                  padx=5, pady=5)

        ttk.Label(edit_frame, text="Описание:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.category_desc_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.category_desc_var, width=40).grid(row=1, column=1, sticky=tk.W + tk.E,
                                                                                  padx=5, pady=5)

        ttk.Button(edit_frame, text="Сохранить изменения", command=self.save_category).grid(row=2, column=0,
                                                                                            columnspan=2, pady=10)

        # Current selected category ID
        self.current_category_id = None

        # Load categories
        self.load_categories()

    def setup_questions_tab(self):
        # Split into frames
        top_frame = ttk.Frame(self.questions_tab)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        main_frame = ttk.Frame(self.questions_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Category selector
        ttk.Label(top_frame, text="Выберите рубрику:").pack(side=tk.LEFT, padx=5)
        self.question_category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(top_frame, textvariable=self.question_category_var, width=30)
        self.category_combobox.pack(side=tk.LEFT, padx=5)
        self.category_combobox.bind("<<ComboboxSelected>>", self.on_question_category_change)

        # Split main frame
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Questions list
        list_frame = ttk.LabelFrame(left_frame, text="Список вопросов")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.question_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
        self.question_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.question_listbox.yview)

        # Bind selection event
        self.question_listbox.bind('<<ListboxSelect>>', self.on_question_select)

        # Buttons for question actions
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Добавить вопрос", command=self.add_new_question).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить вопрос", command=self.delete_selected_question).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Button(button_frame, text="Обновить список", command=self.load_questions).pack(side=tk.LEFT, padx=5)

        # Question edit form
        edit_frame = ttk.LabelFrame(right_frame, text="Редактирование вопроса")
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(edit_frame, text="Текст вопроса:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.question_text_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.question_text_var, width=40).grid(row=0, column=1, sticky=tk.W + tk.E,
                                                                                  padx=5, pady=5)

        ttk.Label(edit_frame, text="Время на ответ (сек):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.time_limit_var = tk.IntVar(value=30)
        ttk.Spinbox(edit_frame, from_=10, to=60, textvariable=self.time_limit_var, width=5).grid(row=1, column=1,
                                                                                                 sticky=tk.W, padx=5,
                                                                                                 pady=5)

        ttk.Label(edit_frame, text="Сложность (1.0-2.0):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.difficulty_var = tk.DoubleVar(value=1.0)
        ttk.Spinbox(edit_frame, from_=1.0, to=2.0, increment=0.1, textvariable=self.difficulty_var, width=5).grid(row=2,
                                                                                                                  column=1,
                                                                                                                  sticky=tk.W,
                                                                                                                  padx=5,
                                                                                                                  pady=5)

        # Answers frame
        answers_frame = ttk.LabelFrame(edit_frame, text="Варианты ответов")
        answers_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)

        self.answer_entries = []
        self.answer_vars = []
        self.correct_answer_var = tk.IntVar(value=0)

        for i in range(4):
            frame = ttk.Frame(answers_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)

            radio = ttk.Radiobutton(frame, text=f"Вариант {i + 1}", variable=self.correct_answer_var, value=i)
            radio.pack(side=tk.LEFT, padx=5)

            answer_var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=answer_var, width=40)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.answer_entries.append(entry)
            self.answer_vars.append(answer_var)

        ttk.Button(edit_frame, text="Сохранить изменения", command=self.save_question).grid(row=4, column=0,
                                                                                            columnspan=2, pady=10)

        # Current selected question ID and answers
        self.current_question_id = None
        self.current_answers = []

        # Load categories for dropdown
        self.load_category_dropdown()

    def load_categories(self):
        """Load categories into the listbox"""
        self.category_listbox.delete(0, tk.END)
        self.categories = get_all_categories()

        for category_id, name, description in self.categories:
            self.category_listbox.insert(tk.END, name)

    def load_category_dropdown(self):
        """Load categories into the dropdown on the questions tab"""
        self.categories = get_all_categories()
        category_names = [name for _, name, _ in self.categories]
        self.category_combobox['values'] = category_names

        if category_names:
            self.category_combobox.current(0)
            self.on_question_category_change(None)

    def on_category_select(self, event):
        """Handle category selection in the listbox"""
        selection = self.category_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        category_id, name, description = self.categories[index]

        self.current_category_id = category_id
        self.category_name_var.set(name)
        self.category_desc_var.set(description)

    def add_new_category(self):
        """Add a new category"""
        self.current_category_id = None
        self.category_name_var.set("")
        self.category_desc_var.set("")

    def save_category(self):
        """Save the current category"""
        name = self.category_name_var.get().strip()
        description = self.category_desc_var.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Название рубрики не может быть пустым")
            return

        try:
            if self.current_category_id:
                # Update existing category
                update_category(self.current_category_id, name, description)
                messagebox.showinfo("Успешно", "Рубрика обновлена")
            else:
                # Add new category
                add_category(name, description)
                messagebox.showinfo("Успешно", "Рубрика добавлена")

            # Refresh lists
            self.load_categories()
            self.load_category_dropdown()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить рубрику: {e}")

    def delete_selected_category(self):
        """Delete the selected category"""
        if not self.current_category_id:
            messagebox.showerror("Ошибка", "Не выбрана рубрика для удаления")
            return

        if not messagebox.askyesno("Подтверждение",
                                   "Вы уверены, что хотите удалить эту рубрику? Все вопросы и ответы в этой рубрике также будут удалены."):
            return

        try:
            delete_category(self.current_category_id)
            messagebox.showinfo("Успешно", "Рубрика удалена")

            # Refresh lists
            self.current_category_id = None
            self.category_name_var.set("")
            self.category_desc_var.set("")
            self.load_categories()
            self.load_category_dropdown()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить рубрику: {e}")

    def on_question_category_change(self, event):
        """Handle category selection in the questions tab"""
        self.load_questions()

    def load_questions(self):
        """Load questions for the selected category"""
        self.question_listbox.delete(0, tk.END)

        selected_category = self.question_category_var.get()
        if not selected_category:
            return

        # Find category ID
        category_id = None
        for cat_id, name, _ in self.categories:
            if name == selected_category:
                category_id = cat_id
                break

        if not category_id:
            return

        # Load questions for this category
        self.questions = get_questions_for_category(category_id, limit=100)  # Get all questions

        for question_id, _, question_text, _, _ in self.questions:
            # Truncate long questions for display
            display_text = question_text if len(question_text) < 50 else question_text[:47] + "..."
            self.question_listbox.insert(tk.END, display_text)

    def on_question_select(self, event):
        """Handle question selection in the listbox"""
        selection = self.question_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        question_id, category_id, question_text, time_limit, difficulty = self.questions[index]

        self.current_question_id = question_id
        self.question_text_var.set(question_text)
        self.time_limit_var.set(time_limit)
        self.difficulty_var.set(difficulty)

        # Load answers
        self.current_answers = get_answers_for_question(question_id)

        # Reset all answer fields
        for i, (answer_var, entry) in enumerate(zip(self.answer_vars, self.answer_entries)):
            if i < len(self.current_answers):
                answer_id, _, answer_text, is_correct = self.current_answers[i]
                answer_var.set(answer_text)
                if is_correct:
                    self.correct_answer_var.set(i)
            else:
                answer_var.set("")

    def add_new_question(self):
        """Add a new question"""
        self.current_question_id = None
        self.question_text_var.set("")
        self.time_limit_var.set(30)
        self.difficulty_var.set(1.0)
        self.current_answers = []

        # Clear answer fields
        for answer_var in self.answer_vars:
            answer_var.set("")
        self.correct_answer_var.set(0)

    def save_question(self):
        """Save the current question"""
        question_text = self.question_text_var.get().strip()
        time_limit = self.time_limit_var.get()
        difficulty = self.difficulty_var.get()

        if not question_text:
            messagebox.showerror("Ошибка", "Текст вопроса не может быть пустым")
            return

        # Validate answers
        answers = []
        correct_index = self.correct_answer_var.get()

        for i, answer_var in enumerate(self.answer_vars):
            answer_text = answer_var.get().strip()
            if not answer_text:
                messagebox.showerror("Ошибка", f"Вариант ответа {i + 1} не может быть пустым")
                return
            answers.append((answer_text, i == correct_index))

        try:
            if self.current_question_id:
                # Update existing question
                update_question(self.current_question_id, question_text, time_limit, difficulty)

                # Update answers
                for i, (answer_text, is_correct) in enumerate(answers):
                    if i < len(self.current_answers):
                        answer_id = self.current_answers[i][0]
                        update_answer(answer_id, answer_text, is_correct)

                messagebox.showinfo("Успешно", "Вопрос обновлен")
            else:
                # Add new question
                # Get selected category
                selected_category = self.question_category_var.get()
                category_id = None
                for cat_id, name, _ in self.categories:
                    if name == selected_category:
                        category_id = cat_id
                        break

                if not category_id:
                    messagebox.showerror("Ошибка", "Не выбрана рубрика")
                    return

                add_question(category_id, question_text, time_limit, difficulty, answers)
                messagebox.showinfo("Успешно", "Вопрос добавлен")

            # Refresh list
            self.load_questions()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить вопрос: {e}")

    def delete_selected_question(self):
        """Delete the selected question"""
        if not self.current_question_id:
            messagebox.showerror("Ошибка", "Не выбран вопрос для удаления")
            return

        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот вопрос?"):
            return

        try:
            delete_question(self.current_question_id)
            messagebox.showinfo("Успешно", "Вопрос удален")

            # Refresh list
            self.current_question_id = None
            self.load_questions()
            self.add_new_question()  # Reset form
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить вопрос: {e}")