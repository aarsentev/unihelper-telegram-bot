from aiogram import Router, F
from aiogram.types import Message
from bot.utils.hashing import sha256_hex
from bot.stats.stats import stats

router = Router()


def get_file_type_info(message: Message, file) -> tuple[str, str]:
    if message.photo:
        return "🖼️", "Изображение"
    elif message.video:
        return "🎬", "Видео"
    elif message.audio:
        return "🎵", "Аудио"
    elif message.voice:
        return "🎤", "Голосовое сообщение"
    elif message.document:
        mime_type = getattr(file, "mime_type", "")
        filename = getattr(file, "file_name", "")

        if mime_type:
            if mime_type.startswith("image/"):
                return "🖼️", "Изображение"
            elif mime_type.startswith("video/"):
                return "🎬", "Видео"
            elif mime_type.startswith("audio/"):
                return "🎵", "Аудио"
            elif "spreadsheet" in mime_type or "excel" in mime_type:
                return "📊", "Таблица"
            elif "zip" in mime_type or "archive" in mime_type or "compressed" in mime_type:
                return "🗜️", "Архив"

        if filename:
            ext = filename.lower().split(".")[-1] if "." in filename else ""
            if ext in ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp"]:
                return "🖼️", "Изображение"
            elif ext in ["mp4", "avi", "mov", "mkv", "webm"]:
                return "🎬", "Видео"
            elif ext in ["mp3", "wav", "flac", "ogg", "m4a"]:
                return "🎵", "Аудио"
            elif ext in ["xls", "xlsx", "csv"]:
                return "📊", "Таблица"
            elif ext in ["zip", "rar", "7z", "tar", "gz"]:
                return "🗜️", "Архив"
            elif ext in ["py", "js", "ts", "java", "cpp", "c", "go", "rs"]:
                return "💻", "Скрипт"
        
        return "📄", "Документ"
    
    return "📎", "Файл"


@router.message(F.document | F.photo | F.video | F.audio | F.voice)
async def fileinfo(message: Message):
    stats.seen_user(message.from_user.id)
    stats.bump("fileinfo")

    file = message.document or getattr(message, "photo", [None])[-1] or message.video or message.audio or message.voice
    if not file:
        await message.answer("Пришлите файл.")
        return

    emoji, file_type = get_file_type_info(message, file)
    filename = getattr(file, "file_name", "")

    extension = ""
    if filename and "." in filename:
        extension = filename.split(".")[-1].upper()
    
    tg_file = await message.bot.get_file(file.file_id)
    stream = await message.bot.download_file(tg_file.file_path)
    chunks = iter(lambda: stream.read(65536), b"")
    digest = sha256_hex(chunks)
    size = getattr(file, "file_size", 0)

    if size < 1024:
        size_str = f"{size} байт"
    elif size < 1024 * 1024:
        size_str = f"{size / 1024:.1f} КБ"
    else:
        size_str = f"{size / (1024 * 1024):.1f} МБ"
    
    response_lines = [
        f"{emoji} {file_type}" + (f" ({extension})" if extension else ""),
    ]
    if filename:
        response_lines.append(f"📝 {filename}")
    response_lines.extend([
        f"📦 {size_str}",
        f"🔐 {digest}"
    ])
    
    await message.answer("\n".join(response_lines))
