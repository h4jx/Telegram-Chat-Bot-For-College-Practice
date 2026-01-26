import openpyxl


class BaseReport:
    key: str = "base"
    title: str = "Base report"

    def build(self, wb: openpyxl.Workbook) -> str:
        raise NotImplementedError
