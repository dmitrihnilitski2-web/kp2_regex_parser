import json
import os
from typing import List
from core.models import Law


class Storage:
    def __init__(self, db_path="data/output/database.json"):
        self.db_path = db_path

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def save_laws(self, laws: List[Law]):
        """Зберігає одразу масив законів у JSON-файл (перезаписує базу)."""
        data = {"laws": [law.to_dict() for law in laws]}
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(
            f"✅ Базу даних успішно збережено у {self.db_path} (законів у базі: {len(laws)})")

    def append_law(self, law: Law):
        """Додає один закон до існуючої бази даних або оновлює його, якщо він вже є."""
        db = self.load_db()

        if "laws" not in db:
            db["laws"] = []

        existing_law_titles = [l.get("law_title") for l in db["laws"]]
        if law.title in existing_law_titles:
            db["laws"] = [l for l in db["laws"]
                          if l.get("law_title") != law.title]

        db["laws"].append(law.to_dict())

        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)

    def load_db(self) -> dict:
        """Завантажує JSON базу даних."""
        if not os.path.exists(self.db_path):
            return {"laws": []}

        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:

            return {"laws": []}
