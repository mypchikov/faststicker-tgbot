from html import escape


async def source_message_link(message, bot) -> str:
    if message.chat.username:
        return f"https://t.me/{message.chat.username}/{message.message_id}"

    chat_type = getattr(message.chat.type, "value", message.chat.type)
    if chat_type in {"group", "supergroup", "channel"}:
        chat_id = str(message.chat.id)
        if chat_id.startswith("-100"):
            return f"https://t.me/c/{chat_id[4:]}/{message.message_id}"

    bot_id = (await bot.get_me()).id
    return f"tg://openmessage?user_id={bot_id}&message_id={message.message_id}"


async def undo_last(message, state) -> None:
    data = await state.get_data()
    stickers = data.get("stickers", [])

    if not stickers:
        await message.answer("The queue is empty.")
        return

    stickers.pop()
    await state.update_data(stickers=stickers)
    await message.answer(f"Last sticker removed. Stickers in queue: {len(stickers)}.")


async def view_queue(message, state) -> None:
    stickers = (await state.get_data()).get("stickers", [])

    if not stickers:
        await message.answer("The queue is empty.")
        return

    lines = []
    for index, sticker in enumerate(stickers, start=1):
        emojis = escape("".join(sticker["emojis"]))
        source_link = escape(sticker.get("source_link", ""), quote=True)
        source = (
            f'<a href="{source_link}">source message</a>'
            if source_link
            else "source message unavailable"
        )
        lines.append(f"{index}. {source} — {emojis}")

    await message.answer("Stickers in queue:\n\n" + "\n".join(lines))
