from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Point:
    number: str
    text: str
    subpoints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "number": self.number,
            "text": self.text,
            "subpoints": self.subpoints
        }


@dataclass
class Part:
    number: Optional[str]
    text: str
    points: List[Point] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "number": self.number,
            "text": self.text,
            "points": [p.to_dict() for p in self.points]
        }


@dataclass
class Article:
    number: int
    title: str
    section: str = ""
    chapter: str = ""
    parts: List[Part] = field(default_factory=list)

    @property
    def content(self):
        return self.parts

    def to_dict(self) -> Dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "section": self.section,
            "chapter": self.chapter,
            "parts": [part.to_dict() for part in self.parts]
        }


@dataclass
class Law:
    title: str
    articles: List[Article] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "law_title": self.title,
            "articles": [article.to_dict() for article in self.articles]
        }
