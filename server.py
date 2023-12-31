# This example requires the 'message_content' intent.
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_guild_channel_update(self, before, after):
        cocoa_press_staff = discord.Guild.get_role(after.guild, 1164974172607365223)
        support_role = discord.Guild.get_role(after.guild, 1164974316052562021)
        if before.category != after.category:
            if after.category_id == 1156046072129540149:
                print(f'Channel update {after} is now in {after.category}')
                await after.set_permissions(cocoa_press_staff, read_messages=True, send_messages=True)
                await after.set_permissions(support_role, read_messages=False, send_messages=False)
            if after.category_id == 1164975645533675530:
                print(f'Channel update {after} is now in {after.category}')
                message = Mail(
                    from_email=os.environ.get('FROM_EMAIL'),
                    to_emails=os.environ.get('TO_EMAIL'),
                    subject='New Discord Ticket Assigned To You',
                    html_content='<strong>There is a new discord ticket assigned to you! Please go to discord</strong>')
                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                except Exception as e:
                    print(e.message)
                await after.set_permissions(support_role, read_messages=True, send_messages=True)
                await after.set_permissions(cocoa_press_staff, read_messages=False, send_messages=False)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))