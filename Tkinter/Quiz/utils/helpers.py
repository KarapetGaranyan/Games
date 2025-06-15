import tkinter as tk
from tkinter import messagebox
import time
import random
import string
import os
from PIL import Image, ImageTk


def show_info(title, message):
    """
    Показывает информационное сообщение

    Args:
        title (str): Заголовок сообщения
        message (str): Текст сообщения
    """
    messagebox.showinfo(title, message)


def show_error(title, message):
    """
    Показывает сообщение об ошибке

    Args:
        title (str): Заголовок сообщения
        message (str): Текст сообщения
    """
    messagebox.showerror(title, message)


def show_warning(title, message):
    """
    Показывает предупреждение

    Args:
        title (str): Заголовок сообщения
        message (str): Текст сообщения
    """
    messagebox.showwarning(title, message)


def confirm_action(title, message):
    """
    Запрашивает подтверждение действия

    Args:
        title (str): Заголовок сообщения
        message (str): Текст сообщения

    Returns:
        bool: True, если пользователь подтвердил действие, иначе False
    """
    return messagebox.askyesno(title, message)


def format_time(seconds):
    """
    Форматирует время в секундах в формат MM:SS

    Args:
        seconds (int): Время в секундах

    Returns:
        str: Отформатированное время
    """
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"


def generate_random_id(length=8):
    """
    Генерирует случайный идентификатор

    Args:
        length (int, optional): Длина идентификатора. По умолчанию 8.

    Returns:
        str: Случайный идентификатор
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def load_image(path, size=None):
    """
    Загружает и при необходимости изменяет размер изображения

    Args:
        path (str): Путь к изображению
        size (tuple, optional): Размер изображения (ширина, высота)

    Returns:
        PhotoImage: Объект изображения для Tkinter
    """
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка при загрузке изображения {path}: {e}")
        # Создаем пустое изображение нужного размера
        if size:
            img = Image.new('RGB', size, color='gray')
        else:
            img = Image.new('RGB', (100, 100), color='gray')
        return ImageTk.PhotoImage(img)


def create_rounded_frame(parent, width, height, bg_color="#ffffff", corner_radius=10):
    """
    Создает скругленный фрейм с помощью Canvas

    Args:
        parent: Родительский виджет
        width (int): Ширина фрейма
        height (int): Высота фрейма
        bg_color (str, optional): Цвет фона. По умолчанию "#ffffff".
        corner_radius (int, optional): Радиус скругления углов. По умолчанию 10.

    Returns:
        Canvas: Созданный объект Canvas
    """
    canvas = tk.Canvas(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)

    # Создаем скругленный прямоугольник
    canvas.create_round_rectangle = lambda x1, y1, x2, y2, radius=corner_radius, **kwargs: \
        canvas.create_polygon(
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            smooth=True, **kwargs)

    canvas.create_round_rectangle(0, 0, width, height, fill=bg_color, outline="")

    return canvas