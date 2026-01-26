import re
from dataclasses import dataclass
from typing import List

import openpyxl

from reports.base_report import BaseReport


@dataclass
class InvalidTopic:
    sheet: str
    cell: str
    value: str


class TopicsFormatReport(BaseReport):
    key = "topics"
    title = "Отчет по темам занятия"

    # Формат: “Урок № _. Тема: _”
    TOPIC_RE = re.compile(r"^\s*Урок\s*№\s*(\d+)\.\s*Тема:\s*(.+)\s*$", re.IGNORECASE)

    def __init__(self, max_items: int = 60, max_len: int = 200):
        self.max_items = max_items
        self.max_len = max_len

    def build(self, wb: openpyxl.Workbook) -> str:
        invalid: List[InvalidTopic] = []

        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=False):
                for cell in row:
                    val = cell.value
                    if val is None:
                        continue
                    if not isinstance(val, str):
                        continue

                    text = val.strip()
                    if not text:
                        continue

                    # чтобы не ругаться на любые строки, проверяем только те,
                    # которые хотя бы похожи на тему
                    looks_like_topic = ("урок" in text.lower()) or ("тема" in text.lower())
                    if looks_like_topic and not self.TOPIC_RE.match(text):
                        clipped = text if len(text) <= self.max_len else text[: self.max_len] + "…"
                        invalid.append(InvalidTopic(sheet=ws.title, cell=cell.coordinate, value=clipped))

        if not invalid:
            return "✅ Все темы соответствуют формату: «Урок № _. Тема: _»"

        lines = [
            "⚠️ Найдены темы НЕ по формату «Урок № _. Тема: _»:",
            ""
        ]

        shown = invalid[: self.max_items]
        for item in shown:
            lines.append(f"• Лист: {item.sheet} | Ячейка: {item.cell}")
            lines.append(f"  «{item.value}»")

        if len(invalid) > self.max_items:
            lines += ["", f"…и ещё {len(invalid) - self.max_items} строк(и)."]

        return "\n".join(lines)
