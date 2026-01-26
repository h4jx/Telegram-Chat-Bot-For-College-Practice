from aiogram.types import Message


async def schedule_command(message: Message, user_state: dict[int, str]):
    user_state[message.from_user.id] = "schedule"

    await message.answer(
        "📅 Задание 1: Отчёт по выставленному расписанию\n\n"
        "Бот ожидает Excel-файл (.xlsx).\n"
        "После отправки файла будет выведено количество пар по каждой дисциплине."
    )
