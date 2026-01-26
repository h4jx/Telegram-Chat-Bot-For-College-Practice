import openpyxl

from reports.topics_format_report import TopicsFormatReport
from reports.schedule_count_report import ScheduleCountReport


class ReportService:
    def __init__(self):
        self._reports = {
            "topics": TopicsFormatReport(),
            "schedule": ScheduleCountReport(),  # пока заглушка, но режим уже есть
        }

    def build(self, key: str, wb: openpyxl.Workbook) -> str:
        report = self._reports.get(key)
        if not report:
            return "Неизвестный тип отчёта."
        return report.build(wb)
