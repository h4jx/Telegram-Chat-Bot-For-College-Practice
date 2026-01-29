from aiogram.types import Message


async def students_command(message: Message, user_state: dict[int, str]):
    user_state[message.from_user.id] = "students"

    await message.answer(
        "👩‍🎓 Отчёт по студентам\n\n"
        "Условия:\n"
        "• ДЗ1 = 1\n"
        "• классная работа < 3\n\n"
        "✅ Отправьте Excel-файл (.xlsx)"
    )
