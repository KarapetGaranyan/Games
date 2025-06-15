import sqlite3
import os
from datetime import datetime

DB_PATH = 'quiz_game.db'


def initialize_database():
    """Инициализирует базу данных при первом запуске приложения"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        avatar_path TEXT,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Создание таблицы категорий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')

    # Создание таблицы вопросов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        question_text TEXT NOT NULL,
        time_limit INTEGER DEFAULT 30,
        difficulty_level REAL DEFAULT 1.0,
        FOREIGN KEY (category_id) REFERENCES Categories (category_id)
    )
    ''')

    # Создание таблицы ответов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Answers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        answer_text TEXT NOT NULL,
        is_correct BOOLEAN NOT NULL CHECK (is_correct IN (0, 1)),
        FOREIGN KEY (question_id) REFERENCES Questions (question_id)
    )
    ''')

    # Создание таблицы истории игр
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS GameHistory (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        total_points INTEGER,
        correct_answers INTEGER,
        total_questions INTEGER,
        date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users (user_id),
        FOREIGN KEY (category_id) REFERENCES Categories (category_id)
    )
    ''')

    # Добавление стандартных категорий
    default_categories = [
        ('История', 'Вопросы об исторических событиях и личностях'),
        ('Наука', 'Вопросы о научных открытиях и явлениях'),
        ('Культура', 'Вопросы о искусстве, литературе и музыке'),
        ('Спорт', 'Вопросы о спортивных событиях и достижениях')
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO Categories (name, description) 
    SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM Categories WHERE name = ?)
    ''', [(c[0], c[1], c[0]) for c in default_categories])

    # Добавление тестовых вопросов для каждой категории
    populate_test_questions(cursor)

    conn.commit()
    conn.close()


def populate_test_questions(cursor):
    """Заполняет базу данных тестовыми вопросами"""
    # Получаем ID категорий
    cursor.execute("SELECT category_id, name FROM Categories")
    categories = cursor.fetchall()

    for cat_id, cat_name in categories:
        # Примеры вопросов для каждой категории (в реальном приложении здесь будет больше вопросов)
        if cat_name == "История":
            add_question_with_answers(cursor, cat_id, "В каком году началась Вторая мировая война?",
                                      ["1937", "1939", "1941", "1940"], 1, 30, 1.0)
            add_question_with_answers(cursor, cat_id, "Кто был первым президентом США?",
                                      ["Джордж Вашингтон", "Томас Джефферсон", "Авраам Линкольн", "Франклин Рузвельт"],
                                      0, 20, 1.0)
        elif cat_name == "Наука":
            add_question_with_answers(cursor, cat_id, "Что измеряется в Ньютонах?",
                                      ["Масса", "Скорость", "Сила", "Ускорение"], 2, 25, 1.0)
            add_question_with_answers(cursor, cat_id, "Какой химический элемент имеет символ 'O'?",
                                      ["Золото", "Кислород", "Осмий", "Олово"], 1, 15, 1.0)
        elif cat_name == "Культура":
            add_question_with_answers(cursor, cat_id, "Кто написал 'Войну и мир'?",
                                      ["Федор Достоевский", "Лев Толстой", "Антон Чехов", "Иван Тургенев"], 1, 20, 1.0)
            add_question_with_answers(cursor, cat_id, "В каком городе находится Лувр?",
                                      ["Лондон", "Рим", "Париж", "Мадрид"], 2, 15, 1.0)
        elif cat_name == "Спорт":
            add_question_with_answers(cursor, cat_id, "Сколько игроков в команде по футболу?",
                                      ["9", "10", "11", "12"], 2, 15, 1.0)
            add_question_with_answers(cursor, cat_id, "В каком году прошли первые современные Олимпийские игры?",
                                      ["1886", "1896", "1900", "1904"], 1, 30, 1.5)


def add_question_with_answers(cursor, category_id, question_text, answers, correct_index, time_limit, difficulty):
    """Добавляет вопрос и соответствующие ответы в базу данных"""
    cursor.execute('''
    INSERT INTO Questions (category_id, question_text, time_limit, difficulty_level)
    VALUES (?, ?, ?, ?)
    ''', (category_id, question_text, time_limit, difficulty))

    question_id = cursor.lastrowid

    for i, answer_text in enumerate(answers):
        is_correct = 1 if i == correct_index else 0
        cursor.execute('''
        INSERT INTO Answers (question_id, answer_text, is_correct)
        VALUES (?, ?, ?)
        ''', (question_id, answer_text, is_correct))


def check_user_exists():
    """Проверяет, существует ли хотя бы один пользователь в базе данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users")
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0


def create_user(username, avatar_path):
    """Создает нового пользователя и возвращает его ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Users (username, avatar_path)
    VALUES (?, ?)
    ''', (username, avatar_path))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def get_user_info(user_id):
    """Возвращает информацию о пользователе по ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT user_id, username, avatar_path, date_created
    FROM Users
    WHERE user_id = ?
    ''', (user_id,))

    user_info = cursor.fetchone()

    conn.close()
    return user_info


def update_user_profile(user_id, username, avatar_path):
    """Обновляет профиль пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE Users
    SET username = ?, avatar_path = ?
    WHERE user_id = ?
    ''', (username, avatar_path, user_id))

    conn.commit()
    conn.close()


