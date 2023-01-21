import hikari, lightbulb, miru
import os
from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(token=f"{os.getenv('discord_token')}")
miru.install(bot)

class TestModal(miru.Modal):
    name = miru.TextInput(label="Name", placeholder="Your Name", required=True)
    bio = miru.TextInput(label="Bio", placeholder="Say a little something about yourself!", style=hikari.TextInputStyle.PARAGRAPH)

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.respond(f"Your name: ```{self.name.value}```\nYour bio: ```{self.bio.value}```")


@bot.command
@lightbulb.command('firstform', 'Produces button and button will produce modal')
@lightbulb.implements(lightbulb.SlashCommand)
async def firstForm(ctx: lightbulb.Context) -> None:
    modal = TestModal(title="Tell us about yourself!")
    await modal.send(ctx.interaction)

bot.run()