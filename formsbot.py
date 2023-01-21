import hikari, lightbulb, miru
import os
from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(token=f"{os.getenv('discord_token')}")
miru.install(bot)

class ModalView(miru.View):
    @miru.button(label="Modal", style=hikari.ButtonStyle.SECONDARY)
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = Modal(title="Title")
        await ctx.respond_with_modal(modal)

class Modal(miru.Modal):
    name = miru.TextInput(label="Name", placeholder="Your Name", required=True)
    bio = miru.TextInput(label="Bio", value="Pre-filled content", style=hikari.TextInputStyle.PARAGRAPH)

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.respond(f"Your name: ```{self.name.value}```\nYour bio: ```{self.bio.value}```")


@bot.command
@lightbulb.command('firstform', 'Produces button and button will produce modal')
@lightbulb.implements(lightbulb.SlashCommand)
async def firstForm(ctx):
    view = ModalView()
    message = await ctx.respond("Test message", components=view)
    await view.start(message)

bot.run()