def get_all_categories():
    """Возвращает список всех категорий"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT category_id, name, description
    FROM Categories
    ORDER BY name
    ''')

    categories = cursor.fetchall()

    conn.close()
    return categories


def get_questions_for_category(category_id, limit=10):
    """Возвращает вопросы для выбранной категории"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT question_id, category_id, question_text, time_limit, difficulty_level
    FROM Questions
    WHERE category_id = ?
    ORDER BY RANDOM()
    LIMIT ?
    ''', (category_id, limit))

    questions = cursor.fetchall()

    conn.close()
    return questions


def get_answers_for_question(question_id):
    """Возвращает варианты ответов для вопроса"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT answer_id, question_id, answer_text, is_correct
    FROM Answers
    WHERE question_id = ?
    ORDER BY RANDOM()
    ''', (question_id,))

    answers = cursor.fetchall()

    conn.close()
    return answers


def save_game_results(user_id, category_id, total_points, correct_answers, total_questions):
    """Сохраняет результаты игры"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO GameHistory (user_id, category_id, total_points, correct_answers, total_questions)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, category_id, total_points, correct_answers, total_questions))

    conn.commit()
    conn.close()


def get_user_statistics(user_id):
    """Возвращает статистику пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, есть ли у пользователя какие-либо игры
    cursor.execute("SELECT COUNT(*) FROM GameHistory WHERE user_id = ?", (user_id,))
    games_count = cursor.fetchone()[0]

    if games_count == 0:
        conn.close()
        # Возвращаем структуру с пустыми значениями
        return {
            'general': (0, 0, 0, 0, 0),
            'categories': [],
            'recent_games': []
        }

    # Общая статистика
    cursor.execute('''
    SELECT COUNT(*) as total_games,
           SUM(total_points) as total_points,
           SUM(correct_answers) as total_correct,
           SUM(total_questions) as total_questions,
           MAX(total_points) as best_score
    FROM GameHistory
    WHERE user_id = ?
    ''', (user_id,))

    general_stats = cursor.fetchone()

    # Статистика по категориям
    cursor.execute('''
    SELECT c.name,
           COUNT(*) as games_played,
           SUM(gh.total_points) as category_points,
           SUM(gh.correct_answers) as category_correct,
           SUM(gh.total_questions) as category_questions
    FROM GameHistory gh
    JOIN Categories c ON gh.category_id = c.category_id
    WHERE gh.user_id = ?
    GROUP BY gh.category_id
    ORDER BY category_points DESC
    ''', (user_id,))

    category_stats = cursor.fetchall()

    # Последние игры
    cursor.execute('''
    SELECT gh.game_id, c.name, gh.total_points, gh.correct_answers, gh.total_questions, gh.date_played
    FROM GameHistory gh
    JOIN Categories c ON gh.category_id = c.category_id
    WHERE gh.user_id = ?
    ORDER BY gh.date_played DESC
    LIMIT 5
    ''', (user_id,))

    recent_games = cursor.fetchall()

    conn.close()

    return {
        'general': general_stats,
        'categories': category_stats,
        'recent_games': recent_games
    }


def add_category(name, description):
    """Adds a new category to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Categories (name, description)
    VALUES (?, ?)
    ''', (name, description))

    category_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return category_id


def update_category(category_id, name, description):
    """Updates an existing category"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE Categories
    SET name = ?, description = ?
    WHERE category_id = ?
    ''', (name, description, category_id))

    conn.commit()
    conn.close()

    return cursor.rowcount > 0


def delete_category(category_id):
    """Deletes a category and its associated questions"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # First delete associated answers
    cursor.execute('''
    DELETE FROM Answers 
    WHERE question_id IN (SELECT question_id FROM Questions WHERE category_id = ?)
    ''', (category_id,))

    # Then delete the questions
    cursor.execute('''
    DELETE FROM Questions
    WHERE category_id = ?
    ''', (category_id,))

    # Finally delete the category
    cursor.execute('''
    DELETE FROM Categories
    WHERE category_id = ?
    ''', (category_id,))

    conn.commit()
    conn.close()

    return cursor.rowcount > 0


def add_question(category_id, question_text, time_limit, difficulty_level, answers):
    """
    Adds a new question with its answers

    Args:
        category_id: ID of the category
        question_text: Text of the question
        time_limit: Time limit in seconds
        difficulty_level: Difficulty level (1.0-2.0)
        answers: List of tuples (answer_text, is_correct)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Add the question
    cursor.execute('''
    INSERT INTO Questions (category_id, question_text, time_limit, difficulty_level)
    VALUES (?, ?, ?, ?)
    ''', (category_id, question_text, time_limit, difficulty_level))

    question_id = cursor.lastrowid

    # Add the answers
    for answer_text, is_correct in answers:
        cursor.execute('''
        INSERT INTO Answers (question_id, answer_text, is_correct)
        VALUES (?, ?, ?)
        ''', (question_id, answer_text, 1 if is_correct else 0))

    conn.commit()
    conn.close()

    return question_id


def update_question(question_id, question_text, time_limit, difficulty_level):
    """Updates an existing question"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE Questions
    SET question_text = ?, time_limit = ?, difficulty_level = ?
    WHERE question_id = ?
    ''', (question_text, time_limit, difficulty_level, question_id))

    conn.commit()
    conn.close()

    return cursor.rowcount > 0


def update_answer(answer_id, answer_text, is_correct):
    """Updates an existing answer"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE Answers
    SET answer_text = ?, is_correct = ?
    WHERE answer_id = ?
    ''', (answer_text, 1 if is_correct else 0, answer_id))

    conn.commit()
    conn.close()

    return cursor.rowcount > 0


def delete_question(question_id):
    """Deletes a question and its associated answers"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # First delete the answers
    cursor.execute('''
    DELETE FROM Answers
    WHERE question_id = ?
    ''', (question_id,))

    # Then delete the question
    cursor.execute('''
    DELETE FROM Questions
    WHERE question_id = ?
    ''', (question_id,))

    conn.commit()
    conn.close()

    return cursor.rowcount > 0