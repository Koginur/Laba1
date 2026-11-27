"""
Модуль системної діагностики інженерного середовища Python.
Освітній компонент: Програмування на Python.
Спеціальність: F7 Комп'ютерна інженерія.
Індивідуальне завдання (Варіант 4): Ліміти рекурсії та пам'яті.
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
        "os_name": platform.system(),
        "os_release": platform.release(),
        "os_architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_compiler": platform.python_compiler(),
        "byte_order": sys.byteorder,
        "interpreter_path": sys.executable,
        "active_conda_env": os.environ.get("CONDA_DEFAULT_ENV", "None (Global/Non-Conda)"),
        "recursion_limit": sys.getrecursionlimit(),
        "thread_switch_interval": sys.getswitchinterval(),
    }
    return system_info


def calculate_memory_footprint() -> dict:
    """
    Обчислює фізичний розмір базових скалярних та складених
    структур даних у байтах за допомогою функції sys.getsizeof.
    """
    # Створення тестових екземплярів різних типів даних
    sample_int_zero = 0
    sample_int_large = 2**64
    sample_float = 3.141592653589793
    sample_complex = 1.0 + 2.0j
    sample_bool = True
    sample_none = None
    sample_str_empty = ""
    sample_str_ascii = "Computer Engineering"
    sample_list_empty = []
    sample_tuple_empty = ()
    sample_dict_empty = {}
    sample_set_empty = set()

    # Формування словника розмірів об'єктів у байтах
    sizes = {
        "int (0)": sys.getsizeof(sample_int_zero),
        "int (2^64)": sys.getsizeof(sample_int_large),
        "float": sys.getsizeof(sample_float),
        "complex": sys.getsizeof(sample_complex),
        "bool": sys.getsizeof(sample_bool),
        "NoneType": sys.getsizeof(sample_none),
        "str (empty)": sys.getsizeof(sample_str_empty),
        "str (ASCII, len=20)": sys.getsizeof(sample_str_ascii),
        "list (empty)": sys.getsizeof(sample_list_empty),
        "tuple (empty)": sys.getsizeof(sample_tuple_empty),
        "dict (empty)": sys.getsizeof(sample_dict_empty),
        "set (empty)": sys.getsizeof(sample_set_empty),
    }
    return sizes


def verify_integer_cache() -> list:
    """
    Здійснює експериментальну верифікацію роботи механізму
    Small Integer Cache для інтервалу [-5, 256] та чисел поза ним.
    """
    cache_results = []
    test_integers = [-5, 0, 100, 256, 257, 1000]

    for val in test_integers:
        # Створення двох незалежних змінних через обчислення
        int_a = int(str(val))
        int_b = int(str(val))
        is_identical = int_a is int_b
        cache_results.append(
            {
                "value": val,
                "id_a": id(int_a),
                "id_b": id(int_b),
                "is_same_object": is_identical,
            }
        )
    return cache_results


# Аудит лімітів рекурсії та накладних витрат скалярів у купі
def audit_recursion_and_scalar_overhead() -> dict:
    """
    Варіант 4: Аудит лімітів рекурсії та визначення накладних витрат
    скалярних типів int та float у купі CPython.
    """
    # Поточний ліміт глибини стека викликів (кадрів рекурсії)
    recursion_limit = sys.getrecursionlimit()

    # Еталонні зразки int різної розрядності та float (IEEE 754 double)
    int_samples = [
        ("int (0)", 0),
        ("int (1)", 1),
        ("int (2^30 - 1)", 2**30 - 1),
        ("int (2^30)", 2**30),
        ("int (2^64)", 2**64),
        ("int (2^128)", 2**128),
    ]
    float_samples = [
        ("float (0.0)", 0.0),
        ("float (pi)", 3.141592653589793),
        ("float (max)", sys.float_info.max),
    ]

    scalar_rows = []

    # Аналіз цілочисельних об'єктів: базовим корисним розміром вважаємо min 4 байти (C int32)
    for label, value in int_samples:
        heap_bytes = sys.getsizeof(value)
        payload_bytes = max(4, (abs(value).bit_length() + 7) // 8)
        overhead_bytes = heap_bytes - payload_bytes
        overhead_ratio = heap_bytes / payload_bytes
        scalar_rows.append(
            {
                "label": label,
                "heap_bytes": heap_bytes,
                "payload_bytes": payload_bytes,
                "overhead_bytes": overhead_bytes,
                "overhead_ratio": overhead_ratio,
            }
        )

    # Аналіз чисел з рухомою комою: у CPython завжди обгортка над IEEE 754 double (8 байтів)
    for label, value in float_samples:
        heap_bytes = sys.getsizeof(value)
        payload_bytes = 8
        overhead_bytes = heap_bytes - payload_bytes
        overhead_ratio = heap_bytes / payload_bytes
        scalar_rows.append(
            {
                "label": label,
                "heap_bytes": heap_bytes,
                "payload_bytes": payload_bytes,
                "overhead_bytes": overhead_bytes,
                "overhead_ratio": overhead_ratio,
            }
        )

    return {
        "recursion_limit": recursion_limit,
        "int_bits_per_digit": sys.int_info.bits_per_digit,
        "int_sizeof_digit": sys.int_info.sizeof_digit,
        "float_mant_dig": sys.float_info.mant_dig,
        "scalar_rows": scalar_rows,
    }


def print_formatted_report() -> None:
    """
    Виводить на екран консолі комплексну діагностичну таблицю
    з використанням сучасних специфікаторів форматування f-strings.
    """
    meta = collect_environment_metadata()
    memory = calculate_memory_footprint()
    cache_data = verify_integer_cache()
    variant4_data = audit_recursion_and_scalar_overhead()

    separator = "=" * 80
    sub_separator = "-" * 80

    print(separator)
    print(f"{'ЗВІТ СИСТЕМНОЇ ДІАГНОСТИКИ СЕРЕДОВИЩА PYTHON':^80}")
    print(separator)

    # Виведення метаданих платформи
    print(f"Операційна система:      {meta['os_name']} {meta['os_release']} ({meta['os_architecture']})")
    print(f"Апаратний процесор:      {meta['processor']}")
    print(f"Версія інтерпретатора:   {meta['python_version']} ({meta['python_implementation']})")
    print(f"Компілятор ядра CPython: {meta['python_compiler']}")
    print(f"Порядок байтів системи:  {meta['byte_order'].upper()}-ENDIAN")
    print(f"Активоване Conda-env:    {meta['active_conda_env']}")
    print(f"Шлях до інтерпретатора:  {meta['interpreter_path']}")
    print(f"Ліміт глибини рекурсії:  {meta['recursion_limit']} кадрів")
    print(f"Квант перемикання GIL:   {meta['thread_switch_interval']} с")

    print(sub_separator)
    print(f"{'ПРОСТОРОВІ НАКЛАДНІ ВИТРАТИ СТРУКТУР ДАНИХ (CPython 64-bit)':^80}")
    print(sub_separator)
    print(f"| {'Тип даних та стан':<30} | {'Розмір у пам`яті (Байти)':<43} |")
    print(sub_separator)
    for type_name, size_bytes in memory.items():
        print(f"| {type_name:<30} | {size_bytes:<43} |")

    print(sub_separator)
    print(f"{'ВЕРИФІКАЦІЯ МЕХАНІЗМУ SMALL INTEGER CACHE':^80}")
    print(sub_separator)
    print(f"| {'Число':<8} | {'Адреса id(a)':<18} | {'Адреса id(b)':<18} | {'a is b':<12} | {'Статус пулу':<10} |")
    print(sub_separator)
    for row in cache_data:
        pool_status = "КЕШОВАНЕ" if row["is_same_object"] else "ДИНАМІЧНЕ"
        print(
            f"| {row['value']:<8} | {row['id_a']:<18} | {row['id_b']:<18} | {str(row['is_same_object']):<12} | {pool_status:<10} |"
        )

    print(sub_separator)
    print(f"{'АУДИТ ЛІМІТІВ РЕКУРСІЇ ТА НАКЛАДНИХ ВИТРАТ СКАЛЯРІВ (ВАРІАНТ 4)':^80}")
    print(sub_separator)
    print(f"Ліміт рекурсії sys.getrecursionlimit():  {variant4_data['recursion_limit']} кадрів")
    print(
        f"Параметри int (sys.int_info):            {variant4_data['int_bits_per_digit']} біт/розряд "
        f"({variant4_data['int_sizeof_digit']} Б)"
    )
    print(f"Точність мантиси float (IEEE 754):       {variant4_data['float_mant_dig']} біт")
    print(sub_separator)
    print(
        f"| {'Об`єкт (тип і значення)':<25} | {'Купа (Б)':<8} | {'Дані (Б)':<8} | {'Накладні (Б)':<12} | {'Коеф.':<7} |"
    )
    print(sub_separator)
    for item in variant4_data["scalar_rows"]:
        print(
            f"| {item['label']:<25} | {item['heap_bytes']:<8} | "
            f"{item['payload_bytes']:<8} | {item['overhead_bytes']:<12} | {item['overhead_ratio']:<6.2f}x |"
        )
    print(separator)


if __name__ == "__main__":
    t_start = time.perf_counter()
    print_formatted_report()
    t_elapsed = time.perf_counter() - t_start
    print(f"Час повної діагностики середовища: {t_elapsed * 1000:.4f} мс\n")