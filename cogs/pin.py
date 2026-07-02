import cog


class Handler(cog.Cog):
    def __init__(self, bot: cog.Bot):
        super().__init__(bot)

    @cog.regMessage(cog.F.text)
    async def pinstickersetlink(self, message: cog.Message, state: cog.FSMContext):
        if message.text:
            if message.text.startswith("https://t.me/addstickers/"):
                await message.pin()

    @cog.regMessage(cog.F.sticker)
    async def pinsticker(self, message: cog.Message, state: cog.FSMContext):
        if message.sticker:
            await message.pin()


def setup(bot: cog.Bot):
    Handler(bot=bot).register()
