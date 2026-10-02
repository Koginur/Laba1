"""
Модуль системної діагностики інженерного середовища Python.
Освітній компонент: Програмування на Python.
Спеціальність: F7 Комп'ютерна інженерія.
"""

import os
import platform
import sys
import time


def collect_environment_metadata() -> dict:
    """
    Здійснює агрегацію характеристик апаратної платформи,
    операційної системи та параметрів інтерпретатора CPython.
    """
    # Збір інформації про версію та архітектуру платформи
    system_info = {
        "recursion_limit": sys.getrecursionlimit(),
    }
    return system_info


def calculate_memory_footprint() -> dict:
    """
    Обчислює фізичний розмір базових скалярних та складених
    структур даних у байтах за допомогою функції sys.getsizeof.
    """
    # Створення тестових екземплярів різних типів даних
    sample_int_zero = 0
    sample_int_large = 2**128
    sample_float = 2.7182818284

    # Формування словника розмірів об'єктів у байтах
    sizes = {
        "int (0)": sys.getsizeof(sample_int_zero),
        "int (2^128)": sys.getsizeof(sample_int_large),
        "float": sys.getsizeof(sample_float)
    }
    return sizes


def print_formatted_report() -> None:
    """
    Виводить на екран консолі комплексну діагностичну таблицю
    з використанням сучасних специфікаторів форматування f-strings.
    """
    meta = collect_environment_metadata()
    memory = calculate_memory_footprint()

    separator = "=" * 80
    sub_separator = "-" * 80

    print(separator)
    print(f"{'ЗВІТ СИСТЕМНОЇ ДІАГНОСТИКИ СЕРЕДОВИЩА PYTHON':^80}")
    print(separator)

    # Виведення метаданих платформи
    print(f"Ліміт глибини рекурсії:  {meta['recursion_limit']} кадрів")

    print(sub_separator)
    print(f"{'ПРОСТОРОВІ НАКЛАДНІ ВИТРАТИ СТРУКТУР ДАНИХ (CPython 64-bit)':^80}")
    print(sub_separator)
    print(f"| {'Тип даних та стан':<30} | {'Розмір у пам`яті (Байти)':<43} |")
    print(sub_separator)
    for type_name, size_bytes in memory.items():
        print(f"| {type_name:<30} | {size_bytes:<43} |")

    print(sub_separator)
    print(separator)


if __name__ == "__main__":
    t_start = time.perf_counter()
    print_formatted_report()
    t_elapsed = time.perf_counter() - t_start
    print(f"Час повної діагностики середовища: {t_elapsed * 1000:.4f} мс\n")


