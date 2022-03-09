from discord import Client

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

client = AfClient()

try:
    client.run(af_token)
except Exception as e:
    Logger.printLog(f"Crashed. Error: {e}", error=True)