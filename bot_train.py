from start import *
from sc2.constants import UnitTypeId

class bot_train(bot_api):

    async def bot_train(self):
        col = await self.count_unit(UnitTypeId.COLOSSUS) + 1
        trp_rat = [4 * col - 2,
                   3 * col,
                   col + 1,
                   2 * col,
                   col,
                   2 * col - 2]
        # Experimental, order: zealot, stalker, sentry, immortal, colossus, archon

        await self.train_probe()
        await self.train_stalker(trp_rat[1])
        await self.train_sentry(trp_rat[2])
        await self.train_zealot(trp_rat[0])
        await self.train_immortal(trp_rat[3])
        await self.train_colossus(trp_rat[4])
        await self.train_hightemplar(trp_rat[5])
        await self.train_observer()

    async def train_probe(self):
        p_exp = await self.count_building(UnitTypeId.ASSIMILATOR) * 3 + \
                await self.count_building(UnitTypeId.NEXUS) * 16
        if self.supply_workers < min(p_exp, 66):
            await self.train_(UnitTypeId.PROBE, UnitTypeId.NEXUS)

    async def train_zealot(self, n):
        if await self.count_unit(UnitTypeId.ZEALOT) < await self.count_unit(UnitTypeId.STALKER):
            await self.warp_in(UnitTypeId.ZEALOT)

    async def train_stalker(self, n):
        if not await self.warp():
            if await self.count_unit(UnitTypeId.STALKER) < 2:
                await self.train_(UnitTypeId.STALKER, UnitTypeId.GATEWAY)
        else:
            if await self.count_unit(UnitTypeId.STALKER) < n:
                await self.warp_in(UnitTypeId.STALKER)

    async def train_sentry(self, n):
        if await self.count_unit(UnitTypeId.SENTRY) < n:
            await self.warp_in(UnitTypeId.SENTRY)

    async def train_immortal(self, n):
        if await self.count_unit(UnitTypeId.IMMORTAL) < n:
            await self.train_(UnitTypeId.IMMORTAL, UnitTypeId.ROBOTICSFACILITY)

    async def train_colossus(self, n):
        if await self.count_unit(UnitTypeId.COLOSSUS) < n:
            await self.train_(UnitTypeId.COLOSSUS, UnitTypeId.ROBOTICSFACILITY)

    async def train_hightemplar(self, n):

        p_cont = await self.count_unit(UnitTypeId.HIGHTEMPLAR) // 2 + await self.count_unit(UnitTypeId.ARCHON)

        if p_cont < n:
            await self.warp_in(UnitTypeId.HIGHTEMPLAR)

    async def train_observer(self):
        if await self.count_unit(UnitTypeId.OBSERVER) < 2:
            await self.train_(UnitTypeId.OBSERVER, UnitTypeId.ROBOTICSFACILITY)




