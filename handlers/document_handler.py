from aiogram import Bot
from aiogram.types import Message

from services.excel_loader import ExcelLoader
from services.report_service import ReportService
from services.message_sender import send_long_message


class DocumentHandler:
    def __init__(self, loader: ExcelLoader, reports: ReportService, user_state: dict[int, str]):
        self.loader = loader
        self.reports = reports
        self.user_state = user_state

    async def handle(self, message: Message, bot: Bot):
        mode = self.user_state.get(message.from_user.id)

        if not mode:
            await message.answer(
                "❗ Сначала выберите задание:\n"
                "• /schedule — отчёт по расписанию\n"
                "• /topics — отчёт по темам занятия"
            )
            return

        try:
            wb = await self.loader.load_workbook_from_message(message, bot)
            result = self.reports.build(mode, wb)

            # сброс режима после успешной обработки
            self.user_state.pop(message.from_user.id, None)

            await send_long_message(message, result)

        except Exception as e:
            await message.answer(f"❌ Ошибка обработки файла: {e}")
