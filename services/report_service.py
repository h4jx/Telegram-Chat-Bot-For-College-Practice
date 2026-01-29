import openpyxl

from reports.topics_format_report import TopicsFormatReport
from reports.schedule_count_report import ScheduleCountReport
from reports.students_report import StudentsRiskReport
from reports.teacher_attendance_report import TeacherAttendanceReport


class ReportService:
    def __init__(self):
        self._reports = {
            "topics": TopicsFormatReport(),
            "schedule": ScheduleCountReport(),
            "students": StudentsRiskReport(),
            "attendance": TeacherAttendanceReport(threshold_percent=40.0),
        }

    def build(self, key: str, wb: openpyxl.Workbook) -> str:
        report = self._reports.get(key)
        if not report:
            return "Неизвестный тип отчёта."
        return report.build(wb)
