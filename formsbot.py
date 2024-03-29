import hikari, miru
import lightbulb
import os
from dotenv import load_dotenv
import csv
import requests
import json

load_dotenv()

# bot = lightbulb.BotApp(token=f"{os.getenv('discord_token')}")
bot = lightbulb.BotApp(token=os.environ['API_KEY'])
miru.install(bot)

field_names = ['Username', 'Feedback']
class TestModal(miru.Modal):
    name = miru.TextInput(label="Username", placeholder="Your Username", required=True)
    feedBack = miru.TextInput(label="Feedback", placeholder="What do you think of the bot? Any improvements?", style=hikari.TextInputStyle.PARAGRAPH)

    async def callback(self, ctx: miru.ModalContext) -> None:
        requests.post('https://sheetdb.io/api/v1/rwjtxn150grj6', json={
            'date': 'DATETIME',
            'name': self.name.value,
            'feedback': self.feedBack.value
        })

        await ctx.respond('Your feedback has been recorded! Thanks!')

@bot.command
@lightbulb.command('feedback', 'Produces modal for feedback')
@lightbulb.implements(lightbulb.SlashCommand)
async def feedback(ctx: lightbulb.Context) -> None:
    modal = TestModal(title="Tell us your feedback!")
    await modal.send(ctx.interaction)

@bot.command
@lightbulb.add_checks(lightbulb.has_roles(1053446321186553931) | lightbulb.owner_only)
@lightbulb.option('limit', 'Limit of results returned.', default='5', type=int)
@lightbulb.option('date', 'Date of feedback. Format=Year-month-day, i.e. 2023-03-28', type=str, required=False)
@lightbulb.command('report', 'This will print out the available rows in the feedback spreadsheet.')
@lightbulb.implements(lightbulb.SlashCommand)
async def report(ctx):
    reportData = requests.get('https://sheetdb.io/api/v1/rwjtxn150grj6', params={'sort_by': 'date', 'sort_order': 'desc', 'limit': ctx.options.limit}).json()

    embedmsg = hikari.Embed(
        title='**Feedback Report**',
        description='~~----------------------~~'
    )
    print(reportData)
    if ctx.options.date == None:
         for i in range(len(reportData)):
            embedmsg.add_field(name=reportData[i]['name'], value=reportData[i]['feedback'])

    else:
        for i in range(len(reportData)):
            if ctx.options.date in reportData[i]['date']:
                embedmsg.add_field(name=reportData[i]['name'], value=reportData[i]['feedback'])
       
    await ctx.respond(embedmsg)

bot.run()