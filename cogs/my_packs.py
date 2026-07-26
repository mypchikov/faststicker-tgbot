from html import escape

import cog


class Handler(cog.Cog):
    def __init__(self, bot: cog.Bot):
        super().__init__(bot)

    @cog.regMessage(cog.F.text == "/my_packs")
    async def my_packs_command(self, message: cog.Message, state: cog.FSMContext):
        await state.clear()
        userpacks = await self.bot.dbm.readStickerpacks(tgId=message.from_user.id)
        if not userpacks:
            await message.reply(
                "You don't have any stickerpacks created with this bot!\nCreate one with /new_pack command!"
            )
            return

        stickerpacks_formatted = []
        bot_username = (await self.bot.get_me()).username

        for stickerpack in userpacks:
            full_pack_name = stickerpack.packName + "_by_" + bot_username
            try:
                tg_stickerset = await self.bot.get_sticker_set(name=full_pack_name)
            except Exception:
                await self.bot.dbm.deleteStickerpacks(
                    tgId=message.from_user.id, packName=stickerpack.packName
                )
                continue

            stickerpacks_formatted.append(
                f'<a href="https://t.me/addstickers/{full_pack_name}">'
                f"<b>{escape(stickerpack.packTitle)}</b></a>\n"
                f"{len(tg_stickerset.stickers)}/120 stickers"
            )

        if not stickerpacks_formatted:
            await message.answer(
                "You don't have any sticker packs created with this bot."
            )
            return

        await message.answer(f"""Your sticker packs:

{"\n\n".join(stickerpacks_formatted)}""")


def setup(bot: cog.Bot):
    Handler(bot=bot).register()
