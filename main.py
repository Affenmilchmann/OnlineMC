from random import choice
from discord import Client, Game, Activity, ActivityType, Intents

from OnlineApp import OnlineApp
from aftoken import af_token
from Logger import Logger

class AfClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app: OnlineApp = False

    def initApp(self):
        self.app = OnlineApp(self)

    async def on_message(self, message):
        if not self.app:
            self.initApp()
        await self.app.onMessage(message)

    async def on_raw_reaction_add(self, payload):
        if not self.app:
            self.initApp()
        await self.app.onReactionAdd(payload)

afIntents = Intents().default()
afIntents.messages = True
client = AfClient(activity=Game(name="with a grass block"), intents=afIntents)

try:
    client.run(af_token)
except Exception as e:
    Logger.printLog(f"Crashed. Error: {e}", error=True)