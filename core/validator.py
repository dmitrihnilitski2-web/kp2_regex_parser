import os


class Validator:
    def __init__(self, log_path="data/logs/unparsed.log"):
        self.log_path = log_path
        self.last_article_num = 0
        self.gaps_found = 0
        self.sections_count = 0
        self.articles_count = 0
        self.empty_nodes = 0

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        with open(self.log_path, 'w', encoding='utf-8') as f:
            f.write("--- Звіт про нерозпізнані фрагменти ---\n")

    def check_article_sequence(self, current_num: int):
        """Контроль послідовності: перевіряє, чи не пропущено статтю."""
        if self.last_article_num != 0 and current_num != self.last_article_num + 1:
            print(
                f"Валідація: Можливий розрив нумерації! Після статті {self.last_article_num} йде {current_num}.")
            self.gaps_found += 1
        self.last_article_num = current_num
        self.articles_count += 1

    def check_empty_node(self, article):
        """Перевірка на «порожні» вузли."""
        if article and not article.content:
            print(
                f"Валідація: Стаття {article.number} '{article.title}' не містить тексту (порожній вузол)!")
            self.empty_nodes += 1

    def log_unparsed(self, text: str):
        """Записує рядки, які не підпали під стандартні патерни норм."""
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(text + "\n")

    def print_summary(self):
        """Виводить фінальну статистику імпорту."""
        print("\nСтатистика імпорту")
        print(
            f"Оброблено {self.sections_count} Розділів, {self.articles_count} Статей.")
        print(f"Знайдено {self.gaps_found} розривів у нумерації.")
        print(f"Знайдено {self.empty_nodes} порожніх статей.")
        print(f"Нестандартні рядки збережено у {self.log_path}")
        print()
