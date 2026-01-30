import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart

from config import BOT_TOKEN
from handlers.start_command import start_command
from handlers.document_handler import DocumentHandler
from services.excel_loader import ExcelLoader
from services.report_service import ReportService

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    user_state: dict[int, str] = {}

    loader = ExcelLoader()
    reports = ReportService()
    doc_handler = DocumentHandler(loader=loader, reports=reports, user_state=user_state)

    # /start
    dp.message.register(start_command, CommandStart())

    # команды
    mode_handlers = ModeHandlers(user_state)
    dp.message.register(mode_handlers.topics, Command("topics"))
    dp.message.register(mode_handlers.schedule, Command("schedule"))
    dp.message.register(mode_handlers.students, Command("students"))
    dp.message.register(mode_handlers.attendance, Command("attendance"))

    # загрузка Excel
    dp.message.register(doc_handler.handle, F.document)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

