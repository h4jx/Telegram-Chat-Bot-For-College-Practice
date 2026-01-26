from aiogram.types import Message

TG_MAX = 4096
SAFE_MAX = 3800


def split_text(text: str, chunk_size: int = SAFE_MAX) -> list[str]:
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for line in text.splitlines(True):
        if len(line) > chunk_size:
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

    return [c[:TG_MAX] for c in chunks if c]


async def send_long_message(message: Message, text: str):
    parts = split_text(text)
    for i, part in enumerate(parts, start=1):
        await message.answer(part)

