class GameSession:
    """Класс, представляющий игровую сессию"""

    def __init__(self, user_id, category_id):
        """Инициализирует новую игровую сессию"""
        self.user_id = user_id
        self.category_id = category_id
        self.total_points = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.current_question = None

    def calculate_points(self, is_correct, time_left, time_limit, difficulty):
        """
        Рассчитывает количество баллов за ответ

        Args:
            is_correct (bool): Правильный ли ответ
            time_left (int): Оставшееся время в секундах
            time_limit (int): Общее время на вопрос
            difficulty (float): Сложность вопроса (множитель)

        Returns:
            int: Количество баллов
        """
        if not is_correct:
            return 0

        # Базовые очки за правильный ответ
        base_points = 100

        # Бонус за скорость (до 50 очков)
        time_bonus = int((time_left / time_limit) * 50) if time_limit > 0 else 0

        # Применение множителя сложности
        return int((base_points + time_bonus) * difficulty)

    def answer_question(self, is_correct, time_left, time_limit, difficulty):
        """
        Обрабатывает ответ на вопрос

        Args:
            is_correct (bool): Правильный ли ответ
            time_left (int): Оставшееся время в секундах
            time_limit (int): Общее время на вопрос
            difficulty (float): Сложность вопроса

        Returns:
            int: Количество баллов за ответ
        """
        self.total_questions += 1

        if is_correct:
            self.correct_answers += 1
            points = self.calculate_points(True, time_left, time_limit, difficulty)
            self.total_points += points
            return points

        return 0

    def get_results(self):
        """
        Возвращает результаты игровой сессии

        Returns:
            dict: Словарь с результатами
        """
        return {
            'user_id': self.user_id,
            'category_id': self.category_id,
            'total_points': self.total_points,
            'correct_answers': self.correct_answers,
            'total_questions': self.total_questions,
            'accuracy': (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0
        }


class QuestionHandler:
    """Класс для обработки вопросов и ответов"""

    def __init__(self, db_manager):
        """
        Инициализирует обработчик вопросов

        Args:
            db_manager: Экземпляр менеджера базы данных
        """
        self.db_manager = db_manager

    def get_questions_for_category(self, category_id, limit=10):
        """
        Получает вопросы для категории

        Args:
            category_id (int): ID категории
            limit (int, optional): Максимальное количество вопросов. По умолчанию 10.

        Returns:
            list: Список вопросов
        """
        return self.db_manager.get_questions_for_category(category_id, limit)

    def get_answers_for_question(self, question_id):
        """
        Получает варианты ответов для вопроса

        Args:
            question_id (int): ID вопроса

        Returns:
            list: Список вариантов ответов
        """
        return self.db_manager.get_answers_for_question(question_id)

    def check_answer(self, answer_id, correct_answer_id):
        """
        Проверяет правильность ответа

        Args:
            answer_id (int): ID выбранного ответа
            correct_answer_id (int): ID правильного ответа

        Returns:
            bool: True, если ответ правильный, иначе False
        """
        return answer_id == correct_answer_id

    def get_correct_answer(self, answers):
        """
        Получает правильный ответ из списка вариантов

        Args:
            answers (list): Список вариантов ответов

        Returns:
            int: ID правильного ответа
        """
        for answer_id, _, _, is_correct in answers:
            if is_correct:
                return answer_id
        return None