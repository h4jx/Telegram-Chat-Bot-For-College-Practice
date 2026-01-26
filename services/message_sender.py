from aiogram.types import Message

TG_MAX = 4096
SAFE_MAX = 3800  # запас под эмодзи/служебные символы


def split_text(text: str, chunk_size: int = SAFE_MAX) -> list[str]:
    """
    Делит текст на куски <= chunk_size, стараясь резать по переносам строк.
    """
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for line in text.splitlines(True):  # True сохраняет \n
        if len(line) > chunk_size:
            # очень длинная строка — режем тупо по кускам
            if current:
                chunks.append("".join(current).strip())
                current, current_len = [], 0
            for i in range(0, len(line), chunk_size):
                chunks.append(line[i:i + chunk_size].strip())
            continue

        if current_len + len(line) > chunk_size:
            chunks.append("".join(current).strip())
            current, current_len = [], 0

        current.append(line)
        current_len += len(line)

    if current:
        chunks.append("".join(current).strip())

    # финальная защита
    return [c[:TG_MAX] for c in chunks if c]


async def send_long_message(message: Message, text: str):
    parts = split_text(text)
    for i, part in enumerate(parts, start=1):
        # Можно добавлять номер части, если хочешь:
        # await message.answer(f"({i}/{len(parts)})\n{part}")
        await message.answer(part)
