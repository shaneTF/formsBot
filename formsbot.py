import hikari, lightbulb, miru
import os
from dotenv import load_dotenv
import csv

load_dotenv()

bot = lightbulb.BotApp(token=f"{os.getenv('discord_token')}")
miru.install(bot)

field_names = ['Username', 'Feedback']
class TestModal(miru.Modal):
    name = miru.TextInput(label="Username", placeholder="Your Username", required=True)
    feedBack = miru.TextInput(label="Feedback", placeholder="What do you think of the bot? Any improvements?", style=hikari.TextInputStyle.PARAGRAPH)

    async def callback(self, ctx: miru.ModalContext) -> None:
        feedbackDict = {"Username": f"{self.name.value}", "Feedback": f"{self.feedBack.value}"}
        with open('feedbackDB.csv', 'a') as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=field_names, lineterminator='\n')
            dict_object.writerow(feedbackDict)

        await ctx.respond('Your feedback has been recorded! Thanks!')

@bot.command
@lightbulb.command('feedback', 'Produces modal for feedback')
@lightbulb.implements(lightbulb.SlashCommand)
async def feedback(ctx: lightbulb.Context) -> None:
    modal = TestModal(title="Tell us your feedback!")
    await modal.send(ctx.interaction)

bot.run()