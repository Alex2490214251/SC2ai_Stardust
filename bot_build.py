from start import *
from sc2.constants import UnitTypeId

class bot_build(bot_api):

    async def bot_build(self):

        await self.build_pylon()
        await self.build_assimilator()
        await self.build_nexus()

        if await self.count_building(UnitTypeId.PYLON) > 1:
            global pylon
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build_gateway()
            await self.build_cyberneticscore()
            if await self.count_building(UnitTypeId.CYBERNETICSCORE) > 0:
                await self.build_roboticsfacility()
                if await self.count_building(UnitTypeId.ROBOTICSFACILITY) > 0:
                    await self.build_roboticsbay()
                if self.units(UnitTypeId.IMMORTAL).ready.exists:
                    await self.build_twilightcouncil()
                    await self.build_forge()
                    if await self.count_building(UnitTypeId.NEXUS) >= 3:
                        await self.build_templararchive()

    async def build_pylon(self):

        t_cons = self.time // 150

        capacity = await self.count_building(UnitTypeId.GATEWAY) * 2 + \
                   await self.count_building(UnitTypeId.ROBOTICSFACILITY) * 6
        potential = await self.count_building(UnitTypeId.PYLON) * 8 - self.supply_used
        pylon_position = self.structures(UnitTypeId.NEXUS).first.position.towards(
            self.game_info.map_center, 9.2)
        if potential < (capacity // max(8 - t_cons, 4)) and await self.count_building(UnitTypeId.PYLON) * 8 < 200:
            await self.build_(UnitTypeId.PYLON, pylon_position)

    async def build_assimilator(self):

        t_cons = self.time // 220

        a_exp = int(await self.count_building(UnitTypeId.NEXUS) * max(1.5, min(t_cons, 2)))
        a_num = await self.count_building(UnitTypeId.ASSIMILATOR)
        if a_num < a_exp:
            await self.build_assimilator_()

    async def build_nexus(self):
        t_cons = self.time // 110
        if self.can_afford(UnitTypeId.NEXUS) and not self.already_pending(UnitTypeId.NEXUS):
            if await self.count_building(UnitTypeId.NEXUS) < max(3, t_cons):
                await self.expand_now()

    async def build_gateway(self):
        t_cons = self.time // 200
        g_exp = int(self.structures(UnitTypeId.NEXUS).ready.amount * min(t_cons, 3)) + min(t_cons, 2)
        g_num = await self.count_building(UnitTypeId.GATEWAY)
        if g_num < g_exp:
            await self.build_(UnitTypeId.GATEWAY, pylon)

    async def build_cyberneticscore(self):
        if await self.count_building(UnitTypeId.CYBERNETICSCORE) < 1:
            await self.build_(UnitTypeId.CYBERNETICSCORE, pylon)

    async def build_twilightcouncil(self):
        if await self.count_building(UnitTypeId.TWILIGHTCOUNCIL) < 1:
            await self.build_(UnitTypeId.TWILIGHTCOUNCIL, pylon)

    async def build_roboticsfacility(self):  # For Stalker & Colossus
        rob_exp = self.structures(UnitTypeId.NEXUS).ready.amount - 1
        if await self.count_building(UnitTypeId.ROBOTICSFACILITY) < rob_exp:
            await self.build_(UnitTypeId.ROBOTICSFACILITY, pylon)

    async def build_roboticsbay(self):  # For Stalker & Colossus
        if await self.count_building(UnitTypeId.ROBOTICSBAY) < 1:
            await self.build_(UnitTypeId.ROBOTICSBAY, pylon)

    async def build_forge(self):  # Stalker & Colossus
        t_cons = self.time // 420
        if self.structures(UnitTypeId.ROBOTICSBAY).exists:
            if await self.count_building(UnitTypeId.FORGE) < t_cons + 1:
                await self.build_(UnitTypeId.FORGE, pylon)

    async def build_templararchive(self):
        if self.structures(UnitTypeId.ROBOTICSBAY).exists:
            if await self.count_building(UnitTypeId.TEMPLARARCHIVE) < 1:
                await self.build_(UnitTypeId.TEMPLARARCHIVE, pylon)


