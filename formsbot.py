import hikari, lightbulb, miru
import os
from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(token=f"{os.getenv('discord_token')}")
miru.install(bot)
# What happens if you create an embed and add fields with callback?
# Maybe try returning input fields with just return not ctx.respond.
class TestModal(miru.Modal):
    name = miru.TextInput(label="Username", placeholder="Your Username", required=True)
    feedBack = miru.TextInput(label="Feedback", placeholder="What do you think of the bot? Any improvements?", style=hikari.TextInputStyle.PARAGRAPH)

    async def callback(self, ctx: miru.ModalContext) -> None:
        print(f"Name: {self.name.value}, feedback: {self.feedBack.value}, Input3: {self.input3.value}")
        await ctx.respond(f"```You feedback has been recorded!```")

@bot.command
@lightbulb.command('feedback', 'Produces modal for feedback')
@lightbulb.implements(lightbulb.SlashCommand)
async def feedback(ctx: lightbulb.Context) -> None:
    modal = TestModal(title="Tell us your feedback!")
    await modal.send(ctx.interaction)

bot.run()