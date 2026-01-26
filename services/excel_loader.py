from io import BytesIO

import openpyxl
from aiogram import Bot
from aiogram.types import Message


class ExcelLoader:
    async def load_workbook_from_message(self, message: Message, bot: Bot) -> openpyxl.Workbook:
        if not message.document:
            raise ValueError("Нет документа в сообщении")

        name = (message.document.file_name or "").lower()
        if not name.endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
            raise ValueError("Нужен файл .xlsx/.xlsm (если у вас .xls — сохраните как .xlsx)")

        buf = BytesIO()
        await bot.download(message.document, destination=buf)
        buf.seek(0)

        return openpyxl.load_workbook(buf, data_only=True)

