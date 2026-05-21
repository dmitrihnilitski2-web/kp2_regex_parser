import os
from core.validator import Validator
from core.parser import RegexEngine
from core.storage import Storage
from core.search import SearchEngine


def run_cli():
    storage = Storage()
    search_engine = SearchEngine()

    while True:
        print("\nПарсер нормативних актів (regex engine)")
        print("1. Обробити папку з текстовими файлами (Масовий парсинг)")
        print("2. Пошук за номером статті")
        print("3. Пошук за ключовим словом")
        print("4. Вихід")

        choice = input("Оберіть дію (1-4): ").strip()

        if choice == '4':
            print("Завершення роботи...")
            break

        elif choice == '1':

            directory = input(
                "Введіть шлях до папки з txt-файлами (натисніть Enter для 'data/input/'): ").strip()
            if not directory:
                directory = os.path.join("data", "input")

            if not os.path.exists(directory):
                print(f"Помилка: Папку '{directory}' не знайдено.")
                print("Створіть її та додайте туди текстові файли законів.")
                continue

            files = [f for f in os.listdir(directory) if f.endswith('.txt')]
            if not files:
                print(f"У папці '{directory}' немає .txt файлів для обробки.")
                continue

            print(
                f"\nЗнайдено файлів: {len(files)}. Починаю масовий парсинг та валідацію...")

            validator = Validator()
            parser = RegexEngine(validator)

            for filename in files:
                filepath = os.path.join(directory, filename)
                print(f"  Обробка: {filename}...")

                validator.last_article_num = 0

                law_ast = parser.parse_file(filepath)
                storage.append_law(law_ast)

            validator.print_summary()

        elif choice == '2':
            num_str = input("Введіть номер статті (тільки цифра): ").strip()
            if num_str.isdigit():
                search_engine.search_by_number(int(num_str))
            else:
                print("Помилка: Номер статті має бути числом.")

        elif choice == '3':
            keyword = input("Введіть слово або фразу для пошуку: ").strip()
            if keyword:
                search_engine.search_by_keyword(keyword)
            else:
                print("Помилка: Пошуковий запит не може бути порожнім.")
        else:
            print("Невірний вибір. Будь ласка, введіть число від 1 до 4.")
