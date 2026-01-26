from aiogram.types import Message


async def topics_command(message: Message, user_state: dict[int, str]):
    user_state[message.from_user.id] = "topics"

    await message.answer(
        "📘 Задание 2: Отчёт по темам занятия\n\n"
        "Бот ожидает Excel-файл (.xlsx).\n"
        "После отправки файла я проверю формат тем:\n"
        "«Урок № _. Тема: _»"
    )
