from aiogram.types import Message

async def attendance_command(message: Message, user_state: dict[int, str]):
    user_state[message.from_user.id] = "attendance"
    await message.answer(
        "📊 Посещаемость преподавателей < 40%\n"
        "✅ Отправьте Excel-файл."
    )
