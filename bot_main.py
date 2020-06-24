from bot_op import bot_op
from bot_build import bot_build
from bot_train import bot_train
from start import start

class Bot_IV(bot_train, bot_build, bot_op, start):

    async def on_step(self, iteration):
        await self.start()

    async def start(self):
        if self.supply_used < 22:
            await self.two_base()
            await self.bot_train()
        else:
            await self.late()

    async def late(self):
        await self.distribute_workers(resource_ratio=1.5)
        await self.bot_op()
        await self.bot_build()
        await self.bot_train()

