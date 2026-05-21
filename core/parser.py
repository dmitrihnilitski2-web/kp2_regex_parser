import os
import re
from core.models import Law, Article, Part, Point
from core.validator import Validator


class RegexEngine:
    def __init__(self, validator: Validator):
        self.validator = validator

        self.re_section = re.compile(
            r"(?i)^[РP]озділ\s+([IVXLCDM]+)\.?\s*(.*)$")
        self.re_chapter = re.compile(r"(?i)^[ГG]лава\s+(\d+)\.?\s*(.*)$")
        self.re_article = re.compile(r"(?i)^[СC]таття\s+(\d+)\.?\s*(.*)$")

        self.re_part = re.compile(r"^(\d+)\.\s*(.*)$")
        self.re_point = re.compile(r"^(\d+)\)\s*(.*)$")
        self.re_subpoint = re.compile(r"^([а-яґєії])\)\s*(.*)$")

    def parse_file(self, filepath: str) -> Law:
        filename = os.path.basename(filepath)
        law = Law(title=filename)

        current_section = ""
        current_chapter = ""
        current_article = None
        current_part = None
        current_point = None

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                match = self.re_section.match(line)
                if match:
                    current_section = f"Розділ {match.group(1)}. {match.group(2)}".strip(
                    )
                    self.validator.sections_count += 1
                    continue

                match = self.re_chapter.match(line)
                if match:
                    current_chapter = f"Глава {match.group(1)}. {match.group(2)}".strip(
                    )
                    continue

                match = self.re_article.match(line)
                if match:

                    if current_article:
                        self.validator.check_empty_node(current_article)

                    art_num = int(match.group(1))
                    art_title = match.group(2).strip()

                    self.validator.check_article_sequence(art_num)

                    current_article = Article(
                        number=art_num,
                        title=art_title,
                        section=current_section,
                        chapter=current_chapter
                    )
                    law.articles.append(current_article)
                    current_part = None
                    current_point = None
                    continue

                if current_article:
                    match_part = self.re_part.match(line)
                    match_point = self.re_point.match(line)
                    match_subpoint = self.re_subpoint.match(line)

                    if match_part:
                        current_part = Part(number=match_part.group(
                            1), text=match_part.group(2).strip())
                        current_article.parts.append(current_part)
                        current_point = None
                    elif match_point:
                        current_point = Point(number=match_point.group(
                            1) + ")", text=match_point.group(2).strip())
                        if not current_part:
                            current_part = Part(number=None, text="")
                            current_article.parts.append(current_part)
                        current_part.points.append(current_point)
                    elif match_subpoint:
                        if not current_point:
                            if not current_part:
                                current_part = Part(number=None, text="")
                                current_article.parts.append(current_part)
                            current_point = Point(number="", text="")
                            current_part.points.append(current_point)
                        current_point.subpoints.append(line)
                    else:
                        self.validator.log_unparsed(line)
                        if current_point:
                            if current_point.subpoints:
                                current_point.subpoints[-1] += " " + line
                            else:
                                current_point.text += " " + line
                        elif current_part:
                            current_part.text += " " + line
                        else:
                            current_part = Part(number=None, text=line)
                            current_article.parts.append(current_part)
                else:

                    self.validator.log_unparsed(
                        f"[Преамбула/Поза статтею] {line}")

        if current_article:
            self.validator.check_empty_node(current_article)

        return law
