import os
import shutil
from PIL import Image


class UserProfile:
    """Класс для управления профилем пользователя"""

    def __init__(self, db_manager):
        """
        Инициализирует менеджер профиля пользователя

        Args:
            db_manager: Экземпляр менеджера базы данных
        """
        self.db_manager = db_manager

        # Директория для хранения аватаров
        self.avatar_dir = os.path.join(os.path.dirname(__file__), "avatars")
        os.makedirs(self.avatar_dir, exist_ok=True)

    def create_user(self, username, avatar_path=None):
        """
        Создает нового пользователя

        Args:
            username (str): Имя пользователя
            avatar_path (str, optional): Путь к файлу аватара

        Returns:
            int: ID созданного пользователя
        """
        # Если передан аватар, копируем его в директорию аватаров
        if avatar_path and os.path.exists(avatar_path):
            # Генерируем имя файла аватара на основе имени пользователя
            avatar_filename = f"avatar_{username.replace(' ', '_').lower()}.png"
            new_avatar_path = os.path.join(self.avatar_dir, avatar_filename)

            # Изменяем размер и сохраняем аватар
            self.resize_and_save_avatar(avatar_path, new_avatar_path)
            avatar_path = new_avatar_path

        # Создаем пользователя в базе данных
        return self.db_manager.create_user(username, avatar_path)

    def get_user_info(self, user_id):
        """
        Получает информацию о пользователе

        Args:
            user_id (int): ID пользователя

        Returns:
            tuple: Информация о пользователе (id, username, avatar_path, date_created)
        """
        return self.db_manager.get_user_info(user_id)

    def update_profile(self, user_id, username, avatar_path=None):
        """
        Обновляет профиль пользователя

        Args:
            user_id (int): ID пользователя
            username (str): Новое имя пользователя
            avatar_path (str, optional): Путь к новому файлу аватара

        Returns:
            bool: True, если обновление успешно, иначе False
        """
        # Если передан новый аватар, обрабатываем его
        if avatar_path and os.path.exists(avatar_path):
            # Получаем текущий аватар пользователя
            user_info = self.get_user_info(user_id)
            if user_info:
                _, _, old_avatar_path, _ = user_info

                # Если старый аватар существует, удаляем его
                if old_avatar_path and os.path.exists(old_avatar_path):
                    try:
                        os.remove(old_avatar_path)
                    except Exception as e:
                        print(f"Ошибка при удалении старого аватара: {e}")

            # Генерируем имя файла для нового аватара
            avatar_filename = f"avatar_{user_id}.png"
            new_avatar_path = os.path.join(self.avatar_dir, avatar_filename)

            # Изменяем размер и сохраняем аватар
            self.resize_and_save_avatar(avatar_path, new_avatar_path)
            avatar_path = new_avatar_path

        # Обновляем профиль в базе данных
        self.db_manager.update_user_profile(user_id, username, avatar_path)
        return True

    def resize_and_save_avatar(self, source_path, destination_path, size=(150, 150)):
        """
        Изменяет размер и сохраняет аватар

        Args:
            source_path (str): Путь к исходному файлу
            destination_path (str): Путь для сохранения
            size (tuple, optional): Размер аватара (ширина, высота). По умолчанию (150, 150).
        """
        try:
            img = Image.open(source_path)
            img = img.resize(size, Image.LANCZOS)
            img.save(destination_path)
        except Exception as e:
            print(f"Ошибка при обработке аватара: {e}")

    def get_user_statistics(self, user_id):
        """
        Получает статистику пользователя

        Args:
            user_id (int): ID пользователя

        Returns:
            dict: Статистика пользователя
        """
        return self.db_manager.get_user_statistics(user_id)