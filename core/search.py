from core.storage import Storage


class SearchEngine:
    def __init__(self):
        self.storage = Storage()

    def search_by_number(self, article_num: int):
        """Шукає повну статтю за її номером і виводить усю її ієрархію."""
        db = self.storage.load_db()
        laws = db.get("laws", [])
        if not laws:
            print("База даних порожня. Спочатку розпарсіть файли.")
            return

        found = False
        for law in laws:
            for art in law.get("articles", []):
                if art["number"] == article_num:
                    self._print_full_article(
                        law.get("law_title", "Невідомий закон"), art)
                    found = True

        if not found:
            print(
                f"Статтю з номером {article_num} не знайдено в жодному із законів бази.")

    def search_by_keyword(self, keyword: str):
        """
        Шукає ключове слово на всіх рівнях (Назва статті, Частина, Пункт, Підпункт)
        і виводить кожну знайдену норму як окремий ізольований запис.
        """
        db = self.storage.load_db()
        laws = db.get("laws", [])
        if not laws:
            print("База даних порожня. Спочатку розпарсіть файли.")
            return

        keyword_lower = keyword.lower()
        found_count = 0

        for law in laws:
            law_title = law.get("law_title", "Невідомий закон")
            for art in law.get("articles", []):

                section = art.get("section", "")
                chapter = art.get("chapter", "")
                art_info = f"Стаття {art['number']}. {art['title']}"

                if keyword_lower in art["title"].lower():
                    self._print_record(
                        law_title, section, chapter, art_info, "Назва статті", art["title"])
                    found_count += 1

                for part in art.get("parts", []):
                    if part["text"] and keyword_lower in part["text"].lower():
                        locator = f"Частина {part['number']}" if part[
                            'number'] else "Абзац (без номера)"
                        self._print_record(
                            law_title, section, chapter, art_info, locator, part["text"])
                        found_count += 1

                    for point in part.get("points", []):
                        if point["text"] and keyword_lower in point["text"].lower():
                            locator = f"Частина {part['number']} -> Пункт {point['number']}"
                            self._print_record(
                                law_title, section, chapter, art_info, locator, point["text"])
                            found_count += 1

                        for subpoint in point.get("subpoints", []):
                            if keyword_lower in subpoint.lower():
                                locator = f"Частина {part['number']} -> Пункт {point['number']} -> Підпункт"
                                self._print_record(
                                    law_title, section, chapter, art_info, locator, subpoint)
                                found_count += 1

        print(f"\nВсього знайдено окремих норм: {found_count}")

    def _print_record(self, law_title: str, section: str, chapter: str, article_info: str, locator: str, text: str):
        """
        Форматує єдину юридичну норму як окремий табличний/блоковий запис
        із збереженням усіх ієрархічних сутностей.
        """
        print(f"\nЗакон:    {law_title}")

        hierarchy = []
        if section:
            hierarchy.append(section)
        if chapter:
            hierarchy.append(chapter)
        if hierarchy:
            print(f"Ієрархія: {' | '.join(hierarchy)}")

        print(f"Сутність: {article_info}")
        print(f"Локація:  {locator}")
        print(f"Текст норми:\n{text.strip()}")

    def _print_full_article(self, law_title: str, art: dict):
        """
        Допоміжний метод для акуратного виводу всього дерева конкретної статті
        при пошуку за номером.
        """
        print(f"\nЗакон: {law_title}")
        if art.get("section"):
            print(f"{art['section']}")
        if art.get("chapter"):
            print(f"{art['chapter']}")
        print(f"Стаття {art['number']}. {art['title']}")

        for part in art.get("parts", []):
            if part["number"] or part["text"]:
                prefix = f"{part['number']} " if part["number"] else ""
                print(f"{prefix}{part['text']}")

            for point in part.get("points", []):
                print(f"  {point['number']} {point['text']}")
                for subpoint in point.get("subpoints", []):
                    print(f"    {subpoint}")
